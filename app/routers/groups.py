from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud as crud
import models as models
import  schema as schemas

from database import SessionLocal

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db=db, group=group)

@router.get("/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group
    
@router.get("/", response_model= list[schemas.Group])
def read_group( db: Session = Depends(get_db)):
    db_groups = crud.get_groups(db)
    if db_groups is None:
        raise HTTPException(status_code=404, detail="Groups not found")
    return db_groups

@router.delete("/groups/{group_id}", response_model=schemas.Group)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    try:
        deleted_group = crud.delete_group(db, group_id)
        return deleted_group
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
