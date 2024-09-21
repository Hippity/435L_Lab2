from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QFileDialog
import csv
from classes.Student import *
from crud.jsonCRUD import *
from crud.databaseCRUD import *
import shared
from shared import courses,instructors,students
import importlib

class ViewAllTab(QWidget):
    def __init__(self):
        """
        Initializes the ViewAllTab, setting up the attributes and initializing the UI.

        Attributes:
            table_widget (QTableWidget): Table widget used to display the data
            table (str): Currently selected table
            courses (list): List of courses from shared.py
            instructors (list): List of instructors from shared.py
            students (list): List of students from shared.py
            students_data (list): List of students in a format that is compatible with table widget
            instructors_data (list): List of instructors in a format that is compatible with table widget
            courses_data (list): List of courses in a format that is compatible with table widget
            search_var (str): Variable used to filter the data
        """
        super().__init__()
        self.table_widget : QTableWidget = None
        self.table : str = 'Student'
        self.courses : list = courses
        self.instructors : list = instructors
        self.students : list = students
        self.students_data : list = []
        self.instructors_data : list = []
        self.courses_data : list = []
        self.search_var : str = ''

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the ViewAllTab. Sets up the layout and adds all the components
        """
        # Vertical Layout
        layout = QVBoxLayout()

        # View All Title
        view_all_title = QLabel("View All")
        view_all_title.setStyleSheet("font-size: 28px;")
        layout.addWidget(view_all_title)

        # Search Input
        self.search_var = QLineEdit()
        self.search_var.setPlaceholderText("Search...")
        self.search_var.textChanged.connect(self.search_data)
        layout.addWidget(self.search_var)

        # Table Widget
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Horizontal Box for Buttons
        button_layout = QHBoxLayout()

        # View Courses Button
        courses_button = QPushButton("View Courses")
        courses_button.clicked.connect(self.show_courses)
        button_layout.addWidget(courses_button)

        # View Students Button
        students_button = QPushButton("View Students")
        students_button.clicked.connect(self.show_students)
        button_layout.addWidget(students_button)

        # View Instructors Button
        instructors_button = QPushButton("View Instructors")
        instructors_button.clicked.connect(self.show_instructors)
        button_layout.addWidget(instructors_button)
        layout.addLayout(button_layout)

        # Horizontal Box for Buttons
        button_layout2 = QHBoxLayout()
 
        # Refresh Data Button
        refresh_button = QPushButton("Refresh Data")
        refresh_button.clicked.connect(self.refresh_data_tree)
        button_layout2.addWidget(refresh_button)

        # Export CSV Button
        export_button = QPushButton("Export CSV")
        export_button.clicked.connect(self.export_csv)
        button_layout2.addWidget(export_button)
        layout.addLayout(button_layout2)

        self.setLayout(layout)

        # Fix data to be compatible with table widget
        self.students_data = self.fix_student_data()
        self.instructors_data = self.fix_instructor_data()
        self.courses_data = self.fix_course_data()

    def update_table_headers(self, headers):
        """
        Updates the headers of the table widget

        Args:
            headers (list): List of headers to set in the table widget.
        """
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setRowCount(0)

    def update_table_data(self, data):
        """
        Updates the table widget data

        Args:
            data (list): List of row data to display in the table widget.
        """
        self.table_widget.setRowCount(0)
        for row_data in data:
            row_number = self.table_widget.rowCount()
            self.table_widget.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(cell_data)))

    def show_courses(self):
        """
        Displays the course data in the table widget with appropriate headers.
        """
        self.table = 'Course'
        headers = ["Course ID", "Course Name", "Instructor", "Enrolled Students"]
        self.update_table_headers(headers)
        self.update_table_data(self.courses_data)

    def show_students(self):
        """
        Displays the student data in the table widget with appropriate headers.
        """
        self.table = 'Student'
        headers = ["Student ID", "Student Name", "Student Age", "Student Email", "Registered Courses"]
        self.update_table_headers(headers)
        self.update_table_data(self.students_data)

    def show_instructors(self):
        """
        Displays the instructor data in the table widget with appropriate headers.
        """
        self.table = 'Instructor'
        headers = ["Instructor ID", "Instructor Name", "Instructor Age", "Instructor Email", "Assigned Courses"]
        self.update_table_headers(headers)
        self.update_table_data(self.instructors_data)

    def search_data(self):
        """
        Filters the data in the current table based on the search query entered by the user.
        """
        query = self.search_var.text().lower()
        if self.table == 'Course':
            filtered_data = [row for row in self.courses_data if query in str(row).lower()]
        elif self.table == 'Student':
            filtered_data = [row for row in self.students_data if query in str(row).lower()]
        elif self.table == 'Instructor':
            filtered_data = [row for row in self.instructors_data if query in str(row).lower()]
        self.update_table_data(filtered_data)

    def export_csv(self):
        """
        Exports the current table data to a CSV file.
        """
        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
        data = []
        for row in range(self.table_widget.rowCount()):
            row_data = [self.table_widget.item(row, column).text() for column in range(self.table_widget.columnCount())]
            data.append(row_data)

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  
                writer.writerows(data)
            QMessageBox.information(self, "Export Successful", f"Data exported successfully to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"An error occurred while exporting: {e}")

    def refresh_data_tree(self):
        """
        Reloads the data from the shared.py and refreshes the table data.
        """
        importlib.reload(shared)

        self.students = students
        self.instructors = instructors
        self.courses = courses

        self.students_data = self.fix_student_data()
        self.instructors_data = self.fix_instructor_data()
        self.courses_data = self.fix_course_data()

        if self.table == 'Student':
            self.update_table_data(self.students_data)
        elif self.table == 'Course':
            self.update_table_data(self.courses_data)
        elif self.table == 'Instructor':
            self.update_table_data(self.instructors_data)

    def fix_student_data(self):
        """
        Formats the student data to be compatible with the table widget.

        Returns:
            list: A list of tuples containing formatted student data.
        """
        rows = []
        for student in self.students:
            student_id = student.student_id
            name = student.name
            age = student.age
            email = student._email
            registered_courses = student.registered_courses
            course_names = [
                next(course.course_name for course in self.courses if course.course_id == course_id) 
                for course_id in registered_courses
            ] if registered_courses else ['No Courses']
            
            rows.append((student_id, name, age, email, ", ".join(course_names)))
        return rows

    def fix_instructor_data(self):
        """
        Formats the instructor data to be compatible with the table widget.

        Returns:
            list: A list of tuples containing formatted instructor data.
        """
        rows = []
        for instructor in self.instructors:
            instructor_id = instructor.instructor_id
            name = instructor.name
            age = instructor.age
            email = instructor._email
            assigned_courses = instructor.assigned_courses
            course_names = [
                next(course.course_name for course in self.courses if course.course_id == course_id)
                for course_id in assigned_courses
            ] if assigned_courses else ['No Courses']
        
            rows.append((instructor_id, name, age, email, ", ".join(course_names)))
        return rows

    def fix_course_data(self):
        """
        Formats the course data to be compatible with the table widget.

        Returns:
            list: A list of tuples containing formatted course data.
        """
        rows = []
        for course in self.courses:
            course_id = course.course_id
            course_name = course.course_name
            instructor_id = course.instructor_id
            instructor_name = next((instructor.name for instructor in self.instructors if instructor.instructor_id == instructor_id), 'No Instructor') if instructor_id else 'No Instructor'
            enrolled_students = course.enrolled_students
            student_names = [
                next(student.name for student in self.students if student.student_id == student_id)
                for student_id in enrolled_students
            ] if enrolled_students else ['No Students']

            rows.append((course_id, course_name, instructor_name, ", ".join(student_names)))
        return rows