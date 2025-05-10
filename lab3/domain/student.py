from .entity import Entity


class IStudent(Entity):
    pass


class Student(IStudent):
    def __init__(self, id_, name: str, grade: int):
        self.validate_name(name)
        self.validate_grade(grade)
        self.name = name
        self.grade = grade
        super().__init__(id_)

    @staticmethod
    def validate_name(name: str):
        if not isinstance(name, str):
            raise ValueError("Student name must be a string")
        if not name:
            raise ValueError("Student name cannot be empty")

    @staticmethod
    def validate_grade(grade: int):
        if not isinstance(grade, int):
            raise ValueError("Student grade must be a integer")
        if grade < 0 or grade > 10:
            raise ValueError("Student grade must be between 0 and 10")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "grade": self.grade}

    @staticmethod
    def from_dict(data):
        return Student(data["id"], data["name"], data["grade"])
