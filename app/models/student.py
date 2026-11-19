
class Student:
    def __init__(self, student_id, name, email, course, marks):
        self.id = student_id
        self.name = name
        self.email = email
        self.course = course
        self.marks = marks

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "course": self.course,
            "marks": self.marks
        }

