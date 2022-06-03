from typing import List
from fastapi import Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["POSTS"]
)


# Get all posts using SQLalchemy / ORM
@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()

    return post


# Cteate new post using SQLalchemy / ORM
@router.post("/", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content,published=post.published)
    new_post = models.Post(**post.dict())  # Using Pydantic Model

    db.add(new_post)  # Add new post on BD
    db.commit()  # Save data changes on DB
    db.refresh(new_post)  # Refresh the DB

    return new_post


# Get post by ID using SQLalchemy / ORM
@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post


# Delete Post using SQLalchemy / ORM
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")

    post.delete(synchronize_session=False)

    db.commit()  # Save data changes on DB

    return Response(status_code=204)


# Update Post using SQL Queries
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()  # Save data changes on DB

    return post_query.first()
