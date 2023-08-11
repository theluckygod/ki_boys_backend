from __future__ import annotations

from typing import List, Union
from datetime import datetime

from pydantic import BaseModel


class SubcriptionBase(BaseModel):
    id: int
    item_id: int
    user_id: int
    
    status: str
    message: Union[str, None] = None
    participants_num: int
    
    is_active: bool
    created_time: datetime
    
    class Config:
        orm_mode = True

class Subcription(SubcriptionBase):
    owner: UserBase
    item_info: ItemBase
    
    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    id: int
    owner_id: int

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


class UserBase(BaseModel):
    id: int
    name: str
    date_of_birth: datetime
    
    is_active: bool
    created_time: datetime
    
    class Config:
        orm_mode = True
    
class User(UserBase):
    items: List[ItemBase] = []
    subcriptions: List[SubcriptionBase] = []

    class Config:
        orm_mode = True


Subcription.update_forward_refs()
Item.update_forward_refs()