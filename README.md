# ⭐ Structural Time (STIME)

**Structural Progression Without Physical Clocks — Reference Transition System**

![Structural-Time](https://img.shields.io/badge/Structural%20Time-STIME-black)
![Time-From-Structure](https://img.shields.io/badge/Time-From%20Structure-purple)
![Deterministic](https://img.shields.io/badge/Deterministic-Resolution-green)
![Clock-Independent](https://img.shields.io/badge/Physical%20Clock-Not%20Required-lightgrey)
![Order-Bounded](https://img.shields.io/badge/Order-Supported%20Independence-lightgrey)
![Sync-Free](https://img.shields.io/badge/Clock%20Synchronization-Not%20Required-lightgrey)
![Transition-Governed](https://img.shields.io/badge/Transitions-Governed%20States-orange)
![Replay](https://img.shields.io/badge/Replay-Deterministic-orange)
![Offline-Ready](https://img.shields.io/badge/Local%20Offline-Resolution%20Supported-blue)
![Reference-Implementation](https://img.shields.io/badge/Reference%20Implementation-Available-blue)

![Verify](https://github.com/OMPSHUNYAYA/Structural-Time/actions/workflows/structural-time-verify.yml/badge.svg)

---

Structural progression without physical clock input.  
Resolution without synchronized timestamps.

**Elapsed time is not measured inside STIME.**  
**A bounded structural-progress value is resolved from declared structural input under explicit acceptance rules.**

---

## ⚡ **Deterministic Structural Progression**

`within the declared model: structural_time = resolve(declared_structural_input, frozen_rules)`

---

## ⚡ **Structure-Based Time Resolution • Reference Implementation**

equal counts of first-seen accepted resulting structural states in the event-based model  
or equivalent accepted normalized structure in the normalized-structure model  
the same frozen rules and implementation version  
supported event streams, permutations, or groupings  
no physical clock input  
no clock synchronization  

→ **the same bounded structural-time value**

**No Physical Clock • No Synchronized Timestamps • No Forced Outcome**

Same structural time does not, by itself, prove that two structural states are identical.

---

## ⚡ **The Shift**

Physical clocks measure physical or civil time.  
Lamport clocks provide logical ordering compatible with causality.  
Vector clocks represent causal history and identify concurrency.  
Structural Time resolves bounded structural progression from accepted structure.

STIME depends on:

- declared structure  
- explicit acceptance rules  
- deterministic normalization or transition governance  
- versioned implementation behaviour  

---

## ⚠️ **Important**

**Structural Time is not a replacement for wall-clock time.**

It does not replace:

- physical clocks or timestamps  
- calendars or duration measurement  
- scheduling systems  
- causal ordering or concurrency detection  
- consensus protocols  
- communication or eventual information sharing  

Within the supplied reference models, STIME demonstrates that physical clock input, synchronized timestamps, and arrival order need not serve as the sole governing authorities over structural progression.

---

## ⚡ **What the Reference Models Demonstrate**

### **Event-Based Reference**

Three independent nodes process equivalent target structure through different supported event streams. Some streams include premature or repeated attempts.

- accepted state-changing transitions return `ADVANCED`  
- duplicate or already represented events return `NO_CHANGE`  
- invalid or premature events return `ABSTAIN`  
- nodes may temporarily hold different states and ticks  
- after all supplied streams complete, each records four first-seen accepted resulting structural states, and the base scenario reaches the same final state hash and structural-time tick  

No shared physical clock, synchronized timestamp, or central coordinator is used.

### **Normalized-Structure Reference**

The AI-style demonstration:

- normalizes supplied structural signals  
- removes duplicate elements  
- checks declared conflict pairs  
- derives structural time from accepted normalized structure  
- produces a deterministic resolution certificate  
- returns `ABSTAIN` when declared conflict is present  

The two references use related structural principles, but they do not use one identical counting rule.

---

## ⚡ **Resolution Boundary**

STIME does not create agreement without information.

Local processing can occur offline. Cross-node equality requires the conditions of the relevant model:

- event-based structural-time equality requires equal counts of first-seen accepted resulting structural states
- event-based state convergence additionally requires the same final canonical structural state
- normalized structural-time equality requires equivalent accepted normalized structure

`equal count(first-seen accepted resulting states) -> equal event-based structural time`

`equal final canonical state -> equal event-based state identity`

`equivalent accepted normalized structure -> equal normalized structural time`

Operational communication, storage, transport, or reconciliation may therefore remain necessary.

---

## 🧭 **Visual Overview**

![Structural Time Overview](docs/Structural-Time-Overview.png)

---

## 📊 **One-Page Comparison**

See how Structural Time compares with traditional and logical clocks:

[📊 Structural Time — Comparison Table](docs/Structural-Time-Comparison.md)

---

## ⚡ **Try it in 30 seconds**

### ▶ **Interactive Structural Time (Visual Demo)**

Open in browser:

`demo/structural_time_interactive_demo.html`

### ▶ **Reference Structural Time (Event-Based)**

Run:

```
python demo/structural_time.py
```

### ▶ **AI-Style Structural Time (Normalized-Structure)**

Run:

```
python demo/structural_time_ai_demo.py
```

---

## 👀 **Observe**

- supported event arrival differences  
- different normalized-signal groupings  
- explicit abstention  
- duplicate suppression  
- local offline execution  
- structural-time equality separated from state-identity equality  

Within the successful reference scenarios:

→ **the documented event streams reach equal structural-time counts and the same final canonical state despite different intermediate accepted states, while equivalent accepted normalized structure produces the same normalized structural-time value**

---

## ⚡ **How to Read the Demos**

### **Event-Based Reference**

`ADVANCED` → an accepted transition changes the declared structural state  
`NO_CHANGE` → a duplicate or already represented event does not change the state  
`ABSTAIN` → an invalid, premature, or incompatible event is refused  

Nodes may diverge during intermediate processing. In the supplied base scenario, the completed streams contain different intermediate accepted states, but each accumulates four first-seen accepted resulting states and reaches the same final canonical state.

### **Normalized-Structure Reference**

`ADVANCED` → a non-empty, conflict-free normalized structure is accepted  
`NO_CHANGE` → no accepted structure is present  
`ABSTAIN` → a declared conflict is detected  

**Important:**

`same structural time != same structural state`

The event-based demonstration therefore compares both the structural-time tick and the structural state hash.

---

## 🔗 **Quick Links**

### 📘 Docs

- [Quickstart](docs/Quickstart.md)
- [FAQ](docs/FAQ.md)
- [Test Guide](docs/Test-Guide.md)
- [Proof Sketch](docs/Proof-Sketch.md)
- [Structural Time Overview](docs/Structural-Time-Overview.png)
- [Comparison Table](docs/Structural-Time-Comparison.md)

---

### ⚡ Demos

- [Python Reference Demo](demo/structural_time.py)
- [AI-Style Demo](demo/structural_time_ai_demo.py)
- [Interactive Visual Demo](demo/structural_time_interactive_demo.html)

---

### 🔍 Verification

- [Verify Instructions](VERIFY/VERIFY.txt)
- [Demo Hash Freeze](VERIFY/FREEZE_DEMO_SHA256.txt)

---

### 📂 Repository

[demo/](demo/) · [docs/](docs/) · [VERIFY/](VERIFY/)

---

## ⚡ **Structural Invariants**

### **Event-Based Reference**

`same count of first-seen accepted resulting structural states -> same event-based structural time`

`same final canonical structural state -> same final state identity within the declared model`

`matching state hashes -> compact evidence of matching canonical state in the supplied demonstrations`

### **Normalized-Structure Reference**

`same accepted normalized structure + same frozen rules -> same normalized structural time`

`same normalized input structure + same frozen rules + same implementation version -> same certificate`

**Important:**

`same structural time != same structure`

Matching structural-time values do not establish matching structural states. The event-based reference also compares canonical state hashes. Declared conflicts are surfaced through `ABSTAIN` in the supplied demonstrations.

---

## ⚡ **Core Identities**

### **Event-Based Model**

`event_structural_time = count(first-seen accepted resulting structural states)`

### **Normalized-Structure Model**

`normalized_structural_time = count(accepted normalized structure)`

Both values are outputs of declared structural-resolution rules. Neither measures elapsed physical time.

---

## ⚡ **Governance Models**

### **Event-Based Governance**

accepted state-changing transition → `ADVANCED`  
duplicate or already represented event → `NO_CHANGE`  
invalid, premature, or incompatible event → `ABSTAIN`

### **Normalized-Structure Governance**

non-empty conflict-free accepted structure → `ADVANCED`  
empty accepted structure → `NO_CHANGE`  
declared conflict → `ABSTAIN`

No artificial advancement.  
No forced convergence from conflicting structure.

---

## ⚖️ **What Structural Time Is**

- a bounded structural-transition and structural-resolution system  
- a deterministic structural-time reference model  
- a way to represent accepted structural progression  
- a research implementation for replay, abstention, and convergence experiments  

---

## ⚠️ **What This Is Not**

- a wall-clock replacement  
- a timestamping protocol  
- a duration-measurement system  
- a scheduling or calendar system  
- a causal clock or concurrency detector  
- a consensus protocol  
- a proof of universal order independence  
- a proof of universal distributed-system convergence  

---

## 💡 **Minimal Definitions**

### **Event-Based Model**

`S = declared structural state`  
`R = frozen transition and acceptance rules`  
`U = first-seen accepted resulting structural states`

`event_structural_time = count(U)`

### **Normalized-Structure Model**

`N = normalized supplied structure`  
`A = accepted conflict-free structure`

`normalized_structural_time = count(A)`

---

## 🧮 **Demonstrated Properties**

Within the supplied examples, frozen rules, and documented boundaries:

- deterministic structural resolution  
- supported arrival-order and grouping independence  
- no physical clock input  
- no synchronized timestamp requirement  
- explicit `NO_CHANGE` and `ABSTAIN` states  
- local offline execution  
- replayable structural-time and state evidence  
- deterministic certificates in the normalized-structure reference  
- documented event streams reach equal structural-time counts despite different intermediate accepted states  
- documented event streams reach the same final canonical state hash  
- normalized structural-time equality from equivalent accepted normalized structure

---

## 🔁 **Replay Boundary**

### **Event-Based Reference**

The supplied event streams reproduce the documented structural-time and final-state results under the same acceptance rules and implementation version. Supported event streams produce the same event-based structural time when they accumulate the same number of first-seen accepted resulting states. Identical final state additionally requires the same final canonical structural state.

### **Normalized-Structure Reference**

`same normalized input structure + same frozen rules + same implementation version -> same structural time + same certificate`

Different supported arrival orders or groupings may produce the same resolution after normalization and acceptance.

Local offline processing does not remove the need for eventual structural sharing when cross-node convergence is required.

---

## 🌍 **Why This Matters**

Physical clocks, Lamport clocks, vector clocks, and STIME solve different problems.

- physical clocks measure physical or civil time  
- Lamport clocks provide logical ordering  
- vector clocks represent causal history and concurrency  
- STIME resolves bounded structural progression from accepted structure  

STIME explores systems in which physical clock input, synchronized timestamps, or arrival sequence do not serve as the sole authority over structural progression.

---

## 🧭 **Exploration Path**

**Immediate:**

- run the event-based reference  
- run the normalized-structure reference  
- inspect `ADVANCED`, `NO_CHANGE`, and `ABSTAIN` outcomes  
- compare structural-time values, state hashes, and certificates  
- evaluate validation and audit-layer use within bounded workflows  

**Further Research:**

- domain-specific transition and acceptance rules  
- formal invariant and convergence analysis  
- distributed reconciliation after eventual structural sharing  
- offline structural-resolution workflows  
- comparison with logical, causal, and physical-time systems  

---

## 🧾 **Structural Lineage**

- [SSUM-Time](https://github.com/OMPSHUNYAYA/SSUM-Time) → structural temporal continuity  
- [STOCRS](https://github.com/OMPSHUNYAYA/STOCRS) → deterministic resolution from complete structure  
- [ORL](https://github.com/OMPSHUNYAYA/Orderless-Ledger) → ledger convergence from complete compatible structure  
- [ORL-Money](https://github.com/OMPSHUNYAYA/ORL-Money) → bounded financial-state resolution  
- [ORL-Chat](https://github.com/OMPSHUNYAYA/ORL-Chat) → bounded conversational-meaning resolution  
- [ORL-AI](https://github.com/OMPSHUNYAYA/ORL-AI) → deterministic decision resolution  
- Structural Time → bounded structural progression from accepted structure 

---

## 📜 **License**

See [LICENSE](LICENSE) for the authoritative licensing terms.

**Reference Implementation:**  
Open use under the software terms stated in the LICENSE file, including use, study, implementation, extension, and deployment as permitted by those terms.

**Architecture:**  
CC BY-NC 4.0 — attribution required; noncommercial use only.

---

## ⚡ **Final Result**

Events arrived in different supported orders.  
The nodes used no shared physical clock.  
Premature input was refused.  
Duplicate input did not advance structural time.

After the supplied event streams completed their documented accepted state evolution, the base event scenario reached:

- the same structural-time tick  
- the same canonical structural state, represented by matching state hashes  

The normalized-structure scenario independently produced the same structural time and certificate from the same normalized input structure under the same rules and implementation version.

STIME did not measure elapsed time.

It resolved bounded structural progression from declared structural input under explicit acceptance rules.
