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


def get_items(db: Session, owner_id: str = None, sport: str = None, skip: int = 0, limit: int = 100):
    temp = db.query(models.Item)
    
    if owner_id is not None:
        temp = temp.filter(models.Item.owner_id == owner_id)
    
    if sport is not None:
        temp = temp.filter(models.Item.type == sport)
    
    return temp.offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_subcriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subcription).offset(skip).limit(limit).all()


def get_subcriptions_me(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Subcription).filter(models.Subcription.user_id == user_id).offset(skip).limit(limit).all()


def create_subcription(db: Session, subcription: schemas.SubcriptionCreate, user_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == subcription.item_id).first()
    if db_item is None:
        raise Exception("Item not found")
    
    if db_item.max_participants <= sum([sub.participants_num for sub in db_item.subcriptions if sub.is_active]): # and sub.status == 'accepted'
        raise Exception("Item is full")
    
    db_subcription = db.query(models.Subcription).filter(models.Subcription.item_id == subcription.item_id) \
                    .filter(models.Subcription.user_id == user_id).first()
    if db_subcription is not None:
        if db_subcription.is_active == False:
            db_subcription.is_active = True
            db.commit()
            db.refresh(db_subcription)
        return db_subcription
    
    db_subcription = models.Subcription(**subcription.dict(), user_id=user_id)
    db.add(db_subcription)
    db.commit()
    db.refresh(db_subcription)
    return db_subcription


def cancel_item(db: Session, item_id: int, user_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item.owner_id == user_id:
        db_item.is_active = False
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        raise Exception("You are not the owner of this item")
    

def leave_subcription(db: Session, subcription_id: int, user_id: int):
    db_subcription = db.query(models.Subcription).filter(models.Subcription.id == subcription_id).first()
    if db_subcription.user_id == user_id:
        db_subcription.is_active = False
        db.commit()
        db.refresh(db_subcription)
        return db_subcription
    else:
        raise Exception("You are not the owner of this subcription")
    

def leave_item_subcription(db: Session, item_id: int, user_id: int):
    db_subcription = db.query(models.Subcription).filter(models.Subcription.item_id == item_id) \
                    .filter(models.Subcription.user_id == user_id).first()
    if db_subcription is not None:
        db_subcription.is_active = False
        db.commit()
        db.refresh(db_subcription)
        return db_subcription
    else:
        raise Exception("You are not the owner of this subcription")