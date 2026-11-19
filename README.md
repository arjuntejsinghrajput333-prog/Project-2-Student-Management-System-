# Student Management System

A simple Student Management System built using Python. This project helps manage student, staff, and admin records using JSON files.

## Features

- Add, view, search, update, and delete student records
- Add, view, search, update, and delete staff records
- Add, view, update, and delete admin records
- Admin and staff login system
- Display student results
- Export student results to a CSV file
- Store records in JSON files

## Technologies Used

- Python
- JSON
- CSV
- VS Code

## Project Structure

```text
Student-Management-System/
│
├── main.py
├── student_service.py
├── README.md
├── .gitignore
│
└── data/
    ├── students.json
    ├── teacher.json
    ├── admin.json
    └── staff_admin.json
```

*Note: Update this structure if your actual filenames or folders are different.*

## Requirements

- Python 3.10 or later
- Visual Studio Code (recommended)

## How to Run

1. Install Python.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run the following command:

```bash
python main.py
```

## Data Storage

The project uses JSON files to store student, staff, and admin records. Student results can be exported to CSV format.

## Security

- Do not upload real passwords or confidential student information to a public repository.
- Keep private configuration files and sensitive data out of GitHub.

## Future Improvements

- Add a database such as MySQL or SQLite.
- Improve password security.
- Add a graphical user interface.
- Add automated testing.

## Author

Arjun Singh Rajput

## License

This project is for educational and learning purposes.
