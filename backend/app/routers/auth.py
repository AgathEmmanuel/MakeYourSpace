from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import engine, get_db
import schemas
import models
from routers import oauth2
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


router = APIRouter(
    prefix="/authenticate",
    tags=['Authenticate']
)


@router.post('/')
def login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)): 
    user_info = db.query(models.Accounts).filter(models.Accounts.email==payload.email).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Credentials are invalid")
    if not password_context.verify(payload.password,user_info.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Credentials are invalid")

    jwt_token = oauth2.create_access_token(data={"user_id": user_info.username})
    return {"token": jwt_token,"token_type": "bearer"}

    
