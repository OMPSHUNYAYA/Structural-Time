import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Event:
    op: str
    account: Optional[str] = None
    tx_id: Optional[str] = None
    from_acct: Optional[str] = None
    to_acct: Optional[str] = None
    amount: Optional[int] = None


class StructuralTimeNode:
    def __init__(self, name: str) -> None:
        self.name = name
        self.tick: int = 0
        self.accounts: set[str] = set()
        self.pending: Dict[str, Dict[str, Any]] = {}
        self.confirmed: Dict[str, Dict[str, Any]] = {}
        self.seen_hashes: set[str] = set()

    def canonical_state(self) -> Dict[str, Any]:
        return {
            "accounts": sorted(self.accounts),
            "pending": dict(sorted(self.pending.items())),
            "confirmed": dict(sorted(self.confirmed.items())),
        }

    def state_hash(self) -> str:
        payload = json.dumps(self.canonical_state(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()

    def event_view(self, event: Event) -> Dict[str, Any]:
        data = asdict(event)
        return {k: v for k, v in data.items() if v is not None}

    def resolve(self, event: Event) -> Dict[str, Any]:
        before = self.state_hash()
        status = self.apply(event)
        after = self.state_hash()

        if status == "ABSTAIN":
            return self.output(event, "ABSTAIN", before)

        if status == "ADVANCED":
            if after not in self.seen_hashes:
                self.tick += 1
                self.seen_hashes.add(after)
            return self.output(event, "ADVANCED", after)

        return self.output(event, "NO_CHANGE", before)

    def apply(self, event: Event) -> str:
        op = event.op.upper()

        if op == "OPEN":
            return self.apply_open(event)

        if op == "MOVE":
            return self.apply_move(event)

        if op == "CONFIRM":
            return self.apply_confirm(event)

        return "ABSTAIN"

    def apply_open(self, event: Event) -> str:
        if not event.account:
            return "ABSTAIN"

        if event.account in self.accounts:
            return "NO_CHANGE"

        self.accounts.add(event.account)
        return "ADVANCED"

    def apply_move(self, event: Event) -> str:
        if not all([event.tx_id, event.from_acct, event.to_acct]):
            return "ABSTAIN"

        if event.amount is None or event.amount <= 0:
            return "ABSTAIN"

        if event.from_acct not in self.accounts or event.to_acct not in self.accounts:
            return "ABSTAIN"

        proposal = {
            "from": event.from_acct,
            "to": event.to_acct,
            "amount": event.amount,
        }

        if event.tx_id in self.pending:
            if self.pending[event.tx_id] == proposal:
                return "NO_CHANGE"
            return "ABSTAIN"

        if event.tx_id in self.confirmed:
            if self.confirmed[event.tx_id] == proposal:
                return "NO_CHANGE"
            return "ABSTAIN"

        self.pending[event.tx_id] = proposal
        return "ADVANCED"

    def apply_confirm(self, event: Event) -> str:
        if not event.tx_id:
            return "ABSTAIN"

        if event.tx_id in self.confirmed:
            return "NO_CHANGE"

        if event.tx_id not in self.pending:
            return "ABSTAIN"

        self.confirmed[event.tx_id] = self.pending.pop(event.tx_id)
        return "ADVANCED"

    def output(self, event: Event, status: str, state_hash: str) -> Dict[str, Any]:
        return {
            "node": self.name,
            "event": self.event_view(event),
            "status": status,
            "tick": self.tick,
            "hash": state_hash[:10],
        }


def run_node(name: str, events: List[Event]) -> StructuralTimeNode:
    node = StructuralTimeNode(name)
    print(f"\n--- {name} ---")
    for event in events:
        print(node.resolve(event))
    return node


def main() -> None:
    events_a = [
        Event("OPEN", account="A"),
        Event("OPEN", account="B"),
        Event("MOVE", tx_id="tx1", from_acct="A", to_acct="B", amount=100),
        Event("CONFIRM", tx_id="tx1"),
    ]

    events_b = [
        Event("OPEN", account="B"),
        Event("OPEN", account="A"),
        Event("CONFIRM", tx_id="tx1"),
        Event("MOVE", tx_id="tx1", from_acct="A", to_acct="B", amount=100),
        Event("CONFIRM", tx_id="tx1"),
    ]

    events_c = [
        Event("MOVE", tx_id="tx1", from_acct="A", to_acct="B", amount=100),
        Event("OPEN", account="A"),
        Event("OPEN", account="B"),
        Event("MOVE", tx_id="tx1", from_acct="A", to_acct="B", amount=100),
        Event("CONFIRM", tx_id="tx1"),
    ]

    node_a = run_node("Node-A", events_a)
    node_b = run_node("Node-B", events_b)
    node_c = run_node("Node-C", events_c)

    print("\n=== FINAL COMPARISON ===")
    print("A:", node_a.state_hash()[:10], "tick:", node_a.tick)
    print("B:", node_b.state_hash()[:10], "tick:", node_b.tick)
    print("C:", node_c.state_hash()[:10], "tick:", node_c.tick)


if __name__ == "__main__":
    main()