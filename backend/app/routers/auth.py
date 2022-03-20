from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import engine, get_db
import schemas
import models
from routers import oauth2
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  



password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


router = APIRouter(
    prefix="/authenticate",
    tags=['Authenticate']
)


@router.post('/',response_model=schemas.UserLoginResponse)
def login_user(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): 
    user_info = db.query(models.Accounts).filter(or_(models.Accounts.email==payload.username,models.Accounts.username==payload.username)).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"The Credentials are invalid with no user info")
    if not password_context.verify(payload.password,user_info.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"The Credentials are invalid with password filure")

    jwt_token = oauth2.create_access_token(data={"user_id": user_info.username})
    return {"jwt_token": jwt_token,"token_type": "bearer"}

    
