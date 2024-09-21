import re

class Person:
    def __init__(self,name :str, age: int, email: str):
        """
        Initializes a Person instance with the provided details.

        Args:
            name (str): The name of the person.
            age (int): The age of the person.
            email (str): The email address of the person.
        """
        self.name = name
        self.age = age
        self._email = email

    def __str__(self):
        """
        Returns the string representation of the person.

        Returns:
            str: The name of the person.
        """
        return self.name
    
    def introduce(self):
        """
        Provides a self-introduction string.

        Returns:
            str: A string introducing the person with their name and age.
        """
        return f"Hi, my name is {self.name} and I am {self.age} years old."
    
    def validate(self):
        """
        Validates the person's details, ensuring that the age is above 17, the name is not too short,
        and the email is in a valid format.

        Returns:
            tuple: A tuple containing:
                - bool: True if validation passed, False otherwise.
                - list: A list of messages indicating success or errors encountered.
        """
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
        """
        Extracts and returns the person's details from a JSON object.

        Args:
            json_object (dict): A dictionary representing the person's data.

        Returns:
            tuple: A tuple containing (name, age, email).
        """
        name = json_object.get("name")
        age = json_object.get("age")
        email = json_object.get("_email")  
        return name, age, email
    
    @classmethod
    def from_db(cls, db_object : tuple):
        """
        Extracts and returns the person's details from a database tuple.

        Args:
            db_object (tuple): A tuple representing the person's data from the database.

        Returns:
            tuple: A tuple containing (name, age, email).
        """
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
