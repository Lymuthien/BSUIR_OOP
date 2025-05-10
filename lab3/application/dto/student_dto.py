from dataclasses import dataclass


@dataclass
class StudentDTO:
    name: str
    grade: int
    id_: int = None

    def __post_init__(self):
        self.validate_grade()
        self.validate_name()

    def validate_grade(self):
        if self.grade < 0 or self.grade > 10:
            raise ValueError("Grade must be between 0 and 10")

    def validate_name(self):
        if not self.name:
            raise ValueError("Name cannot be empty")
