import re


def valid_destination_name(destination):
    ''' validate destination name '''
    regex = "^[a-zA-Z0-9_ ]{1,}$"
    return re.match(regex, destination)


def valid_origin_name(origin):
    ''' validate origin name '''
    regex = "^[a-zA-Z0-9_ ]{5,}$"
    return re.match(regex, origin)


def valid_person_name(customer_name):
    '''validate person's name'''
    regex = "^[A-z][A-z|\.|\s]+$"
    return re.match(regex, customer_name) 


def valid_input(input):
    '''validate input'''
    regex = "^[a-zA-Z0-9_]{1,20}$"
    return re.match(regex,input) 

def valid_email(input):
    """Validate user email."""
    regex = "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
    return re.match(regex, input)

