from enum import Enum

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from database.connection import Base


class UserRole(Enum):
  MEMBER = "member"


class User(Base):
  __tablename__ = "users"

  id = Column(BigInteger, primary_key=True, autoincrement=True)
  full_name = Column(String, nullable=False, unique=True)
  email = Column(String, nullable=False, unique=True)
  password = Column(String)

  boards = relationship("Board", back_populates="creator")
  posts = relationship("Post", back_populates="author")
