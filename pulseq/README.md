# PulseQ package

This package contains the application's implemented modules and will grow as later milestones are completed. Planned responsibilities:

- `models.py`: patient and doctor record definitions.
- `patient_store.py`: custom linked list for patient records.
- `queues.py`: custom FIFO routine queue and binary-heap emergency queue.
- `doctors.py`: doctor directory, availability, and specialization-aware allocation.
- `searching.py`: manual linear search by ID/name and binary search by ID.
- `sorting.py`: manual merge sort and insertion sort.
- `cli.py`: menu-driven interface and input validation.

These modules are added in their designated milestones as the project progresses. The core data structures are implemented directly for learning and viva explanation. Patient IDs are normalised to uppercase and immutable after construction.

## Implemented in Step 4: routine queue

`queues.py` provides `RoutineQueue`, a custom linked FIFO queue for `Patient` records. It implements `enqueue`, `dequeue`, `peek`, `is_empty`, iteration, `view_all`, and `clear`. Enqueue/dequeue/peek/empty checks are O(1); listing the queue is O(n); clear is O(n) to release linked nodes. Empty dequeue and peek operations raise `IndexError` with clear messages. It does not use `collections.deque`.

## Implemented in Step 5: emergency priority queue

`emergency_queue.py` provides `EmergencyPriorityQueue`, a custom binary max-heap. Each `EmergencyCase` stores a patient, an educational urgency score from 1 to 5, and an arrival sequence number. Higher urgency is served first; equal urgency preserves FIFO order. Duplicate patient IDs are rejected while queued and can be queued again after removal. `enqueue` and `dequeue` are O(log n) plus average O(1) ID-set bookkeeping, `peek` and empty checks are O(1), `view_all` is O(n log n), and `clear` is O(n) to release list-held references and clear the ID set. Invalid patient types and invalid urgency scores are rejected. The score is not a clinical triage scale.


## Implemented in Step 6: doctors and allocation

`doctors.py` provides a validated `Doctor` model and a list-backed `DoctorDirectory`. Doctor IDs are normalized and immutable. The directory rejects duplicate IDs, supports lookup and availability changes, and allocates a patient to an available doctor matching the requested specialization. It chooses the least-loaded matching doctor and preserves registration order for load ties. A patient may have one active assignment; `release_patient()` updates the assignment and load so the patient can be reassigned. Registration, lookup and allocation are O(d), where d is the number of doctors. This is administrative demo logic, not clinical decision support.


## Implemented in Step 7: searching

`searching.py` implements three manual algorithms without `bisect`: `linear_search_by_id()` works on records in any order and returns one record or `None`; `linear_search_by_name()` performs case-insensitive partial matching and returns every match in input order, so duplicate names are handled; `binary_search_by_id()` returns a record or `None` using an iterative binary search. Binary search requires the caller to provide records sorted by normalized patient ID in ascending order. It intentionally does not sort or validate the whole sequence, keeping search time O(log n). Linear ID/name search is O(n).
