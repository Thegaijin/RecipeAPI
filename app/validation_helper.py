import re


def username_validator(username):
    """ The function validates the username input.
        It checks if the input matches the expected string structure

        :param str username: The username input
        :return: the username if it meets the specification otherwise false
    """
    username_pattern = re.compile(r'^[a-zA-Z_]+([a-zA-Z0-9]{1,10})$')
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


def email_validator(password):
    """ The function validates the email string entered.
        It checks if the email matches the specified email format

        :param str email: The email input
        :return: the username if it meets the specification otherwise false
    """
    # [A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$
    email_pattern = re.compile(
        r'(^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]+$)')
    if email_pattern.match(password):
        return True
    return False


def name_validator(name):
    """ The function validates the recipe and category name inputs.
        It checks if the name meets the expected structure of input

        :param str name: The recipe or category name input
        :return: the name if it meets the specification otherwise false
    """
    name_pattern = re.compile(r'[a-zA-Z\s]+')
    result = name_pattern.match(name)
    if result is None:
        return False
    result = result.group()
    if len(result) is len(name):
        return True
    return False
