from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from requests import Response


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


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Get all posts from Database
@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()  # Fatching all post
    return {"Message": posts}


# Cteate new post
@app.post("/posts", status_code=201)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published))
    new_post = cursor.fetchone()  # Fatching one post
    conn.commit()  # Save data changes on DB
    return{"MESSAGE": new_post}


# Get post by ID
@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return {"Post Detail": post}


# Delete Post
@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()  # Save data changes on DB

    if deleted_post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")
    return Response(status_code=HTTPException)


# Update Post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UP id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()  # Save data changes on DB

    if deleted_post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")
    return Response(status_code=HTTPException)
