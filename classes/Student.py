from .Person import Person

class Student(Person):
    def __init__(self, name: str, age: int, email: str, student_id: str, registered_courses : list):
        """
        Initializes a Student instance with the provided details.

        Args:
            name (str): The name of the student.
            age (int): The age of the student.
            email (str): The email of the student.
            student_id (str): The unique identifier for the student.
            registered_courses (list): A list of course IDs that the student is registered in.
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = registered_courses

    def register_course(self, course):
        """
        Registers the student to a course if they are not already registered.

        Args:
            course (Course): An instance of the Course class representing the course to register.

        Returns:
            tuple: A tuple containing:
                - bool: True if the student was successfully registered, False if already registered.
                - list: A list of messages indicating success or errors encountered.
        """
        if course.course_id not in self.registered_courses:
            self.registered_courses.append(course.course_id)
            return True, ["Registered in course"]
        else: 
            return False, ["Already registered in course"]
    
    def unregister_course(self, course):
        """
        Unregisters the student from a course if they are currently registered.

        Args:
            course (Course): An instance of the Course class representing the course to unregister.

        Returns:
            tuple: A tuple containing:
                - bool: True if the student was successfully unregistered, False if not registered.
                - list: A list of messages indicating success or errors encountered.
        """
        if course.course_id not in self.registered_courses:
            return False, ["Course not registered"]
        else: 
            self.registered_courses.remove(course.course_id)
            return True, ["Course unregistered in course"]

    def validate(self):
        """
        Validates the student details, ensuring the student ID and other attributes are correct.

        Returns:
            tuple: A tuple containing:
                - bool: True if validation passed, False otherwise.
                - list: A list of messages indicating success or errors encountered.
        """
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
    def from_json(cls, json_object: dict):
        """
        Creates an Student instance from a JSON object.

        Args:
            json_object (dict): A dictionary representing student data.

        Returns:
            Student: An instance of the Student class.
        """        
        name, age, email = super().from_json(json_object)
        student_id = json_object.get("student_id")
        registered_courses = json_object.get("registered_courses",[])
        return cls(name,age,email,student_id,registered_courses)

    @classmethod
    def from_db(cls, db_object: tuple):
        """
        Creates a Student instance from a database tuple.

        Args:
            db_object (tuple): A tuple representing the student data from the database.

        Returns:
            Student: An instance of the Student class.
        """
        name, age, email = super().from_db(db_object)
        student_id = db_object[0]
        registered_courses = db_object[4].split(',') if db_object[4] is not None else []
        return cls(name,age,email,student_id,registered_courses)

 