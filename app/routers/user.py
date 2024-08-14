from ..import models, schemas,utils
from fastapi import FastAPI, HTTPException, Response,status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=['Users']
     )
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    #hash the password - user.password
    hashed_passord = utils.hash(user.password)
    user.password = hashed_passord
    new_user = models.User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    return user