from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class Board(Base):
  __tablename__ = "boards"

  id = Column(BigInteger, primary_key=True, autoincrement=True)
  name = Column(String, nullable=False, unique=True)
  public = Column(Boolean, nullable=False, default=True)
  creator_id = Column(BigInteger, ForeignKey("users.id"))

  creator = relationship("User", back_populates="boards")
  posts = relationship("Post", back_populates="board")
