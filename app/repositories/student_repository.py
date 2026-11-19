
import json
import os


class StudentRepository:
    def __init__(self, file_path="data/students.json"):
        self.file_path = file_path

    def get_all(self):
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r") as file:
            return json.load(file)

    def save_all(self, students):
        os.makedirs(
            os.path.dirname(self.file_path) or ".",
            exist_ok=True
        )

        with open(self.file_path, "w") as file:
            json.dump(students, file, indent=4)

    def add(self, student):
        students = self.get_all()
        students.append(student.to_dict())
        self.save_all(students)
