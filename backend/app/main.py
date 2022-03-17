from multiprocessing import synchronize
from os import sync
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
import time
from psycopg2.extras import RealDictCursor
import db_credential
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    user_id: int
    title: str
    description: Optional[str]=None
    content: Optional[str]=None
    post_status: Optional[bool]=True
    post_id: int

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


@app.get("/")
def root():
    print()
    return {"message": "Helloooooo Worldddddddddddd"}


@app.get("/users")
def create_user(db: Session = Depends(get_db)):
    post=db.query(models.Post).all()
    return {"message":post}

@app.get("/post")
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"message": posts}



@app.post("/post",status_code=status.HTTP_201_CREATED)
def create_post(payload: Post, db: Session = Depends(get_db)):
    post_created=models.Post(**payload.dict())
    db.add(post_created)
    db.commit()
    db.refresh(post_created)
    return {"message": post_created}


@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post_with_id=db.query(models.Post).filter(models.Post.post_id==id).first()
    if not post_with_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"post_data": post_with_id }


@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_deleted=db.query(models.Post).filter(models.Post.post_id==id)
    if post_deleted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post_deleted.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id: int, post: Post,db: Session = Depends(get_db)):
    updated_payload = db.query(models.Post).filter(models.Post.post_id == id)
    updated_post=updated_payload.first()
    print(updated_post)
    if updated_payload.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    updated_payload.update(post.dict(),synchronize_session=False)
    db.commit()
    return {'message': updated_payload.first()}
