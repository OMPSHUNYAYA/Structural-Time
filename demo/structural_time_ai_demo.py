from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from hashlib import sha256
from itertools import permutations
from typing import Dict, FrozenSet, Iterable, List, Optional, Set, Tuple


@dataclass(frozen=True)
class StructuralTimeResult:
    state: str
    structural_time: int
    accepted_structure: Tuple[str, ...]

    def as_tuple(self) -> Tuple[str, int, Tuple[str, ...]]:
        return (self.state, self.structural_time, self.accepted_structure)


@dataclass(frozen=True)
class StructuralGovernanceReport:
    normalized_structure: Tuple[str, ...]
    accepted_structure: Tuple[str, ...]
    conflict_detected: bool
    structural_time: int
    governance_status: str
    resolution_basis: str


CONFLICT_PAIRS: Set[FrozenSet[str]] = {
    frozenset({"fatigue", "no_fatigue"}),
    frozenset({"fever", "no_fever"}),
    frozenset({"cough", "no_cough"}),
    frozenset({"headache", "no_headache"}),
    frozenset({"nausea", "no_nausea"}),
    frozenset({"light_sensitivity", "no_light_sensitivity"}),
    frozenset({"rash", "no_rash"}),
    frozenset({"joint_pain", "no_joint_pain"}),
    frozenset({"travel_history", "no_travel_history"}),
    frozenset({"alert", "no_alert"}),
    frozenset({"verified_source", "unverified_source"}),
    frozenset({"stable_metrics", "unstable_metrics"}),
    frozenset({"low_risk", "high_risk"}),
    frozenset({"critical_signal", "no_critical_signal"}),
}


def normalize(structure: Iterable[str]) -> Tuple[str, ...]:
    return tuple(sorted(set(structure)))


def has_conflict(structure: Set[str]) -> bool:
    return any(pair.issubset(structure) for pair in CONFLICT_PAIRS)


def accepted_structure(structure: Iterable[str]) -> Tuple[str, ...]:
    normalized = normalize(structure)
    if has_conflict(set(normalized)):
        return tuple()
    return normalized


def resolve_structural_time(structure: Iterable[str]) -> StructuralTimeResult:
    normalized = normalize(structure)
    accepted = accepted_structure(normalized)

    if has_conflict(set(normalized)):
        return StructuralTimeResult(
            state="ABSTAIN",
            structural_time=0,
            accepted_structure=accepted,
        )

    if not accepted:
        return StructuralTimeResult(
            state="NO_CHANGE",
            structural_time=0,
            accepted_structure=tuple(),
        )

    return StructuralTimeResult(
        state="ADVANCED",
        structural_time=len(accepted),
        accepted_structure=accepted,
    )


def analyze_structure(structure: Iterable[str]) -> StructuralGovernanceReport:
    normalized = normalize(structure)
    conflict_detected = has_conflict(set(normalized))
    accepted = accepted_structure(normalized)
    structural_time = len(accepted)

    if conflict_detected:
        governance_status = "VISIBLE_CONFLICT"
        resolution_basis = "conflicting structure remains visible; no accepted structure; no forced convergence"
    elif structural_time == 0:
        governance_status = "NO_STRUCTURAL_PROGRESS"
        resolution_basis = "no accepted structure"
    else:
        governance_status = "STRUCTURAL_TIME_RESOLVED"
        resolution_basis = "same accepted structure -> same structural time"

    return StructuralGovernanceReport(
        normalized_structure=normalized,
        accepted_structure=accepted,
        conflict_detected=conflict_detected,
        structural_time=structural_time,
        governance_status=governance_status,
        resolution_basis=resolution_basis,
    )


def certificate(structure: Iterable[str], result: StructuralTimeResult) -> str:
    normalized_structure = ",".join(normalize(structure))
    accepted = ",".join(result.accepted_structure)
    payload = (
        f"structure=[{normalized_structure}]|"
        f"state={result.state}|"
        f"structural_time={result.structural_time}|"
        f"accepted=[{accepted}]"
    )
    return sha256(payload.encode("utf-8")).hexdigest()


def build_resolution_capsule(case_id: str, structure: Iterable[str], result: StructuralTimeResult) -> Dict[str, object]:
    governance = analyze_structure(structure)

    return {
        "case_id": case_id,
        "proof_class": "STRUCTURAL_TIME_PROOF",
        "normalized_structure": list(governance.normalized_structure),
        "accepted_structure": list(result.accepted_structure),
        "state": result.state,
        "structural_time": result.structural_time,
        "governance_status": governance.governance_status,
        "resolution_basis": governance.resolution_basis,
        "time_acceptance_rule": "same accepted structure -> same structural time",
        "certificate": certificate(structure, result),
        "determinism_statement": "same accepted structure -> same structural time -> same certificate",
    }


def merge_all(*structures: Iterable[str]) -> Set[str]:
    merged: Set[str] = set()
    for structure in structures:
        merged |= set(structure)
    return merged


def print_case(name: str, structure: Iterable[str]) -> None:
    normalized = normalize(structure)
    result = resolve_structural_time(normalized)
    governance = analyze_structure(normalized)
    cert = certificate(normalized, result)

    print(name)
    print(f"  Structure           : {list(normalized)}")
    print(f"  State               : {result.state}")
    print(f"  Structural time     : {result.structural_time}")
    print(f"  Accepted structure  : {list(result.accepted_structure)}")
    print(f"  Governance status   : {governance.governance_status}")
    print(f"  Resolution basis    : {governance.resolution_basis}")
    print(f"  Cert                : {cert[:16]}...")
    print()


def print_capsule(title: str, capsule: Dict[str, object]) -> None:
    print(title)
    print(f"  Case ID                   : {capsule['case_id']}")
    print(f"  Proof class               : {capsule['proof_class']}")
    print(f"  Structure                 : {capsule['normalized_structure']}")
    print(f"  Accepted structure        : {capsule['accepted_structure']}")
    print(f"  State                     : {capsule['state']}")
    print(f"  Structural time           : {capsule['structural_time']}")
    print(f"  Governance status         : {capsule['governance_status']}")
    print(f"  Resolution basis          : {capsule['resolution_basis']}")
    print(f"  Acceptance rule           : {capsule['time_acceptance_rule']}")
    print(f"  Determinism statement     : {capsule['determinism_statement']}")
    print(f"  Cert                      : {str(capsule['certificate'])[:16]}...")
    print()


def print_governance_summary(name: str, structure: Iterable[str]) -> None:
    governance = analyze_structure(structure)
    print(name)
    print(f"  Normalized structure : {list(governance.normalized_structure)}")
    print(f"  Accepted structure   : {list(governance.accepted_structure)}")
    print(f"  Conflict detected    : {governance.conflict_detected}")
    print(f"  Structural time      : {governance.structural_time}")
    print(f"  Governance status    : {governance.governance_status}")
    print(f"  Resolution basis     : {governance.resolution_basis}")
    print()


def permutation_check(parts: Tuple[Set[str], ...]) -> Tuple[bool, Optional[StructuralTimeResult], Optional[str], int]:
    reference_result: Optional[StructuralTimeResult] = None
    reference_cert: Optional[str] = None
    checked = 0

    for perm in permutations(parts):
        merged = merge_all(*perm)
        result = resolve_structural_time(merged)
        cert = certificate(merged, result)
        checked += 1

        if reference_result is None:
            reference_result = result
            reference_cert = cert
            continue

        if result != reference_result or cert != reference_cert:
            return False, reference_result, reference_cert, checked

    return True, reference_result, reference_cert, checked


def case_payload(case_id: str, structure: Iterable[str]) -> Dict[str, object]:
    normalized = normalize(structure)
    result = resolve_structural_time(normalized)
    governance = analyze_structure(normalized)
    capsule = build_resolution_capsule(case_id, normalized, result)

    return {
        "structure": list(normalized),
        "state": result.state,
        "structural_time": result.structural_time,
        "accepted_structure": list(result.accepted_structure),
        "certificate": certificate(normalized, result),
        "governance": {
            "normalized_structure": list(governance.normalized_structure),
            "accepted_structure": list(governance.accepted_structure),
            "conflict_detected": governance.conflict_detected,
            "structural_time": governance.structural_time,
            "governance_status": governance.governance_status,
            "resolution_basis": governance.resolution_basis,
        },
        "resolution_capsule": capsule,
    }


def build_summary_payload() -> Dict[str, object]:
    node_a = {"fever"}
    node_b = {"cough"}
    node_c = {"fatigue"}
    merged_abc = merge_all(node_a, node_b, node_c)

    replay_x = {"cough", "fatigue"}
    replay_y = {"fever"}
    replay_z: Set[str] = set()
    merged_xyz = merge_all(replay_x, replay_y, replay_z)

    conflict_a = {"fever"}
    conflict_b = {"cough"}
    conflict_c = {"fatigue", "no_fatigue"}
    merged_conflict = merge_all(conflict_a, conflict_b, conflict_c)

    result_abc = resolve_structural_time(merged_abc)
    result_xyz = resolve_structural_time(merged_xyz)
    result_conflict = resolve_structural_time(merged_conflict)

    perm_ok, perm_result, perm_cert, perm_count = permutation_check((node_a, node_b, node_c))

    return {
        "core_identity": {
            "axiom_1": "correctness = structure",
            "axiom_2": "structural_time = count(accepted_structure)",
        },
        "reference_merge": case_payload("CASE_3NODE_REFERENCE", merged_abc),
        "replay_merge": case_payload("CASE_3NODE_REPLAY", merged_xyz),
        "conflict_merge": case_payload("CASE_CONFLICT_VISIBLE", merged_conflict),
        "resolution_capsules": [
            build_resolution_capsule("CASE_3NODE_REFERENCE", merged_abc, result_abc),
            build_resolution_capsule("CASE_3NODE_REPLAY", merged_xyz, result_xyz),
            build_resolution_capsule("CASE_CONFLICT_VISIBLE", merged_conflict, result_conflict),
        ],
        "permutation_check": {
            "checked": perm_count,
            "independent": perm_ok,
            "state": None if perm_result is None else perm_result.state,
            "structural_time": None if perm_result is None else perm_result.structural_time,
            "certificate": perm_cert,
        },
        "final_checks": {
            "converged_structural_time": result_abc.structural_time == result_xyz.structural_time,
            "matching_certificate": certificate(merged_abc, result_abc) == certificate(merged_xyz, result_xyz),
            "conflict_visible": analyze_structure(merged_conflict).conflict_detected,
            "conflict_not_forced": result_conflict.state == "ABSTAIN",
            "conflict_has_no_accepted_structure": len(result_conflict.accepted_structure) == 0,
        },
        "theorem_block": [
            "same accepted structure -> same structural time",
            "same accepted structure -> same certificate",
            "different arrival groupings of the same accepted structure -> same structural time",
            "conflicting structure -> ABSTAIN",
            "conflict remains visible -> no forced convergence occurs",
            "time is derived from accepted structure, not order",
            "time is derived from accepted structure, not synchronization",
            "structural time is a deterministic function of accepted structure",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-output", action="store_true")
    parser.add_argument("--output", default="structural_time_ai_result.json")
    args = parser.parse_args()

    node_a = {"fever"}
    node_b = {"cough"}
    node_c = {"fatigue"}
    merged_abc = merge_all(node_a, node_b, node_c)

    replay_x = {"cough", "fatigue"}
    replay_y = {"fever"}
    replay_z: Set[str] = set()
    merged_xyz = merge_all(replay_x, replay_y, replay_z)

    conflict_a = {"fever"}
    conflict_b = {"cough"}
    conflict_c = {"fatigue", "no_fatigue"}
    merged_conflict = merge_all(conflict_a, conflict_b, conflict_c)

    result_abc = resolve_structural_time(merged_abc)
    result_xyz = resolve_structural_time(merged_xyz)
    result_conflict = resolve_structural_time(merged_conflict)

    capsule_abc = build_resolution_capsule("CASE_3NODE_REFERENCE", merged_abc, result_abc)
    capsule_xyz = build_resolution_capsule("CASE_3NODE_REPLAY", merged_xyz, result_xyz)
    capsule_conflict = build_resolution_capsule("CASE_CONFLICT_VISIBLE", merged_conflict, result_conflict)

    print("=" * 72)
    print("STRUCTURAL TIME — AI STYLE DEMO")
    print("=" * 72)
    print("Core identity:")
    print("  correctness = structure")
    print("  structural_time = count(accepted_structure)")
    print()

    print("REFERENCE 3-NODE SCENARIO")
    print("-" * 72)
    print_case("Node A", node_a)
    print_case("Node B", node_b)
    print_case("Node C", node_c)
    print_case("Merged A+B+C", merged_abc)
    print_capsule("RESOLUTION CAPSULE — 3-NODE REFERENCE", capsule_abc)

    print("REPLAY / DIFFERENT GROUPING SCENARIO")
    print("-" * 72)
    print_case("Replay Node X", replay_x)
    print_case("Replay Node Y", replay_y)
    print_case("Replay Node Z", replay_z)
    print_case("Merged X+Y+Z", merged_xyz)
    print_capsule("RESOLUTION CAPSULE — 3-NODE REPLAY", capsule_xyz)

    print("CONFLICT VISIBILITY SCENARIO")
    print("-" * 72)
    print_case("Conflict Node A", conflict_a)
    print_case("Conflict Node B", conflict_b)
    print_case("Conflict Node C", conflict_c)
    print_case("Merged Conflict", merged_conflict)
    print_capsule("RESOLUTION CAPSULE — CONFLICT VISIBLE", capsule_conflict)

    print("PERMUTATION-INDEPENDENCE CHECK")
    print("-" * 72)
    perm_ok, perm_result, perm_cert, perm_count = permutation_check((node_a, node_b, node_c))
    print(f"Permutations checked        : {perm_count}")
    print(f"Permutation independence    : {perm_ok}")
    if perm_result is not None:
        print(f"Resolved state              : {perm_result.state}")
        print(f"Resolved structural time    : {perm_result.structural_time}")
    if perm_cert is not None:
        print(f"Resolved cert               : {perm_cert[:16]}...")
    print()

    print("STRUCTURAL GOVERNANCE SUMMARY")
    print("-" * 72)
    print_governance_summary("Reference Merge Governance", merged_abc)
    print_governance_summary("Replay Merge Governance", merged_xyz)
    print_governance_summary("Conflict Merge Governance", merged_conflict)

    cert_abc = certificate(merged_abc, result_abc)
    cert_xyz = certificate(merged_xyz, result_xyz)

    print("FINAL CHECKS")
    print("-" * 72)
    print(f"Reference structural time   : {result_abc.structural_time}")
    print(f"Replay structural time      : {result_xyz.structural_time}")
    print(f"Reference matching replay   : {result_abc.structural_time == result_xyz.structural_time}")
    print(f"Matching certificate        : {cert_abc == cert_xyz}")
    print(f"Conflict visible            : {analyze_structure(merged_conflict).conflict_detected}")
    print(f"No forced convergence       : {result_conflict.state == 'ABSTAIN'}")
    print(f"No accepted conflict state  : {len(result_conflict.accepted_structure) == 0}")
    print()

    print("THEOREM BLOCK")
    print("-" * 72)
    print("same accepted structure -> same structural time")
    print("same accepted structure -> same certificate")
    print("different arrival groupings of the same accepted structure -> same structural time")
    print("conflicting structure -> ABSTAIN")
    print("conflict remains visible -> no forced convergence occurs")
    print("time is derived from accepted structure, not order")
    print("time is derived from accepted structure, not synchronization")
    print("structural time is a deterministic function of accepted structure")
    print()

    print("EXPECTED INTERPRETATION")
    print("-" * 72)
    print("Independent partial nodes can converge to the same structural time through accepted structure alone.")
    print("Different groupings of the same accepted fragments produce the same structural time.")
    print("Conflict is never forced into false convergence.")
    print("Time does not require clocks, ordering, or synchronization to remain identical.")
    print()
    print("In short:")
    print("  structural_time = count(accepted_structure)")
    print("=" * 72)

    if args.write_output:
        payload = build_summary_payload()
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        print(f"Wrote output JSON           : {args.output}")


if __name__ == "__main__":
    main()