from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.hash_password import HashPassword
from database.connection_mongo import Database
from models.users import User, TokenResponse

user_router = APIRouter(
    tags=["User"]
)

users = {}
hash_password = HashPassword()

user_database = Database(User)


@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
  user_exist = await User.find_one(User.email == user.email)
  if user_exist:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User with supplied username exists"
    )

  hashed_password = hash_password.create_hash(user.password)
  user.password = hashed_password
  users[user.email] = user

  await user_database.save(user)
  return {
    "message": "User successfully registered!"
  }


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
  user_exist = await User.find_one(User.email == user.username)

  if not user_exist:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User does not exist"
    )
  if not hash_password.verify_hash(user.password, user_exist.password):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Wrong credentials passed"
    )

  return {
    "message": "User signed in successfully."
  }
