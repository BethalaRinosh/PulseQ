# Tests

Repeatable tests use Python's built-in `unittest`, so no third-party test dependency is required. Current unit-test modules cover patient records and linked-list operations, the routine FIFO queue, the emergency priority queue, and doctor registration/allocation. Searching tests now cover unsorted linear ID lookup, case-insensitive partial name matches, duplicate names, empty/missing results, binary-search boundaries, and invalid inputs. Sorting tests now cover ordering, stability, key functions, reverse order, input preservation, empty/singleton input, and invalid inputs. CLI integration tests now cover the startup disclaimer, exit/EOF, menu and age validation, patient registration, routine/emergency queues, doctor allocation, search/sort menu actions, and deletion safeguards.


Step 6 adds `test_doctors.py` for doctor validation, duplicate IDs, specialization matching, availability, load-aware allocation, duplicate patient assignments, release/reassignment, and clearing state.


Step 7 adds `test_searching.py` for manual linear and binary search. Binary-search fixtures are deliberately sorted by patient ID because sorted input is a required precondition.


Step 8 adds `test_sorting.py` for merge sort and insertion sort. Both functions are expected to return new sorted lists without mutating caller-owned sequences.


Step 9 adds `test_pulseq.py`, which exercises the interactive CLI with injected input and captured output. Run the complete suite from the repository root using `python -m unittest discover -s tests -v`.
