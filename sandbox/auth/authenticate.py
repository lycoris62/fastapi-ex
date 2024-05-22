from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.users.models import User
from auth.hash_password import HashPassword

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")


# async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
#   if not token:
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="Sign in for access"
#     )
#
#   decoded_token = verify_access_token(token)
#   return decoded_token["user"]


def authenticate_user(email: str, password: str, db: Session):
  user = db.query(User).filter(User.email == email).first()
  if not user:
    return False
  if not HashPassword.verify_password(password, user.password):
    return False
  return user

# def authenticate(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> str:
#   if not token:
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="Sign in for access"
#     )
#
#   decoded_token = verify_access_token(token, db)
#   return decoded_token["user"]
