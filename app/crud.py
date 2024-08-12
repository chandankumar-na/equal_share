from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group
    
def delete_group(db: Session, group_id: int):
    try:
        db_group = db.query(models.Group).filter(models.Group.id == group_id).one()
        db.delete(db_group)
        db.commit()
        return db_group
    except NoResultFound:
        db.rollback()
        raise ValueError("Group not found.")

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(
        description=expense.description, 
        amount=expense.amount, 
        payer_id=expense.payer_id,
        group_id=expense.group_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense
