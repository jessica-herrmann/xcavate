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


def _travel_cost(a: np.ndarray, b: np.ndarray, z_weight: float = 1.0) -> float:
    """Compute travel cost between two 3D points with Z-weighting.

    Z-distance is weighted higher because the nozzle travels Z twice
    (retract up then descend) and at a slower speed than XY travel.
    """
    xy_dist = np.linalg.norm(a[:2] - b[:2])
    z_dist = abs(a[2] - b[2])
    return xy_dist + z_weight * z_dist


def enforce_collision_safe_order(
    print_passes: Dict[int, List[int]],
    points: np.ndarray,
    nozzle_radius: float,
    graph: Dict[int, List[int]] | None = None,
    tolerance: float = 0.0,
    tolerance_flag: bool = False,
) -> Dict[int, List[int]]:
    """Split and defer nodes so the nozzle never descends through printed ink.

    Reordering and merging both work at pass granularity, but the collision
    rule is a per-node one: when the nozzle drops to a node, every node below
    it inside the nozzle's XY shadow must already have been printed, or the
    shaft ploughs through material on the way down.  A pass spans a Z-range,
    so no pass-level ordering can satisfy that in general — some passes have
    to be cut.

    This walks the requested pass order and emits a node only once all of its
    below-shadow neighbours are down.  A blocked node ends the current stroke
    and hands the rest of its pass to a second phase, which lays those nodes
    back down once they are released — nearest first, following graph edges so
    the recovered strokes stay continuous.

    The node-level constraint graph only ever points from lower Z to higher Z,
    so it cannot contain a cycle and every deferred node is eventually
    released.  The returned order therefore has zero collisions by
    construction.

    Trade-off: a cut costs the extrusion move spanning it.  Re-entering from
    the node the stroke was cut away from recovers most of them, but not all —
    measured at ~1.5% of vessel segments left undrawn on the test networks,
    with a median length of ~0.02-0.04 mm against a ~0.25 mm filament, so the
    ends are expected to fuse.  Recovering the last of them would mean
    descending onto printed material, which is the very thing this removes.

    Args:
        print_passes: Ordered passes to make safe.
        points: Coordinate array.
        nozzle_radius: Half the nozzle diameter (mm).  ``<= 0`` disables the
            check and returns the input unchanged.
        graph: Adjacency dict, used to keep drained strokes continuous.
        tolerance: 3-D proximity below which a blocker is ignored.
        tolerance_flag: Whether to apply the tolerance exception.

    Returns:
        Passes with sequential indices, collision-safe in the order given.
    """
    from collections import defaultdict

    from scipy.spatial import cKDTree

    if nozzle_radius <= 0 or not print_passes:
        return print_passes

    nodes = sorted({n for k in print_passes for n in print_passes[k]})
    if not nodes:
        return print_passes

    z = points[:, 2]
    index = np.asarray(nodes)
    tree = cKDTree(points[index, :2])

    # Node-level Z-DAG: successors[m] are the nodes m unblocks once printed.
    successors: Dict[int, List[int]] = defaultdict(list)
    in_degree: Dict[int, int] = {n: 0 for n in nodes}
    tol_sq = tolerance * tolerance
    shadows = tree.query_ball_point(points[index, :2], nozzle_radius)
    for local, hits in enumerate(shadows):
        node = int(index[local])
        z_node = z[node]
        for j in hits:
            other = int(index[j])
            if other == node or z[other] >= z_node:
                continue
            if tolerance_flag:
                d = points[other, :3] - points[node, :3]
                if float(d @ d) < tol_sq:
                    continue
            successors[other].append(node)
            in_degree[node] += 1

    emitted: Set[int] = set()
    pending: Set[int] = set()
    ready: Set[int] = set()
    result: Dict[int, List[int]] = {}
    out_idx = 0

    def emit(node: int, stroke: List[int]) -> None:
        emitted.add(node)
        stroke.append(node)
        ready.discard(node)
        for succ in successors.get(node, ()):
            in_degree[succ] -= 1
            if in_degree[succ] == 0 and succ in pending:
                ready.add(succ)

    drawn: Set[Tuple[int, int]] = set()

    def close(stroke: List[int]) -> None:
        nonlocal out_idx
        if stroke:
            for a, b in zip(stroke[:-1], stroke[1:]):
                drawn.add((a, b) if a < b else (b, a))
            result[out_idx] = stroke
            out_idx += 1

    # Pass 1 — follow the requested order, cutting wherever it is unsafe.
    # A cut costs the extrusion move across it, so remember each deferred
    # node's predecessor: pass 2 re-enters from there and draws the segment
    # that the cut would otherwise have left undrawn.
    deferred: List[int] = []
    predecessor: Dict[int, int] = {}
    for k in sorted(print_passes.keys()):
        stroke: List[int] = []
        pass_nodes = print_passes[k]
        for offset, node in enumerate(pass_nodes):
            if node in emitted:
                stroke.append(node)          # retrace over printed ink
            elif in_degree[node] == 0:
                emit(node, stroke)
            else:
                # Hand the whole tail to pass 2.  Deferring just this node and
                # carrying on would shred the rest of the stroke into
                # single-node fragments; the tail is graph-connected, so pass 2
                # can lay it back down in one piece.
                tail = pass_nodes[offset:]
                deferred.extend(tail)
                for j, tail_node in enumerate(tail, start=offset):
                    if j:
                        predecessor.setdefault(tail_node, pass_nodes[j - 1])
                break
        close(stroke)

    # Pass 2 — drain what had to wait.  Anything with a clear column below it
    # is safe to print, so pick by travel and only fall back to depth when the
    # nozzle position is unknown.
    pending.update(n for n in deferred if n not in emitted)
    ready = {n for n in pending if in_degree[n] == 0}
    cursor = points[result[out_idx - 1][-1], :3] if out_idx else None
    while pending:
        if not ready:
            # Unreachable: take the shallowest pending node; every blocker is
            # strictly below it and is itself either emitted or pending, so a
            # pending node with no blockers left always exists. Raise rather
            # than break — falling through here would drop these nodes and
            # emit a print that is silently missing vessel.
            raise RuntimeError(
                f"collision-safe ordering stalled with {len(pending)} nodes "
                f"unplaced; the node-level Z-DAG should make this impossible"
            )
        if cursor is None:
            start = min(ready, key=lambda n: float(z[n]))
        else:
            start = min(ready, key=lambda n: _travel_cost(cursor, points[n, :3]))
        # Re-enter from the node this stroke was cut away from, so the
        # segment spanning the cut still gets extruded.
        stroke = []
        anchor = predecessor.get(start)
        if anchor is None or anchor not in emitted or _is_drawn(anchor, start, drawn):
            anchor = _printed_neighbour(start, graph, emitted, drawn)
        if anchor is not None:
            stroke.append(anchor)
        node: int | None = start
        while node is not None:
            pending.discard(node)
            emit(node, stroke)
            nxt = _next_continuous(node, graph, pending, in_degree)
            if nxt is None and graph is not None:
                # The walk stops here; note the re-entry point for whatever
                # is left hanging off this node.
                for neighbor in graph.get(node, ()):
                    if neighbor != node and neighbor in pending:
                        predecessor[neighbor] = node
            node = nxt
        cursor = points[stroke[-1], :3]
        close(stroke)

    return result


def _printed_neighbour(
    node: int,
    graph: Dict[int, List[int]] | None,
    emitted: Set[int],
    drawn: Set[Tuple[int, int]],
) -> int | None:
    """Find a printed neighbour whose segment to *node* is still missing.

    Re-entering from such a neighbour both restarts the stroke and lays down
    the one piece of vessel the cut would otherwise have skipped.
    """
    if graph is None:
        return None
    for neighbor in graph.get(node, ()):
        if neighbor != node and neighbor in emitted and not _is_drawn(neighbor, node, drawn):
            return neighbor
    return None


def _is_drawn(a: int, b: int, drawn: Set[Tuple[int, int]]) -> bool:
    """Has the segment between two nodes already been extruded?"""
    return ((a, b) if a < b else (b, a)) in drawn


def _next_continuous(
    node: int,
    graph: Dict[int, List[int]] | None,
    pending: Set[int],
    in_degree: Dict[int, int],
) -> int | None:
    """Pick a graph neighbour that can be printed right now, if any."""
    if graph is None:
        return None
    for neighbor in graph.get(node, ()):
        if neighbor != node and neighbor in pending and in_degree[neighbor] == 0:
            return neighbor
    return None


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
