from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from PyQt5.QtCore import Qt
from shared import courses, students

class AddStudentTab(QWidget):
    def __init__(self):
        """
        Initializes the AddStudentTab, setting up the attributes and initializing the UI.

        Attributes:
            student_dropdown (QComboBox): Dropdown of the list of students from shared.py
            student_var (str): Selected student_id
            name_input (QLineEdit): Name input
            age_input (QLineEdit): Age input 
            email_input (QLineEdit): Email input
            student_id_input (QLineEdit): Student ID input
            edit_name_input (QLineEdit): Edit name input
            edit_age_input (QLineEdit): Edit age input 
            edit_email_input (QLineEdit): Edit email input
        """
        super().__init__()
        self.student_dropdown = None
        self.student_var = None
        self.name_input : QLineEdit = None
        self.age_input : QLineEdit = None
        self.email_input : QLineEdit = None
        self.student_id_input : QLineEdit = None
        self.edit_name_input : QLineEdit = None
        self.edit_age_input : QLineEdit = None
        self.edit_email_input : QLineEdit = None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the AddStudentTab. Sets up the layout and adds all the components
        """
        # Grid Layout
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add Student Title
        add_student_title = QLabel("Add Student")
        add_student_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(add_student_title,0,0,1,2)

        # Name Input Label
        name_label = QLabel("Name:")
        layout.addWidget(name_label,1,0)

        # Name Input
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input,1,1)

        # Age Input Label
        age_label = QLabel("Age:")
        layout.addWidget(age_label,2,0)

        # Age Input
        self.age_input = QLineEdit()
        layout.addWidget(self.age_input,2,1)

        # Email Input Label
        email_label = QLabel("Email:")
        layout.addWidget(email_label,3,0)

        # Email Input
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input,3,1)

        # Student ID Input Label
        student_id_label = QLabel("Student ID:")
        layout.addWidget(student_id_label,4,0)

        # Student ID Input
        self.student_id_input = QLineEdit()
        layout.addWidget(self.student_id_input,4,1)

        # Add Student Button
        submit_button = QPushButton("Add Student")
        submit_button.clicked.connect(self.create_student)
        layout.addWidget(submit_button,5,0,1,2)

        # Edit or Remove Student Title
        edit_student_title = QLabel("Edit or Remove Student")
        edit_student_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(edit_student_title,6,0,1,2)

        # Student Dropdown Label
        student_dropdown_label = QLabel("Select Student:")
        layout.addWidget(student_dropdown_label,7,0)

        # Student Dropdown
        self.student_dropdown = QComboBox()
        self.student_dropdown.addItems([student.name for student in students])
        self.student_dropdown.currentIndexChanged.connect(self.on_select)
        layout.addWidget(self.student_dropdown,7,1)

        # Edit Name Input Label
        edit_name_label = QLabel("Name:")
        layout.addWidget(edit_name_label ,8,0)

        # Edit Name Input
        self.edit_name_input = QLineEdit()
        layout.addWidget(self.edit_name_input,8,1)

        # Edit Age Input Label
        edit_age_label = QLabel("Age:")
        layout.addWidget(edit_age_label,9,0)

        # Edit Age Input
        self.edit_age_input = QLineEdit()
        layout.addWidget(self.edit_age_input,9,1)

        # Edit Email Input Label
        edit_email_label = QLabel("Email:")
        layout.addWidget(edit_email_label,10,0)

        # Edit Email Input
        self.edit_email_input = QLineEdit()
        layout.addWidget(self.edit_email_input,10,1)

        # Edit Student Button
        edit_button = QPushButton("Edit Student")
        edit_button.clicked.connect(self.edit_student)
        layout.addWidget(edit_button,11,0,1,2)

        # Remove Student Button
        remove_button = QPushButton("Remove Student")
        remove_button.clicked.connect(self.delete_student)
        layout.addWidget(remove_button,12,0,1,2)

        self.setLayout(layout)

    def create_student(self):
        """
        Adds a student to the db and updates local copy

        Validates the create process and displays success or error messages
        using a QMessageBox.
        """
        try:
            name = self.name_input.text()
            age = int(self.age_input.text())
            email = self.email_input.text()
            student_id = self.student_id_input.text()

            student = Student(name, age, email, student_id, [])

            valid, errors = add_student(student)
            # Commented code for JSON
            # valid, errors = add_entry_json('Student', student)

            if valid:
                QMessageBox.information(self, "Success", f"Student {name} created successfully!")
                self.name_input.clear()
                self.age_input.clear()
                self.email_input.clear()
                self.student_id_input.clear()
                students.append(student)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))

        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def delete_student(self):
        """
        Deletes a student from the db and updates local copy

        Validates the delete process and displays success or error messages
        using a QMessageBox.
        """
        try:
            student_id = self.student_var
            student = next(stud for stud in students if stud.student_id == student_id)
            
            for course_id in student.registered_courses:
                course = next(course for course in courses if course.course_id == course_id)
                course.unenroll_student(student)
                courses.remove(course)
                courses.append(course)
                # Commented code for JSON
                #edit_entry_json('Course', course)
            
            valid, errors = delete_student(student)
            # Commented code for JSON
            # valid, errors = delete_entry_json('Student', student)

            if valid:
                QMessageBox.information(self, "Success", f"Student {student.name} has been removed successfully!")
                self.edit_name_input.clear()
                self.edit_age_input.clear()
                self.edit_email_input.clear()
                students.remove(student)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))

        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def edit_student(self):
        """
        Updates a student in the db and updates local copy

        Validates the edit process and displays success or error messages
        using a QMessageBox.
        """
        try:
            new_name = self.edit_name_input.text()
            new_age = int(self.edit_age_input.text())
            new_email = self.edit_email_input.text()

            student_id = self.student_var
            student = next(stud for stud in students if stud.student_id == student_id)
            
            student.name = new_name
            student.age = new_age
            student._email = new_email

            valid, errors = edit_student(student)
            # Commented code for JSON
            # valid, errors = edit_entry_json('Student', student)

            if valid:
                QMessageBox.information(self, "Success", f"Student {student.name} edited successfully!")
                self.edit_name_input.clear()
                self.edit_age_input.clear()
                self.edit_email_input.clear()
                students.remove(student)
                students.append(student)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))

        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def on_select(self):
        """
        Updates the student_var attribute with the selected student_id and input labels
        """
        idx = self.student_dropdown.currentIndex()
        if idx != -1:
            selected = students[idx]
            self.student_var = selected.student_id
            self.edit_name_input.setText(selected.name)
            self.edit_email_input.setText(selected._email)
            self.edit_age_input.setText(str(selected.age))
    
    def update_ui(self):
        """
        Updated the UI for the instructor dropdown to relfect new data
        """
        self.student_dropdown.clear()
        self.student_dropdown.addItems([student.name for student in students])