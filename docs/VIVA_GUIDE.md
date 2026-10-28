# PulseQ Viva Guide

This guide is written for explaining the current implementation in a DSA project viva. Use synthetic examples only.

## 1. Thirty-second project introduction

PulseQ is a Python command-line academic prototype for hospital workflow management. It demonstrates patient record CRUD, routine FIFO scheduling, emergency priority scheduling with a binary max-heap, specialization-aware doctor allocation, manual searching, and manual sorting. Its purpose is to demonstrate data structures and algorithms, not to make clinical decisions. Data exists only in memory and disappears when the program exits.

## 2. Architecture and data flow

- `main.py` starts `PulseQApp` from `pulseq/cli.py`.
- `PulseQApp` owns four independent structures: `PatientLinkedList`, `RoutineQueue`, `EmergencyPriorityQueue`, and `DoctorDirectory`.
- `Patient` is the validated record model shared by the patient store and queues.
- The CLI validates user input and calls the data-structure methods. It does not replace the custom implementations with built-in sorting, search, or queue libraries.
- Cross-queue checks prevent the same patient from waiting in both the routine and emergency queues.
- Patient deletion is blocked while the patient is waiting in either queue or has an active doctor assignment.

## 3. Data structures and algorithms

### Custom singly linked list

Each node stores a patient reference and a pointer to the next node. The list maintains head, tail, and size.

- Register: first scans for a duplicate ID, then appends at the tail. Overall O(n), append itself O(1).
- Find/update/delete: O(n) because the list must be traversed.
- View all: O(n) to create an insertion-ordered snapshot.
- Why use it: the project brief requires implementing patient storage with a linked list rather than delegating storage to a built-in list.

### Routine FIFO queue

The custom linked queue maintains head and tail pointers.

- Enqueue at tail: O(1).
- Dequeue from head: O(1).
- Peek and empty check: O(1).
- Queue display: O(n).
- FIFO means first in, first out. The first patient added is the first patient removed.

### Emergency binary max-heap

The heap is a Python list used as an array representation of a complete binary tree. For zero-based index i, the parent is `(i - 1) // 2`, the left child is `2 * i + 1`, and the right child is `2 * i + 2`.

- Enqueue inserts at the end and sifts upward: O(log n).
- Dequeue removes the root, moves the last item to the root, and sifts downward: O(log n).
- Peek reads the root: O(1).
- Higher demo urgency scores are served first. Equal scores use arrival sequence to preserve FIFO order.
- The score 1 to 5 is an educational ordering value, not a validated clinical triage scale.

### Doctor directory and allocation

Doctors are held in a Python list, and active assignments are tracked by a dictionary keyed by patient ID.

- A requested specialization is matched case-insensitively.
- Unavailable doctors are excluded from new allocations.
- Among matching available doctors, the least-loaded doctor is chosen. Registration order breaks ties.
- Registration and doctor lookup are O(d); allocation scans doctors in O(d), where d is the number of doctors.
- Releasing an assignment removes it and decrements the doctor's active load.

### Searching

- Linear ID search: O(n), works on records in any order.
- Partial name search: O(n), case-insensitive, returns every match in input order.
- Binary ID search: O(log n), but its input must already be sorted by normalized patient ID in ascending order.
- The CLI sorts a copy with the custom merge sort before calling binary search. The binary-search function itself does not sort or scan the whole collection.

### Sorting

- Merge sort: O(n log n) time and O(n) auxiliary space.
- Insertion sort: O(n) best case for already sorted input, O(n²) average/worst case.
- Both implementations are stable and return a new list, so sorting a display does not mutate the underlying patient records or live emergency heap.

## 4. How to demonstrate the application

From the repository root:

```bash
python main.py
```

Suggested short demo sequence:

1. Register two patients using synthetic data.
2. View all patients and show the uppercase-normalized IDs.
3. Search by partial name, then use binary search by ID.
4. Add one patient to the routine queue and serve the next routine patient to demonstrate FIFO.
5. Add two different patients to the emergency queue with urgency 2 and urgency 5. View or serve the queue to show that urgency 5 comes first.
6. Try adding a patient who is already waiting in the other queue. Explain that the CLI blocks conflicting queue membership.
7. Register two doctors with the same specialization and allocate multiple patients. Show least-load allocation and the active assignment count.
8. Sort patients by age using insertion sort, then by ID using merge sort. Explain that the output is a sorted display copy.
9. Exit and explain that the prototype does not persist records.

Avoid using real names, phone numbers, medical details, or any real patient information in the demo.

## 5. Run the tests

Run all unit and integration tests:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs this command on Python 3.10, 3.12, and 3.13. The test suite includes model validation, linked-list edge cases, FIFO order, heap priority and stable ties, doctor assignment/load rules, search/sort behavior, and CLI interaction tests.

## 6. Common viva questions

**Why is patient registration O(n) if append is O(1)?**  
The tail insertion itself is O(1), but the implementation first scans the list to reject duplicate patient IDs, making the complete registration operation O(n).

**Why use a linked list for patients?**  
It demonstrates node-based storage and pointer relinking. Finding a patient is still O(n); a linked list does not provide constant-time lookup by ID.

**What is the difference between the routine queue and emergency queue?**  
The routine queue uses FIFO order. The emergency queue uses a max-heap so the highest demo urgency is served first, with arrival order as the tie-breaker.

**Why is heap insertion O(log n)?**  
After appending, the new element may move upward through at most the height of the complete binary tree, which is O(log n).

**Why does binary search need sorted data?**  
It discards half the remaining search range at each comparison. That decision is valid only when IDs are ordered. The CLI creates a sorted copy first.

**Why implement both merge sort and insertion sort?**  
They show different trade-offs. Merge sort has O(n log n) time across cases but needs extra space. Insertion sort is simple, stable, and efficient for small or nearly sorted inputs, but has O(n²) worst-case time.

**What does stable sorting mean?**  
If two records have equal sort keys, they remain in their original relative order.

**Why does doctor allocation use the least-loaded doctor?**  
It is a simple scheduling policy to distribute active demo assignments among available doctors. It is not clinical matching or a real staffing policy.

**Does this qualify as a real hospital information system?**  
No. It is a command-line educational prototype. It has no persistent database, authentication, encryption, clinical validation, production audit trail, or regulatory controls. Its urgency score is not medical advice.

## 7. Limitations to state honestly

- Records are stored only in memory and are lost on exit.
- The CLI is single-user and has no authentication or role-based access.
- The urgency score is a simplified demo value, not validated triage.
- There is no database, network API, audit-grade history, or production deployment.
- This implementation is intended to demonstrate DSA concepts and must not be used for real patient-care decisions.
