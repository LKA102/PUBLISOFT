from domain.entities.user_entity import UserEntity
from domain.value_objects.email_vo import EmailVO
from domain.repositories.interfaces.user_interface_repo import UserRepositoryInterface
from supabase import create_client
from config.settings import global_supabase_client
from shared.utils import get_supabase_client

class AuthService:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    def register_user(self, email: str, password: str, role: int) -> UserEntity:
        # Create a new user in Supabase
        response = global_supabase_client.auth.sign_up(email=email, password=password)
        
        if response.error:
            raise Exception(f"Error creating user: {response.error.message}")

        # Extract user data from the response
        user_data = response.user
        user_entity = UserEntity(
            id_user=user_data.id,
            email=EmailVO(email),
            id_role=role,
            user_code=user_data.user_metadata.get("user_code", "default_code")
        )

        # Save the user to the database
        self.user_repo.save(user_entity)

        return user_entity