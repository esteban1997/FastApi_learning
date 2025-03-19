from fastapi import APIRouter,Depends,HTTPException,status,Path
from ..models.models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
  prefix='/user',
  tags=['user']
)

def get_db():
  db = SessionLocal()

  try:
    yield db
  finally:
    db.close()
    
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
  if user is None:
    raise HTTPException(status_code=401,detail='Authentication Failed')
  
  user_model = db.query(Users).filter(Users.username==user.get('username')).first()
  return user_model


@router.put("/change_password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(old_password:str,new_password:str,user:user_dependency,db:db_dependency):
  if user is None:
    raise HTTPException(status_code=401,detail='Authentication Failed')
  
  user_model = db.query(Users).filter(Users.id==user.get('id')).first()
  
  if user_model is None or not bcrypt_context.verify(old_password, user_model.hashed_password):
    raise HTTPException(status_code=401,detail='Incorrect password')
  
  user_model.hashed_password= bcrypt_context.hash(new_password)
  
  db.add(user_model)
  db.commit()
  
  return {"message": "Password changed successfully"}

@router.put("/phonenumber/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency,db:db_dependency,phone_number:str):
  if user is None:
    raise HTTPException(status_code=401,detail='Authentication Failed')
  user_model = db.query(Users).filter(Users.id==user.get('id')).first()
  user_model.phone_number=phone_number
  db.add(user_model)
  db.commit()