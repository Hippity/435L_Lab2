from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from classes.Course import *
from PyQt5.QtCore import Qt
from crud.jsonCRUD import *
from crud.databaseCRUD import *
from shared import instructors, courses

class AddInstructorTab(QWidget):
    def __init__(self):
        """
        Initializes the AddInstructorTab, setting up the attributes and initializing the UI.

        Attributes:
            instructor_dropdown (QComboBox): Dropdown of the list of instructors from shared.py
            instructor_var (str): Selected instructor_id
            name_input (QLineEdit): Name input
            age_input (QLineEdit): Age input 
            email_input (QLineEdit): Email input
            instructor_id_input (QLineEdit): Instructor ID input
            edit_name_input (QLineEdit): Edit name input
            edit_age_input (QLineEdit): Edit age input 
            edit_email_input (QLineEdit): Edit email input
        """
        super().__init__()
        self.instructor_dropdown : QComboBox = None
        self.instructor_var : str = None
        self.name_input : QLineEdit = None
        self.age_input : QLineEdit = None
        self.email_input : QLineEdit = None
        self.instructor_id_input : QLineEdit = None
        self.edit_name_input : QLineEdit = None
        self.edit_age_input : QLineEdit = None
        self.edit_email_input : QLineEdit = None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the AddInstructorTab. Sets up the layout and adds all the components
        """
        # Grid Layout
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add Instructor Title
        add_instructor_title = QLabel("Add Instructor")
        add_instructor_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(add_instructor_title,0,0,1,2)

        # Name Input Label
        name_label = QLabel("Name:")
        layout.addWidget(name_label ,1,0)

        # Name Input
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input, 1,1)

        # Age Input Label
        age_label = QLabel("Age:")
        layout.addWidget(age_label, 2,0)

        # Age Input
        self.age_input = QLineEdit()
        layout.addWidget(self.age_input, 2,1)

        # Email Input Label
        email_label = QLabel("Email:")
        layout.addWidget(email_label, 3,0)

        # Email Input
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input, 3,1)

        # Instructor ID Input Label
        instructor_id_label = QLabel("Instructor ID:")
        layout.addWidget(instructor_id_label, 4,0)

        # Instructor ID Input
        self.instructor_id_input = QLineEdit()
        layout.addWidget(self.instructor_id_input, 4,1)

        # Add Instructor Button
        submit_button = QPushButton("Add Instructor")
        submit_button.clicked.connect(self.create_instructor)
        layout.addWidget(submit_button, 5,0,1,2)

        # Edit or Remove Instructor Title
        edit_instructor_title = QLabel("Edit or Remove Instructor")
        edit_instructor_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(edit_instructor_title, 6,0,1,2)

        # Instructor Dropdown Label
        instructor_dropdown_label = QLabel("Select Instructor:")
        layout.addWidget(instructor_dropdown_label, 7,0)

        # Instructor Dropdown
        self.instructor_dropdown = QComboBox()
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])
        self.instructor_dropdown.currentIndexChanged.connect(self.on_select)
        layout.addWidget(self.instructor_dropdown, 7,1)

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

        # Edit Instructor Button
        edit_button = QPushButton("Edit Instructor")
        edit_button.clicked.connect(self.edit_instructor)
        layout.addWidget(edit_button,11,0,1,2)

        # Remove Instructor Button
        remove_button = QPushButton("Remove Instructor")
        remove_button.clicked.connect(self.delete_instructor)
        layout.addWidget(remove_button,12,0,1,2)

        self.setLayout(layout)

    def create_instructor(self):
        """
        Adds an instructor to the db and updates local copy

        Validates the create process and displays success or error messages
        using a QMessageBox.
        """
        try:
            name = self.name_input.text()
            age = int(self.age_input.text())
            email = self.email_input.text()
            instructor_id = self.instructor_id_input.text()

            instructor = Instructor(name, age, email, instructor_id, [])
            
            valid, errors = add_instructor(instructor)
            # Commented code for JSON
            # valid, errors = add_entry_json('Instructor', instructor)

            if valid:
                QMessageBox.information(self, "Success", f"Instructor {instructor.name} created successfully!")
                self.name_input.clear()
                self.age_input.clear()
                self.email_input.clear()
                self.instructor_id_input.clear()
                instructors.append(instructor)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))
        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def delete_instructor(self):
        """
        Deletes an instructor from the db and updates local copy

        Validates the delete process and displays success or error messages
        using a QMessageBox.
        """
        try:
            instructor_id = self.instructor_var
            instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)
            
            for course_id in instructor.assigned_courses:
                course = next(course for course in courses if course.course_id == course_id)
                course.unassign_instructor(instructor)
                courses.remove(course)
                courses.append(course)
                # Commented code for JSON
                # edit_entry_json('Course', course)
            
            valid, errors = delete_instructor(instructor)
            # Commented code for JSON
            # valid, errors = delete_entry_json('Instructor', instructor)

            if valid:
                QMessageBox.information(self, "Success", f"Instructor {instructor.name} has been removed successfully!")
                self.edit_name_input.clear()
                self.edit_age_input.clear()
                self.edit_email_input.clear()
                instructors.remove(instructor)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))
        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def edit_instructor(self):
        """
        Updates an instructor in the db and updates local copy

        Validates the edit process and displays success or error messages
        using a QMessageBox.
        """
        try:
            new_name = self.edit_name_input.text()
            new_age = int(self.edit_age_input.text())
            new_email = self.edit_email_input.text()

            instructor_id = self.instructor_var
            instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)
            
            instructor.name = new_name
            instructor.age = new_age
            instructor._email = new_email

            valid, errors = edit_instructor(instructor)
            # Commented code for JSON
            # valid, errors = edit_entry_json('Instructor', instructor)

            if valid:
                QMessageBox.information(self, "Success", f"Instructor {instructor.name} edited successfully!")
                self.edit_name_input.clear()
                self.edit_age_input.clear()
                self.edit_email_input.clear()
                instructors.remove(instructor)
                instructors.append(instructor)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))
        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def on_select(self):
        """
        Updates the instructor_var attribute with the selected instructor_id and input labels
        """
        idx = self.instructor_dropdown.currentIndex()
        if idx != -1:
            selected = instructors[idx]
            self.instructor_var = selected.instructor_id
            self.edit_name_input.setText(selected.name)
            self.edit_email_input.setText(selected._email)
            self.edit_age_input.setText(str(selected.age))

    def update_ui(self):
        """
        Updated the UI for the instructor dropdown to relfect new data
        """
        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])