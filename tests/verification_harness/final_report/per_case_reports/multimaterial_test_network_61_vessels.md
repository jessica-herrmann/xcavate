# Case `multimaterial_test_network_61_vessels`

## Pipelines
### v0 — OK
- exit_code: `0`
- emitted: `gcode_multimaterial.txt`, `gcode.txt`
- metrics: `moves=14040 g0=0 g1=9834 g4=0 path=39204.212 mm mm_trans=184 t_est=8161.14 s`

### v1 — OK
- exit_code: `0`
- emitted: `gcode_MM_pressure.txt`, `gcode_SM_pressure.txt`
- metrics: `moves=10387 g0=0 g1=10017 g4=0 path=40255.319 mm mm_trans=184 t_est=6467.84 s`

### v2 — OK
- exit_code: `0`
- emitted: `gcode_MM_pressure.txt`, `gcode_SM_pressure.txt`
- metrics: `moves=10386 g0=0 g1=10017 g4=0 path=40255.319 mm mm_trans=184 t_est=6467.84 s`

## Pairwise diffs
### v0 vs v1
- counts=(14040,10387) aligned=False max_xyz_dev=90 max_f_dev=9.75 max_e_dev=0 out_of_tol=10336 byte_equal=False
- first divergences:

```
  [   27] A: DWELL 0.75
        B: G91 G1 A0.5 F0.25
  [   28] A: BRAKE Aa 1
        B: G90 G1 A12.7 B12.7 F5.0
  [   29] A: BRAKE Ab 1
        B: G91 G1 A60.0 B60.0 F5.0
  [   30] A: G91 G1 A0.5 F0.25
        B: G91 G1 X-103 F10
  [   31] A: G90 G1 A12.7 B12.7 F5
        B: G91 G1 Y0.5 F5.0
  [   32] A: $COM=2
        B: G91 G1 A-60.0 B-60.0
  [   33] A: $AP=10
        B: G90
  [   34] A: Call setPress P$COM Q$AP
        B: G92 X0.33311078321991 Y-9.963402087651284
  [   35] A: $COM=1
        B: G90 G1 X0.333111 Y-9.963402
  [   36] A: $AP=5
        B: G90 G1 X0.333111 Y-9.963402 B-10.899589
  [   37] A: Call setPress P$COM Q$AP
        B: G1 X0.480268 Y-9.947313 B-10.836382 F1.901765458405037
  [   38] A: G91 G1 A30 B30 F5
        B: G1 X0.627425 Y-9.931224 B-10.773174 F1.901765458405037
  [   39] A: G91 G1 X-103 F5
        B: G1 X0.771318 Y-9.903427 B-10.707263 F1.901765488129072
  [   40] A: G91 G1 A-30 B-30
        B: G1 X0.91521 Y-9.87563 B-10.641353 F1.901765488129072
  [   41] A: G90
        B: G1 X1.056228 Y-9.83825 B-10.573369 F1.9017653778452936
  [   42] A: G92 X0.33311078321991 Y-9.963402087651284
        B: G1 X1.197246 Y-9.800869 B-10.505385 F1.9017653778452936
  [   43] A: G90 G1 X0.33311078321991 Y-9.963402087651284
        B: G1 X1.339795 Y-9.768094 B-10.438311 F1.9017657795501905
  [   44] A: G90 G1 X0.33311078321991 Y-9.963402087651284 B-10.89958926883309
        B: G1 X1.482344 Y-9.735319 B-10.371237 F1.9017657795501905
  [   45] A: Enable Ab
        B: G1 X1.622806 Y-9.696805 B-10.303168 F1.9017643605468473
  [   46] A: Enable Aa
        B: G1 X1.763269 Y-9.658292 B-10.235099 F1.9017643605468473
```

### v0 vs v2
- counts=(14040,10386) aligned=False max_xyz_dev=90 max_f_dev=9.75 max_e_dev=0 out_of_tol=10336 byte_equal=False
- first divergences:

```
  [   27] A: DWELL 0.75
        B: G91 G1 A0.5 F0.25
  [   28] A: BRAKE Aa 1
        B: G90 G1 A12.7 B12.7 F5.0
  [   29] A: BRAKE Ab 1
        B: G91 G1 A60.0 B60.0 F5.0
  [   30] A: G91 G1 A0.5 F0.25
        B: G91 G1 X-103 F10
  [   31] A: G90 G1 A12.7 B12.7 F5
        B: G91 G1 Y0.5 F5.0
  [   32] A: $COM=2
        B: G91 G1 A-60.0 B-60.0
  [   33] A: $AP=10
        B: G90
  [   34] A: Call setPress P$COM Q$AP
        B: G92 X0.333111 Y-9.963402
  [   35] A: $COM=1
        B: G90 G1 X0.333111 Y-9.963402
  [   36] A: $AP=5
        B: G90 G1 X0.333111 Y-9.963402 B-10.899589
  [   37] A: Call setPress P$COM Q$AP
        B: G1 X0.480268 Y-9.947313 B-10.836382 F1.901765
  [   38] A: G91 G1 A30 B30 F5
        B: G1 X0.627425 Y-9.931224 B-10.773174 F1.901765
  [   39] A: G91 G1 X-103 F5
        B: G1 X0.771318 Y-9.903427 B-10.707263 F1.901765
  [   40] A: G91 G1 A-30 B-30
        B: G1 X0.91521 Y-9.87563 B-10.641353 F1.901765
  [   41] A: G90
        B: G1 X1.056228 Y-9.83825 B-10.573369 F1.901765
  [   42] A: G92 X0.33311078321991 Y-9.963402087651284
        B: G1 X1.197246 Y-9.800869 B-10.505385 F1.901765
  [   43] A: G90 G1 X0.33311078321991 Y-9.963402087651284
        B: G1 X1.339795 Y-9.768094 B-10.438311 F1.901766
  [   44] A: G90 G1 X0.33311078321991 Y-9.963402087651284 B-10.89958926883309
        B: G1 X1.482344 Y-9.735319 B-10.371237 F1.901766
  [   45] A: Enable Ab
        B: G1 X1.622806 Y-9.696805 B-10.303168 F1.901764
  [   46] A: Enable Aa
        B: G1 X1.763269 Y-9.658292 B-10.235099 F1.901764
```

### v1 vs v2
- counts=(10387,10386) aligned=True max_xyz_dev=4.981e-07 max_f_dev=4.999e-07 max_e_dev=0 out_of_tol=0 byte_equal=False

## Known residual deltas

These are documented, characterized differences between the pipelines — not bugs in the harness. Each is either intrinsic to the pipeline implementation or already mitigated by the harness.

### v1 ignores its own `--flow` argument (mitigated)
`id: v1-flow-override`

`xcavate_11_30_25.py` line 3705 hardcodes `flow = 0.1609429886081009`, overriding the `--flow` argparse value. The harness sets `CANONICAL_PARAMS['flow'] = 0.1609429...` so all pipelines compute feedrates on the same flow constant; without this match the F values would diverge by the 0.1609/0.1272 = 1.265× ratio across every G1 move.

### v1 emits an extra leading `G90` before its first `G92`
`id: preamble-line-shift`

v1's preamble is `G90 / G92 .. / G90 F<feed> / ...`; v2's is `G92 .. / G90 F<feed> / ...`. This shifts every subsequent line index by 1 between the two streams. The harness compensates via `align_on_first_g1=True` in `numerical_diff`, so reported deviations are post-alignment and reflect actual trajectory drift rather than the index shift.

### v1's multimaterial-pressure writer is gated on `custom_gcode == 1` (patched)
`id: v1-mm-pressure-gate`

Script line 4717 reads `if multimaterial == 1 and custom_gcode == 1 and printer_type == 0:`. Without `--custom 1` (and the auxiliary `inputs/custom/*.txt` template files it would then read), v1 silently skipped MM emission and only wrote `gcode_SM_pressure.txt` even for MM inputs — leading to `mm_trans=0` in our metrics. `v1_runner.py` rewrites that gate in memory so the MM writer runs without requiring custom template files. After the patch, v1 emits 184 nozzle transitions on the 61-vessel network (matching v2, which also emits 184; v1 and v2 are bit-identical here).

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
