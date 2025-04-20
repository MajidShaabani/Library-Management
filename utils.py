import json
import os
import re

# Validation functions
def validate_isbn(isbn):
    # Simple validation: ISBN must be 10 or 13 digits
    isbn = isbn.replace("-", "").replace(" ", "")
    if len(isbn) not in [10, 13]:
        return False
    
    # Check if all characters are digits
    if not isbn.isdigit():
        # ISBN-10 can end with 'X'
        if len(isbn) == 10 and isbn[:-1].isdigit() and isbn[-1].upper() == 'X':
            return True
        return False
    
    return True

def validate_name(name):
    # Name should be at least 2 characters and contain only letters and spaces
    if len(name) < 2:
        return False
    return bool(re.match(r"^[a-zA-Z\s]+$", name))

def validate_contact(contact):
    # Simple email or phone validation with regex
    # Email pattern
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    # Phone pattern (10 digits)
    phone_pattern = r"^\d{10}$"
    
    if re.match(email_pattern, contact) or re.match(phone_pattern, contact):
        return True
    return False

def validate_integer(input_str):
    try:
        int(input_str)
        return True
    except ValueError:
        return False

def get_valid_input(prompt, validator_func, error_msg):
    while True:
        user_input = input(prompt)
        if validator_func(user_input):
            return user_input
        print(f"Error: {error_msg}")

# File handling functions
def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []