import schemas
import models
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import engine, get_db
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

router = APIRouter()


@router.get("/user/{username}",response_model=schemas.UserGetResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    user=db.query(models.Accounts).filter(models.Accounts.username==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with user: {username} do not exist")
    return user

@router.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.UserCreateResponse)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    password_hashed = password_context.hash(payload.password)
    payload.password = password_hashed
    user_new=models.Accounts(**payload.dict())
    db.add(user_new)
    db.commit()
    db.refresh(user_new)
    return user_new

