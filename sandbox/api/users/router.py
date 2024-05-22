from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from api.users.models import User
from api.users.schemas import UserSignup, UserLogin
from auth.authenticate import authenticate_user
from auth.hash_password import HashPassword
from auth.jwt_handler import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from database.connection import get_db

user_router = APIRouter(
    tags=["User"]
)


class Token(BaseModel):
  access_token: str
  token_type: str


# @user_router.post("/signup")
# async def signup(user: User):
#   pass

@user_router.get("")
def get_users(db: Session = Depends(get_db)):
  users = db.query(User).all()
  return users


@user_router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(User).get(id)
  return user


@user_router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup, db: Session = Depends(get_db)):
  db_user = User(full_name=user.full_name, email=user.email, password=user.password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


@user_router.post("/signup/token", status_code=status.HTTP_201_CREATED)
def signup2(user: UserSignup, db: Session = Depends(get_db)):
  hashed_password = HashPassword.get_password_hash(user.password)
  db_user = User(full_name=user.full_name, email=user.email, password=hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


@user_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.email == user.email).first()
  if not db_user or db_user.password != user.password:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="못찾음"
    )
  return db_user


@user_router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
      data={"sub": user.email}, expires_delta=access_token_expires
  )
  return Token(access_token=access_token, token_type="bearer")
  # return access_token

# @user_router.get("")
# async def get_users(session: Annotated[AsyncSessionLocal, Depends(get_session)]):
#   result = await session.excute(select(User))
#   users = result.scalars().all()
#   return users

# @user_router.post("/signup")
# async def sign_new_user(user: User) -> dict:
#   user_exist = await User.find_one(User.email == user.email)
#   if user_exist:
#     raise HTTPException(
#         status_code=status.HTTP_409_CONFLICT,
#         detail="User with supplied username exists"
#     )
#
#   hashed_password = hash_password.create_hash(user.password)
#   user.password = hashed_password
#   users[user.email] = user
#
#   await user_database.save(user)
#   return {
#     "message": "User successfully registered!"
#   }
