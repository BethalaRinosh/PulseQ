# PulseQ package

This package contains the implemented modules that power the PulseQ command-line application. Module responsibilities:

- `models.py`: patient and doctor record definitions.
- `patient_store.py`: custom linked list for patient records.
- `queues.py`: custom FIFO routine queue and binary-heap emergency queue.
- `doctors.py`: doctor directory, availability, and specialization-aware allocation.
- `searching.py`: manual linear search by ID/name and binary search by ID.
- `sorting.py`: manual stable merge sort and insertion sort.
- `cli.py`: menu-driven interface and input validation.

The modules are implemented in staged milestones. `cli.py` integrates them into the interactive application. The core data structures are implemented directly for learning and viva explanation. Patient IDs are normalised to uppercase and immutable after construction. Patient and doctor text fields reject invalid direct assignments as well as invalid constructor/update input.

## Implemented in Step 4: routine queue

`queues.py` provides `RoutineQueue`, a custom linked FIFO queue for `Patient` records. It implements `enqueue`, `dequeue`, `peek`, `is_empty`, iteration, `view_all`, and `clear`. Enqueue/dequeue/peek/empty checks are O(1); listing the queue is O(n); clear is O(n) to release linked nodes. Empty dequeue and peek operations raise `IndexError` with clear messages. It does not use `collections.deque`.

## Implemented in Step 5: emergency priority queue

`emergency_queue.py` provides `EmergencyPriorityQueue`, a custom binary max-heap. Each `EmergencyCase` stores a patient, an educational urgency score from 1 to 5, and an arrival sequence number. Higher urgency is served first; equal urgency preserves FIFO order. Duplicate patient IDs are rejected while queued and can be queued again after removal. `enqueue` and `dequeue` are O(log n) plus average O(1) ID-set bookkeeping, `peek` and empty checks are O(1), `contains_patient()` checks membership in O(1) average time, `view_all` is O(n log n), and `clear` is O(n) to release list-held references and clear the ID set. Invalid patient types and invalid urgency scores are rejected. The score is not a clinical triage scale.


## Implemented in Step 6: doctors and allocation

`doctors.py` provides a validated `Doctor` model and a list-backed `DoctorDirectory`. Doctor IDs are normalized and immutable. The directory rejects duplicate IDs, supports lookup and availability changes, and allocates a patient to an available doctor matching the requested specialization. It chooses the least-loaded matching doctor and preserves registration order for load ties. A patient may have one active assignment; `release_patient()` updates the assignment and load so the patient can be reassigned. Registration, lookup and allocation are O(d), where d is the number of doctors. This is administrative demo logic, not clinical decision support.


## Implemented in Step 7: searching

`searching.py` implements three manual algorithms without `bisect`: `linear_search_by_id()` works on records in any order and returns one record or `None`; `linear_search_by_name()` performs case-insensitive partial matching and returns every match in input order, so duplicate names are handled; `binary_search_by_id()` returns a record or `None` using an iterative binary search. Binary search requires the caller to provide records sorted by normalized patient ID in ascending order. It intentionally does not sort or validate the whole sequence, keeping search time O(log n). Linear ID/name search is O(n).


## Implemented in Step 8: sorting

`sorting.py` provides `merge_sort(items, key=None, reverse=False)` and `insertion_sort(items, key=None, reverse=False)`. Both algorithms are implemented manually, return a new list, preserve the input sequence, and are stable when keys compare equal. A key function allows sorting patient records by ID, name, age, or another field. Merge sort is O(n log n) time with O(n) auxiliary space. Insertion sort is O(n) best-case time and O(n²) average/worst-case time; its returned copy uses O(n) space, while the shifting algorithm itself uses O(1) auxiliary space.


## Implemented in Step 9: command-line interface

`cli.py` defines `PulseQApp`, which owns the patient linked list, routine FIFO queue, emergency max-heap, and doctor directory. The menu connects patient registration/view/update/delete, linear and binary search, sorting patients by ID/name/age and emergency cases by urgency/arrival order, routine queue operations, emergency queue operations, doctor registration, specialization-aware allocation, assignment release, and availability toggles. It validates numeric menu choices and age/urgency ranges, retries empty text fields, handles missing records and empty queues with readable messages, and prevents deleting patients who are waiting in a queue or have an active doctor assignment, and prevents the same patient from waiting in both the routine and emergency queues. `main.py` starts the app with `python main.py`.

The startup disclaimer clearly identifies PulseQ as an academic simulation. All records remain in memory and are discarded on exit. The urgency score is a demonstration-only ordering field, not clinical triage. Use synthetic data only.


## Step 10: repository-wide audit and verification

The final audit added regression tests for invalid direct mutation of patient/doctor fields and for cross-queue membership conflicts. GitHub Actions runs the full test suite on Python 3.10, 3.12, and 3.13. All state is still in memory; the app is for synthetic academic demonstrations only.
