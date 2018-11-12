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
    regex = "^[a-zA-Z ]{4,}$"
    return re.match(regex, customer_name) 


def validate_input(input):
    '''validate input'''
    regex = "^[a-zA-Z0-9_]{1,20}$"
    return re.match(regex,input)   


    
def valid_destination(destination):
    '''validate destination name'''
    regex = "^[a-zA-Z 0-9]{3,}$"
    return re.match(regex, destination)