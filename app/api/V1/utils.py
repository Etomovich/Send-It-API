import re


def valid_destination_name(destination):
    """Test destination name if valid."""
    regex = "^[a-zA-Z0-9_ ]{1,}$"
    return re.match(regex, destination)


def valid_origin_name(origin):
    """Test origin name."""
    regex = "^[a-zA-Z0-9_ ]{5,}$"
    return re.match(regex, origin)


def valid_person_name(customer_name):
    """Test person name."""
    regex = "^[a-zA-Z ]{4,}$"
    return re.match(regex, customer_name) 


def validate_input(input):
    """Validate input."""
    regex = "^[a-zA-Z0-9_]{1,20}$"
    return re.match(regex,input)   
