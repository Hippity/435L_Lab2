import sqlite3
from classes.Course import *

database_path = './databaseCRUD/database.db'

def connect_db():
    """
    Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to interact with the database.
    """
    return sqlite3.connect(database_path)

def fetch_courses():
    """
    Retrieve all courses from the database, including their enrolled students as a string e.g(Name1,Name2,Name3)

    Returns:
        list: A list of tuples representing the courses and their enrolled students.
              Each tuple contains (course_id, course_name, instructor_id, enrolled_students)
              Returns an empty list if an error occurs.
    """
    conn : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT c.course_id, c.course_name, c.instructor_id, 
                GROUP_CONCAT(e.student_id) AS enrolled_students
            FROM Course c
            LEFT JOIN Enrollment e ON c.course_id = e.course_id
            GROUP BY c.course_id
        """)
        courses = cursor.fetchall()
        return courses
    except sqlite3.Error as e:
        return []
    finally:
        conn.close()

def add_course(course: Course):
    """
    Add a new course to the database.

    Args:
        course (Course): An instance of the Course class to be added.

    Returns:
        tuple: A tuple containing:
            - bool: True if the course was successfully added, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    valid, errors = course.validate()
    if not valid:
        return False, errors

    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Course (course_id, course_name) VALUES (?, ?)",
                       (course.course_id, course.course_name))
        conn.commit()
        return True, [f"Added course {course.course_name} to table"]
    except sqlite3.Error as e:
        return False, [str(e)]
    finally:
        conn.close()

def edit_course(course: Course):
    """
    Edit an existing course in the database.

    Args:
        course (Course): An instance of the Course class with updated data.

    Returns:
        tuple: A tuple containing:
            - bool: True if the course was successfully edited, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    valid, errors = course.validate()
    if not valid:
        return False, errors

    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Course SET course_name = ? WHERE course_id = ?",
                       (course.course_name, course.course_id))
        conn.commit()
        return True, [f"Edited course {course.course_name} in table"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def delete_course(course: Course):
    """
    Delete an existing course from the database.

    Args:
        course (Course): An instance of the Course class to be deleted.

    Returns:
        tuple: A tuple containing:
            - bool: True if the course was successfully deleted, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    conn: sqlite3.Connection = connect_db()
    cursor: sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Enrollment WHERE course_id = ?", (course.course_id,))
        conn.commit()
        cursor.execute("DELETE FROM Course WHERE course_id = ?", (course.course_id,))
        conn.commit()
        return True, [f"Deleted course {course.course_name} from table"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def fetch_students():
    """
    Retrieve all students from the database, including their registered courses as a string e.g(Course1,Course2,Course3)

    Returns:
        list: A list of tuples representing the students and their registered courses.
              Each tuple contains (student_id, name, age, email, registered_courses).
              Returns an empty list if an error occurs.
    """
    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.student_id, s.name, s.age, s.email, 
                GROUP_CONCAT(e.course_id) AS registered_courses
            FROM Student s
            LEFT JOIN Enrollment e ON s.student_id = e.student_id
            GROUP BY s.student_id
        """)
        students = cursor.fetchall()
        return students
    except sqlite3.Error as e:
        return []
    finally:
        conn.close()

def add_student(student: Student):
    """
    Add a new student to the database.

    Args:
        student (Student): An instance of the Student class to be added.

    Returns:
        tuple: A tuple containing:
            - bool: True if the student was successfully added, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    valid, errors = student.validate()
    if not valid:
        return False, errors

    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Student (student_id, name, age, email) VALUES (?, ?, ?, ?)",
                       (student.student_id, student.name, student.age, student._email))
        conn.commit()
        return True, [f"Added student {student.name} to table"]
    except sqlite3.Error as e:
        return False, [str(e)]
    finally:
        conn.close()

def edit_student(student: Student):
    """
    Edit an existing student in the database.

    Args:
        student (Student): An instance of the Student class with updated data.

    Returns:
        tuple: A tuple containing:
            - bool: True if the student was successfully edited, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    valid, errors = student.validate()
    if not valid:
        return False, errors

    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Student SET name = ?, age = ?, email = ? WHERE student_id = ?",
                       (student.name, student.age, student._email, student.student_id))
        conn.commit()
        return True, [f"Edited student {student.name} in table"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def delete_student(student: Student):
    """
    Delete an existing student from the database.

    Args:
        student (Student): An instance of the Student class to be deleted.

    Returns:
        tuple: A tuple containing:
            - bool: True if the student was successfully deleted, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Enrollment WHERE student_id = ?", (student.student_id,))
        conn.commit()
        cursor.execute("DELETE FROM Student WHERE student_id = ?", (student.student_id,))
        conn.commit()
        return True, [f"Deleted student {student.name} from table"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def register_course(student: Student, course: Course):
    """
    Register a student to a course in the database.

    Args:
        student (Student): An instance of the Student class.
        course (Course): An instance of the Course class.

    Returns:
        tuple: A tuple containing:
            - bool: True if the student was successfully registered, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Enrollment (course_id, student_id) VALUES (?, ?)",
                       (course.course_id, student.student_id))
        conn.commit()
        return True, [f"Added student {student.name} to course {course.course_name}"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def unregister_course(student: Student, course : Course):
    """
    Unregister a student to a course in the database.

    Args:
        student (Student): An instance of the Student class.
        course (Course): An instance of the Course class.

    Returns:
        tuple: A tuple containing:
            - bool: True if the student was successfully unregistered, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Enrollment WHERE course_id = ? AND student_id = ?",
                       (course.course_id, student.student_id))
        conn.commit()
        return True, [f"Removed student {student.name} from course {course.course_name}"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def fetch_instructors():
    """
    Retrieve all instructors from the database, including their assigned courses as a string e.g(Course1,Course2,Course3)

    Returns:
        list: A list of tuples representing the intructors and their assigned courses.
              Each tuple contains (instructor_id, name, age, email, assigned_courses).
              Returns an empty list if an error occurs.
    """
    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT i.instructor_id, i.name, i.age, i.email, 
                GROUP_CONCAT(c.course_id) AS assigned_courses
            FROM Instructor i
            LEFT JOIN Course c ON i.instructor_id = c.instructor_id
            GROUP BY i.instructor_id
        """)
        instructors = cursor.fetchall()
        return instructors
    except sqlite3.Error as e:
        return []
    finally:
        conn.close()

def add_instructor(instructor: Instructor):
    """
    Add a new instructor to the database.

    Args:
        instructor (Instructor): An instance of the Instructor class to be added.

    Returns:
        tuple: A tuple containing:
            - bool: True if the instructor was successfully added, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    valid, errors = instructor.validate()
    if not valid:
        return False, errors

    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Instructor (instructor_id, name, age, email) VALUES (?, ?, ?, ?)",
                       (instructor.instructor_id, instructor.name, instructor.age, instructor._email))
        conn.commit()
        return True, [f"Added instructor {instructor.name} to table"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def edit_instructor(instructor: Instructor):
    """
    Edit an existing instructor in the database.

    Args:
        instructor (Instructor): An instance of the Instructor class with updated data.

    Returns:
        tuple: A tuple containing:
            - bool: True if the instructor was successfully edited, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    valid, errors = instructor.validate()
    if not valid:
        return False, errors

    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Instructor SET name = ?, age = ?, email = ? WHERE instructor_id = ?",
                       (instructor.name, instructor.age, instructor._email, instructor.instructor_id))
        conn.commit()
        return True, [f"Edited instructor {instructor.name} in table"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def delete_instructor(instructor: Instructor):
    """
    Delete an existing instructor from the database.

    Args:
        instructor (Instructor): An instance of the Instructor class to be deleted.

    Returns:
        tuple: A tuple containing:
            - bool: True if the instructor was successfully deleted, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Course SET instructor_id = NULL WHERE instructor_id = ?", (instructor.instructor_id,))
        conn.commit()
        cursor.execute("DELETE FROM Instructor WHERE instructor_id = ?", (instructor.instructor_id,))
        conn.commit()
        return True, [f"Deleted instructor {instructor.name} from table"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()
 
def assign_instructor(instructor : Instructor, course : Course):
    """
    Assigns an instructor to a course in the database. Changes the intructor_id field of the course

    Args:
        instructor (Instructor): An instance of the Instructor class.
        course (Course): An instance of the Course class.

    Returns:
        tuple: A tuple containing:
            - bool: True if the instructor was successfully assigned, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Course SET instructor_id = ? WHERE course_id = ?", (instructor.instructor_id,course.course_id))
        conn.commit()
        return True, [f"Added instructor {instructor.name} to course {course.course_name}"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

def unassign_instructor(instructor : Instructor, course : Course):
    """
    Unassigns an instructor to a course in the database. Changes the intructor_id field of the course

    Args:
        instructor (Instructor): An instance of the Instructor class.
        course (Course): An instance of the Course class.

    Returns:
        tuple: A tuple containing:
            - bool: True if the instructor was successfully unassigned, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    conn  : sqlite3.Connection = connect_db()
    cursor : sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Course SET instructor_id = NULL WHERE course_id = ? AND instructor_id = ?", (course.course_id,instructor.instructor_id))
        conn.commit()
        return True, [f"Removed instructor {instructor.name} from course {course.course_name}"]
    except sqlite3.Error as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()
