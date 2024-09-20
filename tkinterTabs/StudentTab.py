import tkinter as tk
from tkinter import ttk, messagebox
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from shared import courses, students

class StudentTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.student_var : tk.StringVar = tk.StringVar()
        self.name_var : tk.StringVar = tk.StringVar()
        self.age_var : tk.StringVar = tk.StringVar()
        self.email_var : tk.StringVar = tk.StringVar()
        self.student_dropdown : ttk.Combobox = None

        self.init_ui()

    def init_ui(self):
        tk.Label(self, text="Add Student", font=("Arial", 28)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Name:").grid(row=1, column=0, padx=0, pady=5)
        self.name_input = tk.Entry(self)
        self.name_input.grid(row=1, column=1, padx=0, pady=5)

        tk.Label(self, text="Age:").grid(row=2, column=0, padx=0, pady=5)
        self.age_input = tk.Entry(self)
        self.age_input.grid(row=2, column=1, padx=0, pady=5)

        tk.Label(self, text="Email:").grid(row=3, column=0, padx=0, pady=5)
        self.email_input = tk.Entry(self)
        self.email_input.grid(row=3, column=1, padx=0, pady=5)

        tk.Label(self, text="Student ID:").grid(row=4, column=0, padx=0, pady=5)
        self.student_id_input = tk.Entry(self)
        self.student_id_input.grid(row=4, column=1, padx=0, pady=5)

        submit_button = tk.Button(self, text="Add Student", command=self.create_student)
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Edit or Remove Student", font=("Arial", 28)).grid(row=6, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Select Student:").grid(row=7, column=0, padx=0, pady=5)
        self.student_dropdown = ttk.Combobox(self, values=[student.name for student in students], state='readonly')
        self.student_dropdown.grid(row=7, column=1, padx=0, pady=5)
        self.student_dropdown.bind("<<ComboboxSelected>>", self.on_select)

        tk.Label(self, text="Name:").grid(row=8, column=0, padx=0, pady=5)
        self.edit_name_input = tk.Entry(self, textvariable=self.name_var)
        self.edit_name_input.grid(row=8, column=1, padx=0, pady=5)

        tk.Label(self, text="Age:").grid(row=9, column=0, padx=0, pady=5)
        self.edit_age_input = tk.Entry(self, textvariable=self.age_var)
        self.edit_age_input.grid(row=9, column=1, padx=0, pady=5)

        tk.Label(self, text="Email:").grid(row=10, column=0, padx=0, pady=5)
        self.edit_email_input = tk.Entry(self, textvariable=self.email_var)
        self.edit_email_input.grid(row=10, column=1, padx=0, pady=5)

        edit_button = tk.Button(self, text="Edit Student", command=self.edit_student)
        edit_button.grid(row=11, column=0, columnspan=1, pady=0)

        delete_button = tk.Button(self, text="Remove Student", command=self.delete_student)
        delete_button.grid(row=11, column=1, columnspan=1, pady=0)

    def create_student(self):
        try:
            name = self.name_input.get()
            age = int(self.age_input.get())
            email = self.email_input.get()
            student_id = self.student_id_input.get()

            student : Student = Student(name, age, email, student_id, [])

            #valid, errors = add_entry_json('Student', student)
            valid, errors = add_student(student)

            if valid:
                messagebox.showinfo("Success", f"Student {name} created successfully!")
                self.name_input.delete(0, tk.END)
                self.age_input.delete(0, tk.END)
                self.email_input.delete(0, tk.END)
                self.student_id_input.delete(0, tk.END)
                students.append(student)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))

        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def delete_student(self):
        try:
            student_id = self.student_var.get()

            student : Student = next(student for student in students if student.student_id == student_id)

            for course_id in student.registered_courses:
                course : Course = next(course for course in courses if course.course_id == course_id)
                valid, errors = course.unenroll_student(student)
                # valid, errors = edit_entry_json('Course', course)
                if not valid:
                    messagebox.showwarning("Input Error", "\n".join(errors))
                    return
                courses.remove(course)
                courses.append(course)

            #valid, errors = delete_entry_json('Student', student)
            valid, errors = delete_student(student)

            if valid:
                messagebox.showinfo("Success", f"Student {student.name} has been removed successfully!")
                self.edit_name_input.delete(0, tk.END)
                self.edit_age_input.delete(0, tk.END)
                self.edit_email_input.delete(0, tk.END)
                students.remove(student)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))

        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def edit_student(self):
        try:
            new_name = self.edit_name_input.get()
            new_age = int(self.edit_age_input.get())
            new_email = self.edit_email_input.get()

            student_id = self.student_var.get()
            student = next(student for student in students if student.student_id == student_id)

            student.name = new_name
            student.age = new_age
            student._email = new_email

            #valid, errors = edit_entry_json('Student', student)
            valid, errors = edit_student(student)

            if valid:
                messagebox.showinfo("Success", f"Student {student.name} edited successfully!")
                self.edit_name_input.delete(0, tk.END)
                self.edit_age_input.delete(0, tk.END)
                self.edit_email_input.delete(0, tk.END)
                students.remove(student)
                students.append(student)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))

        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def update_ui(self):
        self.student_dropdown['values'] = [student.name for student in students]

    def on_select(self, event):
        idx = self.student_dropdown.current()
        if idx != -1:
            selected = students[idx]
            self.student_var.set(selected.student_id)
            self.name_var.set(selected.name)
            self.age_var.set(selected.age)
            self.email_var.set(selected._email)
