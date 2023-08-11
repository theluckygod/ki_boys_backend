from __future__ import annotations

from typing import List, Union
from datetime import datetime
import json

from pydantic import BaseModel


class SubcriptionBase(BaseModel):
    id: int
    item_id: int
    user_id: str
    
    status: str
    message: Union[str, None] = None
    participants_num: int
    
    is_active: bool
    created_time: datetime
    
    class Config:
        orm_mode = True

class Subcription(SubcriptionBase):
    subcriber: UserBase
    item_info: ItemBase
    
    class Config:
        orm_mode = True


class SubcriptionCreate(BaseModel):
    item_id: int
    user_id: str
    
    message: Union[str, None] = None
    participants_num: Union[int, None] = 1
    

class ItemBase(BaseModel):
    id: int
    owner_id: str

    title: str
    description: Union[str, None] = None
    
    type: str
    location: Union[str, None] = None
    price: Union[float, None] = None
    max_participants: int
    start_time: Union[datetime, None] = None
    subcription_deadline: Union[datetime, None] = None
    
    is_active: bool
    created_time: datetime
    
    class Config:
        orm_mode = True

class Item(ItemBase):
    owner: UserBase
    subcribers: List[SubcriptionBase] = []

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    title: str
    description: Union[str, None] = None
    
    type: str
    location: Union[str, None] = None
    price: Union[float, None] = None
    max_participants: int
    start_time: Union[datetime, None] = None
    subcription_deadline: Union[datetime, None] = None
    

class UserBase(BaseModel):
    id: str
    name: str
    date_of_birth: Union[datetime, None]
    picture: str
    
    is_active: bool
    created_time: datetime
    
    class Config:
        orm_mode = True
    
class User(UserBase):
    items: List[ItemBase] = []
    subcriptions: List[SubcriptionBase] = []

    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    id: str
    name: str
    picture: str
    
    def from_json(data):
        return UserCreate(id=data["id"], name=data["name"], picture=json.dumps(data["picture"]))


Subcription.update_forward_refs()
Item.update_forward_refs()