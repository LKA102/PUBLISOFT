from dataclasses import dataclass
import bcrypt

@dataclass(frozen=True)
class EmailVO:
    """
    Value Object for Email.
    This class encapsulates the email address and ensures its validity.
    """
    
    email: str
        
    def __str__(self):
        return self.email

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate the email format using a simple regex pattern.
        """
        import re
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None
    

@dataclass(frozen=True)
class UserCodeVO:
    """
    Value Object for User Code.
    This class encapsulates the user code and ensures its validity.
    """
    
    user_code: str

    def __str__(self):
        return self.user_code
    
    # Temporary method
    @classmethod
    def generate_user_code(cls) -> 'UserCodeVO':
        """
        Generate a random user code.
        For simplicity, let's assume the user code is a random string number with max 8 digits.
        """
        import random

        first_digit = random.choice(['1', '2'])
        remaining_digits = ''.join(random.choices('0123456789', k=7))
        user_code = first_digit + remaining_digits
        return cls(user_code=user_code)
    
    @staticmethod
    def is_valid_user_code(user_code: str) -> bool:
        """
        Validate the user code format.
        For simplicity, let's assume a valid user code is alphanumeric and between 5 to 20 characters.
        """
        return isinstance(user_code, str) and user_code.isalnum() and 5 <= len(user_code) <= 20
    
@dataclass(frozen=True)
class PasswordHashVO:
    """
    Value Object for Password Hash.
    This class encapsulates the hashed password and provides methods for password hashing and verification.
    """
    
    hash_password: str

    def __str__(self):
        return self.hash_password
    
    @staticmethod
    def is_valid_hash_password(hash_password: str) -> bool:
        """
        Validate the password hash format.
        For simplicity, let's assume a valid hash is a non-empty string.
        """
        return isinstance(hash_password, str) and len(hash_password) > 0

    @staticmethod
    def generate_hash_password(password: str) -> 'PasswordHashVO':
        """
        Hash the given password using bcrypt.
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return PasswordHashVO(hash_password=hashed.decode('utf-8'))
    
    @staticmethod
    def verify_password(password: str, hash_passwordVO: 'PasswordHashVO') -> bool:
        """
        Static method to verify the given password against the stored hash.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hash_passwordVO.hash_password.encode('utf-8'))