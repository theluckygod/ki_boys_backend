from typing import Union, List
from typing_extensions import Annotated
import requests

from fastapi import FastAPI, Header, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
AUTHORIZED_TOKENS = {}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def verify_token(req: Request):
    token = req.headers["token"]
    if token not in AUTHORIZED_TOKENS:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return AUTHORIZED_TOKENS[token]


@app.get("/users/me")
async def get_me(token: Annotated[str, Header()], db: Session = Depends(get_db)):
    if token not in AUTHORIZED_TOKENS:
        # response = requests.get(url="https://graph.zalo.me/v2.0/me",
        #                         headers={"access_token": token})
    
        response = {
            "is_sensitive": False,
            "name": "Tùng Nguyễn",
            "id": "3681046936240438345",
            "error": 0,
            "message": "Success",
            "picture": {
                "data": {
                    "url": "https://s120-ava-talk.zadn.vn/a/a/6/e/37/120/84f0ddd1d0f1edf0831c92cf4960e3ec.jpg"
                }
            }
        }
        
        user = schemas.UserCreate.from_json(response)
        db_user = crud.get_user(db, user_id=user.id)
        if db_user is None:
            db_user = crud.create_user(db=db, user=user)
    else:
        db_user = AUTHORIZED_TOKENS[token]

    AUTHORIZED_TOKENS[token] = db_user
    return db_user


@app.get("/users/", response_model=List[schemas.User])
async def read_users(user_info: schemas.User = Depends(verify_token), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/items/", response_model=List[schemas.Item])
@app.get("/api/list", response_model=List[schemas.Item])
async def read_items(user_info: schemas.User = Depends(verify_token), sport: Union[str, None] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, sport=sport, skip=skip, limit=limit)
    return items


@app.get("/subcriptions/", response_model=List[schemas.Subcription])
async def read_subcriptions(user_info: schemas.User = Depends(verify_token), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subcriptions = crud.get_subcriptions(db, skip=skip, limit=limit)
    return subcriptions

@app.post("/api/register/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, user_info: schemas.User = Depends(verify_token), db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item, user_id=user_info.id)

@app.post("/api/join", response_model=schemas.Subcription)
async def create_subcription(subcription: schemas.SubcriptionCreate, 
                             user_info: schemas.User = Depends(verify_token), 
                             db: Session = Depends(get_db)):
    return crud.create_subcription(db=db, subcription=subcription, item_id=subcription.item_id, user_id=user_info.id)


if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--log_level", type=str, default="info")
    args = parser.parse_args()

    uvicorn.run("main:app", host=args.host, port=args.port,
                workers=args.workers, log_level=args.log_level, reload=True)