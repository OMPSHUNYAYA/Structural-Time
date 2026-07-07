# ⭐ Structural Time — Comparison Table

This document compares **Structural Time (STIME)** with physical clocks, Lamport logical clocks, and vector clocks.

The systems serve different purposes:

- physical clocks represent physical or civil time
- Lamport clocks preserve a logical ordering compatible with causality
- vector clocks represent causal history and identify concurrent events
- STIME resolves a bounded structural-progress value from accepted structure

STIME is not presented as a replacement for the other systems.

---

## 🧭 **STIME Scope**

The repository contains two related reference models.

### **Event-Based Structural Time**

The event-based reference advances structural time only when an accepted event produces a new structural state.

`valid state-changing transition -> ADVANCED`

`duplicate or already represented transition -> NO_CHANGE`

`invalid, premature, or incompatible transition -> ABSTAIN`

Within this model:

`structural_time = count(unique accepted state changes)`

### **Normalized-Structure Structural Time**

The signal-based reference first normalizes the supplied structure and checks it for declared conflicts.

Within this model:

`structural_time = count(accepted normalized structure)`

`conflicting structure -> ABSTAIN`

Both models apply the same central discipline:

`same accepted structure + same rules -> same structural time`

However:

`same structural time != same structure`

---

## 📊 **Comparison**

| **Aspect** | **Physical / Wall Clocks** | **Lamport Logical Clocks** | **Vector Clocks** | **Structural Time (STIME)** |
|---|---|---|---|---|
| **Primary Purpose** | Represent physical, elapsed, or civil time | Produce a logical ordering compatible with happened-before relations | Represent causal history and identify concurrency | Represent bounded structural progression from accepted structure |
| **Core Mechanism** | Oscillator, calibration, timestamps, and optional external synchronization | Scalar logical counter updated during local and communicated events | Per-process vector of logical counters | Accepted structural transitions or accepted normalized structure |
| **Uses Physical Time** | Yes | No | No | No, within the declared structural model |
| **Requires Physical Clock Synchronization** | Required when multiple systems need aligned physical time; not required merely to run a local clock | No | No | No |
| **Requires Communication** | Synchronization protocols require communication; a local clock may continue offline with drift | Cross-process causal relationships require message exchange | Cross-process causal history requires vector exchange | Local resolution can operate offline; cross-node convergence requires nodes eventually to possess the same accepted structure |
| **What Advances the Value?** | Passage of physical time measured by the clock | A local event, send, or receive operation under the clock algorithm | A local event and the merging of received causal metadata | An accepted state-changing transition, or an accepted normalized structural element, depending on the reference model |
| **Role of Arrival Order** | Timestamps may assist ordering, but clock skew can affect comparisons | Event and message history determines logical values | Event and message history determines vector values | Supported arrival permutations may resolve identically after normalization and acceptance |
| **Causal Ordering** | Not guaranteed by timestamps alone | Preserves happened-before implication, but cannot identify concurrency by itself | Represents causal partial order and identifies concurrent events | Not provided; STIME does not attempt to track causality |
| **Concurrency Detection** | No | No, without an additional tie-breaking or causal mechanism | Yes | No |
| **Intermediate Divergence** | Possible through clock skew, delay, or unsynchronized sources | Expected across independent processes | Expected across independent processes | Permitted; nodes may differ until their accepted structures become equivalent |
| **Final Cross-Node Agreement** | Approximate physical-time agreement depends on synchronization quality | Logical clocks do not themselves guarantee application-state convergence | Vector clocks do not themselves guarantee application-state convergence | Same accepted structure and frozen rules produce the same structural time; identical state additionally requires equivalent accepted state |
| **Duplicate Handling** | Not defined by the clock itself; duplicates may receive timestamps | Not defined as an application conflict rule | Not defined as an application conflict rule | Duplicate or already represented structure returns `NO_CHANGE` in the event-based model |
| **Invalid or Premature Input** | Not governed by the clock itself | Not inherently governed by the clock | Not inherently governed by the clock | Explicitly refused through `ABSTAIN` under the declared rules |
| **Conflict Handling** | External to the clock | External to the logical clock | Concurrent updates may be identified; application-level conflict resolution remains external | Declared conflict remains visible and does not produce forced structural convergence |
| **Offline Operation** | A local hardware clock can operate offline, subject to drift and calibration limits | Local logical progress can continue offline; cross-process relationships require later exchange | Local vector progress can continue offline; merging requires later exchange | Local structural resolution can operate offline; equivalent final resolution requires equivalent accepted structure |
| **Replay Behaviour** | Recorded timestamps can be replayed, but newly generated physical timestamps are environment-dependent | Deterministic for the same declared event and message history | Deterministic for the same declared process, event, and message history | Deterministic for the same accepted structure, frozen rules, normalization, and implementation version |
| **Same Value Implies Same Structure?** | No | No | Not necessarily | No |
| **Primary Strength** | Physical-time measurement, duration, calendars, deadlines, and scheduling | Compact logical ordering compatible with causal precedence | Detailed causal history and concurrency detection | Explicit acceptance, refusal, duplicate suppression, order-insensitive supported resolution, and reproducible structural progress |
| **Primary Limitation** | Drift, skew, calibration, and synchronization error | Cannot identify concurrency and does not represent physical time | Metadata grows with the number of represented processes and membership can be difficult | Does not provide wall-clock time, duration, scheduling, causal ordering, consensus, or universal order independence |

---

## 🔍 **Central Distinction**

Lamport and vector clocks attach logical values to event histories.

STIME asks a different bounded question:

**Has the declared structure changed in a way that the active rules accept as structural progress?**

The event-based model therefore advances only when the declared structural state changes through an accepted transition.

The normalized-structure model derives the same structural time whenever normalization produces the same accepted structure.

`accepted structure -> structural time`

The value is an output of the declared structural-resolution rules. It is not a measurement of elapsed time.

---

## ⚠️ **Communication and Convergence Boundary**

STIME does not imply that distributed systems can reach the same state without ever exchanging information.

Independent nodes may process locally without synchronized clocks or a central coordinator. However, they can resolve the same final structural time only after they possess equivalent accepted structure under the same rules.

`eventual equivalent accepted structure -> equivalent structural time`

Operational communication, transport, storage, or reconciliation may therefore remain necessary to make the relevant structure available.

The eliminated dependency is narrower:

**Wall-clock time, synchronized timestamps, and arrival order need not serve as the sole governing authorities over structural progression within the declared model.**

---

## ⚠️ **Conflict Boundary**

STIME does not manufacture agreement from incompatible structure.

In the normalized-structure demonstration:

`declared conflict -> ABSTAIN`

In the interactive event-based conflict scenario, nodes with incompatible accepted states may still hold the same tick count while their state hashes differ.

Therefore:

`same structural time != same structural state`

A valid convergence claim requires examination of both:

- structural-time equality
- accepted-state or state-identity equality

---

## ✅ **What the Repository Demonstrates**

Within its declared examples, STIME demonstrates:

- structural progression without physical clock input
- deterministic duplicate suppression
- explicit refusal of invalid or premature transitions
- explicit visibility of declared conflicts
- supported permutation independence
- local offline processing
- convergence after equivalent accepted structure becomes available
- replayable structural-time and state evidence

These are repository-bounded implementation results. They do not establish universal convergence for arbitrary distributed systems or arbitrary transition rules.

---

## ⭐ **One-Line Comparison**

**Physical clocks measure time. Lamport clocks order events. Vector clocks represent causal history. STIME resolves bounded structural progression from accepted structure.**
