from fastapi import Cookie, HTTPException, status
from typing import Annotated
from jose import jwt
from config.settings import settings


def getcurrentuser(required: bool = True):
    def _gettoken(accesstoken: Annotated[str, Cookie()] = None):
        if not required and not accesstoken:
            return None
        try:
            if not accesstoken:
                raise Exception("Login required")
            obj = jwt.decode(accesstoken, settings.JWT_SECRET)
            loginuser = dict(
                id_user=obj.get("id_user"),
                email=obj.get("email"),
                role=obj.get("role"),
                user_code=obj.get("user_code")
            )
            return loginuser
        except Exception as e:
            print(str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Login required",
            )
    return _gettoken