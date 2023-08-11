from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    date_of_birth = Column(DateTime)
    picture = Column(String)

    is_active = Column(Boolean, nullable=False, server_default='fnord')
    created_time = Column(DateTime, nullable=False, server_default='fnord')
    
    items = relationship("Item", back_populates="owner")
    subcriptions = relationship("Subcription")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    
    title = Column(String, nullable=False)
    description = Column(String)
    
    type = Column(String)
    location = Column(String)
    price = Column(Float)
    max_participants = Column(Integer)
    start_time = Column(DateTime)
    subcription_deadline = Column(DateTime)

    is_active = Column(Boolean, nullable=False, server_default='fnord')
    created_time = Column(DateTime, nullable=False, server_default='fnord')

    owner = relationship("User", back_populates="items")
    subcribers = relationship("Subcription")
    
class Subcription(Base):
    __tablename__ = "subcriptions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(String, ForeignKey("users.id"))
    
    status = Column(String, nullable=False, default='waiting')
    message = Column(String)
    participants_num = Column(Integer, nullable=False)
       
    is_active = Column(Boolean, nullable=False, server_default='fnord')
    created_time = Column(DateTime, nullable=False, server_default='fnord')
    
    subcriber = relationship("User")
    item_info = relationship("Item")