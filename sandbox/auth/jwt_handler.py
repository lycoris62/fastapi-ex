import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends
from jwt import InvalidTokenError, PyJWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from api.users.models import User
from auth.authenticate import oauth2_scheme
from database.connection import get_db

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
  email: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def verify_access_token(token: str, db: Session) -> dict:
  try:
    data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

    expire = data.get("expires")

    if expire is None:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="No access token supplied"
      )
    if datetime.utcnow() > datetime.utcfromtimestamp(expire):
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Token expired!"
      )
    # user_exist = User.find_one(User.email == data["user"])
    user_exist = db.query(User).filter(User.email == data["email"]).first()

    if not user_exist:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Invalid token"
      )

    return data

  except PyJWTError:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token"
    )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
    token_data = TokenData(email=email)
  except InvalidTokenError:
    raise credentials_exception
  # user = get_user(fake_users_db, username=token_data.username)
  user = db.query(User).filter(User.email == email).first()
  if user is None:
    raise credentials_exception
  return user

# def create_access_token(user: str):
#   payload = {
#     "user": user,
#     "expires": time.time() + 3600
#   }
#
#   token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
#   return token


# def verify_access_token(token: str):
#   try:
#     data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#     expire = data.get("expires")
#
#     if expire is None:
#       raise HTTPException(
#           status_code=status.HTTP_400_BAD_REQUEST,
#           detail="No access token supplied"
#       )
#     if datetime.utcnow() > datetime.utcfromtimestamp(expire):
#       raise HTTPException(
#           status_code=status.HTTP_403_FORBIDDEN,
#           detail="Token expired!"
#       )
#     return data
#
#   except JWTError:
#     raise HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         detail="Invalid token"
#     )
