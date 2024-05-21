from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class Post(Base):
  __tablename__ = "posts"

  id = Column(BigInteger, primary_key=True, autoincrement=True)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  board_id = Column(BigInteger, ForeignKey("boards.id"))
  author_id = Column(BigInteger, ForeignKey("users.id"))

  author = relationship("User", back_populates="posts")
  board = relationship("Board", back_populates="posts")
