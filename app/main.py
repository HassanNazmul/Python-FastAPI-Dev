from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, Depends, status
import psycopg2
import time
from psycopg2.extras import RealDictCursor

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


@app.get("/")
def root():
    return {"Message": "HELLO FAST-API"}


# Get all posts using SQL Queries
@app.get("/query/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()  # Fatching all post

    return {"detail": posts}


# Cteate new post using SQL Queries
@app.post("/query/posts", status_code=201)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published))
    new_post = cursor.fetchone()  # Fatching one post

    conn.commit()  # Save data changes on DB

    return{"detail": new_post}


# Get post by ID using SQL Queries
@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return {"Post Detail": post}


# Delete Post using SQL Queries
@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()

    conn.commit()  # Save data changes on DB

    if deleted_post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Post using SQL Queries
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UP id = %s RETURNING *""", (str(id)))
    post = cursor.fetchone()

    conn.commit()  # Save data changes on DB

    if post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")
    return Response(status_code=HTTPException)


# Get all posts using SQLalchemy / ORM
@app.get("/orm/posts")
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()

    return {"detail": post}


# Cteate new post using SQLalchemy / ORM
@app.post("/orm/posts", status_code=201)
def create_post(post: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content,published=post.published)
    new_post = models.Post(**post.dict())  # Using Pydantic Model

    db.add(new_post)  # Add new post on BD
    db.commit()  # Save data changes on DB
    db.refresh(new_post)  # Refresh the DB

    return{"detail": new_post}


# Get post by ID using SQLalchemy / ORM
@app.get("/orm/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return {"detail": post}


# Delete Post using SQLalchemy / ORM
@app.delete("/orm/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")

    post.delete(synchronize_session=False)

    db.commit()  # Save data changes on DB

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Post using SQL Queries
@app.put("/orm/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")

    post_query.update(updated_post.dict(), synchronize_session=False)

    conn.commit()  # Save data changes on DB

    return {"detail": post_query.first()}
