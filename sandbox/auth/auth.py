# from fastapi import Depends
# from fastapi.security import OAuth2PasswordBearer
# from passlib.context import CryptContext
#
# from api.users.models import User
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def verify_password(plain_password, hashed_password):
#   return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#   return pwd_context.hash(password)
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#   user = User(full_name="name03", email="name03@naver.com", password="!qwer1234")
#   return user
