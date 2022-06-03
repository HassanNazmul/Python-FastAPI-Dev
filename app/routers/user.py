from typing import List
from fastapi import Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db

router = APIRouter()


# Get all users using SQLalchemy
@router.get("/users", response_model=List[schemas.UserOut])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user


# Cteate new User using SQLalchemy
@router.post("/users", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.passwoed
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())  # Using Pydantic Model

    db.add(new_user)  # Add new post on BD
    db.commit()  # Save data changes on DB
    db.refresh(new_user)  # Refresh the DB

    return new_user


# Get users by ID using SQLalchemy
@router.get("/users/{id}", response_model=schemas.UserIDOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} dose not EXIST!")

    return user


# Update Post using SQL Queries
@router.put("/users/{id}", response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)

    user = user_query.first()

    if user == None:
        raise HTTPException(
            status_code=404, detail=f"User with id: {id} dose not EXIST!")

    user_query.update(updated_user.dict(), synchronize_session=False)

    db.commit()  # Save data changes on DB

    return user_query.first()


# Delete User using SQLalchemy
@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if user.first() == None:
        raise HTTPException(
            status_code=404, detail=f"User with id: {id} dose not EXIST!")

    user.delete(synchronize_session=False)

    db.commit()  # Save data changes on DB

    return Response(status_code=204)
