from sqlalchemy.orm import Session

from api.boards.models import Board
from api.posts.models import Post
from api.users.models import User


# def get_user(db: Session, user_id: int):
#   return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(User).offset(skip).limit(limit).all()


def get_posts(db):
  return db.query(Post).all()


def get_boards(db):
  return db.query(Board).all()
