import re

class Person:
    def __init__(self,name :str, age: int, email: str):
        self.name = name
        self.age = age
        self._email = email

    def __str__(self):
        return self.name
    
    def introduce(self):
        return f"Hi, my name is {self.name} and I am {self.age} years old."
    
    def validate(self):
        errors = []

        if self.age == "" or not self.age or self.age < 17:
            errors.append("Not a valid age")
        if len(self.name) <= 1:
            errors.append("Not a valid name")
        if not is_valid_email(self._email):
            errors.append("Not a valid email")

        if errors:
            return False, errors
        else:
            return True, ["Validation Passed!"]

    @classmethod
    def from_json(cls, json_object : dict):
        name = json_object.get("name")
        age = json_object.get("age")
        email = json_object.get("_email")  
        return name, age, email
    
    @classmethod
    def from_db(cls, db_object : tuple):
        name = db_object[1]
        age = db_object[2]
        email = db_object[3]
        return name, age, email
    

def is_valid_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, email):
        return True
    else:
        return False
