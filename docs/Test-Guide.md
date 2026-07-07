# ⭐ Structural Time (STIME) — Test Guide

**Bounded Verification for the Event-Based, Normalized-Structure, and Interactive Reference Models**

This guide explains how to run and verify the supplied Structural Time (STIME) demonstrations.

The repository contains three demonstrations:

- `demo/structural_time.py` — event-based structural-transition reference  
- `demo/structural_time_ai_demo.py` — normalized-structure reference  
- `demo/structural_time_interactive_demo.html` — interactive base and conflict scenarios  

The demonstrations use no physical clock input or synchronized timestamps to calculate structural time.

They do not establish universal convergence, consensus, causal ordering, or production suitability.

---

## **1. Requirements**

### **Python Demonstrations**

Required:

- Python 3.9 or later  
- a terminal opened in the repository root  

No external Python packages are required.

### **Interactive Demonstration**

Required:

- a modern web browser  

No server or internet connection is required after the repository has been downloaded.

---

## **2. Quick Test Matrix**

| Test | File | Main Verification |
|---|---|---|
| Event-Based Reference | `demo/structural_time.py` | Different event streams reach equal ticks and the same final canonical state |
| Normalized-Structure Reference | `demo/structural_time_ai_demo.py` | Normalization, conflict refusal, permutation independence, and deterministic certificates |
| Interactive Base Scenario | `demo/structural_time_interactive_demo.html` | Equal structural time and equal final-state representation |
| Interactive Conflict Scenario | `demo/structural_time_interactive_demo.html` | Equal structural time can coexist with different final states |

---

# **PART I — EVENT-BASED REFERENCE**

## **3. Run the Event-Based Demo**

From the repository root, run:

```text
python demo/structural_time.py
```

On Windows, this may also be run with:

```text
py demo/structural_time.py
```

No setup or configuration is required.

---

## **4. What the Event-Based Demo Contains**

The demonstration creates three independent nodes:

- `Node-A`  
- `Node-B`  
- `Node-C`  

Each node begins with:

- an empty account set  
- no pending transactions  
- no confirmed transactions  
- structural-time tick `0`  

The nodes process equivalent target structure through different event streams.

Some streams contain:

- different event arrival orders  
- premature attempts  
- repeated attempts after the required structure becomes available  

The nodes do not share:

- a physical clock  
- synchronized timestamps  
- a structural-time counter  
- a central coordinator  

---

## **5. Event-Based Resolution States**

### **ADVANCED**

An accepted transition changes the declared structural state.

Examples:

- opening a new account  
- creating a valid pending transaction  
- confirming an existing pending transaction  

The event-based implementation increments the tick when the accepted resulting state hash has not previously been counted by the node.

### **NO_CHANGE**

The supplied event is already represented in the structural state.

Examples:

- opening an account that is already open  
- repeating the same pending transaction proposal  
- confirming an already confirmed transaction  

The state and tick remain unchanged.

### **ABSTAIN**

The supplied event does not satisfy the active transition rules.

Examples:

- `MOVE` before both accounts exist  
- `CONFIRM` before the transaction is pending  
- a non-positive transaction amount  
- an unknown operation  
- an incompatible transaction claim  

The state and tick remain unchanged.

---

## **6. Expected Event-Based Behaviour**

### **Node-A**

Node-A processes:

1. `OPEN(A)`  
2. `OPEN(B)`  
3. `MOVE(tx1, A -> B, 100)`  
4. `CONFIRM(tx1)`  

All four transitions are accepted.

Expected final tick:

```text
4
```

---

### **Node-B**

Node-B processes:

1. `OPEN(B)`  
2. `OPEN(A)`  
3. an early `CONFIRM(tx1)`  
4. `MOVE(tx1, A -> B, 100)`  
5. `CONFIRM(tx1)` again  

The first confirmation returns:

```text
ABSTAIN
```

because no pending transaction exists yet.

After the valid `MOVE`, the repeated confirmation is accepted.

Expected final tick:

```text
4
```

---

### **Node-C**

Node-C first attempts the transaction before the required accounts exist.

The first `MOVE` returns:

```text
ABSTAIN
```

The node then opens both accounts, retries the transaction, and confirms it.

Expected final tick:

```text
4
```

---

## **7. Event-Based Pass Conditions**

At the end of the script, verify that:

- Node-A tick is `4`  
- Node-B tick is `4`  
- Node-C tick is `4`  
- all three displayed final hash prefixes are identical  

The expected structural-time result is:

```text
A: <matching-hash-prefix> tick: 4
B: <matching-hash-prefix> tick: 4
C: <matching-hash-prefix> tick: 4
```

The exact displayed hash prefix may be treated as implementation output.

The important test conditions are:

```text
tick_A = tick_B = tick_C = 4
```

and:

```text
canonical_state_A = canonical_state_B = canonical_state_C
```

The script displays shortened SHA-256 state hashes as compact evidence of the matching canonical states.

---

## **8. What the Event-Based Demo Demonstrates**

Within the supplied streams and rules, it demonstrates:

- local processing without physical clock input  
- no synchronized timestamp requirement  
- deterministic transition evaluation  
- safe refusal of premature events  
- retry after required structure becomes available  
- different intermediate accepted states  
- monotonic local structural-time ticks  
- equal final ticks  
- the same final canonical structural state  

It does not prove that every event permutation will converge.

---

## **9. Event-Order Boundary**

The supplied event streams are intentionally supported examples.

Different arbitrary orderings may change:

- which events are premature  
- whether required events are retried  
- which transitions are accepted  
- the number of counted states  
- the final structural state  

Therefore:

```text
supported event streams may converge
```

does not imply:

```text
every possible event permutation must converge
```

---

## **10. Manual Duplicate Test**

The default event-based stream primarily demonstrates premature refusal and retry.

To verify `NO_CHANGE`, open a Python interpreter from the repository root:

```text
python
```

Then run:

```python
from demo.structural_time import Event, StructuralTimeNode

node = StructuralTimeNode("Duplicate-Test")

print(node.resolve(Event("OPEN", account="A")))
print(node.resolve(Event("OPEN", account="A")))
```

Expected behaviour:

- the first `OPEN(A)` returns `ADVANCED`  
- the second `OPEN(A)` returns `NO_CHANGE`  
- the tick remains `1` after the duplicate  

Exit the interpreter with:

```python
exit()
```

---

## **11. Manual Invalid-Input Test**

Open a Python interpreter:

```text
python
```

Then run:

```python
from demo.structural_time import Event, StructuralTimeNode

node = StructuralTimeNode("Invalid-Test")

print(node.resolve(Event("CONFIRM", tx_id="missing")))
```

Expected result:

```text
status = ABSTAIN
tick = 0
```

The missing transaction is not accepted and does not advance structural time.

---

# **PART II — NORMALIZED-STRUCTURE REFERENCE**

## **12. Run the Normalized-Structure Demo**

From the repository root, run:

```text
python demo/structural_time_ai_demo.py
```

On Windows:

```text
py demo/structural_time_ai_demo.py
```

---

## **13. What the Normalized-Structure Demo Does**

The demonstration:

1. collects structural signals  
2. removes duplicate signals  
3. sorts the signals into canonical form  
4. checks declared conflict pairs  
5. derives accepted structure  
6. calculates normalized structural time  
7. generates a deterministic certificate  

The central calculation is:

```text
normalized_structural_time = count(accepted normalized structure)
```

---

## **14. Reference Three-Node Scenario**

The supplied nodes contain:

```text
Node A = {"fever"}
Node B = {"cough"}
Node C = {"fatigue"}
```

After set merge and normalization:

```text
["cough", "fatigue", "fever"]
```

Expected result:

```text
state = ADVANCED
structural_time = 3
accepted_structure = ["cough", "fatigue", "fever"]
```

---

## **15. Replay and Different-Grouping Scenario**

The same final structural signals are distributed differently:

```text
Replay Node X = {"cough", "fatigue"}
Replay Node Y = {"fever"}
Replay Node Z = {}
```

The empty replay node produces:

```text
state = NO_CHANGE
structural_time = 0
```

After merging all replay inputs, the normalized structure is again:

```text
["cough", "fatigue", "fever"]
```

Expected merged replay result:

```text
state = ADVANCED
structural_time = 3
```

The reference merge and replay merge should produce:

- the same normalized input structure  
- the same accepted structure  
- the same structural-time value  
- the same certificate  

---

## **16. Conflict Scenario**

The conflict scenario includes:

```text
"fatigue"
"no_fatigue"
```

These signals form a declared conflict pair.

Expected merged conflict result:

```text
state = ABSTAIN
structural_time = 0
accepted_structure = []
```

The conflict remains visible.

It is not converted into an accepted result.

---

## **17. Permutation Test**

The normalized-structure script checks all permutations of the three reference signal groups.

For three groups, the expected number of permutations is:

```text
6
```

Expected output includes:

```text
Permutations checked        : 6
Permutation independence    : True
Resolved state              : ADVANCED
Resolved structural time    : 3
```

This verifies permutation independence for the supplied set-union and normalization model.

It does not establish universal order independence for arbitrary transition systems.

---

## **18. Normalized-Structure Pass Conditions**

In the final checks, verify:

```text
Reference structural time   : 3
Replay structural time      : 3
Reference matching replay   : True
Matching certificate        : True
Conflict visible            : True
No forced convergence       : True
No accepted conflict state  : True
```

These are the primary pass conditions for the normalized-structure reference.

---

## **19. Write the JSON Verification Output**

To write the full result payload to JSON, run:

```text
python demo/structural_time_ai_demo.py --write-output
```

The default output file is:

```text
structural_time_ai_result.json
```

To choose another location:

```text
python demo/structural_time_ai_demo.py --write-output --output demo/structural_time_ai_result.json
```

The JSON output includes:

- normalized structures  
- accepted structures  
- governance status  
- structural-time values  
- certificates  
- resolution capsules  
- permutation results  
- final checks  

---

## **20. Certificate Verification Boundary**

The normalized-structure certificate incorporates:

- normalized input structure  
- resolution state  
- structural-time value  
- accepted structure  

Therefore:

```text
same normalized input structure
+ same rules
+ same implementation version
-> same certificate
```

Accepted structure alone is not sufficient to guarantee certificate identity.

Different conflicting inputs may both produce an empty accepted structure while retaining different normalized input structures and different certificates.

---

# **PART III — INTERACTIVE DEMONSTRATION**

## **21. Open the Interactive Demo**

Open this file in a modern browser:

```text
demo/structural_time_interactive_demo.html
```

It may be opened by:

- double-clicking the file  
- dragging it into a browser  
- using the browser’s Open File command  

No local server is required.

---

## **22. Interactive Controls**

The interface provides:

- **Scenario** selector  
- **Step** button  
- **Auto Play** button  
- **Reset** button  

Use **Step** to observe one event position at a time.

Use **Auto Play** to process the scenario automatically.

---

## **23. Base Convergence Test**

Select:

```text
Base Convergence
```

Run the scenario to completion.

Expected final metrics:

```text
Structural View       = Converged
Structural Time Equal = Yes
Truth Identity Equal  = Yes
```

Expected node ticks:

```text
[4, 4, 4]
```

The displayed state hashes should match.

The scenario demonstrates that the supplied streams reach:

- equal structural-time counts  
- the same final canonical state representation  

despite different intermediate processing paths.

---

## **24. Conflict Scenario Test**

Select:

```text
Conflict / Abstain
```

Run the scenario to completion.

Node-A and Node-C accept a transaction amount of `100`.

Node-B accepts a transaction amount of `200`.

Expected final metrics:

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

Equal structural-time values do not establish final-state identity.

---

## **25. What to Observe in the Interactive Demo**

During execution, observe:

- the current event for each node  
- `ADVANCED`, `NO_CHANGE`, or `ABSTAIN` status  
- each node’s local tick  
- each node’s displayed state hash  
- intermediate divergence  
- final structural-time equality  
- final state-identity equality or inequality  

Structural-time comparison and state comparison must remain separate.

---

# **PART IV — INTERPRETATION**

## **26. Core Event-Based Identity**

For the supplied event-based implementation:

```text
event_structural_time =
count(first-seen accepted resulting structural states)
```

From the same empty initial state, its reachable final-state count is:

```text
event_structural_time =
count(accounts)
+ count(pending)
+ 2 × count(confirmed)
```

This identity is specific to the current monotonic reference model.

It must not be generalized to modified models that permit deletion, reversal, alternative transition paths, or revisiting earlier states.

---

## **27. Core Normalized-Structure Identity**

For the normalized-structure reference:

```text
normalized_structural_time =
count(accepted normalized structure)
```

If declared conflict is present:

```text
state = ABSTAIN
structural_time = 0
accepted_structure = []
```

---

## **28. Structural Time and State Identity**

The following implication is invalid:

```text
same structural time -> same structural state
```

The correct interpretation is:

```text
same structural time = same value under the relevant counting model
```

State identity requires a separate comparison of:

- canonical structural state  
- state hash  
- accepted structure  
- normalized input structure  
- certificate  

depending on the reference model and application.

---

## **29. Physical-Time Boundary**

The supplied resolution algorithms do not read:

- wall-clock time  
- timestamps  
- GPS time  
- NTP time  
- elapsed duration  

Therefore, their structural-time calculations do not require physical clock input.

This does not imply that operational systems never need physical time for:

- scheduling  
- deadlines  
- latency measurement  
- legal timestamps  
- monitoring  
- human coordination  

---

## **30. Communication Boundary**

Local structural resolution can run offline.

Cross-node convergence may still require:

- communication  
- event transfer  
- shared storage  
- retry of premature events  
- reconciliation  
- eventual availability of relevant structure  

STIME does not create agreement without information.

---

## **31. What These Tests Demonstrate**

Within the supplied rules, scenarios, and implementation version, the tests demonstrate:

- deterministic structural resolution  
- no physical clock input in the calculation  
- no synchronized timestamp requirement  
- explicit `ADVANCED`, `NO_CHANGE`, and `ABSTAIN` outcomes  
- duplicate suppression  
- invalid and premature input refusal  
- monotonic event-based ticks  
- supported event-order tolerance  
- deterministic normalized-structure calculation  
- set-based permutation independence in the normalized model  
- deterministic normalized certificates  
- visible conflict  
- no forced state convergence  
- structural-time equality separated from structural-state identity  

---

## **32. What These Tests Do Not Demonstrate**

The demonstrations do not establish:

- universal order independence  
- universal distributed convergence  
- consensus  
- causal ordering  
- concurrency detection  
- network-protocol correctness  
- crash recovery  
- durable persistence  
- authentication or authorization  
- malicious-input resistance  
- arbitrary rule correctness  
- physical-time replacement  
- scheduling correctness  
- production or safety-critical suitability  

---

## **33. Suggested Verification Sequence**

1. Run `demo/structural_time.py`.  
2. Confirm all final ticks are `4`.  
3. Confirm all final displayed hash prefixes match.  
4. Run `demo/structural_time_ai_demo.py`.  
5. Confirm the reference and replay structural times are `3`.  
6. Confirm the certificates match.  
7. Confirm six permutations are checked successfully.  
8. Confirm the conflict result is `ABSTAIN`.  
9. Open the interactive demo.  
10. Run **Base Convergence** and verify time and state equality.  
11. Run **Conflict / Abstain** and verify time equality with state inequality.  
12. Optionally write and inspect the JSON verification output.  

---

## **34. Troubleshooting**

### **Python Command Not Found**

Try:

```text
py demo/structural_time.py
```

or verify that Python 3.9 or later is installed.

### **File Not Found**

Confirm that the terminal is open in the repository root.

The following directories should be visible:

```text
demo/
docs/
VERIFY/
```

### **Interactive Demo Does Not Open**

Open the HTML file directly in another modern browser.

No web server is required.

### **Unexpected Output**

Confirm that:

- the demonstration files have not been modified  
- the same implementation version is being used  
- the event streams and conflict rules remain unchanged  
- the script is being run from the intended repository copy  

---

## ⭐ **Final Test Summary**

A successful verification should establish:

### **Event-Based Reference**

```text
final ticks = [4, 4, 4]
final canonical states = equal
```

### **Normalized-Structure Reference**

```text
reference structural time = 3
replay structural time = 3
matching certificate = True
permutation independence = True
conflict result = ABSTAIN
```

### **Interactive Conflict Scenario**

```text
structural_time_equal = Yes
truth_identity_equal = No
```

---

## ⭐ **One-Line Summary**

**The STIME test suite demonstrates bounded deterministic structural-time resolution under explicit acceptance rules, including premature-input refusal, duplicate suppression, supported order tolerance, normalized permutation independence, visible conflict, and separate verification of structural-time equality and structural-state identity.**
