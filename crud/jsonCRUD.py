import json

file_path = "./data.json"

def load_json():
    """
    Load data from a JSON file.

    Reads the JSON data from the file specified by `file_path` and returns it.

    Returns:
        dict: The data loaded from the JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_data(new_data):
    """
    Save data to a JSON file.

    Writes the given data to the JSON file specified by `file_path`.

    Args:
        new_data (dict): The data to be saved into the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(new_data, f, indent=4)

def add_entry_json(table_type, entry):
    """
    Add a new entry to a specified table in the JSON data.

    Validates the entry and adds it to the specified table in the JSON data if it doesn't already exist.

    Args:
        table_type (str): The type of table to which the entry should be added, 'Course', 'Student', or 'Instructor'
        entry (object): An object representing the entry to be added. Entry can be Course, Student, Instructor

    Returns:
        tuple: A tuple containing:
            - bool: True if the entry was successfully added, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    data = load_json()

    if table_type not in data:
        return False,["Table does not exist"]
    
    valid , errors = entry.validate()

    if not valid:
        return valid, errors
    
    id = str(getattr(entry, "course_id", None) or getattr(entry, "student_id", None) or getattr(entry, "instructor_id", None))
    
    for _, item in enumerate(data[table_type]):
            if item.get('student_id') == id or item.get('course_id') == id or item.get('instructor_id')== id:
                print(item,id)
                return False, [f'{table_type} already exists in table']

    data[table_type].append(entry.__dict__)

    save_data(data)
    return True, [f"Added {table_type} to table"]

def edit_entry_json(table_type, entry):
    """
    Edit an existing entry in a specified table in the JSON data.

    Validates the entry and updates the existing entry in the specified table.

    Args:
        table_type (str): The type of table in which the entry should be edited, 'Course', 'Student', or 'Instructor'
        entry (object): An object representing the entry to be edited. Entry can be Course, Student, Instructor

    Returns:
        tuple: A tuple containing:
            - bool: True if the entry was successfully edited, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    data = load_json()

    if table_type not in data:
        return False,["Table does not exist"]
    
    valid , errors = entry.validate()

    if not valid:
        return valid, errors
    
    id = getattr(entry, "course_id", None) or getattr(entry, "student_id", None) or getattr(entry, "instructor_id", None)
    
    not_in_table = True
    for index, item in enumerate(data[table_type]):
            if item.get('student_id') == id or item.get('course_id') == id or item.get('instructor_id') == id:
                data[table_type][index] = entry.__dict__
                not_in_table = False
                break
    
    if not_in_table:
        return False, [f'{table_type} not in table']

    save_data(data)
    return True, [f"Editted {table_type} in table"]

def delete_entry_json(table_type, entry):
    """
    Delete an existing entry from a specified table in the JSON data.

    Finds and removes the entry from the specified table based on the entry's ID.

    Args:
        table_type (str): The type of table from which the entry should be deleted, 'Course', 'Student', or 'Instructor'
        entry (object): An object representing the entry to be deleted. Entry can be Course, Student, Instructor

    Returns:
        tuple: A tuple containing:
            - bool: True if the entry was successfully deleted, False otherwise.
            - list: A list of messages indicating success or errors encountered.
    """
    data = load_json()

    if table_type not in data:
        return False,["Table does not exist"]
    
    id = getattr(entry, "course_id", None) or getattr(entry, "student_id", None) or getattr(entry, "instructor_id", None)

    not_in_table = True
    for index, item in enumerate(data[table_type]):
            if item.get('student_id') == id or item.get('course_id') == id or item.get('instructor_id') ==id:
                data[table_type].pop(index)
                not_in_table = False
                break

    if not_in_table:
        return False, [f'{table_type} not in table']

    save_data(data)
    return True, [f"Deleted {table_type} from table"]