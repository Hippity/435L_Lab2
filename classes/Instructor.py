from .Person import Person

class Instructor(Person):
    def __init__(self, name: str, age: int, email: str, instructor_id: str, assigned_courses: list):
        """
        Initializes an Instructor instance with the provided details.

        Args:
            name (str): The name of the instructor.
            age (int): The age of the instructor.
            email (str): The email of the instructor.
            instructor_id (str): The unique identifier for the instructor.
            assigned_courses (list): A list of course IDs that the instructor is assigned to.
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses

    def assign_course(self, course):
        """
        Assigns the instructor to a course if not already assigned.

        Args:
            course (Course): An instance of the Course class to assign the instructor to.

        Returns:
            tuple: A tuple containing:
                - bool: True if the instructor was successfully assigned, False if already assigned.
                - list: A list of messages indicating success or errors encountered.
        """
        if course.course_id not in self.assigned_courses:
            self.assigned_courses.append(course.course_id)
            return True, ["Assigned to course"]
        else: 
            return False, ["Already assigned to course"]
        
    def unassign_course(self, course):
        """
        Unassigns the instructor from a course if they are currently assigned.

        Args:
            course (Course): An instance of the Course class to unassign the instructor from.

        Returns:
            tuple: A tuple containing:
                - bool: True if the instructor was successfully unassigned, False if not assigned to course.
                - list: A list of messages indicating success or errors encountered.
        """
        if course.course_id not in self.assigned_courses:
            return False, ["Course not assigned course"]
        else: 
            self.assigned_courses.remove(course.course_id)
            return True, ["Instructor uassigned to course"]

    def validate(self):
        """
        Validates the instructor details, ensuring the instructor ID and other attributes are correct.

        Returns:
            tuple: A tuple containing:
                - bool: True if validation passed, False otherwise.
                - list: A list of messages indicating success or errors encountered.
        """
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
        """
        Creates an Instructor instance from a JSON object.

        Args:
            json_object (dict): A dictionary representing instructor data.

        Returns:
            Instructor: An instance of the Instructor class.
        """        
        name, age, email = super().from_json(json_object)
        instructor_id = json_object.get("instructor_id")
        assigned_courses = json_object.get("assigned_courses",[])
        return cls(name,age,email,instructor_id,assigned_courses)

    @classmethod
    def from_db(cls, db_object: tuple):
        """
        Creates an Instructor instance from a database tuple.

        Args:
            db_object (tuple): A tuple representing instructor data from the database.

        Returns:
            Instructor: An instance of the Instructor class.
        """
        name, age, email = super().from_db(db_object)
        course_id = db_object[0]
        assigned_courses = db_object[4].split(',') if db_object[4] is not None else []
        return cls(name,age,email,course_id,assigned_courses)