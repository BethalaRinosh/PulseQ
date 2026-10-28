"""Unit tests for the custom linked FIFO routine queue."""

import unittest

from pulseq.models import Patient
from pulseq.queues import RoutineQueue


def patient(patient_id: str, name: str | None = None) -> Patient:
    return Patient(
        patient_id=patient_id,
        name=name or patient_id,
        age=24,
        sex="Unspecified",
        contact="demo@example.test",
        reason="Routine appointment",
    )


class RoutineQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = RoutineQueue()

    def test_new_queue_is_empty(self) -> None:
        self.assertTrue(self.queue.is_empty())
        self.assertFalse(self.queue)
        self.assertEqual(len(self.queue), 0)
        self.assertEqual(self.queue.view_all(), [])

    def test_enqueue_and_fifo_order(self) -> None:
        self.queue.enqueue(patient("P1"))
        self.queue.enqueue(patient("P2"))
        self.queue.enqueue(patient("P3"))
        self.assertEqual([p.patient_id for p in self.queue], ["P1", "P2", "P3"])
        self.assertEqual(len(self.queue), 3)

    def test_peek_does_not_remove_patient(self) -> None:
        self.queue.enqueue(patient("P1"))
        self.assertEqual(self.queue.peek().patient_id, "P1")
        self.assertEqual(len(self.queue), 1)

    def test_dequeue_empty_raises_clear_error(self) -> None:
        with self.assertRaisesRegex(IndexError, "empty routine queue"):
            self.queue.dequeue()

    def test_peek_empty_raises_clear_error(self) -> None:
        with self.assertRaisesRegex(IndexError, "empty routine queue"):
            self.queue.peek()

    def test_dequeue_returns_fifo_and_resets_tail(self) -> None:
        self.queue.enqueue(patient("P1"))
        self.queue.enqueue(patient("P2"))
        self.assertEqual(self.queue.dequeue().patient_id, "P1")
        self.assertEqual(self.queue.dequeue().patient_id, "P2")
        self.assertTrue(self.queue.is_empty())

        # Enqueue after becoming empty must correctly reset both endpoints.
        self.queue.enqueue(patient("P3"))
        self.assertEqual(self.queue.peek().patient_id, "P3")
        self.assertEqual(self.queue.dequeue().patient_id, "P3")
        self.assertTrue(self.queue.is_empty())

    def test_rejects_non_patient_items(self) -> None:
        with self.assertRaises(TypeError):
            self.queue.enqueue("not a patient")  # type: ignore[arg-type]
        self.assertTrue(self.queue.is_empty())

    def test_clear_resets_queue(self) -> None:
        self.queue.enqueue(patient("P1"))
        self.queue.enqueue(patient("P2"))
        self.queue.clear()
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)
        self.assertEqual(self.queue.view_all(), [])


if __name__ == "__main__":
    unittest.main()
