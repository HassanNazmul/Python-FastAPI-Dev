from typing import List
from .database import engine, get_db
from . import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, Depends, status
import psycopg2
import time
from psycopg2.extras import RealDictCursor

from .routers import post, user


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Database Connection
while True:  # Run While Loop
    try:
        conn = psycopg2.connect(
            host="localhost", database="fastapi", user="postgres",
            password="root", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Succsessfull!")
        break  # If Database Connected Stop The LOOP
    except Exception as error:
        print("Connection to database Failed")
        print("Error: ", error)
        time.sleep(10)  # If Database Not Connected Run the LOOP Again in 10sec


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"Message": "HELLO FAST-API"}
