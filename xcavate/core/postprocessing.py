"""Post-processing: subdivision of DFS passes, downsampling, overlap, and pass reordering.

Replaces xcavate.py lines 997-1106 (subdivision), 3218-3248 (downsampling),
3729-3806 (overlap SM), 3880-3955 (overlap MM).
"""

import heapq

import numpy as np
from typing import Dict, List, Set, Tuple


def subdivide_passes(
    print_passes: Dict[int, List[int]],
    graph: Dict[int, List[int]],
    points: np.ndarray,
) -> Dict[int, List[int]]:
    """Break DFS passes at backtrack points where successive nodes are not neighbors.

    DFS can backtrack, creating non-consecutive node sequences within a single
    pass. This function splits passes at those discontinuities and ensures each
    resulting segment starts with the lower-z node (bottom-up print order).

    Args:
        print_passes: Raw DFS passes {pass_idx: [node_indices]}.
        graph: Adjacency dict {node: [neighbors]}.
        points: Coordinate array (N, 3+).

    Returns:
        Subdivided passes, re-indexed sequentially.
    """
    # Find break points in each pass
    break_points = {}
    for i in print_passes:
        breaks = []
        for idx in range(len(print_passes[i]) - 1):
            current_node = print_passes[i][idx]
            next_node = print_passes[i][idx + 1]
            if next_node not in graph[current_node]:
                breaks.append(next_node)
        break_points[i] = breaks

    # Split passes at break points
    new_matrix = {}
    for i in break_points:
        if not break_points[i]:
            continue
        new_passes = {}
        start = 0
        for counter, bp in enumerate(break_points[i]):
            end = print_passes[i].index(bp)
            new_passes[counter] = print_passes[i][start:end]
            start = end
        # Last segment
        new_passes[len(break_points[i])] = print_passes[i][start:]
        new_matrix[i] = new_passes

    # Compute total number of passes
    num_new = sum(len(v) for v in new_matrix.values()) - len(new_matrix)
    num_total = len(print_passes) + num_new

    # Assemble subdivided passes
    result = {}
    counter = 0
    counter_old = 0
    while counter < num_total:
        if counter_old in new_matrix:
            for sub_idx in range(len(new_matrix[counter_old])):
                result[counter] = new_matrix[counter_old][sub_idx]
                counter += 1
            counter_old += 1
        else:
            result[counter] = print_passes[counter_old]
            counter += 1
            counter_old += 1

    # Ensure each segment starts with the lower-z node
    for i in result:
        if len(result[i]) < 2:
            continue
        first_z = points[result[i][0], 2]
        last_z = points[result[i][-1], 2]
        if first_z > last_z:
            result[i].reverse()

    return result


def downsample_passes(
    print_passes: Dict[int, List[int]],
    points: np.ndarray,
    downsample_factor: int,
    branchpoint_list: List[int],
    branchpoint_list_keys: List[int],
    endpoint_nodes: List[int],
) -> Dict[int, List[int]]:
    """Reduce point density while preserving structural nodes.

    First/last nodes, branchpoints (parents + daughters), and vessel endpoints
    are always kept. Other nodes are kept every `downsample_factor` indices.

    Args:
        print_passes: Current passes.
        points: Coordinate array.
        downsample_factor: Keep every Nth non-structural node.
        branchpoint_list: Daughter node indices.
        branchpoint_list_keys: Parent branchpoint indices.
        endpoint_nodes: Vessel endpoint indices.

    Returns:
        Downsampled passes.
    """
    structural = set(branchpoint_list) | set(branchpoint_list_keys) | set(endpoint_nodes)
    result = {}

    for i in print_passes:
        nodes = print_passes[i]
        if len(nodes) <= 3:
            result[i] = list(nodes)
            continue

        downsampled = []
        for j, node in enumerate(nodes):
            # Always keep first, last, and structural nodes
            if j == 0 or j == len(nodes) - 1 or node in structural:
                downsampled.append(node)
            elif j % downsample_factor == 0:
                downsampled.append(node)
        result[i] = downsampled

    return result


def add_overlap(
    print_passes: Dict[int, List[int]],
    num_overlap: int,
) -> Dict[int, List[int]]:
    """Add nodal overlap between connected passes for gap closure.

    Args:
        print_passes: Current passes.
        num_overlap: Number of overlap nodes to add.

    Returns:
        Passes with overlapping endpoints.
    """
    if num_overlap <= 0:
        return print_passes

    return _add_overlap_retrace(print_passes, num_overlap)


def _add_overlap_retrace(
    print_passes: Dict[int, List[int]],
    num_overlap: int,
) -> Dict[int, List[int]]:
    """Original overlap: scan all previous passes for shared last-node, retrace backwards.

    For each pass i (from 1 onward):
      1. Get last node of pass i
      2. Search all passes j < i for that node
      3. If found at index idx in pass j, retrace backwards:
         append nodes [idx-1, idx-2, ...] from pass j to END of pass i
         up to num_overlap nodes
    """
    result = {i: list(v) for i, v in print_passes.items()}
    pass_indices = sorted(result.keys())

    pass_ends_on_shared = []
    pass_with_shared = []
    common_node = []

    # Find passes whose last node appears in an earlier pass
    for idx, i in enumerate(pass_indices):
        if idx == 0:
            continue
        check_last_node = result[i][-1]
        for j in pass_indices:
            if j >= i:
                break
            for k in result[j]:
                if k == check_last_node:
                    pass_ends_on_shared.append(i)
                    pass_with_shared.append(j)
                    common_node.append(check_last_node)

    # Retrace backwards from shared node in earlier pass
    for track_point, shared_pass in enumerate(pass_with_shared):
        if track_point >= len(pass_ends_on_shared):
            break
        node = common_node[track_point]
        if node not in result[shared_pass]:
            continue
        idx = result[shared_pass].index(node)
        if idx == 0:
            continue
        idx_count = 0
        while idx_count < num_overlap and (idx - (idx_count + 1)) >= 0:
            result[pass_ends_on_shared[track_point]].append(
                result[shared_pass][idx - (idx_count + 1)]
            )
            idx_count += 1

    return result


def _compute_pass_dependencies(
    print_passes: Dict[int, List[int]],
    points: np.ndarray,
    nozzle_radius: float,
) -> Dict[int, Set[int]]:
    """Compute collision dependencies between passes.

    Pass A depends on pass B (B must be printed before A) if any node in A
    has a node in B directly below it within the nozzle XY shadow: the nozzle
    would have to drive down through B's material to reach A.

    Returns:
        Dict mapping pass key to the set of pass keys that must precede it.
    """
    from scipy.spatial import cKDTree

    pass_keys = sorted(print_passes.keys())
    deps: Dict[int, Set[int]] = {k: set() for k in pass_keys}

    all_xy = points[:, :2]
    tree = cKDTree(all_xy)

    node_to_pass: Dict[int, int] = {}
    for k in pass_keys:
        for node in print_passes[k]:
            node_to_pass[node] = k

    for k in pass_keys:
        for node in print_passes[k]:
            z_node = points[node, 2]
            for other in tree.query_ball_point(all_xy[node], nozzle_radius):
                if other == node:
                    continue
                other_pass = node_to_pass.get(other)
                if other_pass is None or other_pass == k:
                    continue
                if points[other, 2] < z_node:
                    deps[k].add(other_pass)

    return deps


def _make_dependencies_acyclic(
    deps: Dict[int, Set[int]],
    print_passes: Dict[int, List[int]],
    points: np.ndarray,
) -> Dict[int, Set[int]]:
    """Turn the raw pass-level collision graph into a usable DAG.

    A pass spans a Z-range, so pass A routinely has a node below a node of B
    *and* vice versa.  Those mutual pairs make the raw graph cyclic — on real
    networks a single strongly-connected component can swallow almost every
    pass, leaving no satisfiable "ready" set at all and no constraints for the
    scheduler to respect.

    A mutual pair is physically unsatisfiable either way round, so one
    direction has to be given up.  We give up the top-down direction: pairs are
    oriented to match a bottom-up linear extension of the one-way edges.
    """
    pass_keys = sorted(print_passes.keys())
    min_z = {k: float(np.min(points[print_passes[k], 2])) for k in pass_keys}

    edges = {(d, k) for k in pass_keys for d in deps.get(k, set()) if d != k}
    mutual = {(a, b) for (a, b) in edges if (b, a) in edges}
    one_way = edges - mutual

    succ: Dict[int, List[int]] = {k: [] for k in pass_keys}
    in_deg: Dict[int, int] = {k: 0 for k in pass_keys}
    for a, b in one_way:
        succ[a].append(b)
        in_deg[b] += 1

    heap = [(min_z[k], k) for k in pass_keys if in_deg[k] == 0]
    heapq.heapify(heap)
    rank: Dict[int, int] = {}
    while heap:
        _, k = heapq.heappop(heap)
        rank[k] = len(rank)
        for nxt in succ[k]:
            in_deg[nxt] -= 1
            if in_deg[nxt] == 0:
                heapq.heappush(heap, (min_z[nxt], nxt))

    for k in sorted((k for k in pass_keys if k not in rank), key=lambda k: min_z[k]):
        rank[k] = len(rank)

    acyclic: Dict[int, Set[int]] = {k: set() for k in pass_keys}
    for a, b in one_way | mutual:
        if rank[a] < rank[b]:
            acyclic[b].add(a)
    return acyclic


def reorder_passes_nearest_neighbor(
    print_passes: Dict[int, List[int]],
    points: np.ndarray,
    nozzle_radius: float = 0.0,
) -> Dict[int, List[int]]:
    """Reorder passes to minimize total nozzle travel between pass endpoints.

    Greedy nearest-neighbor, but constrained so the schedule stays bottom-up:
    a pass is only eligible once every pass below it in the nozzle shadow has
    been printed.  Without that constraint the greedy happily climbs to the top
    of the network early and finishes at the bath floor, driving the nozzle
    down through everything already extruded.

    Args:
        print_passes: Current passes.
        points: Coordinate array.
        nozzle_radius: Half the nozzle diameter (mm).  0 disables collision
            constraints and reproduces the plain travel-only ordering.

    Returns:
        Reordered passes with sequential indices.
    """
    if len(print_passes) <= 1:
        return print_passes

    pass_keys = sorted(print_passes.keys())

    deps: Dict[int, Set[int]] = {}
    if nozzle_radius > 0:
        deps = _compute_pass_dependencies(print_passes, points, nozzle_radius)
        deps = _make_dependencies_acyclic(deps, print_passes, points)

    start_coords = {}
    end_coords = {}
    min_z = {}
    for k in pass_keys:
        nodes = print_passes[k]
        start_coords[k] = points[nodes[0], :3]
        end_coords[k] = points[nodes[-1], :3]
        min_z[k] = float(np.min(points[nodes, 2]))

    scheduled: Set[int] = set()

    def is_ready(k: int) -> bool:
        return all(d in scheduled for d in deps.get(k, set()))

    # Start at the deepest pass that is free to go, not at whichever pass
    # happens to be numbered first.
    ready_start = [k for k in pass_keys if is_ready(k)]
    first = min(ready_start or pass_keys, key=lambda k: min_z[k])

    ordered = [first]
    scheduled.add(first)
    remaining = set(pass_keys) - {first}

    while remaining:
        current_end = end_coords[ordered[-1]]
        candidates = [k for k in remaining if is_ready(k)]
        if not candidates:
            # Nothing is free; descending is what damages the print, so take
            # the deepest pass left rather than the nearest one.
            candidates = [min(remaining, key=lambda k: min_z[k])]

        best_key = min(
            candidates,
            key=lambda k: float(np.linalg.norm(start_coords[k] - current_end)),
        )
        ordered.append(best_key)
        remaining.remove(best_key)
        scheduled.add(best_key)

    return {i: print_passes[k] for i, k in enumerate(ordered)}
