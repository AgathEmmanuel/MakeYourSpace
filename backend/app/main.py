from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
import time
from psycopg2.extras import RealDictCursor
import db_credential


app = FastAPI()

class Post(BaseModel):
    user_id: int
    title: str
    description: Optional[str]=None
    content: Optional[str]=None

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

sample_posts=[]

@app.get("/post")
def get_posts():
    db_cursor.execute("""SELECT * FROM posts""")
    posts=db_cursor.fetchall()
    print("get_post initiated")
    return {"message": posts}



@app.post("/post",status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    db_cursor.execute("""INSERT INTO posts (user_id,title,content,description) VALUES (%s,%s,%s,%s) RETURNING * """,(payload.user_id,payload.title,payload.content,payload.description))
    post_created = db_cursor.fetchone()
    db_connect.commit()
    return {"message": post_created}


def find_post(id):
    for posti in sample_posts:
        if posti["id"]==id:
            return posti


@app.get("/post/{id}")
def get_post(id: int, response: Response ):
    db_cursor.execute("""SELECT * from posts WHERE user_id = %s """,(str(id)))
    post_with_id = db_cursor.fetchone()
    if not post_with_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"post_data": post_with_id }


def delete_post_index(id):
    for i,p in enumerate(sample_posts):
        if p['id']==id:
            print(p)
            return i

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    db_cursor.execute("""DELETE FROM posts WHERE user_id = %s returning *""", (str(id)))
    post_deleted = db_cursor.fetchone()
    db_connect.commit()
    if post_deleted==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update_post_index(id):
    for i,p in enumerate(sample_posts):
        if p['id']==id:
            print(p)
            return i


@app.put("/post/{id}")
def update_post(id: int, updated_payload: Post):
    print(updated_payload)
    db_cursor.execute("""UPDATE posts SET title = %s, content = %s, description = %s WHERE user_id = %s RETURNING *""",(updated_payload.title,updated_payload.content,updated_payload.description,str(id)))
    updated_post = db_cursor.fetchone()
    db_connect.commit()
    if update_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    return {'message': updated_post}
