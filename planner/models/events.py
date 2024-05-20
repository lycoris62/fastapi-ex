from typing import List, Optional

from beanie import Document
from pydantic import BaseModel


class Event(Document):
  title: str
  image: str
  description: str
  location: str
  tags: List[str]

  class Config:
    arbitrary_types_allowed = True
    json_schema_extra = {
      "example": {
        "title": "title01",
        "image": "https://cataas.com/cat",
        "description": "desc01",
        "tags": ["cat", "cute"],
        "location": "Korea"
      }
    }

  class Settings:
    name = "events"


class EventUpdate(BaseModel):
  title: Optional[str]
  image: Optional[str]
  description: Optional[str]
  tags: Optional[List[str]]
  location: Optional[str]

  class Config:
    arbitrary_types_allowed = True
    json_schema_extra = {
      "example": {
        "title": "title01",
        "image": "https://cataas.com/cat",
        "description": "desc01",
        "tags": ["cat", "cute"],
        "location": "Korea"
      }
    }

# class Event(SQLModel, table=True):
#   id: Optional[int] = Field(default=None, primary_key=True)
#   title: str
#   image: str
#   description: str
#   location: str
#   tags: List[str] = Field(sa_column=Column(JSON))
#
#   class Config:
#     arbitrary_types_allowed = True
#     json_schema_extra = {
#       "example": {
#         "id": 1,
#         "title": "title01",
#         "image": "https://cataas.com/cat",
#         "description": "desc01",
#         "tags": ["cat", "cute"],
#         "location": "Korea"
#       }
#     }
#
#
# class EventUpdate(SQLModel):
#   title: Optional[str]
#   image: Optional[str]
#   description: Optional[str]
#   tags: Optional[List[str]]
#   location: Optional[str]
#
#   class Config:
#     arbitrary_types_allowed = True
#     json_schema_extra = {
#       "example": {
#         "title": "title01",
#         "image": "https://cataas.com/cat",
#         "description": "desc01",
#         "tags": ["cat", "cute"],
#         "location": "Korea"
#       }
#     }
