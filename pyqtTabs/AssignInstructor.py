from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from classes.Course import *
from crud.jsonCRUD import *
from crud.databaseCRUD import *
from shared import courses, instructors

class AssignInstructorTab(QWidget):
    def __init__(self):
        """
        Initializes the AssignInstructorTab, setting up the attributes and initializing the UI.

        Attributes:
            course_dropdown (QComboBox): Dropdown of the list of courses from shared.py
            instructor_dropdown (QComboBox): Dropdown of the list of instructors from shared.py
            course_var (str): Selected course_id
            instructor_var (str): Selected instructor_id
        """
        super().__init__()
        self.course_dropdown : QComboBox = None
        self.instructor_dropdown : QComboBox = None
        self.course_var : str = None
        self.instructor_var : str = None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the AssignInstructorTab. Sets up the layout and adds all the components
        """
        # Grid Layout
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Assign Instructor Title
        title_label = QLabel("Assign Instructor")
        title_label.setStyleSheet("font-size: 28px;")
        layout.addWidget(title_label ,0, 0 ,1 , 2)

        # Course Dropdown Label
        course_label = QLabel("Select Course:")
        layout.addWidget(course_label ,1, 0 )

        # Select Course Dropdown
        self.course_dropdown = QComboBox()
        self.course_dropdown.addItems([course.course_name for course in courses])
        self.course_dropdown.currentIndexChanged.connect(self.on_course_select)
        layout.addWidget(self.course_dropdown ,1, 1 )

        # Instructor Dropdown Label
        instructor_label = QLabel("Select Instructor:")
        layout.addWidget(instructor_label ,2, 0 )

        # Select Instructor Dropdown
        self.instructor_dropdown = QComboBox()
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])
        self.instructor_dropdown.currentIndexChanged.connect(self.on_instructor_select)
        layout.addWidget(self.instructor_dropdown,2, 1 )

        # Assign Course Button
        assign_button = QPushButton("Assign Course")
        assign_button.clicked.connect(lambda: self.assign_instructor())
        layout.addWidget(assign_button,3, 0,1,2 )

        # Unassign Course Button
        unassign_button = QPushButton("Unassign Course")
        unassign_button.clicked.connect(lambda: self.unassign_instructor())
        layout.addWidget(unassign_button,4, 0,1,2 )

        # Refresh Data Button
        refresh_button = QPushButton("Refresh Data")
        refresh_button.clicked.connect(self.update_ui)
        layout.addWidget(refresh_button,5, 0 ,1,2)

        self.setLayout(layout)

    def assign_instructor(self):
        """
        Assigns an instructor to a course and updates the local copy

        Validates the assignment process and displays success or error messages
        using a QMessageBox.
        """
        course_id = self.course_var
        instructor_id = self.instructor_var

        course = next(course for course in courses if course.course_id == course_id)
        instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)

        valid1, errors1 = instructor.assign_course(course)
        valid2, errors2 = course.assign_instructor(instructor)

        if not valid1 and not valid2:
            QMessageBox.warning(self, "Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
            return
        elif not valid1:
            QMessageBox.warning(self, "Input Error", "\n".join(errors1))
            return
        elif not valid2:
            QMessageBox.warning(self, "Input Error", "\n".join(errors2))
            return
        
        valid, errors = assign_instructor(instructor,course)

        if valid:
            QMessageBox.information(self, "Success", f"{instructor.name} assigned to {course.course_name}!")
        else:
            QMessageBox.warning(self, "Input Error", "\n".join(errors))

        # Commented code that works for JSON files

        # valid1, errors1 = edit_entry_json('Course', course)
        # valid2, errors2 = edit_entry_json('Instructor', instructor)

        # if valid1 and valid2:
        #     QMessageBox.information(self, "Success", f"{instructor.name} assigned to {course.course_name}!")
        # elif not valid1 and not valid2:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
        # elif not valid1:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors1))
        # elif not valid2:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors2))

    def unassign_instructor(self):
        """
        Unassigns an instructor to a course and updates the local copy

        Validates the unassignment process and displays success or error messages
        using a QMessageBox.
        """
        course_id = self.course_var
        instructor_id = self.instructor_var

        course = next(course for course in courses if course.course_id == course_id)
        instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)

        valid1, errors1 = instructor.unassign_course(course)
        valid2, errors2 = course.unassign_instructor(instructor)

        if not valid1 and not valid2:
            QMessageBox.warning(self, "Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
            return
        elif not valid1:
            QMessageBox.warning(self, "Input Error", "\n".join(errors1))
            return
        elif not valid2:
            QMessageBox.warning(self, "Input Error", "\n".join(errors2))
            return
        
        valid, errors = unassign_instructor(instructor,course)

        if valid:
            QMessageBox.information(self, "Success", f"{instructor.name} assigned to {course.course_name}!")
        else:
            QMessageBox.warning(self, "Input Error", "\n".join(errors))

        # Commented code that works for JSON files

        # valid1, errors1 = edit_entry_json('Course', course)
        # valid2, errors2 = edit_entry_json('Instructor', instructor)

        # if valid1 and valid2:
        #     QMessageBox.information(self, "Success", f"{instructor.name} unassigned from {course.course_name}!")
        # elif not valid1 and not valid2:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
        # elif not valid1:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors1))
        # elif not valid2:
        #     QMessageBox.warning(self, "Input Error", "\n".join(errors2))

    def on_course_select(self):
        """
        Updates the course_var attribute with the selected course_id
        """
        idx = self.course_dropdown.currentIndex()
        if idx != -1:
            selected = courses[idx]
            self.course_var = selected.course_id

    def on_instructor_select(self):
        """
        Updates the instructor_var attribute with the selected instructor_id
        """
        idx = self.instructor_dropdown.currentIndex()
        if idx != -1:
            selected = instructors[idx]
            self.instructor_var = selected.instructor_id

    def update_ui(self):
        """
        Updates the UI for the course and instructor dropdown to reflect new data
        """
        self.course_dropdown.clear()
        self.course_dropdown.addItems([course.course_name for course in courses])
        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])