from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from shared import courses, instructors

class AssignInstructorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.course_dropdown = None
        self.instructor_dropdown = None
        self.course_var = None
        self.instructor_var = None

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel("Assign Instructor")
        title_label.setStyleSheet("font-size: 28px;")
        layout.addWidget(title_label ,0, 0 ,1 , 2)

        course_label = QLabel("Select Course:")
        layout.addWidget(course_label ,1, 0 )

        self.course_dropdown = QComboBox()
        self.course_dropdown.addItems([course.course_name for course in courses])
        self.course_dropdown.currentIndexChanged.connect(self.on_course_select)
        layout.addWidget(self.course_dropdown ,1, 1 )

        instructor_label = QLabel("Select Instructor:")
        layout.addWidget(instructor_label ,2, 0 )

        self.instructor_dropdown = QComboBox()
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])
        self.instructor_dropdown.currentIndexChanged.connect(self.on_instructor_select)
        layout.addWidget(self.instructor_dropdown,2, 1 )

        assign_button = QPushButton("Assign Course")
        assign_button.clicked.connect(lambda: self.assign_instructor())
        layout.addWidget(assign_button,3, 0,1,2 )

        unassign_button = QPushButton("Unassign Course")
        unassign_button.clicked.connect(lambda: self.unassign_instructor())
        layout.addWidget(unassign_button,4, 0,1,2 )

        refresh_button = QPushButton("Refresh Data")
        refresh_button.clicked.connect(self.update_ui)
        layout.addWidget(refresh_button,5, 0 ,1,2)

        self.setLayout(layout)

    def on_course_select(self):
        idx = self.course_dropdown.currentIndex()
        if idx != -1:
            selected = courses[idx]
            self.course_var = selected.course_id

    def on_instructor_select(self):
        idx = self.instructor_dropdown.currentIndex()
        if idx != -1:
            selected = instructors[idx]
            self.instructor_var = selected.instructor_id

    def assign_instructor(self):
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

    def update_ui(self):
        self.course_dropdown.clear()
        self.course_dropdown.addItems([course.course_name for course in courses])

        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])
