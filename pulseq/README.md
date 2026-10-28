# PulseQ package

This package will contain the application's modules. Planned responsibilities:

- `models.py`: patient and doctor record definitions.
- `patient_store.py`: custom linked list for patient records.
- `queues.py`: custom FIFO routine queue and binary-heap emergency queue.
- `doctors.py`: doctor directory and specialization-aware allocation.
- `searching.py`: manual linear and binary search.
- `sorting.py`: manual merge sort and insertion sort.
- `cli.py`: menu-driven interface and input validation.

These modules are planned only; they will be added in their designated milestones. No DSA implementation is included in this scaffold.


## Implemented in Step 4: routine queue

`queues.py` provides `RoutineQueue`, a custom linked FIFO queue for `Patient` records. It implements `enqueue`, `dequeue`, `peek`, `is_empty`, iteration, `view_all`, and `clear`. Enqueue/dequeue/peek/empty checks are O(1); listing the queue is O(n). Empty dequeue and peek operations raise `IndexError` with clear messages. It does not use `collections.deque`. The emergency heap remains a later step.
