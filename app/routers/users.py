from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud as crud
import models as models
import  schema as schemas
from database import SessionLocal

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
    
@router.get("/", response_model= list[schemas.User])
def read_users( db: Session = Depends(get_db)):
    db_users = crud.get_users(db)
    if db_users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return db_users
