from typing import Optional, List

from sqlmodel import SQLModel, Field


class Event(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str
  image: str
  description: str
  location: str
  tags: List[str]
