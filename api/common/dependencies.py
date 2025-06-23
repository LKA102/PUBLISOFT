# Here we will define global dependencies for the application.
from fastapi import Cookie, HTTPException, status
from typing import Annotated 
from jose import jwt 
from config import settings

def getcurrentuser(required: bool = True):
    def _gettoken(accesstoken: Annotated[str, Cookie()] = None):
        if not required and not accesstoken:
            return None
        try:
            if not accesstoken:
                raise Exception("Login required")
            obj = jwt.decode(accesstoken, settings.JWT_SECRET)
            loginuser = dict(
                bplevel=obj["bplevel"],
                bpcode=obj["bpcode"],
                loginid=obj["loginid"],
                loginemail=obj["loginemail"],
                loginname=obj["loginname"],
                bpname=obj["bpname"],
                bpparentcode=obj["bpparentcode"],
                pricelist=obj["pricelist"],
            )
            return loginuser
        except Exception as e:
            print(str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Login required",
            )
    return _gettoken
