
from app.models.student import Student
from app.repositories.student_repository import StudentRepository
from app.utils.validation import (
    validate_name,
    validate_email,
    validate_marks
)


class StudentService:
    def __init__(self):
        self.repository = StudentRepository()

    def add_student(self, student_id, name, email, course, marks):
        if not validate_name(name):
            raise ValueError("Name cannot be empty.")

        if not validate_email(email):
            raise ValueError("Enter a valid Gmail address.")

        if not course.strip():
            raise ValueError("Course cannot be empty.")

        if not validate_marks(marks):
            raise ValueError("Marks must be between 0 and 100.")

        student = Student(
            student_id,
            name.strip().title(),
            email.strip().lower(),
            course.strip().title(),
            marks
        )

        self.repository.add(student)
        return student

    def get_all_students(self):
        return self.repository.get_all()
