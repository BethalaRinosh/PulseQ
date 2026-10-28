"""Record models used by PulseQ.

Patient data is synthetic/demo-only. This academic prototype is not a clinical
record system and must not be used to make real patient-care decisions.
"""

from dataclasses import dataclass


@dataclass
class Patient:
    """A single patient record for demonstration purposes."""

    patient_id: str
    name: str
    age: int
    sex: str
    contact: str
    reason: str

    def __setattr__(self, name: str, value: object) -> None:
        if name == "patient_id" and "patient_id" in self.__dict__:
            raise AttributeError("Patient ID is immutable after construction.")
        if name in {"name", "sex", "contact", "reason"}:
            labels = {
                "name": "Name",
                "sex": "Sex",
                "contact": "Contact",
                "reason": "Reason for visit",
            }
            value = self._required_text(value, labels[name])
        if name == "age":
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError("Age must be an integer.")
            if not 0 <= value <= 130:
                raise ValueError("Age must be between 0 and 130.")
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "patient_id", self._required_text(self.patient_id, "Patient ID").upper()
        )
        self.name = self._required_text(self.name, "Name")
        self.sex = self._required_text(self.sex, "Sex")
        self.contact = self._required_text(self.contact, "Contact")
        self.reason = self._required_text(self.reason, "Reason for visit")

        if isinstance(self.age, bool) or not isinstance(self.age, int):
            raise ValueError("Age must be an integer.")
        if not 0 <= self.age <= 130:
            raise ValueError("Age must be between 0 and 130.")

    @staticmethod
    def _required_text(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return value.strip()

    def update(self, **changes: object) -> None:
        """Update supported fields after validating the complete new record."""
        allowed = {"name", "age", "sex", "contact", "reason"}
        unknown = set(changes) - allowed
        if unknown:
            raise ValueError(f"Unsupported patient field(s): {', '.join(sorted(unknown))}")

        candidate = {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "sex": self.sex,
            "contact": self.contact,
            "reason": self.reason,
        }
        candidate.update(changes)
        validated = Patient(**candidate)
        self.name = validated.name
        self.age = validated.age
        self.sex = validated.sex
        self.contact = validated.contact
        self.reason = validated.reason
