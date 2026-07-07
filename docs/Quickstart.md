# ⭐ Structural Time (STIME) — Quickstart

**Bounded Structural Progression Without Physical Clock Input**

This quickstart explains how to run the three supplied Structural Time (STIME) demonstrations:

- `demo/structural_time.py` — event-based structural-transition reference  
- `demo/structural_time_ai_demo.py` — normalized-structure reference  
- `demo/structural_time_interactive_demo.html` — interactive base and conflict scenarios  

The demonstrations calculate structural-time values without reading physical clocks or synchronized timestamps.

---

## ⚡ **Fastest Way to Begin**

Open a terminal in the repository root.

Run:

```text
python demo/structural_time.py
```

On Windows, this may also be run with:

```text
py demo/structural_time.py
```

No external Python packages are required.

---

## 👀 **What the Event-Based Demo Shows**

The demonstration creates:

- `Node-A`  
- `Node-B`  
- `Node-C`  

The nodes process equivalent target structure through different supported event streams.

Some streams include:

- different arrival orders  
- premature attempts  
- later retries  

The nodes use no shared:

- physical clock  
- synchronized timestamp  
- structural-time counter  
- central coordinator  

---

## ⚡ **Expected Event-Based Result**

The final output should show:

```text
A: <matching-hash-prefix> tick: 4
B: <matching-hash-prefix> tick: 4
C: <matching-hash-prefix> tick: 4
```

Verify:

```text
tick_A = tick_B = tick_C = 4
```

and:

```text
canonical_state_A = canonical_state_B = canonical_state_C
```

The displayed shortened hashes provide compact evidence that the final canonical states match.

---

## 🔬 **What Happens During the Run**

### **Node-A**

Processes four accepted transitions:

1. `OPEN(A)`  
2. `OPEN(B)`  
3. `MOVE(tx1, A -> B, 100)`  
4. `CONFIRM(tx1)`  

Final tick:

```text
4
```

### **Node-B**

Attempts `CONFIRM(tx1)` before the transaction exists.

The early confirmation returns:

```text
ABSTAIN
```

The transaction is later created and confirmed successfully.

Final tick:

```text
4
```

### **Node-C**

Attempts `MOVE(tx1)` before the required accounts exist.

The early move returns:

```text
ABSTAIN
```

The accounts are then opened, the move is retried, and the transaction is confirmed.

Final tick:

```text
4
```

---

## ⚖️ **Event-Based Resolution States**

### **ADVANCED**

An accepted transition changes the declared structural state.

```text
accepted state-changing transition -> ADVANCED
```

The tick increments when the accepted resulting state hash has not previously been counted by the node.

### **NO_CHANGE**

The input is already represented in the current state.

```text
duplicate or already represented input -> NO_CHANGE
```

The state and tick remain unchanged.

### **ABSTAIN**

The input is invalid, premature, unknown, or incompatible under the active rules.

```text
invalid or premature input -> ABSTAIN
```

The state and tick remain unchanged.

The default event-based run primarily demonstrates premature refusal and later retry. See the Test Guide for a direct duplicate test.

---

## 📌 **Event-Based Identity**

For the supplied implementation:

```text
event_structural_time =
count(first-seen accepted resulting structural states)
```

From the same empty initial state:

```text
event_structural_time =
count(accounts)
+ count(pending)
+ 2 × count(confirmed)
```

This identity is specific to the current monotonic reference model.

---

## ⚠️ **Order Boundary**

The supplied event streams demonstrate supported order tolerance.

They do not prove that every event permutation will converge.

Different arbitrary orderings may change:

- which events are premature  
- whether required events are retried  
- which transitions are accepted  
- the intermediate state path  
- the final state  

Therefore:

```text
supported event streams may converge
```

does not imply:

```text
all possible event permutations must converge
```

---

# **NORMALIZED-STRUCTURE DEMO**

## ⚡ **Run the AI-Style Reference**

Run:

```text
python demo/structural_time_ai_demo.py
```

On Windows:

```text
py demo/structural_time_ai_demo.py
```

The demonstration:

- removes duplicate signals  
- sorts signals into canonical form  
- checks declared conflict pairs  
- derives accepted structure  
- calculates normalized structural time  
- generates deterministic certificates  
- checks all six permutations of the three reference signal groups  

---

## 👀 **Expected Normalized-Structure Results**

The reference signals normalize to:

```text
["cough", "fatigue", "fever"]
```

Expected result:

```text
state = ADVANCED
structural_time = 3
accepted_structure = ["cough", "fatigue", "fever"]
```

The differently grouped replay input should produce:

```text
Reference structural time   : 3
Replay structural time      : 3
Reference matching replay   : True
Matching certificate        : True
```

The permutation check should show:

```text
Permutations checked        : 6
Permutation independence    : True
Resolved structural time    : 3
```

---

## ⚠️ **Normalized Conflict Result**

The conflict scenario contains:

```text
"fatigue"
"no_fatigue"
```

Expected result:

```text
state = ABSTAIN
structural_time = 0
accepted_structure = []
```

The declared conflict remains visible and is not converted into an accepted result.

---

## 📌 **Normalized-Structure Identity**

For the normalized-structure reference:

```text
normalized_structural_time =
count(accepted normalized structure)
```

Therefore:

```text
same accepted normalized structure
+ same frozen rules
-> same normalized structural time
```

Certificate identity requires:

```text
same normalized input structure
+ same rules
+ same implementation version
-> same certificate
```

---

## 💾 **Optional JSON Output**

Run:

```text
python demo/structural_time_ai_demo.py --write-output
```

The default output file is:

```text
structural_time_ai_result.json
```

To select another location:

```text
python demo/structural_time_ai_demo.py --write-output --output demo/structural_time_ai_result.json
```

---

# **INTERACTIVE DEMO**

## ⚡ **Open the Visual Demonstration**

Open:

```text
demo/structural_time_interactive_demo.html
```

Use:

- **Step** to process one event position at a time  
- **Auto Play** to run the full scenario  
- **Reset** to restart  
- **Scenario** to switch between base and conflict demonstrations  

No local server is required.

---

## ✅ **Base Convergence Scenario**

Select:

```text
Base Convergence
```

Expected final result:

```text
Structural View       = Converged
Structural Time Equal = Yes
Truth Identity Equal  = Yes
```

Expected ticks:

```text
[4, 4, 4]
```

The displayed final state hashes should match.

---

## ⚠️ **Conflict Scenario**

Select:

```text
Conflict / Abstain
```

Node-A and Node-C accept an amount of `100`.

Node-B accepts an amount of `200`.

Expected final result:

```text
Structural View       = Conflict Visible
Structural Time Equal = Yes
Truth Identity Equal  = No
```

Expected ticks:

```text
[4, 4, 4]
```

Expected state-hash relationship:

```text
Node-A hash = Node-C hash
Node-B hash != Node-A hash
```

This demonstrates:

```text
same structural time != same structural state
```

---

## ⚠️ **Critical Interpretation**

Structural-time equality and structural-state identity are separate questions.

Equal structural-time values mean only that the values are equal under the relevant counting model.

They do not prove that:

- the final states are identical  
- the inputs were identical  
- the rules were identical  
- the evidence is authentic  
- the underlying claims are true  

State identity must be checked separately.

---

## 🔁 **Determinism Check**

Run the event-based demo multiple times:

```text
python demo/structural_time.py
```

Under the same:

- ordered event streams  
- initial state  
- transition rules  
- canonicalization  
- counted-state history  
- implementation version  

the documented results should repeat.

Run the normalized-structure demo multiple times:

```text
python demo/structural_time_ai_demo.py
```

Under the same:

- normalized input structure  
- conflict rules  
- acceptance rules  
- certificate construction  
- implementation version  

the structural-time values and certificates should repeat.

---

## 🚫 **What STIME Does Not Provide**

STIME does not provide:

- physical-time measurement  
- wall-clock timestamps  
- duration measurement  
- scheduling  
- latency guarantees  
- causal ordering  
- concurrency detection  
- consensus  
- authentication  
- authorization  
- universal order independence  
- universal distributed convergence  
- production or safety certification  

---

## ✅ **What the Demonstrations Establish**

Within the supplied rules, scenarios, and implementation version, they demonstrate:

- deterministic structural resolution  
- no physical clock input in the calculation  
- no synchronized timestamp requirement  
- explicit `ADVANCED`, `NO_CHANGE`, and `ABSTAIN` outcomes  
- premature-input refusal  
- duplicate suppression under the declared rules  
- monotonic event-based ticks  
- supported event-order tolerance  
- deterministic normalization  
- set-based permutation independence in the normalized model  
- deterministic normalized certificates  
- visible conflict  
- no forced state convergence  
- separate structural-time and structural-state verification  

---

## 🌐 **Communication Boundary**

Local structural resolution can operate offline.

Cross-node convergence may still require:

- communication  
- event transfer  
- shared storage  
- retry of premature events  
- reconciliation  
- eventual availability of relevant structure  

STIME does not create agreement without information.

---

## 📁 **Repository Structure**

```text
Structural-Time/

├── README.md
├── LICENSE
│
├── demo/
│   ├── structural_time.py
│   ├── structural_time_ai_demo.py
│   └── structural_time_interactive_demo.html
│
├── docs/
│   ├── FAQ.md
│   ├── Quickstart.md
│   ├── Test-Guide.md
│   ├── Proof-Sketch.md
│   ├── Structural-Time-Comparison.md
│   └── Structural-Time-Overview.png
│
└── VERIFY/
    ├── VERIFY.txt
    └── FREEZE_DEMO_SHA256.txt
```

---

## 📚 **Next Documents**

- [FAQ](FAQ.md)  
- [Test Guide](Test-Guide.md)  
- [Proof Sketch](Proof-Sketch.md)  
- [Comparison Table](Structural-Time-Comparison.md)  

---

## ⚡ **Suggested Two-Minute Verification**

1. Run `python demo/structural_time.py`.  
2. Confirm final ticks `[4, 4, 4]`.  
3. Confirm the final displayed hash prefixes match.  
4. Run `python demo/structural_time_ai_demo.py`.  
5. Confirm reference and replay structural times equal `3`.  
6. Confirm `Matching certificate = True`.  
7. Confirm six permutations pass.  
8. Confirm the declared conflict returns `ABSTAIN`.  
9. Open the interactive demo.  
10. Verify base state equality and conflict-state inequality.  

---

## ⭐ **One-Line Summary**

**Structural Time (STIME) demonstrates bounded deterministic structural-time resolution from declared structural input under explicit acceptance rules, without using physical clock input or synchronized timestamps, while keeping structural-time equality separate from structural-state identity.**
