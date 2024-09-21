import tkinter as tk
from tkinter import ttk
from tkinterTabs.StudentTab import AddStudentTab
from tkinterTabs.InstructorTab import AddInstructorTab
from tkinterTabs.CourseTab import AddCourseTab
from tkinterTabs.AssignInstructor import AssignInstructorTab
from tkinterTabs.RegisterCourse import RegisterCourseTab
from tkinterTabs.ViewAll import ViewAllTab

class SchoolManagementSystem:
    def __init__(self, root):
        """
        Initializes the SchoolManagementSystem class, setting up the main window and adding all tabs.

        Args:
            root (tk.Tk): The main application window.
        """
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("800x600")

        # Create a notebook to manage the tabs
        self.notebook = ttk.Notebook(self.root)

        # Initialize each tab and add it to the notebook with titles
        self.notebook.add(AddStudentTab(self.notebook), text="Add Student")
        self.notebook.add(AddInstructorTab(self.notebook), text="Add Instructor")
        self.notebook.add(AddCourseTab(self.notebook), text="Add Course")
        self.notebook.add(AssignInstructorTab(self.notebook), text="Assign Instructor")
        self.notebook.add(RegisterCourseTab(self.notebook), text="Register Course")
        self.notebook.add(ViewAllTab(self.notebook), text="View All")

        # Display the notebook in the main window
        self.notebook.pack(expand=True, fill='both')

    def run(self):
        """
        Starts the main event loop for the Tkinter application.
        """
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    
    app = SchoolManagementSystem(root)
    
    app.run()
