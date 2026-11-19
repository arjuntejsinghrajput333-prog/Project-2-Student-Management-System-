
def validate_name(name):
    return bool(name.strip())


def validate_email(email):
    return email.endswith("@gmail.com") and email != "@gmail.com"


def validate_marks(marks):
    return isinstance(marks, int) and 0 <= marks <= 100
