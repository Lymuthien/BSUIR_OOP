from dataclasses import dataclass


@dataclass
class StudentDTO:
    name: str
    grade: int
    id_: int | None = None
