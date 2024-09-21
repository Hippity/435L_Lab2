from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from shared import courses, students, instructors

class AddCourseTab(QWidget):
    def __init__(self):
        """
        Initializes the AddCourseTab, setting up the attributes and initializing the UI.

        Attributes:
            course_dropdown (QComboBox): Dropdown of the list of courses from shared.py
            course_var (str): Selected course_id
            name_input (QLineEdit): Course Name Input
            course_id_input (QLineEdit): Course ID Input
            edit_name_input (QLineEdit): Edit Course Name input
        """
        super().__init__()
        self.course_dropdown : QComboBox = None
        self.course_var : str = None
        self.name_input : QLineEdit = None
        self.course_id_input : QLineEdit = None
        self.edit_name_input : QLineEdit = None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the AddCourseTab. Sets up the layout and adds all the components
        """
        # Grid Layout
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add Course Title
        add_course_title = QLabel("Add Course")
        add_course_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(add_course_title,0, 0 ,1 , 2)

        # Course Name Input Label
        name_label = QLabel("Course Name:")
        layout.addWidget(name_label,1, 0)

        # Course Name Input
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input,1, 1)

        # Course ID Input Label
        course_id_label = QLabel("Course ID:")
        layout.addWidget(course_id_label ,2, 0)

        # Course ID Input
        self.course_id_input = QLineEdit()
        layout.addWidget(self.course_id_input ,2, 1)

        # Add Couse Button
        submit_button = QPushButton("Add Course")
        submit_button.clicked.connect(self.create_course)
        layout.addWidget( submit_button ,3, 0,1 , 2)

        # Edit or Remove Course Title
        edit_course_title = QLabel("Edit or Remove Course")
        edit_course_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(edit_course_title ,4, 0,1, 2)

        # Course Dropdown Label
        course_dropdown_label = QLabel("Select Course:")
        layout.addWidget(course_dropdown_label ,5, 0)

        # Course Dropdown
        self.course_dropdown = QComboBox()
        self.course_dropdown.addItems([course.course_name for course in courses])
        self.course_dropdown.currentIndexChanged.connect(self.on_select)
        layout.addWidget(self.course_dropdown ,5, 1)

        # Edit Course Name Input Label
        edit_name_label = QLabel("Course Name:")
        layout.addWidget(edit_name_label ,6, 0)

        # Edit Course Name Input
        self.edit_name_input = QLineEdit()
        layout.addWidget(self.edit_name_input ,6, 1)

        # Edit Course Button
        edit_button = QPushButton("Edit Course")
        edit_button.clicked.connect(self.edit_course)
        layout.addWidget(edit_button ,7, 0,1 , 2)

        # Remove Course Button
        remove_button = QPushButton("Remove Course")
        remove_button.clicked.connect(self.delete_course)
        layout.addWidget(remove_button ,8, 0 ,1, 2)

        self.setLayout(layout)

    def create_course(self):
        """
        Adds a course to the db and updates local copy

        Validates the create process and displays success or error messages
        using a QMessageBox.
        """
        try:
            name = self.name_input.text()
            course_id = self.course_id_input.text()

            course = Course(course_id, name, "", [])

            valid, errors = add_course(course)
            # Commented Code for JSON 
            # valid, errors = add_entry_json('Course', course)

            if valid:
                QMessageBox.information(self, "Success", f"Course {course.course_name} created successfully!")
                self.name_input.clear()
                self.course_id_input.clear()
                courses.append(course)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))
        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def delete_course(self):
        """
        Deletes a course from the db and updates local copy

        Validates the delete process and displays success or error messages
        using a QMessageBox.
        """
        try:
            course_id = self.course_var
            course = next(course for course in courses if course.course_id == course_id)

            for student_id in course.enrolled_students:
                student = next(student for student in students if student.student_id == student_id)
                student.unregister_course(course)
                students.remove(student)
                students.append(student)
                # Commented Code for JSON
                # edit_entry_json('Student', student)


            if course.instructor_id:
                instructor = next(inst for inst in instructors if inst.instructor_id == course.instructor_id)
                instructor.unassign_course(course)
                instructors.remove(instructor)
                instructors.append(instructor)
                # Commented Code for JSON
                # edit_entry_json('Instructor', instructor)

            # Commented Code for JSON
            # valid, errors = delete_entry_json('Course', course)
            valid, errors = delete_course(course)

            if valid:
                QMessageBox.information(self, "Success", f"Course {course.course_name} has been removed successfully!")
                self.edit_name_input.clear()
                courses.remove(course)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))
        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def edit_course(self):
        """
        Updates a course in the db and updates local copy

        Validates the edit process and displays success or error messages
        using a QMessageBox.
        """
        try:
            course_id = self.course_var
            new_name = self.edit_name_input.text()

            course = next(course for course in courses if course.course_id == course_id)
            course.course_name = new_name

            # Commented Code for JSON 
            #valid, errors = edit_entry_json('Course', course)
            valid, errors = edit_course(course)

            if valid:
                QMessageBox.information(self, "Success", f"Course {course.course_name} has been edited successfully!")
                self.edit_name_input.clear()
                courses.remove(course)
                courses.append(course)
                self.update_ui()
            else:
                QMessageBox.warning(self, "Input Error", "\n".join(errors))
        except Exception as e:
            QMessageBox.warning(self, "Exception", str(e))

    def on_select(self):
        """
        Updates the course_var attribute with the selected course_id and input labels
        """
        idx = self.course_dropdown.currentIndex()
        if idx != -1:
            selected = courses[idx]
            self.course_var = selected.course_id
            self.edit_name_input.setText(selected.course_name)

    def update_ui(self):
        """
        Updated the UI for the course dropdown to relfect new data
        """
        self.course_dropdown.clear()
        self.course_dropdown.addItems([course.course_name for course in courses])
