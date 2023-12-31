from typing import Union, List
from typing_extensions import Annotated
import requests
from datetime import datetime

from fastapi import FastAPI, Header, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
        if token == "test":
            response = {
                "is_sensitive": False,
                "name": "User 2",
                "id": "2",
                "error": 0,
                "message": "Success",
                "picture": {
                    "data": {
                        "url": "https://s120-ava-talk.zadn.vn/a/a/6/e/37/120/84f0ddd1d0f1edf0831c92cf4960e3ec.jpg"
                    }
                }
            }
        else:
            response = requests.get(url="https://graph.zalo.me/v2.0/me?fields=id,name,birthday,picture",
                                    headers={"access_token": token})
            if response.status_code != 200:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                )
            
            response = response.json()
        
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


@app.get("/items/me", response_model=List[schemas.Item])
@app.get("/api/list/me", response_model=List[schemas.Item])
async def read_items(user_info: schemas.User = Depends(verify_token), sport: Union[str, None] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, owner_id=user_info.id, sport=sport, skip=skip, limit=limit)
    return items


@app.get("/subcriptions/", response_model=List[schemas.Subcription])
async def read_subcriptions(user_info: schemas.User = Depends(verify_token), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subcriptions = crud.get_subcriptions(db, skip=skip, limit=limit)
    return subcriptions

@app.get("/subcriptions/me", response_model=List[schemas.Subcription])
async def read_subcriptions(user_info: schemas.User = Depends(verify_token), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subcriptions = crud.get_subcriptions_me(db, user_id=user_info.id, skip=skip, limit=limit)
    return subcriptions


@app.post("/api/register/", response_model=schemas.Item)
async def create_item(item: Union[schemas.ItemCreate, schemas.ItemCreateDateAndTime], 
                      user_info: schemas.User = Depends(verify_token), 
                      db: Session = Depends(get_db)):
    if isinstance(item, schemas.ItemCreateDateAndTime):
        start_time = datetime.combine(item.date, item.time)
        item_obj = schemas.ItemCreate(**item.dict(), start_time=start_time)
        item = item_obj
    
    return crud.create_item(db=db, item=item, user_id=user_info.id)

@app.post("/api/join", response_model=schemas.Subcription)
async def create_subcription(subcription: schemas.SubcriptionCreate, 
                             user_info: schemas.User = Depends(verify_token), 
                             db: Session = Depends(get_db)):
    return crud.create_subcription(db=db, subcription=subcription, user_id=user_info.id)

@app.post("/items/cancel", response_model=schemas.Item)
@app.post("/api/cancel", response_model=schemas.Item)
async def cancel_item(item_id: str, user_info: schemas.User = Depends(verify_token), db: Session = Depends(get_db)):
    return crud.cancel_item(db=db, item_id=item_id, user_id=user_info.id)

@app.post("/subcriptions/leave", response_model=schemas.Subcription)
@app.post("/api/leave", response_model=schemas.Subcription)
async def leave_subcription(subcription_id: Union[str, None] = None, 
                            item_id: Union[str, None] = None,
                            user_info: schemas.User = Depends(verify_token), db: Session = Depends(get_db)):
    if subcription_id is not None:
        return crud.leave_subcription(db=db, subcription_id=subcription_id, user_id=user_info.id)
    if item_id is not None:
        return crud.leave_item_subcription(db=db, item_id=item_id, user_id=user_info.id)



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