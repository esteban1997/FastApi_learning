from ..database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from pydantic import BaseModel,Field

class Users(Base):
  __tablename__ = 'users'
  id = Column(Integer,primary_key=True,index=True)
  email = Column(String,unique=True)
  username = Column(String,unique=True)
  first_name = Column(String)
  last_name = Column(String)
  hashed_password = Column(String)
  is_active = Column(Boolean,default=True)
  role = Column(String)
  phone_number = Column(String)

class Todos(Base):
  __tablename__ = 'todos'
  id = Column(Integer,primary_key=True,index=True)
  title = Column(String)
  descripcion = Column(String)
  priority = Column(Integer)
  complete = Column(Boolean,default=False)
  owner_id = Column(Integer,ForeignKey("users.id"))
  
class TodoRequest(BaseModel):
  title:str = Field(min_length=3)
  descripcion:str = Field(max_length=100)
  priority:int = Field(gt=0,lt=6)
  complete:bool