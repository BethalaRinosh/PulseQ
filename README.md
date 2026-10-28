# PulseQ

**Advanced Hospital Management and Emergency Response System**  
Academic DSA micro-project built with Python 3 and the standard library.

> **Academic prototype disclaimer:** PulseQ is an educational simulation for demonstrating data structures and algorithms. It does not replace professional medical judgment, validated clinical triage protocols, or a real hospital information system. It must not be used to make real patient-care decisions.

## Project status

**Current milestone:** Step 1 of 10 — repository and reference audit.  
The repository was empty when work began. No application code has been written yet.

## Planned features

- Patient registration and record management (create, view, update, delete).
- First-come-first-served routine patient/appointment queue.
- Emergency queue ordered by urgency, with stable arrival-order tie-breaking.
- Doctor directory and allocation by specialization and availability.
- Patient searching by ID/name and sorting by name, age, urgency, and arrival time.
- Menu-driven CLI, input validation, and a small repeatable test suite.

## Planned data structures and algorithms

| Requirement | Planned implementation |
|---|---|
| Patient records | Custom singly linked list |
| Routine flow | Custom FIFO queue |
| Emergency flow | Custom binary heap priority queue |
| Doctor details | Python lists/arrays |
| Searching | Manual linear search and binary search |
| Sorting | Manual merge sort and insertion sort |
| Complexity documentation | Big-O table in this README |

All required core DSA structures and algorithms will be implemented directly for educational clarity, not delegated to `collections.deque`, `heapq`, or built-in sorting.

## How to run

The CLI entry point and run command will be documented after the initial application scaffold is created. The planned runtime is Python 3; the target is standard-library-only.

## References and credits

These sources were reviewed for architecture ideas, DSA examples, testing approaches, and triage context. PulseQ will not copy their core DSA implementations.

- [ianberwa/hospital-system](https://github.com/ianberwa/hospital-system) — Python hospital queue/triage example using a linked FIFO queue and binary heap. GitHub metadata currently reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [dhanushsr26/hospital-priority-queue-python](https://github.com/dhanushsr26/hospital-priority-queue-python) — patient priority queue and merge-sort example. GitHub metadata currently reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [SudharsanSaravanan/Hospital_Mangement_System](https://github.com/SudharsanSaravanan/Hospital_Mangement_System) — patient-priority project illustrating heap-based ordering and patient lookup concepts. GitHub metadata currently reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [Sidoine20/EmergencyHospitalSystem](https://github.com/Sidoine20/EmergencyHospitalSystem) — modular DSA hospital-management example. Its GitHub repository metadata declares the **MIT License**. We may consult its structure and tests; any adapted code would require MIT attribution and license preservation. No code has been copied.
- [World Health Organization: Interagency Integrated Triage Tool](https://www.who.int/tools/triage) — background on acuity-based prioritisation and red/yellow/green urgency categories. PulseQ will be an educational severity simulation, not an implementation or validation of a clinical protocol.

## Big-O complexity

Detailed operation-by-operation complexity analysis will be filled in as each custom data structure and algorithm is implemented and tested.

## Progress log

| Step | Status | Work |
|---|---|---|
| 1. Repository and reference audit | In progress | Confirmed the repository was empty, reviewed relevant reference projects and checked declared license metadata. |
| 2. Project scaffold and README | Pending | Establish the clean module/file structure and expand run instructions, complexity documentation, and the project log. |
| 3. Patient records with linked list | Pending | Implement patient CRUD and duplicate-ID protection. |
| 4. Routine appointment queue | Pending | Implement custom FIFO queue. |
| 5. Emergency priority queue | Pending | Implement custom binary heap and stable urgency ties; run checkpoint tests. |
| 6. Doctors and allocation | Pending | Add doctor records and specialization-aware allocation. |
| 7. Searching | Pending | Implement linear and binary search. |
| 8. Sorting | Pending | Implement merge sort and insertion sort. |
| 9. CLI integration | Pending | Integrate modules and add startup disclaimer and input validation. |
| 10. Testing and final documentation | Pending | Run full edge-case audit, fix defects, and finish documentation. |

**Next:** Complete Step 1 by committing this audit record, then stop for review before Step 2.
