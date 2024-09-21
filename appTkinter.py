from tkinterTabs.StudentTab import AddStudentTab
from tkinterTabs.InstructorTab import AddInstructorTab
from tkinterTabs.CourseTab import AddCourseTab
from tkinterTabs.AssignInstructor import AssignInstructorTab
from tkinterTabs.RegisterCourse import RegisterCourseTab
from tkinterTabs.ViewAll import ViewAllTab
import tkinter as tk
from tkinter import ttk

"""
This module sets up and launches a School Management System application using the Tkinter library.

It sets up a Tkinter Notebook and adds each tab to it.
of the main window.

"""

# Initialize the main application window
root = tk.Tk() 
root.title("School Management System")
root.geometry("800x600")

# Create a notebook to manage the tabs
notebook = ttk.Notebook(root)

# Initialize each tab and add it to the notebook with  titles
notebook.add(AddStudentTab(notebook), text="Add Student")
notebook.add(AddInstructorTab(notebook), text="Add Instructor")
notebook.add(AddCourseTab(notebook), text="Add Course")
notebook.add(AssignInstructorTab(notebook), text="Assign Instructor")
notebook.add(RegisterCourseTab(notebook), text="Register Course")
notebook.add(ViewAllTab(notebook), text="View All")

# Display the notebook in the main window
notebook.pack(expand=True, fill='both')

# Start the application's main event loop
root.mainloop()