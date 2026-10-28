# PulseQ

**Advanced Hospital Management and Emergency Response System**  
Academic DSA micro-project built with Python 3 and the standard library.

> **Academic prototype disclaimer:** PulseQ is an educational simulation for demonstrating data structures and algorithms. It does not replace professional medical judgment, validated clinical triage protocols, or a real hospital information system. It must not be used to make real patient-care decisions.

## Project status

**Current milestone:** Step 10 of 10: final audit and verification.  
All core DSA modules are connected to a text menu with input validation, a startup disclaimer, cross-queue consistency checks, and an in-memory application entry point.

## Features

- Patient registration and record management (create, view, update, delete).
- Duplicate patient ID protection (case-insensitive IDs).
- Patient IDs are trimmed and normalised to uppercase.
- Patient age validation (integer from 0 through 130).
- Routine patients flow through a custom linked FIFO queue with enqueue, dequeue, peek, iteration, and clear operations.
- Emergency cases use a custom binary max-heap: urgency scores range from 1 to 5, higher scores are served first, equal scores preserve arrival order, and duplicate patient IDs are rejected while queued.
- Doctor records include specialization and availability. Allocation selects an available matching specialist with the smallest active assignment count; ties preserve doctor registration order. A patient can have only one active doctor assignment.
- Manual linear search finds IDs in any order and returns all case-insensitive partial name matches, including duplicate names.
- Manual binary search finds a patient ID in a collection already sorted by normalized patient ID. It does not sort the records or use Python's `bisect` module.
- Manual merge sort and insertion sort return sorted copies of sequences, support a custom key and reverse ordering, preserve the input, and remain stable for equal keys.
- Menu-driven CLI supports patient CRUD, linear/name/binary search, routine FIFO queue operations, emergency priority queue operations, doctor registration/allocation, availability changes, and sorting patient records by ID/name/age or emergency cases by urgency/arrival order. A patient cannot be waiting in both routine and emergency queues at the same time.

## Project structure

    PulseQ/
    ├── README.md
    ├── .gitignore
    ├── .github/
    │   └── workflows/
    │       └── tests.yml
    ├── main.py
    ├── pulseq/
    │   ├── __init__.py
    │   ├── README.md
    │   ├── models.py
    │   ├── patient_store.py
    │   ├── queues.py
    │   ├── emergency_queue.py
    │   ├── doctors.py
    │   ├── searching.py
    │   ├── sorting.py
    │   └── cli.py
    ├── tests/
    │   ├── README.md
    │   ├── test_patient_store.py
    │   ├── test_routine_queue.py
    │   ├── test_emergency_queue.py
    │   ├── test_doctors.py
    │   ├── test_searching.py
    │   ├── test_sorting.py
    │   └── test_pulseq.py
    ├── docs/
    │   ├── README.md
    │   └── VIVA_GUIDE.md
    └── examples/
        └── README.md

### Module responsibilities

| Module | Responsibility |
|---|---|
| pulseq/models.py | Validated Patient record model and safe field updates |
| pulseq/patient_store.py | Custom singly linked list; patient register, find, view, update, delete, and clear |
| pulseq/queues.py | Custom linked FIFO queue for routine patients |
| pulseq/emergency_queue.py | Custom binary max-heap with stable FIFO ties for equal urgency |
| pulseq/doctors.py | Doctor records, availability, specialization matching and load-aware allocation |
| pulseq/searching.py | Manual linear ID/name search and binary search by ID on a sorted sequence |
| pulseq/sorting.py | Manual stable merge sort and insertion sort with optional key/reverse options |
| pulseq/cli.py | Menu-driven CLI, startup disclaimer, input validation, and module integration |
| main.py | Application entry point (`python main.py`) |
| docs/VIVA_GUIDE.md | Viva explanations, DSA concepts, complexity, demo flow, and common questions |
| tests/test_patient_store.py | Unit tests for patient model and linked-list CRUD |
| tests/test_routine_queue.py | Unit tests for FIFO ordering and queue edge cases |
| tests/test_emergency_queue.py | Unit tests for heap ordering, stable ties, validation, and edge cases |
| tests/test_doctors.py | Unit tests for doctor records, matching, availability, assignment and release |
| tests/test_searching.py | Unit tests for linear and binary search, empty/missing records, duplicate names, case-insensitive matching and invalid inputs |
| tests/test_sorting.py | Unit tests for both sorting algorithms, ordering, stability, keys, reverse order and input preservation |
| tests/test_pulseq.py | CLI integration tests for startup, input validation, patient registration, queues, doctors, searching, sorting and exit |

The linked list is implemented directly using nodes with patient and next fields. The patient-record container does not delegate storage to a built-in list. The view_all method returns a list snapshot for display; it is not the backing store. The routine queue likewise uses linked nodes and head/tail pointers rather than a built-in queue. The emergency priority queue implements heap insertion and removal manually; it does not use a built-in priority queue.

## Viva and demonstration guide

Use [`docs/VIVA_GUIDE.md`](docs/VIVA_GUIDE.md) for a project introduction, architecture and DSA explanations, a suggested demo sequence, Big-O reasoning, test commands, and common viva questions.

## Continuous integration

GitHub Actions runs the full unittest suite on Python 3.10, 3.12, and 3.13 for pushes to `main`, pull requests, and manual dispatch. The workflow is defined in `.github/workflows/tests.yml`.

## Requirements and current run status

- Python 3.10 or newer is the target.
- No third-party packages are required or planned.
- The CLI runs with Python 3.10 or newer using only the standard library.
- All patient and doctor records are held in memory and disappear when the program exits.

Run the routine-queue unit tests from the repository root:

    python -m unittest discover -s tests -p "test_routine_queue.py" -v

Run the patient-record tests with:

    python -m unittest discover -s tests -p "test_patient_store.py" -v

Run the emergency-queue unit tests with:

    python -m unittest discover -s tests -p "test_emergency_queue.py" -v

Run the doctor-directory unit tests with:

    python -m unittest discover -s tests -p "test_doctors.py" -v

Run the search-algorithm unit tests with:

    python -m unittest discover -s tests -p "test_searching.py" -v

Run the sorting-algorithm unit tests with:

    python -m unittest discover -s tests -p "test_sorting.py" -v

Run the CLI integration tests with:

    python -m unittest discover -s tests -p "test_pulseq.py" -v

Launch the application from the repository root:

    python main.py

Run all unit and integration tests with:

    python -m unittest discover -s tests -v

**Verification note:** The committed unit and integration test suite is now run by GitHub Actions on Python 3.10, 3.12, and 3.13. See the latest workflow run for the authoritative result. Earlier isolated harness results are historical and are not substitutes for the committed suite.

## Patient linked-list behaviour

- register(patient): append at the tail after checking for a duplicate ID.
- find(patient_id): search by case-insensitive ID.
- view_all(): return records in insertion order.
- update(patient_id, **changes): update name, age, sex, contact, or reason for visit after validating a candidate record.
- delete(patient_id): remove and return a record, correctly handling head, middle, tail, and final-node removal.
- clear(): reset the list.
- Empty/missing lookups return None for find; update/delete raise KeyError for missing IDs; duplicate registration raises ValueError.

The record model rejects empty text fields and ages outside 0–130. Patient IDs are normalised to uppercase and cannot be reassigned after construction.

## Routine FIFO queue behaviour

The routine queue uses custom linked nodes with head and tail references. It preserves first-come-first-served order and does not use `collections.deque`.

- `enqueue(patient)`: add to the tail in O(1).
- `dequeue()`: remove and return the head in O(1); raises `IndexError` when empty.
- `peek()`: return the head without removing it in O(1); raises `IndexError` when empty.
- `is_empty()` and `len(queue)`: O(1).
- `view_all()`: return a FIFO-ordered snapshot in O(n).
- `clear()`: reset head, tail and size while releasing linked nodes in O(n).

The queue accepts `Patient` objects only. After the final patient is dequeued, both endpoints are reset so later enqueues remain valid. Patient IDs cannot be reassigned after a `Patient` is constructed.

## Emergency priority queue behaviour

EmergencyPriorityQueue is a custom binary max-heap backed by a Python list. It stores EmergencyCase entries containing a patient, an urgency score, and an arrival sequence number. Urgency is a demonstration-only integer from 1 (lower) to 5 (higher), not a clinical triage scale.

- enqueue(patient, urgency): validate and insert, then sift upward in O(log n).
- peek(): return the highest-priority EmergencyCase without removal in O(1); raises IndexError when empty.
- dequeue(): remove the root, move the final entry to the root, then sift downward in O(log n); raises IndexError when empty.
- Equal urgency: earlier arrival is served first.
- view_all(): return a priority-ordered snapshot without changing the live heap in O(n log n).
- clear(): clear stored entries in O(n) because list-held references must be released.
- is_empty() and len(queue): O(1).

Invalid patient types raise TypeError; urgency values must be integers 1 through 5, with booleans rejected explicitly. Duplicate patient IDs are rejected while queued, then become eligible again after dequeue.

## Doctor directory and allocation behaviour

`DoctorDirectory` stores doctor records in a Python list, which is permitted for the doctor directory. Doctor IDs are trimmed, uppercased and immutable after construction. Duplicate IDs are rejected. Specialization matching is case-insensitive, and unavailable doctors are excluded from new assignments.

For a requested specialization, allocation chooses the available matching doctor with the smallest number of active assignments. If loads tie, registration order breaks the tie. Each patient may have only one active assignment. `release_patient()` clears that assignment and reduces the doctor's load, allowing the patient to be reassigned later. Making a doctor unavailable does not cancel existing assignments. These are scheduling demonstrations, not clinical decisions.

## Big-O complexity

Let n be the number of patient records.

| Operation | Implementation | Time complexity |
|---|---|---|
| Register patient | Duplicate scan plus tail append | O(n) overall; append itself is O(1) |
| Find patient by ID | Linked-list traversal | O(n) |
| View all records | Traverse and create a snapshot | O(n) |
| Update patient | Find plus fixed-field validation | O(n) |
| Delete patient by ID | Find node and relink pointers | O(n) |
| Clear all records | Release linked nodes and reset head/tail/size | O(n) |
| Routine enqueue | Linked queue tail pointer | O(1) |
| Routine dequeue | Linked queue head pointer | O(1) |
| Routine peek / empty check | Head reference / size state | O(1) |
| Routine queue snapshot | Traverse linked nodes | O(n) |
| Linked-list storage | One node per patient | O(n) space |
| Linear search by ID or name | Scan patient sequence | O(n) |
| Binary search by ID | Manual search on records sorted by patient ID | O(log n) |
| Emergency enqueue/dequeue | Custom binary max-heap with sift-up/sift-down | O(log n) |
| Peek most urgent emergency | Heap root | O(1) |
| Emergency priority snapshot | Copy heap and remove entries in priority order | O(n log n) |
| Emergency heap storage | One entry per waiting case | O(n) space |
| Merge sort | Manual stable divide-and-conquer sort | O(n log n) |
| Insertion sort | Manual stable comparison-based sort | O(n) best; O(n²) average/worst |
| Doctor registration / lookup | Duplicate scan or doctor-list traversal | O(d) |
| Doctor allocation | Scan doctors and select least-loaded matching specialist | O(d) |
| Find a patient's assigned doctor | Assignment dictionary lookup plus doctor lookup | O(d) |
| Release a patient assignment | Doctor lookup and assignment update | O(d) |

Here, d is the number of doctors. Patient registration is O(n) overall because duplicate IDs must be rejected; the physical tail append after validation is O(1). Doctor allocation and lookup are O(d). These complexity claims describe the current implementation or explicitly labelled future design.

## Safety and limitations

- This is an academic prototype, not a production hospital information system.
- Emergency urgency scores are for demonstration only and are not a validated clinical decision tool.
- Use synthetic demo records only. Do not enter real patient information.
- The current linked-list records exist in memory only and are not persisted to disk.
- No authentication, encryption, audit-grade logging, regulatory compliance, or production database is included.
- A priority score must not be treated as a substitute for a qualified clinician's assessment.

## References and credits

These sources were reviewed for architecture ideas, DSA examples, testing approaches, and triage context. PulseQ's required core DSA implementations are written directly for learning and viva explanation. No source code has been copied.

- [ianberwa/hospital-system](https://github.com/ianberwa/hospital-system): Python hospital queue/triage example using a linked FIFO queue and binary heap. GitHub metadata reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [dhanushsr26/hospital-priority-queue-python](https://github.com/dhanushsr26/hospital-priority-queue-python): patient priority queue and merge-sort example. GitHub metadata reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [SudharsanSaravanan/Hospital_Mangement_System](https://github.com/SudharsanSaravanan/Hospital_Mangement_System): patient-priority project illustrating heap-based ordering and patient lookup concepts. GitHub metadata reports **no declared license**. Reference only; do not copy code unless permission/license is established.
- [Sidoine20/EmergencyHospitalSystem](https://github.com/Sidoine20/EmergencyHospitalSystem): modular DSA hospital-management example. Its GitHub repository metadata declares the **MIT License**. Any adapted code would require MIT attribution and license preservation; no code has been copied.
- [World Health Organization: Interagency Integrated Triage Tool](https://www.who.int/tools/triage): background on acuity-based prioritisation and red/yellow/green urgency categories. PulseQ will be an educational severity simulation, not an implementation or validation of a clinical protocol.
- [kompalwargangotri/hospital-management-system-dsa](https://github.com/kompalwargangotri/hospital-management-system-dsa): reviewed for doctor-directory, specialization, availability, and duplicate-ID design ideas. License metadata was not verified; no code has been copied.

## Progress log

| Step | Status | Work |
|---|---|---|
| 1. Repository and reference audit | Complete | Confirmed the repository was empty, reviewed relevant reference projects, and checked declared license metadata. |
| 2. Project scaffold and README | Complete | Added package scaffold, project-area READMEs, .gitignore, module responsibilities, target run/test commands, safety limitations, complexity targets, and progress log. |
| 3. Patient records with linked list | Complete; CI verified | Added validated patient model, custom singly linked list CRUD, duplicate-ID checks, and unit tests. The committed suite is now verified by the cross-version CI workflow. |
| 4. Routine appointment queue | Complete; CI verified | Added custom linked FIFO queue and tests for FIFO order, empty operations, peek, type checks, clear, and reuse after becoming empty. Cleanup complexity was corrected to O(n). The committed suite is verified by CI. |
| 5. Emergency priority queue | Complete; CI verified | Added custom binary max-heap, stable FIFO tie-breaking, duplicate-ID protection, urgency validation, and unit tests. Audit found and fixed a mutable-patient-ID consistency risk by making patient IDs immutable after construction. The committed suite is verified by CI. |
| 6. Doctors and allocation | Complete | Added validated doctor records, duplicate-ID protection, availability toggles, case-insensitive specialization matching, least-loaded allocation with stable registration-order ties, single active assignment per patient, release/reassignment, and unit tests. Alignment checkpoint reviewed before Step 7. |
| 7. Searching | Complete; user reports all tests passed | Added manual linear search by ID, case-insensitive partial-name search returning all matches, and manual binary search by ID for pre-sorted records. Added edge-case tests. |
| 8. Sorting | Complete; user reports all tests passed | Added stable merge sort and insertion sort with optional key and reverse options. Both return a new list and leave input unchanged. Added tests for ordering, empty/singleton input, stability, key-based patient sorting, reverse order, and invalid inputs. |
| 9. CLI integration | Complete; CI verified | Added `main.py` and a menu-driven CLI integrating patient CRUD, searching, sorting, routine/emergency queues, doctor records/allocation, and availability. Added startup disclaimer, input validation, friendly empty/missing handling, deletion guards, and CLI integration tests. |
| 10. Final audit and verification | Complete | Completed the cross-module edge-case audit, fixed conflicting queue membership and invalid direct model mutations, added regression tests and cross-version GitHub Actions CI, and refreshed documentation. |

**Step 10 audit notes:** The cross-module audit found two integrity gaps: the CLI could place one patient in both waiting queues, and validated patient/doctor text fields could later be overwritten directly with invalid values. The CLI now rejects cross-queue duplicates, and direct model assignments validate before changing stored values. Regression tests cover these cases. The CI workflow runs the complete suite across supported Python versions. The application remains an educational in-memory simulation, not a production hospital system. Binary search requires records sorted by normalized patient ID.
