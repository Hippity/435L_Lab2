from tkinterTabs.StudentTab import StudentTab
from tkinterTabs.InstructorTab import InstructorTab
from tkinterTabs.CourseTab import CourseTab
from tkinterTabs.AssignInstructor import AssignInstructorTab
from tkinterTabs.RegisterCourse import RegisterCourseTab
from tkinterTabs.ViewAll import ViewAllTab
import tkinter as tk
from tkinter import ttk

root = tk.Tk() 
root.title("School Management System")
root.geometry("800x600")

notebook = ttk.Notebook(root)

add_student_tab = StudentTab(notebook)
add_instructor_tab = InstructorTab(notebook)
add_course_tab = CourseTab(notebook)
assign_instructor_tab = AssignInstructorTab(notebook)
register_course_tab = RegisterCourseTab(notebook)
view_all_tab = ViewAllTab(notebook)

notebook.add(add_student_tab, text="Add Student")
notebook.add(add_instructor_tab, text="Add Instructor")
notebook.add(add_course_tab, text="Add Course")
notebook.add(assign_instructor_tab, text="Assign Instructor")
notebook.add(register_course_tab, text="Register Course")
notebook.add(view_all_tab, text="View All")

notebook.pack(expand=True, fill='both')

root.mainloop()
