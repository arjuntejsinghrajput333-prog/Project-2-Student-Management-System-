
import unittest

from app.models.student import Student
from app.utils.validation import (
    validate_name,
    validate_email,
    validate_marks
)


class TestStudent(unittest.TestCase):

    def test_student_creation(self):
        student = Student(
            1, "Arjun", "arjun@gmail.com", "Data Science", 85
        )

        self.assertEqual(student.name, "Arjun")
        self.assertEqual(student.marks, 85)

    def test_valid_name(self):
        self.assertTrue(validate_name("Arjun"))

    def test_invalid_name(self):
        self.assertFalse(validate_name(" "))

    def test_valid_email(self):
        self.assertTrue(validate_email("arjun@gmail.com"))

    def test_valid_marks(self):
        self.assertTrue(validate_marks(85))

    def test_invalid_marks(self):
        self.assertFalse(validate_marks(150))


if __name__ == "__main__":
    unittest.main()
