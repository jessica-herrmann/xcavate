# Case `network_0_b_splines_9_vessels`

## Pipelines
### v0 — OK
- exit_code: `0`
- emitted: `gcode.txt`
- metrics: `moves=3878 g0=0 g1=3447 g4=0 path=858.715 mm mm_trans=0 t_est=1239.40 s`

### v1 — OK
- exit_code: `0`
- emitted: `gcode_SM_pressure.txt`
- metrics: `moves=3645 g0=0 g1=3447 g4=0 path=858.715 mm mm_trans=0 t_est=1239.40 s`

### v2 — OK
- exit_code: `0`
- emitted: `gcode_SM_pressure.txt`
- metrics: `moves=3644 g0=0 g1=3447 g4=0 path=858.715 mm mm_trans=0 t_est=1239.40 s`

## Pairwise diffs
### v0 vs v1
- counts=(3878,3645) aligned=False max_xyz_dev=38.41 max_f_dev=9.877 max_e_dev=0 out_of_tol=3478 byte_equal=False
- first divergences:

```
  [  160] A: Enable Aa
        B: G91
  [  161] A: G91
        B: G1 A0.5 F0.25
  [  162] A: DWELL 0.08
        B: G90
  [  163] A: BRAKE Aa 1
        B: G1 A21.627870899027588 F10
  [  164] A: G1 A0.5 F0.25
        B: G90
  [  165] A: G90
        B: G1 X7.15097 Y8.026653
  [  166] A: G1 A21.627870899027588 F10
        B: G90
  [  167] A: G90
        B: G1 X7.15097 Y8.026653 A-20.089128
  [  168] A: BRAKE Aa 1
        B: G91
  [  169] A: G1 X7.15097048196175 Y8.026652947212586
        B: G90
  [  170] A: G90
        B: G1 X7.15097 Y8.026653 A-20.089128 F0.5853263835609995
  [  171] A: G1 X7.15097048196175 Y8.026652947212586 A-20.08912822191734
        B: G1 X7.057148 Y8.178653 A-20.088211 F0.5853263835609995
  [  172] A: Enable Aa
        B: G1 X6.963326 Y8.330652 A-20.087293 F0.5853263835609995
  [  173] A: G91
        B: G1 X6.869504 Y8.482652 A-20.086376 F0.585326173477171
  [  174] A: BRAKE Aa 0
        B: G1 X6.767314 Y8.628684 A-20.074746 F0.585326173477171
  [  175] A: DWELL 0.08
        B: G1 X6.665123 Y8.774717 A-20.063116 F0.585326173477171
  [  176] A: G90
        B: G1 X6.562932 Y8.920749 A-20.051487 F0.5853264115424792
  [  177] A: G1 X7.15097048196175 Y8.026652947212586 A-20.08912822191734 F0.5853263835609995
        B: G1 X6.454469 Y9.061169 A-20.031207 F0.5853264115424792
  [  178] A: G1 X7.057148421771113 Y8.178652644424007 A-20.088210802442184 F0.5853263835609995
        B: G1 X6.346007 Y9.201588 A-20.010928 F0.5853264115424792
  [  179] A: G1 X6.963326361580477 Y8.33065234163543 A-20.08729338296703 F0.5853263835609995
        B: G1 X6.237544 Y9.342008 A-19.990649 F0.585327164119148
```

### v0 vs v2
- counts=(3878,3644) aligned=False max_xyz_dev=38.41 max_f_dev=9.877 max_e_dev=0 out_of_tol=3478 byte_equal=False
- first divergences:

```
  [  160] A: Enable Aa
        B: G91
  [  161] A: G91
        B: G1 A0.5 F0.25
  [  162] A: DWELL 0.08
        B: G90
  [  163] A: BRAKE Aa 1
        B: G1 A21.627870899027588 F10
  [  164] A: G1 A0.5 F0.25
        B: G90
  [  165] A: G90
        B: G1 X7.15097 Y8.026653
  [  166] A: G1 A21.627870899027588 F10
        B: G90
  [  167] A: G90
        B: G1 X7.15097 Y8.026653 A-20.089128
  [  168] A: BRAKE Aa 1
        B: G91
  [  169] A: G1 X7.15097048196175 Y8.026652947212586
        B: G90
  [  170] A: G90
        B: G1 X7.15097 Y8.026653 A-20.089128 F0.585326
  [  171] A: G1 X7.15097048196175 Y8.026652947212586 A-20.08912822191734
        B: G1 X7.057148 Y8.178653 A-20.088211 F0.585326
  [  172] A: Enable Aa
        B: G1 X6.963326 Y8.330652 A-20.087293 F0.585326
  [  173] A: G91
        B: G1 X6.869504 Y8.482652 A-20.086376 F0.585326
  [  174] A: BRAKE Aa 0
        B: G1 X6.767314 Y8.628684 A-20.074746 F0.585326
  [  175] A: DWELL 0.08
        B: G1 X6.665123 Y8.774717 A-20.063116 F0.585326
  [  176] A: G90
        B: G1 X6.562932 Y8.920749 A-20.051487 F0.585326
  [  177] A: G1 X7.15097048196175 Y8.026652947212586 A-20.08912822191734 F0.5853263835609995
        B: G1 X6.454469 Y9.061169 A-20.031207 F0.585326
  [  178] A: G1 X7.057148421771113 Y8.178652644424007 A-20.088210802442184 F0.5853263835609995
        B: G1 X6.346007 Y9.201588 A-20.010928 F0.585326
  [  179] A: G1 X6.963326361580477 Y8.33065234163543 A-20.08729338296703 F0.5853263835609995
        B: G1 X6.237544 Y9.342008 A-19.990649 F0.585327
```

### v1 vs v2
- counts=(3645,3644) aligned=True max_xyz_dev=0 max_f_dev=4.991e-07 max_e_dev=0 out_of_tol=0 byte_equal=False

## Known residual deltas

These are documented, characterized differences between the pipelines — not bugs in the harness. Each is either intrinsic to the pipeline implementation or already mitigated by the harness.

### v1 ignores its own `--flow` argument (mitigated)
`id: v1-flow-override`

`xcavate_11_30_25.py` line 3705 hardcodes `flow = 0.1609429886081009`, overriding the `--flow` argparse value. The harness sets `CANONICAL_PARAMS['flow'] = 0.1609429...` so all pipelines compute feedrates on the same flow constant; without this match the F values would diverge by the 0.1609/0.1272 = 1.265× ratio across every G1 move.

### v1 emits an extra leading `G90` before its first `G92`
`id: preamble-line-shift`

v1's preamble is `G90 / G92 .. / G90 F<feed> / ...`; v2's is `G92 .. / G90 F<feed> / ...`. This shifts every subsequent line index by 1 between the two streams. The harness compensates via `align_on_first_g1=True` in `numerical_diff`, so reported deviations are post-alignment and reflect actual trajectory drift rather than the index shift.

### v2's iterative DFS produces one more raw pass than v1's recursive DFS
`id: dfs-extra-pass`

v2 uses an explicit-stack iterative DFS in `xcavate/core/pathfinding.py` with reversed neighbour push order; v1 uses a recursive DFS that iterates `graph[node]` in native order. On the 4-vessel network, v2 produces **14 raw passes** (lengths sorted: 5, 11, 12, 13, 20, 33, 68, 97, 113, 163, 203, 227, 397, 418) while v1 produces **13**. The extra pass is typically a 2-node bridge through a branchpoint that v1 absorbs into an adjacent pass. Same vessels are printed; the split boundary differs.

### `run_full_gap_closure_pipeline` distributes branchpoint nodes differently
`id: gap-closure-branchpoint-distribution`

After subdivision (which is algorithmically equivalent in both pipelines), v2's gap-closure prepends/appends shared branchpoint nodes to stitch passes — e.g. v2 pass 1 starts with `[1571, 1572, ...]` even though `subdivide_passes` returned `[1572, ...]`. Pass 2 ends with the same node it started with (`[985, 489, ..., 393, 985]`). v1's gap closure makes the same kind of additions but distributes them across different passes, leaving one fewer net pass. Net effect: same printed segments and same vessel coverage, slightly different pass boundaries and therefore slightly different jog choreography between passes.

### Branchpoint daughter-selection ties resolved differently across pipelines
`id: branchpoint-tiebreak-large-network`

On dense vasculature (e.g., the 500-vessel network with 63,904 interpolated points), some vessel endpoints have two or more candidate "daughter" nodes at *exactly equal* distance. Each pipeline uses a different tiebreaker:
  • v2 → `scipy.cKDTree.query(point, k=N)` (binary tree)
  • v1 → nested-loop brute force with strict-less comparison
  • v0 → nested-loop brute force with slightly different loop ordering than v1
When ties occur, the three implementations pick different daughter nodes. On the 4/9/14-vessel networks ties are rare, so the graphs match exactly (`v1 ↔ v2 = 0` mm). On the 500-vessel network ~38 adjacency-list entries differ between v2 and v1 — different branchpoint daughter pairs cascade through DFS into a different pass order, producing the ~70 mm `max_xyz_dev` between every pair (v0↔v1 = 71.16, v0↔v2 = 69.94, v1↔v2 = 70.19). All three pipelines still print the same vessels with the same total path; only the visit order differs.

To force byte-equivalence we'd need to add an explicit secondary tiebreaker (e.g., "on equal distance, pick smaller node index") and apply it identically to all three implementations. None of the three is currently "correct" — they're all valid choices for the same geometric configuration.
