import tkinter as tk
from tkinter import ttk, messagebox
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from shared import courses, students

class RegisterCourseTab(tk.Frame):
    def __init__(self, parent):
        """
        Initializes the RegisterCourseTab, setting up the attributes and initializing the UI.

        Attributes:
            course_dropdown (ttk.Combobox): Dropdown of the list of courses from shared.py
            student_dropdown (ttk.Combobox): Dropdown of the list of students from shared.py
            course_var (tk.StringVar): Selected course_id
            student_var (tk.StringVar): Selected student_id
        """
        super().__init__(parent)
        self.course_dropdown : ttk.Combobox = None
        self.student_dropdown : ttk.Combobox = None
        self.course_var : tk.StringVar = tk.StringVar()
        self.student_var : tk.StringVar = tk.StringVar()

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the RegisterCourseTab. Sets up the layout and adds all the components
        """
        # Register Course Title
        tk.Label(self, text="Register Course", font=("Arial", 28)).grid(row=0, column=0, columnspan=2, pady=10)

        # Course Dropdown Label
        tk.Label(self, text="Select Course: ").grid(row=1, column=0, padx=0, pady=5)
        # Course Dropdown
        self.course_dropdown = ttk.Combobox(self, values=[course.course_name for course in courses], state='readonly')
        self.course_dropdown.grid(row=1, column=1, padx=0, pady=5)
        self.course_dropdown.bind("<<ComboboxSelected>>", self.on_course_select)

        # Student Dropdown Label
        tk.Label(self, text="Select Student: ").grid(row=2, column=0, padx=0, pady=5)
        # Student Label
        self.student_dropdown = ttk.Combobox(self, values=[student.name for student in students], state='readonly')
        self.student_dropdown.grid(row=2, column=1, padx=0, pady=5)
        self.student_dropdown.bind("<<ComboboxSelected>>", self.on_student_select)

        # Register Course Button
        register_button = tk.Button(self, text="Register Course", command=self.assign_student)
        register_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Unregister Course Button
        unregister_button = tk.Button(self, text="Unregister Course", command=self.unassign_student)
        unregister_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Refresh Data Button
        refresh_button = tk.Button(self, text="Refresh Data", command=self.update_ui)
        refresh_button.grid(row=7, column=0, columnspan=2, pady=10)

    def assign_student(self):
        """
        Registers a student to a course in the db and updates the local copy

        Validates the registration process and displays success or error messages
        using a messageBox.
        """
        try:
            course_id = self.course_var.get()
            student_id = self.student_var.get()

            course : Course = next(course for course in courses if course.course_id == course_id)
            student : Student = next(student for student in students if student.student_id == student_id)

            valid1, errors1 = student.register_course(course)
            valid2, errors2 = course.enroll_student(student)

            if not valid1 and not valid2:
                messagebox.showwarning("Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
                return
            elif not valid1:
                messagebox.showwarning("Input Error", "\n".join(errors1))
                return
            elif not valid2:
                messagebox.showwarning("Input Error", "\n".join(errors2))
                return
            
            valid, errors = register_course(student,course)
            if valid:
                messagebox.showinfo("Success", f"{student.name} assigned to {course.course_name}!")
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))

            # valid1, errors1 = edit_entry_json('Course', course)
            # valid2, errors2 = edit_entry_json('Student', student)

            # if valid1 and valid2:
            #     messagebox.showinfo("Success", f"{student.name} assigned to {course.course_name}!")
            # elif not valid1 and not valid2:
            #     messagebox.showwarning("Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
            # elif not valid1:
            #     messagebox.showwarning("Input Error", "\n".join(errors1))
            # elif not valid2:
            #     messagebox.showwarning("Input Error", "\n".join(errors2))

        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def unassign_student(self):
        """
        Unregisters a student to a course in the db and updates the local copy

        Validates the unregistration process and displays success or error messages
        using a messageBox.
        """
        try:
            course_id = self.course_var.get()
            student_id = self.student_var.get()

            course : Course = next(course for course in courses if course.course_id == course_id)
            student : Student = next(student for student in students if student.student_id == student_id)

            valid1, errors1 = student.unregister_course(course)
            valid2, errors2 = course.unenroll_student(student)

            if not valid1 and not valid2:
                messagebox.showwarning("Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
                return
            elif not valid1:
                messagebox.showwarning("Input Error", "\n".join(errors1))
                return
            elif not valid2:
                messagebox.showwarning("Input Error", "\n".join(errors2))
                return
            
            valid, errors = unregister_course(student,course)
            if valid:
                messagebox.showinfo("Success", f"{student.name} unassigned from {course.course_name}!")
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))

            # valid1, errors1 = edit_entry_json('Course', course)
            # valid2, errors2 = edit_entry_json('Student', student)

            # if valid1 and valid2:
            #     messagebox.showinfo("Success", f"{student.name} unassigned from {course.course_name}!")
            # elif not valid1 and not valid2:
            #     messagebox.showwarning("Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
            # elif not valid1:
            #     messagebox.showwarning("Input Error", "\n".join(errors1))
            # elif not valid2:
            #     messagebox.showwarning("Input Error", "\n".join(errors2))

        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def on_course_select(self, event):
        """
        Updates the course_var attribute with the selected course_id
        """
        idx = self.course_dropdown.current()
        if idx != -1:
            selected = courses[idx]
            self.course_var.set(selected.course_id)

    def on_student_select(self, event):
        """
        Updates the student_var attribute with the selected student_id
        """
        idx = self.student_dropdown.current()
        if idx != -1:
            selected = students[idx]
            self.student_var.set(selected.student_id)
            
    def update_ui(self):
        """
         Updates the UI for the course and student dropdown to reflect the new data
        """
        self.course_dropdown['values'] = [course.course_name for course in courses]
        self.student_dropdown['values'] = [student.name for student in students]