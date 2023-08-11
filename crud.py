from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_subcriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subcription).offset(skip).limit(limit).all()


def create_subcription(db: Session, subcription: schemas.SubcriptionCreate, item_id: int, user_id: int):
    db_subcription = models.Subcription(**subcription.dict(), item_id=item_id, user_id=user_id)
    db.add(db_subcription)
    db.commit()
    db.refresh(db_subcription)
    return db_subcription