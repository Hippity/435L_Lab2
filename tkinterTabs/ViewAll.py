import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from classes.Course import *
from jsonCRUD.jsonCRUD import *
import shared
from shared import courses,instructors,students
import importlib

class ViewAllTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.table = 'Student'

        self.courses = courses
        self.instructors = instructors
        self.students = students

        self.students_data = self.fix_student_data()
        self.instructors_data = self.fix_instructor_data()
        self.courses_data = self.fix_course_data()

        self.init_ui()

    def init_ui(self):
        tk.Label(self, text="View All", font=("Arial", 28)).pack(pady=10)

        search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=search_var)
        search_entry.pack()
        search_entry.bind('<KeyRelease>', lambda event: self.search_data(self.treeview, search_var.get()))

        self.treeview = ttk.Treeview(self, show="headings", height=10)
        self.treeview.pack(pady=10, fill='both', expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=0)

        courses_button = tk.Button(button_frame, text="View Courses", command=self.show_courses)
        courses_button.pack(side="left", padx=5)

        students_button = tk.Button(button_frame, text="View Students", command=self.show_students)
        students_button.pack(side="left", padx=5)

        instructors_button = tk.Button(button_frame, text="View Instructors", command=self.show_instructors)
        instructors_button.pack(side="left", padx=5)

        button_frame2 = tk.Frame(self)
        button_frame2.pack(pady=0)

        refresh_button = tk.Button(button_frame2, text="Refresh Data", command=self.refresh_data_tree)
        refresh_button.pack(side="left", padx=5)

        export_button = tk.Button(button_frame2, text="Export CSV", command=self.export_csv)
        export_button.pack(side="left", padx=5)

        self.show_students()

    def update_tree_headers(self, headers):
        self.treeview["columns"] = headers
        for col in headers:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=150)

    def update_tree_data(self, data):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        
        for row in data:
            self.treeview.insert("", "end", values=row)

    def show_courses(self):
        self.table = 'Course'
        headers = ["Course ID", "Course Name", "Instructor", "Enrolled Students"]
        self.update_tree_headers(headers)
        self.update_tree_data(self.courses_data)

    def show_students(self):
        self.table = 'Student'
        headers = ["Student ID", "Student Name", "Student Age", "Student Email", "Registered Courses"]
        self.update_tree_headers(headers)
        self.update_tree_data(self.students_data)

    def show_instructors(self):
        self.table = 'Instructor'
        headers = ["Instructor ID", "Instructor Name", "Instructor Age", "Instructor Email", "Assigned Courses"]
        self.update_tree_headers(headers)
        self.update_tree_data(self.instructors_data)

    def search_data(self, treeview, query):
        query = query.lower()
        if treeview["columns"] == ("Course ID", "Course Name", "Instructor", "Enrolled Students"):
            filtered_data = [row for row in self.courses_data if query in str(row).lower()]
        elif treeview["columns"] == ("Student ID", "Student Name", "Student Age", "Student Email", "Registered Courses"):
            filtered_data = [row for row in self.students_data if query in str(row).lower()]
        elif treeview["columns"] == ("Instructor ID", "Instructor Name", "Instructor Age", "Instructor Email", "Assigned Courses"):
            filtered_data = [row for row in self.instructors_data if query in str(row).lower()]
        self.update_tree_data(filtered_data)

    def export_csv(self):
        headers = self.treeview["columns"]
        data = [self.treeview.item(item)["values"] for item in self.treeview.get_children()]

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  
                writer.writerows(data)    
            messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting: {e}")

    def refresh_data_tree(self):
        importlib.reload(shared)

        self.students = students
        self.instructors = instructors
        self.courses = courses

        self.students_data = self.fix_student_data()
        self.instructors_data = self.fix_instructor_data()
        self.courses_data = self.fix_course_data()

        if self.table == 'Student':
            self.update_tree_data(self.students_data)
        elif self.table == 'Course':
            self.update_tree_data(self.courses_data)
        elif self.table == 'Instructor':
            self.update_tree_data(self.instructors_data)

    def fix_student_data(self):
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
            rows.append((student_id, name, age, email, " ".join(course_names)))
        return rows

    def fix_instructor_data(self):
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
            rows.append((instructor_id, name, age, email, " ".join(course_names)))
        return rows

    def fix_course_data(self):
        rows = []
        for course in self.courses:
            course_id = course.course_id
            course_name = course.course_name
            instructor_id = course.instructor_id
            instructor_name = list(filter(lambda instructor: instructor.instructor_id == instructor_id, self.instructors))[0].name if instructor_id else 'No Instructor'
            enrolled_students = course.enrolled_students
            student_names = [
                next(student.name for student in self.students if student.student_id == student_id)
                for student_id in enrolled_students
            ] if enrolled_students else ['No Students']
            rows.append((course_id, course_name, instructor_name, " ".join(student_names)))
        return rows
