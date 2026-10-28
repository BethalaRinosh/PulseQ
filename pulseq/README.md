# PulseQ package

This package will contain the application's modules. Planned responsibilities:

- `models.py`: patient and doctor record definitions.
- `patient_store.py`: custom linked list for patient records.
- `queues.py`: custom FIFO routine queue and binary-heap emergency queue.
- `doctors.py`: doctor directory and specialization-aware allocation.
- `searching.py`: manual linear and binary search.
- `sorting.py`: manual merge sort and insertion sort.
- `cli.py`: menu-driven interface and input validation.

These modules are added in their designated milestones as the project progresses. The core data structures are implemented directly for learning and viva explanation.

## Implemented in Step 4: routine queue

`queues.py` provides `RoutineQueue`, a custom linked FIFO queue for `Patient` records. It implements `enqueue`, `dequeue`, `peek`, `is_empty`, iteration, `view_all`, and `clear`. Enqueue/dequeue/peek/empty checks are O(1); listing the queue is O(n). Empty dequeue and peek operations raise `IndexError` with clear messages. It does not use `collections.deque`.

## Implemented in Step 5: emergency priority queue

`emergency_queue.py` provides `EmergencyPriorityQueue`, a custom binary max-heap. Each `EmergencyCase` stores a patient, an educational urgency score from 1 to 5, and an arrival sequence number. Higher urgency is served first; equal urgency preserves FIFO order. `enqueue` and `dequeue` are O(log n), `peek` and empty checks are O(1), `view_all` is O(n log n), and `clear` is O(n) to release list-held references. Invalid patient types and invalid urgency scores are rejected. The score is not a clinical triage scale.
