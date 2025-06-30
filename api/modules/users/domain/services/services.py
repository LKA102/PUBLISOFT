
def validate_email_format(email: str) -> bool:
    """
    Validates the format of an email address.
    
    Args:
        email (str): The email address to validate.
        
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None