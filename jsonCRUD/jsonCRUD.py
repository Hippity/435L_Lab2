import json

file_path = "./jsonCRUD/data.json"

def load_json():
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_data(new_data):
    with open(file_path, 'w') as f:
        json.dump(new_data, f, indent=4)

def add_entry_json(table_type, entry):

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