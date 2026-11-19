import json
import csv
from app.services.student_service import StudentService

student_service = StudentService()


# ======================= ADMIN =======================

def add_admin():
    name = input("Enter Admin Name: ").strip().title()
    password = input("Enter Admin Password: ").strip()

    if not name or not password:
        print("Name and password cannot be empty!")
        return

    # Load existing admin data
    try:
        with open("data/admin.json", "r") as file:
            admins = json.load(file)

        # Convert a single dictionary into a list
        if isinstance(admins, dict):
            if "name" in admins:
                admins = [admins]
            else:
                admins = list(admins.values())

        if not isinstance(admins, list):
            print("Invalid admin data format!")
            return

        # Check that every admin record is a dictionary
        if any(not isinstance(admin, dict) for admin in admins):
            print("Invalid admin record in admin.json!")
            return

    except FileNotFoundError:
        admins = []

    except json.JSONDecodeError:
        print("Admin data file contains invalid JSON!")
        return

    # Generate the next admin ID
    try:
        if admins:
            admin_id = max(
                int(admin.get("id", 0))
                for admin in admins
            ) + 1
        else:
            admin_id = 1

    except (ValueError, TypeError):
        print("Invalid admin ID in admin.json!")
        return

    # Create a new admin record
    admin = {
        "id": admin_id,
        "name": name,
        "password": password
    }

    admins.append(admin)

    # Save admin data
    try:
        with open("data/admin.json", "w") as file:
            json.dump(admins, file, indent=4)

        print("\nAdmin added successfully!")
        print(f"Admin ID: {admin_id}")
        print(f"Admin Name: {name}")

    except OSError as error:
        print(f"Error saving admin data: {error}")


def view_all_admin():
    def load_list(path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Data file not found: {path}")
            return []
        except json.JSONDecodeError:
            print(f"{path} contains invalid JSON!")
            return []

        if isinstance(data, dict):
            data = [data]
        return data

    admins = load_list("data/admin.json")
    sub_admins = load_list("data/staff_admin.json")

    print("\n" + "=" * 65)
    print("                  MAIN ADMIN DATA")
    print("=" * 65)

    if admins:
        print(f"{'ID':<5} {'Name':<20} {'Password':<20}")
        print("-" * 65)

        for data in admins:
            print(
                f"{str(data.get('id', 'N/A')):<5} "
                f"{data.get('name', 'N/A'):<20} "
                f"{data.get('password', 'N/A'):<20}"
            )
    else:
        print("No Admin Found!")

    print("\n" + "=" * 65)
    print("                   SUB-ADMIN DATA")
    print("=" * 65)

    if sub_admins:
        print(f"{'ID':<5} {'Name':<20} {'Password':<20}")
        print("-" * 65)

        for data in sub_admins:
            print(
                f"{str(data.get('id', 'N/A')):<5} "
                f"{data.get('name', 'N/A'):<20} "
                f"{data.get('password', 'N/A'):<20}"
            )
    else:
        print("No Sub-Admin Found!")

    print("=" * 65)


def update_admin():
    print("\n===== UPDATE ADMIN =====")
    print("1. Main Admin (admin.json)")
    print("2. Sub-Admin (staff_admin.json)")

    file_choice = input("Enter your choice: ").strip()

    if file_choice == "1":
        path = "data/admin.json"
    elif file_choice == "2":
        path = "data/staff_admin.json"
    else:
        print("Invalid choice!")
        return

    try:
        with open(path, "r") as file:
            admins = json.load(file)

        # Convert a single dictionary into a list
        if isinstance(admins, dict):
            if "name" in admins:
                admins = [admins]
            else:
                admins = list(admins.values())

        if not isinstance(admins, list) or not admins:
            print("No admin records found!")
            return

        print("\n===== ALL RECORDS =====")
        for admin in admins:
            if isinstance(admin, dict):
                print(
                    f"ID: {admin.get('id', 'N/A')} | "
                    f"Name: {admin.get('name', 'N/A')}"
                )

        admin_id = input("Enter ID to update: ").strip()

        if not admin_id.isdigit():
            print("Please enter a valid ID!")
            return

        data = next(
            (
                admin for admin in admins
                if isinstance(admin, dict)
                and str(admin.get("id")) == admin_id
            ),
            None
        )

        if data is None:
            print("Record not found!")
            return

        print("\n1. Name")
        print("2. Password")

        update_choice = input("What do you want to update?: ").strip().lower()

        if update_choice in ["1", "name"]:
            new_name = input("Enter New Name: ").strip().title()

            if not new_name:
                print("Name cannot be empty!")
                return

            data["name"] = new_name

        elif update_choice in ["2", "password"]:
            new_password = input("Enter New Password: ").strip()

            if not new_password:
                print("Password cannot be empty!")
                return

            data["password"] = new_password

        else:
            print("Invalid update option!")
            return

        with open(path, "w") as file:
            json.dump(admins, file, indent=4)

        print("Record updated successfully!")

    except FileNotFoundError:
        print(f"{path} not found!")

    except json.JSONDecodeError:
        print(f"{path} contains invalid JSON!")

    except OSError as error:
        print(f"File error: {error}")


def delete_admin():
    try:
        with open("data/admin.json", "r") as file:
            admins = json.load(file)

        # Support a single dictionary or a list
        if isinstance(admins, dict):
            if "name" in admins:
                admins = [admins]
            else:
                admins = list(admins.values())

        if not isinstance(admins, list):
            print("Invalid admin data format!")
            return

        if not admins:
            print("No Admins Found!")
            return

        print("\n===== ALL ADMINS =====")
        for admin in admins:
            if isinstance(admin, dict):
                print(
                    f"ID: {admin.get('id', 'N/A')} | "
                    f"Username: {admin.get('name', 'N/A')}"
                )

        admin_id = input("Enter Admin ID to delete: ").strip()

        if not admin_id.isdigit():
            print("Please enter a valid Admin ID!")
            return

        found_admin = next(
            (
                admin for admin in admins
                if isinstance(admin, dict)
                and str(admin.get("id")) == admin_id
            ),
            None
        )

        if found_admin is None:
            print("Admin Not Found!")
            return

        # Prevent deleting the only remaining admin
        if len(admins) == 1:
            print("Cannot delete the only admin!")
            return

        print(f"Admin: {found_admin.get('name', 'N/A')}")
        confirm = input("Are you sure you want to delete? (yes/no): ")
        confirm = confirm.strip().lower()

        if confirm == "yes":
            admins.remove(found_admin)

            with open("data/admin.json", "w") as file:
                json.dump(admins, file, indent=4)

            print("Admin deleted successfully!")
        else:
            print("Delete cancelled!")

    except FileNotFoundError:
        print("Admin data file not found!")

    except json.JSONDecodeError:
        print("Admin data file contains invalid JSON!")


# ======================= STAFF =======================

def add_staff():
    name = input("Enter Staff Name:- ").strip().title()

    while True:
        email = input("Enter Staff Email:- ").strip().lower()

        if email.endswith("@gmail.com") and email != "@gmail.com":
            break
        else:
            print("Invalid email! Please enter a valid @gmail.com address.")

    subject = input("Enter Staff Subject:- ").strip().capitalize()

    while True:
        try:
            salary = int(input("Enter Staff Salary:- "))
            if salary < 0:
                print("Salary cannot be negative!")
                continue
            break
        except ValueError:
            print("Please enter a valid numeric salary!")

    while True:
        password = input("Enter Staff Password:- ").strip()

        if password:
            break
        print("Password cannot be empty!")

    try:
        with open("data/teacher.json", "r") as file:
            teachers = json.load(file)

    except FileNotFoundError:
        teachers = []

    if teachers:
        staff_id = max(int(item["id"]) for item in teachers) + 1
    else:
        staff_id = 1

    staff = {
        "name": name,
        "email": email,
        "subject": subject,
        "salary": salary,
        "password": password,
        "id": staff_id
    }

    teachers.append(staff)

    with open("data/teacher.json", "w") as file:
        json.dump(teachers, file, indent=4)

    print(f"Staff added successfully! ID: {staff_id}")


def view_all_staff():
    try:
        with open("data/teacher.json", "r") as file:
            staffs = json.load(file)

        if not staffs:
            print("No Staff Found!")
            return

        print("=" * 87)
        print(f"{'ID':<5}{'Name':<20}{'Email':<30}{'Subject':<15}{'Salary':<10}")
        print("=" * 87)

        for data in staffs:
            print(
                f"{data['id']:<5}"
                f"{data['name']:<20}"
                f"{data['email']:<30}"
                f"{data['subject']:<15}"
                f"{str(data.get('salary', 'N/A')):<10}"
            )
            print("-" * 87)

    except FileNotFoundError:
        print("No Staff Found!")

    except json.JSONDecodeError:
        print("Staff data file contains invalid JSON!")


def search_staff():
    try:
        with open("data/teacher.json", "r") as file:
            staffs = json.load(file)

        if not staffs:
            print("No Staff Found!")
            return

        print("\n===== SEARCH STAFF =====")
        print("1. Search by Staff ID")
        print("2. Search by Staff Name")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_value = input("Enter Staff ID: ").strip()

            if not search_value.isdigit():
                print("Please enter a valid numeric Staff ID.")
                return

            found_staffs = [
                staff for staff in staffs
                if str(staff["id"]) == search_value
            ]

        elif choice == "2":
            search_name = input("Enter Staff Name: ").strip().lower()

            if not search_name:
                print("Staff name cannot be empty!")
                return

            found_staffs = [
                staff for staff in staffs
                if search_name in staff["name"].lower()
            ]

        else:
            print("Invalid choice!")
            return

        if found_staffs:
            print("\n" + "=" * 95)
            print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Subject':<15} {'Salary':<10}")
            print("=" * 95)

            for data in found_staffs:
                print(
                    f"{data['id']:<5} "
                    f"{data['name']:<20} "
                    f"{data['email']:<30} "
                    f"{data['subject']:<15} "
                    f"{str(data.get('salary', 'N/A')):<10}"
                )

            print("=" * 95)

        else:
            print("Staff Not Found!")

    except FileNotFoundError:
        print("Staff data file not found!")

    except json.JSONDecodeError:
        print("Staff data file contains invalid JSON!")


def update_staff():
    try:
        with open("data/teacher.json", "r") as file:
            staffs = json.load(file)

        if not isinstance(staffs, list):
            print("Invalid staff data format!")
            return

        if not staffs:
            print("No staff records found!")
            return

        print("\n===== UPDATE STAFF =====")
        print("1. Search by Staff ID")
        print("2. Search by Staff Name")

        search_choice = input("Enter your choice: ").strip().lower()

        if search_choice in ["1", "id"]:
            staff_id = input("Enter Staff ID: ").strip()

            if not staff_id.isdigit():
                print("Please enter a valid Staff ID!")
                return

            found_staffs = [
                staff for staff in staffs
                if str(staff.get("id")) == staff_id
            ]

        elif search_choice in ["2", "name"]:
            staff_name = input("Enter Staff Name: ").strip().lower()

            if not staff_name:
                print("Staff name cannot be empty!")
                return

            found_staffs = [
                staff for staff in staffs
                if staff.get("name", "").lower() == staff_name
            ]

        else:
            print("Invalid choice!")
            return

        if not found_staffs:
            print("Staff not found!")
            return

        if len(found_staffs) > 1:
            print("\nMultiple staff records found:")

            for staff in found_staffs:
                print(f"ID: {staff['id']} | Name: {staff['name']}")

            selected_id = input(
                "Enter the Staff ID you want to update: "
            ).strip()

            found_staffs = [
                staff for staff in found_staffs
                if str(staff.get("id")) == selected_id
            ]

            if not found_staffs:
                print("Staff ID not found!")
                return

        data = found_staffs[0]

        print("\n===== CURRENT STAFF DETAILS =====")
        print(f"ID: {data.get('id')}")
        print(f"Name: {data.get('name')}")
        print(f"Email: {data.get('email')}")
        print(f"Subject: {data.get('subject')}")
        print(f"Salary: {data.get('salary')}")

        print("\nWhat do you want to update?")
        print("1. Name")
        print("2. Email")
        print("3. Subject")
        print("4. Salary")
        print("5. Password")

        update_choice = input("Enter your choice: ").strip().lower()

        if update_choice in ["1", "name"]:
            new_name = input("Enter New Name: ").strip()

            if not new_name:
                print("Name cannot be empty!")
                return

            data["name"] = new_name.title()

        elif update_choice in ["2", "email"]:
            new_email = input("Enter New Email: ").strip().lower()

            if (
                not new_email
                or "@" not in new_email
                or new_email.startswith("@")
                or new_email.endswith("@")
                or "." not in new_email.split("@")[-1]
            ):
                print("Please enter a valid email address!")
                return

            data["email"] = new_email

        elif update_choice in ["3", "subject"]:
            new_subject = input("Enter New Subject: ").strip()

            if not new_subject:
                print("Subject cannot be empty!")
                return

            data["subject"] = new_subject.title()

        elif update_choice in ["4", "salary"]:
            salary_input = input("Enter New Salary: ").strip()

            try:
                new_salary = float(salary_input)

                if new_salary < 0:
                    print("Salary cannot be negative!")
                    return

                if not new_salary.is_integer():
                    print("Please enter salary in whole rupees!")
                    return

                data["salary"] = int(new_salary)

            except ValueError:
                print("Please enter a valid numeric salary!")
                return

        elif update_choice in ["5", "password"]:
            new_password = input("Enter New Password: ").strip()

            if not new_password:
                print("Password cannot be empty!")
                return

            data["password"] = new_password

        else:
            print("Invalid update choice!")
            return

        with open("data/teacher.json", "w") as file:
            json.dump(staffs, file, indent=4)

        print("\nStaff updated successfully!")

    except FileNotFoundError:
        print("Error: data/teacher.json file not found!")

    except json.JSONDecodeError:
        print("Error: teacher.json contains invalid JSON!")

    except OSError as error:
        print(f"File error: {error}")


def delete_staff():
    try:
        with open("data/teacher.json", "r") as file:
            staffs = json.load(file)

        staff_id = int(input("Enter Staff ID to delete: "))

        found = False

        for data in staffs:
            if int(data["id"]) == staff_id:
                print("=" * 90)
                print(f"Delete Staff {data['name']}")
                print(f"\nName:-{data['name']}")
                print(f"Email:-{data['email']}")
                print(f"Subject:-{data['subject']}")
                print(f"Salary:-{data.get('salary', 'N/A')}")

                delete = input(
                    f"Enter (Y,N) to Delete {data['name']}:-"
                ).strip().lower()

                if delete == "y":
                    staffs.remove(data)

                    with open("data/teacher.json", "w") as file:
                        json.dump(staffs, file, indent=4)

                    print("Staff deleted successfully!")
                else:
                    print("Delete cancelled!")

                found = True
                break

        if not found:
            print("Staff not found!")

    except FileNotFoundError:
        print("Staff data file not found!")

    except json.JSONDecodeError:
        print("Staff data file contains invalid JSON!")

    except ValueError:
        print("Please enter a valid numeric Staff ID.")


# ======================= STUDENT =======================

def add_student():
    print("\n===== ADD STUDENT =====")

    name = input("Enter Student Name: ").strip()
    email = input("Enter Student Email: ").strip()
    course = input("Enter Student Course: ").strip()

    try:
        marks = int(input("Enter Student Marks (0-100): "))

        # Get the next student ID
        students = student_service.get_all_students()

        if students:
            student_id = max(
                int(student.get("id", 0))
                for student in students
            ) + 1
        else:
            student_id = 1

        # Add student using StudentService
        student = student_service.add_student(
            student_id, name, email, course, marks
        )

        print("\nStudent added successfully!")
        print(f"Student ID: {student.id}")
        print(f"Name: {student.name}")
        print(f"Email: {student.email}")
        print(f"Course: {student.course}")
        print(f"Marks: {student.marks}")

    except ValueError as error:
        print(f"Error: {error}")


def view_all_students():
    try:
        with open("data/students.json", "r") as file:
            students = json.load(file)

        if not students:
            print("No Student Found!")
            return

        print("=" * 87)
        print(f"{'ID':<5}{'Name':<20}{'Email':<30}{'Course':<15}{'Marks':<10}")
        print("=" * 87)

        for data in students:
            print(
                f"{data['id']:<5}"
                f"{data['name']:<20}"
                f"{data['email']:<30}"
                f"{data['course']:<15}"
                f"{str(data.get('marks', 'N/A')):<10}"
            )
            print("-" * 87)

    except FileNotFoundError:
        print("No Student Found!")

    except json.JSONDecodeError:
        print("Student data file contains invalid JSON!")


def search_student():
    try:
        with open("data/students.json", "r") as file:
            students = json.load(file)

        if not isinstance(students, list):
            print("Invalid student data format!")
            return

        if not students:
            print("No Students Found!")
            return

        print("\n===== SEARCH STUDENT =====")
        print("1. Search by Student ID")
        print("2. Search by Student Name")

        choice = input("Enter your choice: ").strip().lower()

        if choice in ["1", "id"]:
            search_value = input("Enter Student ID: ").strip()

            if not search_value.isdigit():
                print("Please enter a valid numeric Student ID!")
                return

            found_students = [
                student for student in students
                if str(student.get("id", "")) == search_value
            ]

        elif choice in ["2", "name"]:
            search_name = input("Enter Student Name: ").strip().lower()

            if not search_name:
                print("Student name cannot be empty!")
                return

            found_students = [
                student for student in students
                if search_name in str(student.get("name", "")).lower()
            ]

        else:
            print("Invalid choice!")
            return

        if not found_students:
            print("Student Not Found!")
            return

        print("\n" + "=" * 95)
        print(
            f"{'ID':<5} {'Name':<20} {'Email':<30} "
            f"{'Course':<15} {'Marks':<10}"
        )
        print("=" * 95)

        for data in found_students:
            print(
                f"{str(data.get('id', 'N/A')):<5} "
                f"{str(data.get('name', 'N/A')):<20} "
                f"{str(data.get('email', 'N/A')):<30} "
                f"{str(data.get('course', 'N/A')):<15} "
                f"{str(data.get('marks', 'N/A')):<10}"
            )

        print("=" * 95)

    except FileNotFoundError:
        print("Student data file not found!")

    except json.JSONDecodeError:
        print("Student data file contains invalid JSON!")

    except OSError as error:
        print(f"File error: {error}")


def update_student():
    try:
        with open("data/students.json", "r") as file:
            students = json.load(file)

        if not students:
            print("No Students Found!")
            return

        print("\n===== FIND STUDENT TO UPDATE =====")
        print("1. Search by Student ID")
        print("2. Search by Student Name")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_value = input("Enter Student ID: ").strip()

            if not search_value.isdigit():
                print("Please enter a valid Student ID!")
                return

            found_students = [
                student for student in students
                if str(student["id"]) == search_value
            ]

        elif choice == "2":
            search_name = input("Enter Student Name: ").strip().lower()

            found_students = [
                student for student in students
                if search_name and search_name in student["name"].lower()
            ]

        else:
            print("Invalid choice!")
            return

        if not found_students:
            print("Student Not Found!")
            return

        if len(found_students) > 1:
            print("Multiple students found:")
            for student in found_students:
                print(f"ID: {student['id']} | Name: {student['name']}")

            selected_id = input("Enter the ID of the student to update: ").strip()

            if not selected_id.isdigit():
                print("Invalid Student ID!")
                return

            selected_student = next(
                (student for student in found_students
                 if str(student["id"]) == selected_id),
                None
            )

            if selected_student is None:
                print("Student not found!")
                return
        else:
            selected_student = found_students[0]

        data = selected_student

        print("\n" + "=" * 50)
        print(f"Update Student: {data['name']} (ID: {data['id']})")
        print(f"1. Name:-{data['name']}")
        print(f"2. Email:-{data['email']}")
        print(f"3. Course:-{data['course']}")
        print(f"4. Marks:-{data['marks']}")

        update_choice = input("Enter your update option: ").strip().lower()

        if update_choice in ["1", "name"]:
            new_name = input("Enter New Name: ").strip()

            if not new_name:
                print("Name cannot be empty!")
                return

            data["name"] = new_name.title()

        elif update_choice in ["2", "email"]:
            while True:
                email = input("Enter New Email: ").strip().lower()

                if email.endswith("@gmail.com") and email != "@gmail.com":
                    data["email"] = email
                    break

                print("Invalid email! Enter an @gmail.com address.")

        elif update_choice in ["3", "course"]:
            new_course = input("Enter New Course: ").strip()

            if not new_course:
                print("Course cannot be empty!")
                return

            data["course"] = new_course.capitalize()

        elif update_choice in ["4", "marks"]:
            try:
                marks = int(input("Enter New Marks (0-100): "))

                if not 0 <= marks <= 100:
                    print("Marks must be between 0 and 100!")
                    return

                data["marks"] = marks

            except ValueError:
                print("Please enter valid numeric marks!")
                return

        else:
            print("Invalid update option!")
            return

        with open("data/students.json", "w") as file:
            json.dump(students, file, indent=4)

        print("Student updated successfully!")

    except FileNotFoundError:
        print("Student data file not found!")

    except json.JSONDecodeError:
        print("Student data file contains invalid JSON!")


def delete_student():
    try:
        with open("data/students.json", "r") as file:
            students = json.load(file)

        student_id = int(input("Enter Student ID to delete: "))

        found = False

        for data in students:
            if int(data["id"]) == student_id:
                print("=" * 90)
                print(f"Delete Student {data['name']}")
                print(f"\nName:-{data['name']}")
                print(f"Email:-{data['email']}")
                print(f"Course:-{data['course']}")
                print(f"Marks:-{data['marks']}")

                delete = input(
                    f"Enter (Y,N) to Delete {data['name']}:-"
                ).strip().lower()

                if delete == "y":
                    students.remove(data)

                    with open("data/students.json", "w") as file:
                        json.dump(students, file, indent=4)

                    print("Student deleted successfully!")
                else:
                    print("Delete cancelled!")

                found = True
                break

        if not found:
            print("Student not found!")

    except FileNotFoundError:
        print("Student data file not found!")

    except json.JSONDecodeError:
        print("Student data file contains invalid JSON!")

    except ValueError:
        print("Please enter a valid numeric Student ID.")


def see_all_staff_and_student_data():
    try:
        # Load student data
        with open("data/students.json", "r") as file:
            students = json.load(file)

        # Load staff data
        with open("data/teacher.json", "r") as file:
            staff = json.load(file)

        print("\n" + "=" * 90)
        print("                 ALL STUDENT DATA")
        print("=" * 90)

        if students:
            print(
                f"{'ID':<5} {'Name':<20} {'Email':<30} "
                f"{'Course':<15} {'Marks':<10}"
            )
            print("-" * 90)

            for student in students:
                print(
                    f"{str(student.get('id', 'N/A')):<5} "
                    f"{student.get('name', 'N/A'):<20} "
                    f"{student.get('email', 'N/A'):<30} "
                    f"{student.get('course', 'N/A'):<15} "
                    f"{str(student.get('marks', 'N/A')):<10}"
                )
        else:
            print("No Students Found!")

        print("\n" + "=" * 90)
        print("                   ALL STAFF DATA")
        print("=" * 90)

        if staff:
            print(
                f"{'ID':<5} {'Name':<20} {'Email':<30} "
                f"{'Subject':<20} {'Salary':<10}"
            )
            print("-" * 90)

            for member in staff:
                print(
                    f"{str(member.get('id', 'N/A')):<5} "
                    f"{member.get('name', 'N/A'):<20} "
                    f"{member.get('email', 'N/A'):<30} "
                    f"{member.get('subject', 'N/A'):<20} "
                    f"{str(member.get('salary', 'N/A')):<10}"
                )
        else:
            print("No Staff Found!")

        print("=" * 90)

    except FileNotFoundError as error:
        print(f"Data file not found: {error.filename}")

    except json.JSONDecodeError:
        print("A JSON data file contains invalid JSON!")


def student_result():
    try:
        with open("data/students.json", "r") as file:
            students = json.load(file)

        if not isinstance(students, list) or not students:
            print("No Students Found!")
            return

        print("\n===== STUDENT MARKSHEET =====")
        print("1. All Students Result")
        print("2. Search by Student ID")
        print("3. Search by Student Name")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            results = students

        elif choice == "2":
            student_id = input("Enter Student ID: ").strip()
            results = [
                student for student in students
                if str(student.get("id", "")) == student_id
            ]

        elif choice == "3":
            name = input("Enter Student Name: ").strip().lower()

            if not name:
                print("Student name cannot be empty!")
                return

            results = [
                student for student in students
                if name in str(student.get("name", "")).lower()
            ]

        else:
            print("Invalid choice!")
            return

        if not results:
            print("No matching student found!")
            return

        print("\n" + "=" * 100)
        print(
            f"{'ID':<6} {'Name':<20} {'Email':<36} "
            f"{'Course':<20} {'Marks':<10} {'Result':<8}"
        )
        print("-" * 100)

        for student in results:
            try:
                marks = float(student.get("marks", 0))

                if 0 <= marks <= 100:
                    result = "PASS" if marks >= 40 else "FAIL"
                    marks_display = f"{marks:g}"
                else:
                    result = "N/A"
                    marks_display = "N/A"

            except (ValueError, TypeError):
                result = "N/A"
                marks_display = "N/A"

            print(
                f"{str(student.get('id', 'N/A')):<6} "
                f"{str(student.get('name', 'N/A')):<20} "
                f"{str(student.get('email', 'N/A')):<36} "
                f"{str(student.get('course', 'N/A')):<20} "
                f"{marks_display:<10} {result:<8}"
            )

        print("=" * 100)

        export = input(
            "Export results to CSV for Excel? (y/n): "
        ).strip().lower()

        if export == "y":
            filename = input(
                "Enter filename (default: student_marksheet.csv): "
            ).strip()

            if not filename:
                filename = "student_marksheet.csv"

            if not filename.lower().endswith(".csv"):
                filename += ".csv"

            with open(
                filename, "w", newline="", encoding="utf-8-sig"
            ) as file:
                writer = csv.writer(file)

                writer.writerow([
                    "Student ID", "Name", "Email",
                    "Course", "Marks", "Result"
                ])

                for student in results:
                    try:
                        marks = float(student.get("marks", 0))

                        if 0 <= marks <= 100:
                            result = "PASS" if marks >= 40 else "FAIL"
                            marks_display = f"{marks:g}"
                        else:
                            result = "N/A"
                            marks_display = "N/A"

                    except (ValueError, TypeError):
                        marks_display = "N/A"
                        result = "N/A"

                    writer.writerow([
                        student.get("id", "N/A"),
                        student.get("name", "N/A"),
                        student.get("email", "N/A"),
                        student.get("course", "N/A"),
                        marks_display,
                        result
                    ])

            print(f"Marksheet saved successfully: {filename}")
            print("You can open this CSV file in Microsoft Excel.")

    except FileNotFoundError:
        print("Student data file not found!")

    except json.JSONDecodeError:
        print("Student data file contains invalid JSON!")

    except OSError as error:
        print(f"File error: {error}")


# ======================= STAFF LOGIN HELPER =======================

def load_staff_accounts():
    """Return all staff accounts: staff added via Add Staff (teacher.json)
    plus the older sub-admin accounts (staff_admin.json)."""
    accounts = []

    for path in ["data/teacher.json", "data/staff_admin.json"]:
        try:
            with open(path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            print(f"Warning: {path} contains invalid JSON!")
            continue

        # Support list or dictionary format
        if isinstance(data, dict):
            if "name" in data:
                data = [data]
            else:
                data = list(data.values())

        if isinstance(data, list):
            accounts.extend(item for item in data if isinstance(item, dict))

    return accounts


# ======================= MAIN PROGRAM =======================

while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Admin Login")
    print("2. Staff Login")
    print("3. Exit")

    user = input("Enter Your Choice: ").strip().lower()

    # ========== ADMIN LOGIN ==========
    if user in ["1", "admin", "admin login"]:
        try:
            with open("data/admin.json", "r") as file:
                admin_data = json.load(file)

            # Support list or dictionary format
            if isinstance(admin_data, dict):
                if "name" in admin_data:
                    admin_data = [admin_data]
                else:
                    admin_data = list(admin_data.values())

            if not isinstance(admin_data, list):
                print("Invalid admin data format!")
                continue

            admin_name = input("Enter Admin Name: ").strip()
            admin_password = input("Enter Admin Password: ")

            logged_in = False

            for admin in admin_data:
                if not isinstance(admin, dict):
                    continue

                if (
                    admin.get("name", "").lower() == admin_name.lower()
                    and admin.get("password") == admin_password
                ):
                    logged_in = True
                    break

            if logged_in:
                print("Login successful!")
                print(f"Welcome, Admin {admin_name}!")

                while True:
                    print("\n===== ADMIN MENU =====")
                    print("1. Add Student")
                    print("2. View All Students")
                    print("3. Search Student")
                    print("4. Update Student")
                    print("5. Delete Student")
                    print("6. Add Staff")
                    print("7. View All Staff")
                    print("8. Search Staff")
                    print("9. Update Staff")
                    print("10. Delete Staff")
                    print("11. Add Admin")
                    print("12. View All Admin")
                    print("13. Delete Admin")
                    print("14. Update Admin")
                    print("15. See All Staff & Student Data")
                    print("16. Logout")

                    admin_choice = input(
                        "Enter Admin Choice: "
                    ).strip().lower()

                    if admin_choice in ["1", "add student"]:
                        add_student()

                    elif admin_choice in ["2", "view all students"]:
                        view_all_students()

                    elif admin_choice in ["3", "search student"]:
                        search_student()

                    elif admin_choice in ["4", "update student"]:
                        update_student()

                    elif admin_choice in ["5", "delete student"]:
                        delete_student()

                    elif admin_choice in ["6", "add staff"]:
                        add_staff()

                    elif admin_choice in ["7", "view all staff"]:
                        view_all_staff()

                    elif admin_choice in ["8", "search staff"]:
                        search_staff()

                    elif admin_choice in ["9", "update staff"]:
                        update_staff()

                    elif admin_choice in ["10", "delete staff"]:
                        delete_staff()

                    elif admin_choice in ["11", "add admin"]:
                        add_admin()

                    elif admin_choice in ["12", "view all admin"]:
                        view_all_admin()

                    elif admin_choice in ["13", "delete admin"]:
                        delete_admin()

                    elif admin_choice in ["14", "update admin"]:
                        update_admin()

                    elif admin_choice in [
                        "15", "see all staff & student data"
                    ]:
                        see_all_staff_and_student_data()

                    elif admin_choice in ["16", "logout"]:
                        print("Admin logged out.")
                        break

                    else:
                        print("Invalid choice!")

            else:
                print("Invalid username or password!")

        except FileNotFoundError:
            print("Admin JSON file not found. Check the file path.")

        except json.JSONDecodeError:
            print("Admin JSON file has invalid data.")

    # ========== STAFF LOGIN ==========
    elif user in ["2", "staff", "staff login"]:
        try:
            staff_data = load_staff_accounts()

            if not staff_data:
                print("No staff accounts found!")
                continue

            staff_name = input("Enter Staff Name or Email: ").strip()
            staff_password = input("Enter Staff Password: ")

            logged_in = False

            for staff in staff_data:
                stored_password = staff.get("password")

                if not stored_password:
                    continue

                name_match = (
                    str(staff.get("name", "")).lower() == staff_name.lower()
                    or str(staff.get("email", "")).lower() == staff_name.lower()
                )

                if name_match and stored_password == staff_password:
                    logged_in = True
                    break

            if logged_in:
                print("Login successful!")
                print(f"Welcome, Staff {staff_name}!")

                while True:
                    print("\n===== STAFF MENU =====")
                    print("1. Add Student")
                    print("2. View All Students")
                    print("3. Search Student")
                    print("4. Update Student")
                    print("5. Student Result")
                    print("6. Logout")

                    staff_choice = input(
                        "Enter Staff Choice: "
                    ).strip().lower()

                    if staff_choice in ["1", "add student"]:
                        add_student()

                    elif staff_choice in ["2", "view all students"]:
                        view_all_students()

                    elif staff_choice in ["3", "search student"]:
                        search_student()

                    elif staff_choice in ["4", "update student"]:
                        update_student()

                    elif staff_choice in ["5", "student result"]:
                        student_result()

                    elif staff_choice in ["6", "logout"]:
                        print("Staff logged out.")
                        break

                    else:
                        print("Invalid choice!")

            else:
                print("Invalid username or password!")

        except FileNotFoundError:
            print("Staff JSON file not found. Check the file path.")

        except json.JSONDecodeError:
            print("Staff JSON file has invalid data.")

    # ========== EXIT ==========
    elif user in ["3", "exit"]:
        print("Thank you! Goodbye!")
        break

    else:
        print("Invalid choice!")