import sqlite3
from classes.Course import *

database_path = './databaseCRUD/database.db'

def connect_db():
    return sqlite3.connect(database_path)

def fetch_courses():
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
