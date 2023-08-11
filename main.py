from typing import Union, List
from typing_extensions import Annotated
import requests

from fastapi import FastAPI, Header, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/me")
async def get_me(token: Annotated[str, Header()]):
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
    return response


@app.get("/users/", response_model=List[schemas.User])
async def read_users(token: Annotated[str, Header()], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/items/", response_model=List[schemas.Item])
def read_items(token: Annotated[str, Header()], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/subcriptions/", response_model=List[schemas.Subcription])
def read_subcriptions(token: Annotated[str, Header()], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subcriptions = crud.get_subcriptions(db, skip=skip, limit=limit)
    return subcriptions


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