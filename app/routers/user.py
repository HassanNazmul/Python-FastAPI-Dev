from fastapi import Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db

router = APIRouter()


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
