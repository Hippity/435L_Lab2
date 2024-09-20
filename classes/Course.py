from .Instructor import Instructor
from .Student import Student

class Course:
    def __init__(self,course_id : str, course_name: str, instructor_id : str, enrolled_students: list ):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor_id = instructor_id
        self.enrolled_students = enrolled_students

    def __str__(self):
        return self.course_name

    def assign_instructor(self, instructor: Instructor):
        if not self.instructor_id:
            self.instructor_id = instructor.instructor_id
            return True ,["Instructor Assigned"]
        else:
            return False,["Instructor Already Assigned"]
        
    def unassign_instructor(self, instructor: Instructor):
        if not self.instructor_id == instructor.instructor_id:
            return False ,["Instructor not assigned in course"]
        else:
            self.instructor_id = ""
            return True,["Instructor unassigned"]
        
    def enroll_student(self, student : Student):
        if student.student_id not in self.enrolled_students:
            self.enrolled_students.append(student.student_id)
            return True, ["Student assigned to course"]
        else: 
            return False, ["Student already in course"]
    
    def unenroll_student(self, student : Student):
        if student.student_id not in self.enrolled_students:
            return False, ["Student not in course"]
        else: 
            self.enrolled_students.remove(student.student_id)
            return True, ["Student unregistered to course"]

    def validate(self):
        errors = []

        if len(self.course_name) != 7:
            errors.append("Not a valid course name")
        if len(self.course_id) != 5:
            errors.append("Not a valid course id")

        if errors:
            return False, errors
        else:
            return True, ["Validation Passed!"]
        
    @classmethod
    def from_json(cls, json_object : dict):
        course_id = json_object.get("course_id")
        course_name = json_object.get("course_name")
        instructor_id = json_object.get("instructor_id") 
        enrolled_students = json_object.get("enrolled_students",[])
        return cls(course_id,course_name,instructor_id,enrolled_students) 

    @classmethod
    def from_db(cls, db_object : tuple):
        course_id = db_object[0]
        course_name = db_object[1]
        instructor_id = db_object[2]
        enrolled_students = db_object[3].split(",") if db_object[3] is not None else []
        return cls(course_id,course_name,instructor_id,enrolled_students)