from .Person import Person

class Student(Person):
    def __init__(self, name: str, age: int, email: str, student_id: str, registered_courses : list):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = registered_courses

    def register_course(self, course):
        if course.course_id not in self.registered_courses:
            self.registered_courses.append(course.course_id)
            return True, ["Registered in course"]
        else: 
            return False, ["Already registered in course"]
    
    def unregister_course(self, course):
        if course.course_id not in self.registered_courses:
            return False, ["Course not registered"]
        else: 
            self.registered_courses.remove(course.course_id)
            return True, ["Course unregistered in course"]


    def validate(self):
        error = None
        if (len(self.student_id) != 5):
            error = "Not a valid student_id"

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
    def from_db(cls, db_object: tuple):
        name, age, email = super().from_db(db_object)
        student_id = db_object[0]
        registered_courses = db_object[4].split(',') if db_object[4] is not None else []
        return cls(name,age,email,student_id,registered_courses)

 