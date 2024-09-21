import tkinter as tk
from tkinter import ttk, messagebox
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from shared import instructors, courses

class AddInstructorTab(tk.Frame):
    def __init__(self, parent):
        """
        Initializes the AddInstructorTab, setting up the attributes and initializing the UI.

        Attributes:
            instructor_dropdown (ttk.Combobox): Dropdown of the list of instructors from shared.py
            instructor_var (tk.StringVar): Selected instructor_id
            name_var (tk.StringVar): Selected instructor name for set edit_name_input
            age_var (tk.StringVar): Selected instructor age for set edit_age_input
            email_var (tk.StringVar): Selected instructor name for set edit_email_input
            name_input (tk.Entry): Name input
            age_input (tk.Entry): Age input
            email_input (tk.Entry): Email input
            instructor_id_input (tk.Entry): Instructor ID input
            edit_name_input (tk.Entry): Edit name input
            edit_age_input (tk.Entry): Edit age input
            edit_email_input (tk.Entry): Edit email input
        """
        super().__init__(parent)
        self.instructor_dropdown : ttk.Combobox = None
        self.instructor_var : tk.StringVar = tk.StringVar()
        self.name_var : tk.StringVar = tk.StringVar()
        self.age_var : tk.StringVar = tk.StringVar()
        self.email_var : tk.StringVar = tk.StringVar()
        self.name_input :tk.Entry = None
        self.age_input : tk.Entry = None
        self.email_input : tk.Entry = None
        self.instructor_id_input : tk.Entry = None
        self.edit_name_input : tk.Entry = None
        self.edit_age_input : tk.Entry = None
        self.edit_email_input : tk.Entry = None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the AddInstructorTab. Sets up the layout and adds all the components
        """
        # Add Instructor Title
        tk.Label(self, text="Add Instructor", font=("Arial", 28)).grid(row=0, column=0, columnspan=2, pady=10)

        # Name Input Label
        tk.Label(self, text="Name:").grid(row=1, column=0, padx=0, pady=5)
        # Name Input
        self.name_input = tk.Entry(self)
        self.name_input.grid(row=1, column=1, padx=0, pady=5)

        # Age Input Label
        tk.Label(self, text="Age:").grid(row=2, column=0, padx=0, pady=5)
        # Age Input
        self.age_input = tk.Entry(self)
        self.age_input.grid(row=2, column=1, padx=0, pady=5)

        # Email Input Label
        tk.Label(self, text="Email:").grid(row=3, column=0, padx=0, pady=5)
        # Email Input
        self.email_input = tk.Entry(self)
        self.email_input.grid(row=3, column=1, padx=0, pady=5)

        # Instructor ID Input Label
        tk.Label(self, text="Instructor ID:").grid(row=4, column=0, padx=0, pady=5)
        # Instructor ID Input
        self.instructor_id_input = tk.Entry(self)
        self.instructor_id_input.grid(row=4, column=1, padx=0, pady=5)

        # Add Instructor Button
        submit_button = tk.Button(self, text="Add Instructor", command=self.create_instructor)
        submit_button.grid(row=5, column=0, columnspan=2, pady=0)

        # Edit or Remove Instructor Title
        tk.Label(self, text="Edit or Remove Instructor", font=("Arial", 28)).grid(row=6, column=0, columnspan=2, pady=10)

        # Instructor Dropdown Title
        tk.Label(self, text="Select Instructor:").grid(row=7, column=0, padx=0, pady=5)
        # Instructor Dropdown
        self.instructor_dropdown = ttk.Combobox(self, values=[instructor.name for instructor in instructors], state='readonly')
        self.instructor_dropdown.grid(row=7, column=1, padx=0, pady=5)
        self.instructor_dropdown.bind("<<ComboboxSelected>>", self.on_select)

        # Edit Name Input Label
        tk.Label(self, text="Name:").grid(row=8, column=0, padx=0, pady=5)
        # Edit Name Input
        self.edit_name_input = tk.Entry(self, textvariable=self.name_var)
        self.edit_name_input.grid(row=8, column=1, padx=0, pady=5)

        # Edit Age Input Label
        tk.Label(self, text="Age:").grid(row=9, column=0, padx=0, pady=5)
        # Edit Age Input
        self.edit_age_input = tk.Entry(self, textvariable=self.age_var)
        self.edit_age_input.grid(row=9, column=1, padx=0, pady=5)

        # Edit Email Input Label
        tk.Label(self, text="Email:").grid(row=10, column=0, padx=0, pady=5)
        # Edit Email Input
        self.edit_email_input = tk.Entry(self, textvariable=self.email_var)
        self.edit_email_input.grid(row=10, column=1, padx=0, pady=5)

        # Edit Instructor Button
        edit_button = tk.Button(self, text="Edit Instructor", command=self.edit_instructor)
        edit_button.grid(row=11, column=0, columnspan=1, pady=0)

        # Remove Instructor Button
        delete_button = tk.Button(self, text="Remove Instructor", command=self.delete_instructor)
        delete_button.grid(row=11, column=1, columnspan=1, pady=0)

    def create_instructor(self):
        """
        Adds an instructor to the db and updates local copy

        Validates the create process and displays success or error messages
        using a messageBox.
        """
        try:
            name = self.name_input.get()
            age = int(self.age_input.get())
            email = self.email_input.get()
            instructor_id = self.instructor_id_input.get()

            instructor : Instructor = Instructor(name, age, email, instructor_id, [])

            # valid, errors = add_entry_json('Instructor', instructor)
            valid, errors = add_instructor(instructor)

            if valid:
                messagebox.showinfo("Success", f"Instructor {instructor.name} created successfully!")
                self.name_input.delete(0, tk.END)
                self.age_input.delete(0, tk.END)
                self.email_input.delete(0, tk.END)
                self.instructor_id_input.delete(0, tk.END)
                instructors.append(instructor)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))

        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def delete_instructor(self):
        """
        Deletes an instructor from the db and updates local copy

        Validates the delete process and displays success or error messages
        using a messageBox.
        """
        try:
            instructor_id = self.instructor_var.get()

            instructor : Instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)

            for course_id in instructor.assigned_courses:
                course : Course = next(course for course in courses if course.course_id == course_id)
                valid, errors = course.unassign_instructor(instructor)
                # valid, errors = edit_entry_json('Course', course)
                if not valid:
                    messagebox.showwarning("Input Error", "\n".join(errors))
                    return
                courses.remove(course)
                courses.append(course)

            # valid, errors = delete_entry_json('Instructor', instructor)
            valid, errors = delete_instructor(instructor)

            if valid:
                messagebox.showinfo("Success", f"Instructor {instructor.name} has been removed successfully!")
                self.edit_name_input.delete(0, tk.END)
                self.edit_age_input.delete(0, tk.END)
                self.edit_email_input.delete(0, tk.END)
                instructors.remove(instructor)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))

        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def edit_instructor(self):
        """
        Updates an instructor in the db and updates local copy

        Validates the edit process and displays success or error messages
        using a QMessageBox.
        """
        try:
            new_name = self.edit_name_input.get()
            new_age = int(self.edit_age_input.get())
            new_email = self.edit_email_input.get()

            instructor_id = self.instructor_var.get()
            instructor : Instructor = next(inst for inst in instructors if inst.instructor_id == instructor_id)

            instructor.name = new_name
            instructor.age = new_age
            instructor._email = new_email

            # valid, errors = edit_entry_json('Instructor', instructor)
            valid, errors = edit_instructor(instructor)

            if valid:
                messagebox.showinfo("Success", f"Instructor {instructor.name} edited successfully!")
                self.edit_name_input.delete(0, tk.END)
                self.edit_age_input.delete(0, tk.END)
                self.edit_email_input.delete(0, tk.END)
                instructors.remove(instructor)
                instructors.append(instructor)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))

        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def on_select(self, event):
        """
        Updates the instructor_var attribute with the selected instructor_id and input labels
        """
        idx = self.instructor_dropdown.current()
        if idx != -1:
            selected = instructors[idx]
            self.instructor_var.set(selected.instructor_id)
            self.name_var.set(selected.name)
            self.age_var.set(selected.age)
            self.email_var.set(selected._email)

    def update_ui(self):
        """
        Updated the UI for the instructor dropdown to relfect new data
        """
        self.instructor_dropdown['values'] = [instructor.name for instructor in instructors]
