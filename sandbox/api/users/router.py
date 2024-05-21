from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.users.models import User
from database.connection import get_db

user_router = APIRouter(
    tags=["User"]
)


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
