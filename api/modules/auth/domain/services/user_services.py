from modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.auth.domain.value_objects.vo import PasswordHashVO
from modules.auth.domain.entities.user import User

def validar_credenciales(email: str, password: str, uok: SqlAlchemyUnitOfWork) -> User:
    """
    Validate user credentials.
    This function checks if the provided email and password are valid.
    """
    # Load the user by email
    user = uok.user_repository.load_by_email(email)
    if not user:
        raise ValueError("User not found")

    # Verify the password
    if not PasswordHashVO.verify_password(password, user.hash_password):
        raise ValueError("Invalid password")
    
    return user
    

