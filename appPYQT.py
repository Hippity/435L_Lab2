import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QMainWindow
from pyqtTabs.InstructorTab import AddInstructorTab
from pyqtTabs.StudentTab import AddStudentTab
from pyqtTabs.ViewAll import ViewAllTab
from pyqtTabs.CourseTab import AddCourseTab
from pyqtTabs.AssignInstructor import AssignInstructorTab
from pyqtTabs.RegisterCourse import RegisterCourseTab

class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        """
        Initializes the SchoolManagementSystem window with multiple tabs for different functionalities.

        It sets up a QTabWidget and adds each tab to it, then sets this widget as the central widget
        of the main window.
        """
        super().__init__()
        self.setWindowTitle("School Management System")

        tabs = QTabWidget()
        tabs.addTab(AddStudentTab(), "Add Student")
        tabs.addTab(AddInstructorTab(), "Add Instructor")
        tabs.addTab(AddCourseTab(), "Add Course")
        tabs.addTab(AssignInstructorTab(), "Assign Instructor")
        tabs.addTab(RegisterCourseTab(), "Register Course")
        tabs.addTab(ViewAllTab(), "View All")

        self.setCentralWidget(tabs)

def main():
    """
    Initializes the QApplication, creates an instance of the SchoolManagementSystem window,
    displays it, and starts the event loop.
    """
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()