import tkinter as tk
from tkinter import ttk, messagebox
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from shared import courses, instructors

class AssignInstructorTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.course_dropdown : ttk.Combobox = None
        self.instructor_dropdown : ttk.Combobox = None
        self.course_var : tk.StringVar = tk.StringVar()
        self.instructor_var : tk.StringVar = tk.StringVar()

        self.init_ui()

    def init_ui(self):
        tk.Label(self, text="Assign Instructor", font=("Arial", 28)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Select Course: ").grid(row=1, column=0, padx=0, pady=5)
        self.course_dropdown = ttk.Combobox(self, values=[course.course_name for course in courses], state='readonly')
        self.course_dropdown.grid(row=1, column=1, padx=0, pady=5)
        self.course_dropdown.bind("<<ComboboxSelected>>", self.on_course_select)

        tk.Label(self, text="Select Instructor: ").grid(row=2, column=0, padx=0, pady=5)
        self.instructor_dropdown = ttk.Combobox(self, values=[instructor.name for instructor in instructors], state='readonly')
        self.instructor_dropdown.grid(row=2, column=1, padx=0, pady=5)
        self.instructor_dropdown.bind("<<ComboboxSelected>>", self.on_instructor_select)

        assign_button = tk.Button(self, text="Assign Course", command=self.assign_instructor)
        assign_button.grid(row=5, column=0, columnspan=2, pady=10)

        unassign_button = tk.Button(self, text="Unassign Course", command=self.unassign_instructor)
        unassign_button.grid(row=6, column=0, columnspan=2, pady=10)

        refresh_button = tk.Button(self, text="Refresh Data", command=self.update_ui)
        refresh_button.grid(row=7, column=0, columnspan=2, pady=10)

    def assign_instructor(self):
        course_id = self.course_var.get()
        instructor_id = self.instructor_var.get()

        course : Course = next(course for course in courses if course.course_id == course_id)
        instructor : Instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)

        valid1, errors1 = instructor.assign_course(course)
        valid2, errors2 = course.assign_instructor(instructor)

        if not valid1 and not valid2:
            messagebox.showwarning("Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
            return
        elif not valid1:
            messagebox.showwarning("Input Error", "\n".join(errors1))
            return
        elif not valid2:
            messagebox.showwarning("Input Error", "\n".join(errors2))
            return
        
        valid, errors = assign_instructor(instructor,course)
        if valid:
            messagebox.showinfo("Success", f"{instructor.name} assigned to {course.course_name}!")
        else:
            messagebox.showwarning("Input Error", "\n".join(errors))

        # valid1, errors1 = edit_entry_json('Course', course)
        # valid2, errors2 = edit_entry_json('Instructor', instructor)

        # if valid1 and valid2:
        #     messagebox.showinfo("Success", f"{instructor.name} assigned to {course.course_name}!")
        # elif not valid1 and not valid2:
        #     messagebox.showwarning("Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
        # elif not valid1:
        #     messagebox.showwarning("Input Error", "\n".join(errors1))
        # elif not valid2:
        #     messagebox.showwarning("Input Error", "\n".join(errors2))

    def unassign_instructor(self):
        course_id = self.course_var.get()
        instructor_id = self.instructor_var.get()

        course : Course = next(course for course in courses if course.course_id == course_id)
        instructor : Instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)

        valid1, errors1 = instructor.unassign_course(course)
        valid2, errors2 = course.unassign_instructor(instructor)

        if not valid1 and not valid2:
            messagebox.showwarning("Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
            return
        elif not valid1:
            messagebox.showwarning("Input Error", "\n".join(errors1))
            return
        elif not valid2:
            messagebox.showwarning("Input Error", "\n".join(errors2))
            return
        
        valid, errors = unassign_instructor(instructor,course)
        if valid:
            messagebox.showinfo("Success", f"{instructor.name} unassigned from {course.course_name}!")
        else:
            messagebox.showwarning("Input Error", "\n".join(errors))

        # valid1, errors1 = edit_entry_json('Course', course)
        # valid2, errors2 = edit_entry_json('Instructor', instructor)

        # if valid1 and valid2:
        #     messagebox.showinfo("Success", f"{instructor.name} unassigned from {course.course_name}!")
        # elif not valid1 and not valid2:
        #     messagebox.showwarning("Input Error", "\n".join(errors1) + "\n" + "\n".join(errors2))
        # elif not valid1:
        #     messagebox.showwarning("Input Error", "\n".join(errors1))
        # elif not valid2:
        #     messagebox.showwarning("Input Error", "\n".join(errors2))

    def on_course_select(self, event):
        idx = self.course_dropdown.current()
        if idx != -1:
            selected = courses[idx]
            self.course_var.set(selected.course_id)

    def on_instructor_select(self, event):
        idx = self.instructor_dropdown.current()
        if idx != -1:
            selected = instructors[idx]
            self.instructor_var.set(selected.instructor_id)

    def update_ui(self):
        self.course_dropdown['values'] = [course.course_name for course in courses]
        self.instructor_dropdown['values'] = [instructor.name for instructor in instructors]
