from jose import JWTError, jwt 
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional
import schemas
from datetime import datetime, timedelta  

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = "09d25e094faa6ca25adfadfaagljafaldfjld56c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_access_token(token: str, auth_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,ALGORITHM) 
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise auth_exception
        jwt_token_data = schemas.JwtTokenData(user_id=user_id)
    except JWTError:
        raise auth_exception
    return jwt_token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return validate_access_token(token,auth_exception)