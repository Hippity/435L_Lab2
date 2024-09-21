from jsonCRUD.jsonCRUD import load_json
from classes.Course import *
from databaseCRUD.databaseCRUD import *

"""
Contains the local copy of the data that is shared throughout the app
"""

# Commented code that works for the JSON File

# data = load_json()
# courses = [Course.from_json(course) for course in data["Course"]]
# instructors = [Instructor.from_json(instructor) for instructor in data["Instructor"]]
# students = [Student.from_json(student) for student in data["Student"]]

courses = [Course.from_db(course) for course in fetch_courses()]
instructors = [Instructor.from_db(instructor) for instructor in fetch_instructors()]
students = [Student.from_db(students) for students in fetch_students()]
