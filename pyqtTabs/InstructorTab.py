from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from classes.Course import *
from PyQt5.QtCore import Qt
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from shared import instructors, courses

class AddInstructorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.instructor_dropdown = None
        self.instructor_var = None
        self.age_var = None
        self.email_var = None
        self.name_var = None

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        add_instructor_title = QLabel("Add Instructor")
        add_instructor_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(add_instructor_title,0,0,1,2)

        name_label = QLabel("Name:")
        layout.addWidget(name_label ,1,0)

        self.name_input = QLineEdit()
        layout.addWidget(self.name_input, 1,1)

        age_label = QLabel("Age:")
        layout.addWidget(age_label, 2,0)

        self.age_input = QLineEdit()
        layout.addWidget(self.age_input, 2,1)

        email_label = QLabel("Email:")
        layout.addWidget(email_label, 3,0)

        self.email_input = QLineEdit()
        layout.addWidget(self.email_input, 3,1)

        instructor_id_label = QLabel("Instructor ID:")
        layout.addWidget(instructor_id_label, 4,0)

        self.instructor_id_input = QLineEdit()
        layout.addWidget(self.instructor_id_input, 4,1)

        submit_button = QPushButton("Add Instructor")
        submit_button.clicked.connect(self.create_instructor)
        layout.addWidget(submit_button, 5,0,1,2)

        edit_instructor_title = QLabel("Edit or Remove Instructor")
        edit_instructor_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(edit_instructor_title, 6,0,1,2)

        instructor_dropdown_label = QLabel("Select Instructor:")
        layout.addWidget(instructor_dropdown_label, 7,0)

        self.instructor_dropdown = QComboBox()
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])
        self.instructor_dropdown.currentIndexChanged.connect(self.on_select)
        layout.addWidget(self.instructor_dropdown, 7,1)

        edit_name_label = QLabel("Name:")
        layout.addWidget(edit_name_label ,8,0)

        self.edit_name_input = QLineEdit()
        layout.addWidget(self.edit_name_input,8,1)

        edit_age_label = QLabel("Age:")
        layout.addWidget(edit_age_label,9,0)

        self.edit_age_input = QLineEdit()
        layout.addWidget(self.edit_age_input,9,1)

        edit_email_label = QLabel("Email:")
        layout.addWidget(edit_email_label,10,0)

        self.edit_email_input = QLineEdit()
        layout.addWidget(self.edit_email_input,10,1)

        edit_button = QPushButton("Edit Instructor")
        edit_button.clicked.connect(self.edit_instructor)
        layout.addWidget(edit_button,11,0,1,2)

        remove_button = QPushButton("Remove Instructor")
        remove_button.clicked.connect(self.delete_instructor)
        layout.addWidget(remove_button,12,0,1,2)

        self.setLayout(layout)

    def create_instructor(self):
        try:
            name = self.name_input.text()
            age = int(self.age_input.text())
            email = self.email_input.text()
            instructor_id = self.instructor_id_input.text()

            instructor = Instructor(name, age, email, instructor_id, [])
            
            #valid, errors = add_entry_json('Instructor', instructor)
            valid, errors = add_instructor(instructor)

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
        try:
            instructor_id = self.instructor_var
            instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)
            
            for course_id in instructor.assigned_courses:
                course = next(course for course in courses if course.course_id == course_id)
                course.unassign_instructor(instructor)
                #edit_entry_json('Course', course)
                courses.remove(course)
                courses.append(course)
            
            #valid, errors = delete_entry_json('Instructor', instructor)
            valid, errors = delete_instructor(instructor)

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
        try:
            new_name = self.edit_name_input.text()
            new_age = int(self.edit_age_input.text())
            new_email = self.edit_email_input.text()

            instructor_id = self.instructor_var
            instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)
            
            instructor.name = new_name
            instructor.age = new_age
            instructor._email = new_email

            #valid, errors = edit_entry_json('Instructor', instructor)
            valid, errors = edit_instructor(instructor)

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

    def update_ui(self):
        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])

    def on_select(self):
        idx = self.instructor_dropdown.currentIndex()
        if idx != -1:
            selected = instructors[idx]
            self.instructor_var = selected.instructor_id
            self.edit_name_input.setText(selected.name)
            self.edit_email_input.setText(selected._email)
            self.edit_age_input.setText(str(selected.age))
