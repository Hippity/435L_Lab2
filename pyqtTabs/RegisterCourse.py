from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QMessageBox
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from PyQt5.QtCore import Qt
from shared import courses, students

class RegisterCourseTab(QWidget):
    def __init__(self):
        """
        Initializes the RegisterCourseTab, setting up the attributes and initializing the UI.

        Attributes:
            course_dropdown (QComboBox): Dropdown of the list of courses from shared.py
            student_dropdown (QComboBox): Dropdown of the list of students from shared.py
            course_var (str): Selected course_id
            student_var (str): Selected student_id
        """
        super().__init__()
        self.course_dropdown : QComboBox = None
        self.student_dropdown : QComboBox = None
        self.course_var : str = None
        self.student_var : str = None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the RegisterCourseTab. Sets up the layout and adds all the components
        """
        # Grid Layout
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Register Course Title
        register_course_title = QLabel("Register Course")
        register_course_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(register_course_title,0,0,1,2)

        # Course Dropdown Label
        course_label = QLabel("Select Course:")
        layout.addWidget(course_label,1,0)

        # Select Course Dropdown
        self.course_dropdown = QComboBox()
        self.course_dropdown.addItems([course.course_name for course in courses])
        self.course_dropdown.currentIndexChanged.connect(self.on_course_select)
        layout.addWidget(self.course_dropdown,1,1)

        # Student Dropdown Label
        student_label = QLabel("Select Student:")
        layout.addWidget(student_label,2,0)

        # Select Student Dropdown
        self.student_dropdown = QComboBox()
        self.student_dropdown.addItems([student.name for student in students])
        self.student_dropdown.currentIndexChanged.connect(self.on_student_select)
        layout.addWidget(self.student_dropdown,2,1)

        # Register Course Button
        register_button = QPushButton("Register Course")
        register_button.clicked.connect(self.assign_student)
        layout.addWidget(register_button,3,0,1,2)

        # Unregister Course Button
        unregister_button = QPushButton("Unregister Course")
        unregister_button.clicked.connect(self.unassign_student)
        layout.addWidget(unregister_button,4,0,1,2)

        # Refresh Data Button
        refresh_button = QPushButton("Refresh Data")
        refresh_button.clicked.connect(self.update_ui)
        layout.addWidget(refresh_button,5,0,1,2)

        self.setLayout(layout)

    def assign_student(self):
        """
        Registers a student to a course in the db and updates the local copy

        Validates the registration process and displays success or error messages
        using a QMessageBox.
        """
        course_id = self.course_var
        student_id = self.student_var

        course = next(course for course in courses if course.course_id == course_id)
        student = next(student for student in students if student.student_id == student_id)

        valid1, errors1 = student.register_course(course)
        valid2, errors2 = course.enroll_student(student)

        if not valid1 and not valid2:
            QMessageBox.warning(self, "Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
            return
        elif not valid1:
            QMessageBox.warning(self, "Input Error", "\n".join(errors1))
            return
        elif not valid2:
            QMessageBox.warning(self, "Input Error", "\n".join(errors2))
            return
        
        valid, errors = register_course(student,course)

        if valid:
            QMessageBox.information(self, "Success", f"{student.name} assigned to {course.course_name}!")
        else:
            QMessageBox.warning(self, "Input Error", "\n".join(errors))
        
        # Commented code for JSON
        # valid1, errors1 = edit_entry_json('Course', course)
        # valid2, errors2 = edit_entry_json('Student', student)

        # if valid1 and valid2:
        #     QMessageBox.information(self, "Success", f"{student.name} assigned to {course.course_name}!")
        # elif not valid1 and not valid2:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
        #     return
        # elif not valid1:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors1))
        #     return
        # elif not valid2:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors2))
        #     return

    def unassign_student(self):
        """
        Unregisters a student to a course in the db and updates the local copy

        Validates the unregistration process and displays success or error messages
        using a QMessageBox.
        """
        course_id = self.course_var
        student_id = self.student_var

        course = next(course for course in courses if course.course_id == course_id)
        student = next(student for student in students if student.student_id == student_id)

        valid1, errors1 = student.unregister_course(course)
        valid2, errors2 = course.unenroll_student(student)

        if not valid1 and not valid2:
            QMessageBox.warning(self, "Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
            return
        elif not valid1:
            QMessageBox.warning(self, "Input Error", "\n".join(errors1))
            return
        elif not valid2:
            QMessageBox.warning(self, "Input Error", "\n".join(errors2))
            return
        
        valid, errors = unregister_course(student,course)

        if valid:
            QMessageBox.information(self, "Success", f"{student.name} unassigned to {course.course_name}!")
        else:
            QMessageBox.warning(self, "Input Error", "\n".join(errors))
        
        # Commented code for JSON
        # valid1, errors1 = edit_entry_json('Course', course)
        # valid2, errors2 = edit_entry_json('Student', student)

        # if valid1 and valid2:
        #     QMessageBox.information(self, "Success", f"{student.name} unassigned from {course.course_name}!")
        # elif not valid1 and not valid2:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
        #     return
        # elif not valid1:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors1))
        #     return
        # elif not valid2:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors2))
        #     return

    def on_course_select(self):
        """
        Updates the course_var attribute with the selected course_id
        """
        idx = self.course_dropdown.currentIndex()
        if idx != -1:
            selected = courses[idx]
            self.course_var = selected.course_id

    def on_student_select(self):
        """
        Updates the student_var attribute with the selected student_id
        """
        idx = self.student_dropdown.currentIndex()
        if idx != -1:
            selected = students[idx]
            self.student_var = selected.student_id

    def update_ui(self):
        """
         Updates the UI for the course and student dropdown to reflect the new data
        """
        self.course_dropdown.clear()
        self.course_dropdown.addItems([course.course_name for course in courses])
        self.student_dropdown.clear()
        self.student_dropdown.addItems([student.name for student in students])