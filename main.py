from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional,List
from database import SessionLocal
import models

app = FastAPI()


class User(BaseModel):
    id:int
    name:str
    email:str
    password:str
    
    class Config:
        orm_model=True

class Login(BaseModel):
    name:str
    password:str

db=SessionLocal()

@app.get('/users',response_model=List[User],status_code=200)
def getall():
    users=db.query(models.User).all()

    return users

@app.post('/save',response_model=User,status_code=201)
def saveuser(user:User):

    db_item=db.query(models.User).filter(models.User.name==user.name).first()

    if db_item is not None:
        raise status.HTTP_302_FOUND
    
    new_item=models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_item)
    db.commit()

    return new_item

@app.put('/login')
def login(luse:Login):

    item_to_update=db.query(models.User).filter(models.User.name==luse.name).first()
    if item_to_update is None:
         raise status.HTTP_400_BAD_REQUEST

    return item_to_update