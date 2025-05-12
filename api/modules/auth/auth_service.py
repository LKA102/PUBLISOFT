from domain.entities.user_entity import UserEntity
from domain.value_objects.email_vo import EmailVO
from domain.repositories.interfaces.user_interface_repo import UserRepositoryInterface
from enums.state_enum import StateEnum
from supabase import create_client
from config.settings import settings, global_supabase_client
from shared.utils import get_supabase_client
import random
import string
from jose import jwt

class AuthService:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo
        
    def login_user(self, email: str, password: str):
        # Authenticate the user with Supabase
        response = global_supabase_client.auth.sign_in_with_password(credentials={
            "email": email,
            "password": password
        })
        
        if not response:
            raise Exception(f"Error logging in user: {response.error.message}")
        
        
        # Extract user data from the response
        session = response.session
        supabase_access_token = session.access_token
        supabase_refresh_token = session.refresh_token
        expires_in = session.expires_in
        
        # Fetch additional user data (e.g., role) from your database
        user_entity = self.user_repo.get_by_email(email)
        if not user_entity:
            raise Exception("User not found in the database")
        
        # Create own custom JWT payload
        payload = {
            "id_user": str(user_entity.id_user),
            "email": str(user_entity.email),
            "role": user_entity.id_role,
            "user_code": user_entity.user_code,
            "supabase_access_token": supabase_access_token,
            "supabase_refresh_token": supabase_refresh_token,
        }
        
        jwt_token = jwt.encode(payload, settings.JWT_SECRET)
        return {
            "access_token": jwt_token,
            "expires_in": expires_in,
            "token_type": "bearer"
            }
        
        
        

    def register_user(self, email: str, password: str, role: int) -> UserEntity:
        # Create a new user in Supabase
        response = global_supabase_client.auth.sign_up(credentials={
            "email": email,
            "password": password
        })
        
        if not response:
            raise Exception(f"Error creating user: {response.error.message}")

        # Extract user data from the response
        user_data = response.user

        user_entity = UserEntity(
            id_user=user_data.id,
            email=EmailVO(email),
            id_role=role,
            id_state=StateEnum.ACTIVO.value,
            user_code=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) #This is temporary, should be replaced with a proper user code generation logic
        )

        # Save the user to the database
        self.user_repo.save(user_entity)

        return user_entity