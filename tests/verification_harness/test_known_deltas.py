"""Tests for the known-deltas catalog and report formatter."""
from dataclasses import dataclass
from pathlib import Path

from .compare import Metrics
from .known_deltas import KNOWN_DELTAS, format_for_case
from .report import PipelineResult


@dataclass
class _Case:
    multimaterial: bool


def _ok(name: str) -> PipelineResult:
    return PipelineResult(
        name=name, status="OK", gcode_paths=[Path("/tmp/x.txt")],
        metrics=Metrics(0, 0, 0, 0, 0.0, 0, 0.0),
        stderr_excerpt="", exit_code=0,
    )


def _fail(name: str) -> PipelineResult:
    return PipelineResult(
        name=name, status="FAIL", gcode_paths=[], metrics=None,
        stderr_excerpt="boom", exit_code=1,
    )


def test_catalog_has_expected_ids():
    ids = {d.id for d in KNOWN_DELTAS}
    expected = {
        "v1-flow-override",
        "preamble-line-shift",
        "v1-mm-pressure-gate",
        "dfs-extra-pass",
        "gap-closure-branchpoint-distribution",
        "branchpoint-tiebreak-large-network",
        "v0-keyerror",
    }
    assert expected.issubset(ids)


def test_mm_only_deltas_suppress_on_sm_case():
    case = _Case(multimaterial=False)
    results = {"v0": _ok("s"), "v1": _ok("x"), "v2": _ok("m")}
    section = format_for_case(case, results, {})
    # MM-only deltas must NOT appear
    assert "v1-mm-pressure-gate" not in section
    # universally-relevant deltas SHOULD appear
    assert "v1-flow-override" in section


def test_mm_deltas_appear_on_mm_case():
    case = _Case(multimaterial=True)
    results = {"v0": _fail("s"), "v1": _ok("x"), "v2": _ok("m")}
    section = format_for_case(case, results, {})
    assert "v1-mm-pressure-gate" in section


def test_v0_keyerror_only_when_v0_failed():
    case = _Case(multimaterial=False)
    section_ok = format_for_case(case, {"v0": _ok("s"), "v2": _ok("m")}, {})
    assert "v0-keyerror" not in section_ok
    section_fail = format_for_case(case, {"v0": _fail("s"), "v2": _ok("m")}, {})
    assert "v0-keyerror" in section_fail


def test_dfs_and_gap_closure_deltas_only_when_both_modern_pipelines_ok():
    case = _Case(multimaterial=False)
    section_only_v2 = format_for_case(case, {"v2": _ok("m"), "v1": _fail("x")}, {})
    assert "dfs-extra-pass" not in section_only_v2
    section_both = format_for_case(case, {"v2": _ok("m"), "v1": _ok("x")}, {})
    assert "dfs-extra-pass" in section_both


def test_section_starts_with_documented_header():
    case = _Case(multimaterial=True)
    section = format_for_case(case, {"v1": _ok("x"), "v2": _ok("m")}, {})
    assert section.startswith("## Known residual deltas\n")
