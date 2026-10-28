"""Unit tests for the custom emergency binary-heap priority queue."""

import unittest

from pulseq.emergency_queue import EmergencyPriorityQueue
from pulseq.models import Patient


def patient(patient_id: str, name: str | None = None) -> Patient:
    return Patient(
        patient_id=patient_id,
        name=name or patient_id,
        age=30,
        sex="Unspecified",
        contact="demo@example.test",
        reason="Emergency demonstration",
    )


class EmergencyPriorityQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = EmergencyPriorityQueue()

    def test_new_queue_is_empty(self) -> None:
        self.assertTrue(self.queue.is_empty())
        self.assertFalse(self.queue)
        self.assertEqual(len(self.queue), 0)
        self.assertEqual(self.queue.view_all(), [])

    def test_dequeues_highest_urgency_first(self) -> None:
        self.queue.enqueue(patient("P1"), 2)
        self.queue.enqueue(patient("P2"), 5)
        self.queue.enqueue(patient("P3"), 3)
        self.assertEqual(
            [(case.patient.patient_id, case.urgency) for case in self.queue.view_all()],
            [("P2", 5), ("P3", 3), ("P1", 2)],
        )

    def test_equal_urgency_preserves_arrival_order(self) -> None:
        self.queue.enqueue(patient("P1"), 4)
        self.queue.enqueue(patient("P2"), 4)
        self.queue.enqueue(patient("P3"), 4)
        self.assertEqual(
            [self.queue.dequeue().patient.patient_id for _ in range(3)],
            ["P1", "P2", "P3"],
        )

    def test_equal_priority_cases_keep_fifo_order_around_higher_priority(self) -> None:
        self.queue.enqueue(patient("P1"), 3)
        self.queue.enqueue(patient("P2"), 5)
        self.queue.enqueue(patient("P3"), 3)
        self.assertEqual(
            [case.patient.patient_id for case in self.queue.view_all()],
            ["P2", "P1", "P3"],
        )

    def test_peek_does_not_remove_case(self) -> None:
        self.queue.enqueue(patient("P1"), 2)
        self.queue.enqueue(patient("P2"), 5)
        self.assertEqual(self.queue.peek().patient.patient_id, "P2")
        self.assertEqual(len(self.queue), 2)

    def test_empty_peek_and_dequeue_raise_clear_errors(self) -> None:
        with self.assertRaisesRegex(IndexError, "empty emergency priority queue"):
            self.queue.peek()
        with self.assertRaisesRegex(IndexError, "empty emergency priority queue"):
            self.queue.dequeue()

    def test_dequeue_restores_heap_after_root_removal(self) -> None:
        for patient_id, urgency in [
            ("P1", 2), ("P2", 5), ("P3", 1), ("P4", 4), ("P5", 3)
        ]:
            self.queue.enqueue(patient(patient_id), urgency)
        self.assertEqual(
            [self.queue.dequeue().patient.patient_id for _ in range(5)],
            ["P2", "P4", "P5", "P1", "P3"],
        )
        self.assertTrue(self.queue.is_empty())

    def test_rejects_non_patient(self) -> None:
        with self.assertRaises(TypeError):
            self.queue.enqueue("not a patient", 5)  # type: ignore[arg-type]
        self.assertTrue(self.queue.is_empty())

    def test_rejects_invalid_urgency_values(self) -> None:
        for urgency in (0, 6, -1, 1.5, "5", True, None):
            with self.subTest(urgency=urgency):
                with self.assertRaises(ValueError):
                    self.queue.enqueue(patient("P1"), urgency)  # type: ignore[arg-type]
                self.assertTrue(self.queue.is_empty())

    def test_clear_resets_queue_and_queue_can_be_reused(self) -> None:
        self.queue.enqueue(patient("P1"), 4)
        self.queue.enqueue(patient("P2"), 5)
        self.queue.clear()
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)
        self.queue.enqueue(patient("P3"), 3)
        self.assertEqual(self.queue.dequeue().patient.patient_id, "P3")

    def test_view_all_does_not_mutate_heap(self) -> None:
        self.queue.enqueue(patient("P1"), 2)
        self.queue.enqueue(patient("P2"), 5)
        first = self.queue.view_all()
        self.assertEqual([case.patient.patient_id for case in first], ["P2", "P1"])
        self.assertEqual(len(self.queue), 2)
        self.assertEqual(self.queue.peek().patient.patient_id, "P2")


if __name__ == "__main__":
    unittest.main()
