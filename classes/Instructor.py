from .Person import Person

class Instructor(Person):
    def __init__(self, name: str, age: int, email: str, instructor_id: str, assigned_courses: list):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses

    def assign_course(self, course):
        if course.course_id not in self.assigned_courses:
            self.assigned_courses.append(course.course_id)
            return True, ["Assigned to course"]
        else: 
            return False, ["Already assigned to course"]
        
    def unassign_course(self, course):
        if course.course_id not in self.assigned_courses:
            return False, ["Course not assigned course"]
        else: 
            self.assigned_courses.remove(course.course_id)
            return True, ["Instructor uassigned to course"]

    def validate(self):
        error = None
        if (len(self.instructor_id) != 5):
            error = "Not a valid instructor_id"

        if error is None:
            return super().validate()
        else:
            valid , errors = super().validate()
            if valid:
                return False, [error]
            else:
                errors.append(error)
                return False, errors

    @classmethod
    def from_json(cls, json_object: dict):
        name, age, email = super().from_json(json_object)
        instructor_id = json_object.get("instructor_id")
        assigned_courses = json_object.get("assigned_courses",[])
        return cls(name,age,email,instructor_id,assigned_courses)

    @classmethod
    def from_db(cls, db_object: tuple):
        name, age, email = super().from_db(db_object)
        course_id = db_object[0]
        assigned_courses = db_object[4].split(',') if db_object[4] is not None else []
        return cls(name,age,email,course_id,assigned_courses)