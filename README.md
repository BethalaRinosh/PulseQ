# PulseQ

**Advanced Hospital Management and Emergency Response System**  
Academic DSA micro-project built with Python 3 and the standard library.

> **Academic prototype disclaimer:** PulseQ is an educational simulation for demonstrating data structures and algorithms. It does not replace professional medical judgment, validated clinical triage protocols, or a real hospital information system. It must not be used to make real patient-care decisions.

## Project status

**Current milestone:** Step 2 of 10 — project scaffold and documentation.  
The repository scaffold is in place. The application is not yet runnable because the CLI and core modules are intentionally deferred to later steps.

## Planned features

- Patient registration and record management (create, view, update, delete).
- First-come-first-served routine patient/appointment queue.
- Emergency queue ordered by urgency, with stable arrival-order tie-breaking.
- Doctor directory and allocation by specialization and availability.
- Patient searching by ID/name and sorting by name, age, urgency, and arrival time.
- Menu-driven CLI, input validation, and a small repeatable test suite.

## Project structure

```text
PulseQ/
├── README.md
├── .gitignore
├── pulseq/
│   ├── __init__.py
│   └── README.md
├── tests/
│   └── README.md
├── docs/
│   └── README.md
└── examples/
    └── README.md
```

Planned modules to be added in their own milestones:

| Module | Responsibility |
|---|---|
| `pulseq/models.py` | Patient and doctor record definitions |
| `pulseq/patient_store.py` | Custom singly linked list and patient CRUD |
| `pulseq/queues.py` | Custom FIFO queue and binary-heap priority queue |
| `pulseq/doctors.py` | Doctor directory and specialization-aware allocation |
| `pulseq/searching.py` | Manual linear and binary search |
| `pulseq/sorting.py` | Manual merge sort and insertion sort |
| `pulseq/cli.py` | Menu-driven CLI, startup disclaimer, and input validation |
| `main.py` | Application entry point |
| `tests/test_pulseq.py` | Built-in `unittest` coverage for core behaviours |

The scaffold contains no DSA implementations yet. This is deliberate so each algorithm can be built and reviewed in its planned step.

## Requirements

- Python 3 (target: Python 3.10 or newer).
- No third-party packages are planned; the test suite will use Python's built-in `unittest`.

## How to run

**Not runnable yet.** The CLI entry point will be created during the implementation milestones. Once integrated, the intended launch command from the repository root is:

```bash
python main.py
```

The intended test command will be:

```bash
python -m unittest discover -s tests -v
```

These commands are documented as the target workflow; they will be verified after the corresponding files exist.

## Planned data structures and algorithms

| Requirement | Planned implementation |
|---|---|
| Patient records | Custom singly linked list |
| Routine flow | Custom FIFO queue |
| Emergency flow | Custom binary heap priority queue |
| Doctor details | Python lists/arrays |
| Searching | Manual linear search and binary search |
| Sorting | Manual merge sort and insertion sort |
| Complexity documentation | Operation-by-operation Big-O table below |

All required core DSA structures and algorithms will be implemented directly for educational clarity, not delegated to `collections.deque`, `heapq`, or built-in sorting.

## Big-O complexity

The table will be completed as each operation is implemented and tested. Expected complexity targets for the planned structures:

| Operation | Planned structure/algorithm | Expected time |
|---|---|---|
| Find patient by ID in linked list | Linear traversal | O(n) |
| Insert patient at linked-list head | Singly linked list | O(1) |
| Delete patient by ID | Singly linked list | O(n) |
| Enqueue/dequeue routine patient | Linked FIFO queue with head/tail | O(1) |
| Insert/remove emergency case | Binary heap | O(log n) |
| Peek most urgent emergency | Binary heap root | O(1) |
| Linear search | Unsorted collection | O(n) |
| Binary search | Sorted array/list | O(log n) |
| Merge sort | Divide-and-conquer sorting | O(n log n) |
| Insertion sort | Comparison-based sorting | O(n²) worst case |
| Doctor lookup by specialization | Doctor list scan | O(d) |

Here, `n` is the number of patients and `d` is the number of doctors. Final documentation will distinguish best/average/worst cases where relevant and confirm the complexity against the implemented code.

## Safety and limitations

- This is an academic prototype, not a production hospital information system.
- Severity labels are for demonstration only and are not a validated clinical decision tool.
- The prototype will not store or process real patient data; use synthetic demo records only.
- No authentication, encryption, audit-grade logging, regulatory compliance, or production database is included.
- A priority score must not be treated as a substitute for a qualified clinician's assessment.

## References and credits

These sources were reviewed for architecture ideas, DSA examples, testing approaches, and triage context. PulseQ will not copy their core DSA implementations.

- [ianberwa/hospital-system](https://github.com/ianberwa/hospital-system) — Python hospital queue/triage example using a linked FIFO queue and binary heap. GitHub metadata reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [dhanushsr26/hospital-priority-queue-python](https://github.com/dhanushsr26/hospital-priority-queue-python) — patient priority queue and merge-sort example. GitHub metadata reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [SudharsanSaravanan/Hospital_Mangement_System](https://github.com/SudharsanSaravanan/Hospital_Mangement_System) — patient-priority project illustrating heap-based ordering and patient lookup concepts. GitHub metadata reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [Sidoine20/EmergencyHospitalSystem](https://github.com/Sidoine20/EmergencyHospitalSystem) — modular DSA hospital-management example. Its GitHub repository metadata declares the **MIT License**. We may consult its structure and tests; any adapted code would require MIT attribution and license preservation. No code has been copied.
- [World Health Organization: Interagency Integrated Triage Tool](https://www.who.int/tools/triage) — background on acuity-based prioritisation and red/yellow/green urgency categories. PulseQ will be an educational severity simulation, not an implementation or validation of a clinical protocol.

## Progress log

| Step | Status | Work |
|---|---|---|
| 1. Repository and reference audit | Complete | Confirmed the repository was empty, reviewed relevant reference projects, and checked declared license metadata. |
| 2. Project scaffold and README | Complete | Added a package scaffold, project-area READMEs, Python-focused `.gitignore`, module responsibilities, target run/test commands, safety limitations, complexity targets, and this progress log. |
| 3. Patient records with linked list | Pending | Implement patient CRUD and duplicate-ID protection. |
| 4. Routine appointment queue | Pending | Implement custom FIFO queue. |
| 5. Emergency priority queue | Pending | Implement custom binary heap and stable urgency ties; run checkpoint tests. |
| 6. Doctors and allocation | Pending | Add doctor records and specialization-aware allocation. |
| 7. Searching | Pending | Implement linear and binary search. |
| 8. Sorting | Pending | Implement merge sort and insertion sort. |
| 9. CLI integration | Pending | Integrate modules and add startup disclaimer and input validation. |
| 10. Testing and final documentation | Pending | Run full edge-case audit, fix defects, and finish documentation. |

**Next:** Step 3 — implement patient records using a custom linked list. Do not begin until the Step 2 review is complete.
