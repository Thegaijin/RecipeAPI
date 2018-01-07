# validation_helper.py
''' This scripts handles the data input validations '''
import re


def username_validator(username):
    """ The function validates the username input.
        It checks if the input matches the expected string structure

        :param str username: The username input
        :return: the username if it meets the specification otherwise false
    """
    username_pattern = re.compile(r'^\w+([a-zA-Z0-9]{1,10})$')
    if username_pattern.match(username):
        return True
    return False


def password_validator(password):
    """ The function validates the username input.
        It checks if the input matches the expected string structure

        :param str username: The username input
        :return: the username if it meets the specification otherwise false
    """
    password_pattern = re.compile(r'^\w{6,25}$')
    if password_pattern.match(password):
        return True
    return False


def name_validator(name):
    """ The function validates the recipe and category name inputs.
        It checks if the input matches the expected string structure

        :param str name: The recipe or category name input
        :return: the name if it meets the specification otherwise false
    """
    name_pattern = re.compile(r'[a-zA-Z\s]+')
    result = name_pattern.match(name)
    result = result.group()
    if len(result) is len(name):
        return True
    return False


def details_validator(details):
    """ The function validates the username input.
        It checks if the input matches the expected string structure

        :param str username: The username input
        :return: the username if it meets the specification otherwise false
    """
    details_pattern = re.compile(r'^[a-zA-Z\,\'\.\s]+$')
    result = details_pattern.match(details)
    result = result.group()
    if len(result) is len(details):
        return True
    return False
