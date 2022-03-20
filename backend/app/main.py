from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
import time
from psycopg2.extras import RealDictCursor
import db_credential
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from routers import user,post




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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



app.include_router(post.router)
app.include_router(user.router)


