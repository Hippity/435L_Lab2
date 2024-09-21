"""
This module serves as the central location for maintaining the local copy of data shared throughout the application.

It fetches data for courses, instructors, and students either from a JSON file or a database, depending on the active code section.

Imports:
    - load_json (from crud.jsonCRUD): Function to load data from a JSON file (currently commented out).
    - fetch_courses, fetch_instructors, fetch_students (from crud.databaseCRUD): Functions to fetch data from the database.
    - Course, Instructor, Student (from classes.Course): Classes representing the main data structures.

Attributes:
    courses (list): A list of Course objects fetched from the database (or JSON).
    instructors (list): A list of Instructor objects fetched from the database (or JSON).
    students (list): A list of Student objects fetched from the database (or JSON).

Usage:
    The module provides shared data that is accessed throughout the application, with `courses`, `instructors`, and `students`
    being available for use in different parts of the program.

"""

from crud.jsonCRUD import load_json
from crud.databaseCRUD import fetch_courses , fetch_instructors , fetch_students
from classes.Course import *

# Commented code that works for the JSON File
# data = load_json()
# courses = [Course.from_json(course) for course in data["Course"]]
# instructors = [Instructor.from_json(instructor) for instructor in data["Instructor"]]
# students = [Student.from_json(student) for student in data["Student"]]

courses = [Course.from_db(course) for course in fetch_courses()]
instructors = [Instructor.from_db(instructor) for instructor in fetch_instructors()]
students = [Student.from_db(students) for students in fetch_students()]
