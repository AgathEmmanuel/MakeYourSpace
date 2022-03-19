from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
from fastapi.params import Body
import psycopg2
import time
from psycopg2.extras import RealDictCursor
import db_credential
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")




models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try: 
        db_connect = psycopg2.connect(host='localhost',database=db_credential.db_database,user=db_credential.db_user,password=db_credential.db_password,cursor_factory=RealDictCursor) 
        db_cursor = db_connect.cursor()
        print("Connected to the database succesfully")
        break
    except Exception as error:
        print("Connection to the database failed")
        print(error)
        time.sleep(3)





# for this get request having .app() function we are getting a list as output
# and adding response_model=schemas.PostGetResponse results in validation error
@app.get("/post",response_model=List[schemas.PostGetResponse])
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    print(type(posts))
    return posts

@app.post("/post",status_code=status.HTTP_201_CREATED,response_model=schemas.PostCreateResponse)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post_new=models.Post(**payload.dict())
    db.add(post_new)
    db.commit()
    db.refresh(post_new)
    return post_new


@app.get("/post/{id}",response_model=schemas.PostGetResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post_with_id=db.query(models.Post).filter(models.Post.post_id==id).first()
    if not post_with_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post_with_id 


@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_deleted=db.query(models.Post).filter(models.Post.post_id==id)
    if post_deleted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post_deleted.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}",response_model=schemas.PostUpdateResponse)
def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db)):
    updated_payload = db.query(models.Post).filter(models.Post.post_id == id)
    if updated_payload.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    updated_payload.update(post.dict(),synchronize_session=False)
    db.commit()
    return post

@app.get("/user/{username}",response_model=schemas.UserGetResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    user=db.query(models.Accounts).filter(models.Accounts.username==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, info=f"user with user: {username} do not exist")
    return user

@app.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.UserCreateResponse)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    password_hashed = password_context.hash(payload.password)
    payload.password = password_hashed
    user_new=models.Accounts(**payload.dict())
    db.add(user_new)
    db.commit()
    db.refresh(user_new)
    return user_new

