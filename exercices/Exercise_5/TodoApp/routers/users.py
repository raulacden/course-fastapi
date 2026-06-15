from typing import Annotated

from fastapi import APIRouter, Depends,  HTTPException, Path
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from models import User
from .auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

    
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerificationRequest(BaseModel):
    password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(User).filter(User.id == user.get("id")).first()

@router.put("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerificationRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_model = db.query(User).filter(User.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user.get('id')} not found")
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    
@router.put("/me/change-phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_model = db.query(User).filter(User.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user.get('id')} not found")
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()