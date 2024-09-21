import tkinter as tk
from tkinter import ttk, messagebox
from classes.Course import *
from jsonCRUD.jsonCRUD import *
from databaseCRUD.databaseCRUD import *
from shared import courses, students, instructors

class AddCourseTab(tk.Frame):
    def __init__(self, parent):
        """
        Initializes the AddCourseTab, setting up the attributes and initializing the UI.

        Attributes:
            course_dropdown (ttk.Combobox): Dropdown of the list of courses from shared.py
            course_var (tk.StringVar): Selected course_id
            course_var (tk.StringVar): Selected course name for set edit_name_input
            name_input (tk.Entry): Course Name Input
            course_id_input (tk.Entry): Course ID Input
            edit_name_input (tk.Entry): Edit Course Name input
        """
        super().__init__(parent)
        self.course_dropdown : ttk.Combobox = None
        self.course_var : tk.StringVar = tk.StringVar()
        self.name_var : tk.StringVar = tk.StringVar()
        self.name_input : tk.Entry = None
        self.course_id_input : tk.Entry = None
        self.edit_name_input : tk.Entry = None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI of the AddCourseTab. Sets up the layout and adds all the components
        """
        # Add Course Title
        tk.Label(self, text="Add Course", font=("Arial", 28)).grid(row=0, column=0, columnspan=2, pady=10)

        # Course Name Input Label
        tk.Label(self, text="Course Name:").grid(row=1, column=0, padx=0, pady=5)
        # Course Name Input
        self.name_input = tk.Entry(self)
        self.name_input.grid(row=1, column=1, padx=0, pady=5)

        # Course ID Input Label
        tk.Label(self, text="Course ID:").grid(row=2, column=0, padx=0, pady=5)
        # Course ID Input 
        self.course_id_input = tk.Entry(self)
        self.course_id_input.grid(row=2, column=1, padx=0, pady=5)

        # Add Course Button
        submit_button = tk.Button(self, text="Add Course", command=self.create_course)
        submit_button.grid(row=5, column=0, columnspan=2, pady=0)

        # Edit or Remove Course Title
        tk.Label(self, text="Edit or Remove Course", font=("Arial", 28)).grid(row=6, column=0, columnspan=2, pady=10)

        # Course Dropdown Label
        tk.Label(self, text="Select Course: ").grid(row=7, column=0, padx=0, pady=5)
        # Course Dropdown
        self.course_dropdown = ttk.Combobox(self, values=[course.course_name for course in courses], state='readonly')
        self.course_dropdown.grid(row=7, column=1, padx=0, pady=5)
        self.course_dropdown.bind("<<ComboboxSelected>>", self.on_select)

        # Edit Course Name Input Label
        tk.Label(self, text="Course Name:").grid(row=8, column=0, padx=0, pady=5)
        # Edit Course Name Input
        self.edit_name_input = tk.Entry(self, textvariable=self.name_var)
        self.edit_name_input.grid(row=8, column=1, padx=0, pady=5)

        # Edit Course Button
        edit_button = tk.Button(self, text="Edit Course", command=self.edit_course)
        edit_button.grid(row=9, column=0, columnspan=1, pady=0)

        # Remove Course Button
        delete_button = tk.Button(self, text="Remove Course", command=self.delete_course)
        delete_button.grid(row=9, column=1, columnspan=1, pady=0)

    def create_course(self):
        """
        Adds a course to the db and updates local copy

        Validates the create process and displays success or error messages
        using a messageBox.
        """
        try:
            name = self.name_input.get()
            course_id = self.course_id_input.get()

            course : Course = Course(course_id, name, "", [])
            # valid, errors = add_entry_json('Course', course)
            valid, errors = add_course(course)

            if valid:
                messagebox.showinfo("Success", f"Course {course.course_name} created successfully!")
                self.name_input.delete(0, tk.END)
                self.course_id_input.delete(0, tk.END)
                courses.append(course)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))
        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def delete_course(self):
        """
        Deletes a course from the db and updates local copy

        Validates the delete process and displays success or error messages
        using a messageBox.
        """
        try:
            course_id = self.course_var.get()

            course : Course = next(course for course in courses if course.course_id == course_id)

            for student_id in course.enrolled_students:
                student : Student = next(student for student in students if student.student_id == student_id)
                valid, errors = student.unregister_course(course)
                # valid, errors = edit_entry_json('Student', student)
                if not valid:
                    messagebox.showwarning("Input Error", "\n".join(errors))
                    return
                students.remove(student)
                students.append(student)

            if course.instructor_id:
                instructor : Instructor = next(inst for inst in instructors if inst.instructor_id == course.instructor_id)
                valid, errors = instructor.unassign_course(course)
                # valid, errors = edit_entry_json('Instructor', instructor)
                if not valid:
                    messagebox.showwarning("Input Error", "\n".join(errors))
                    return
                instructors.remove(instructor)
                instructors.append(instructor)

            # valid, errors = delete_entry_json('Course',course)
            valid, errors = delete_course(course)

            if valid:
                messagebox.showinfo("Success", f"Course {course.course_name} has been removed successfully!")
                self.edit_name_input.delete(0, tk.END)
                courses.remove(course)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))
        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def edit_course(self):
        """
        Updates a course in the db and updates local copy

        Validates the edit process and displays success or error messages
        using a messageBox.
        """
        try:
            course_id = self.course_var.get()
            new_name = self.edit_name_input.get()

            course : Course = next(course for course in courses if course.course_id == course_id)

            course.course_name = new_name

            # valid, errors = edit_entry_json('Course',course)
            valid, errors = edit_course(course)

            if valid:
                messagebox.showinfo("Success", f"Course {course.course_name} has been edited successfully!")
                self.edit_name_input.delete(0, tk.END)
                courses.remove(course)
                courses.append(course)
                self.update_ui()
            else:
                messagebox.showwarning("Input Error", "\n".join(errors))
        except Exception as e:
            messagebox.showwarning("Exception", str(e))

    def on_select(self, event):
        """
        Updates the course_var attribute with the selected course_id and input labels
        """
        idx = self.course_dropdown.current()
        if idx != -1:
            selected = courses[idx]
            self.course_var.set(selected.course_id)
            self.name_var.set(selected.course_name)

    def update_ui(self):
        """
        Updated the UI for the course dropdown to relfect new data
        """
        self.course_dropdown['values'] = [course.course_name for course in courses]

