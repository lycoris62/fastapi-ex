from typing import List

from pydantic import BaseModel


class Event(BaseModel):
  id: int
  title: str
  image: str
  description: str
  tags: List[str]
  location: str

  class Config:
    json_schema_extra = {
      "example": {
        "id": 1,
        "title": "title01",
        "image": "https://cataas.com/cat",
        "description": "desc01",
        "tags": ["cat", "cute"],
        "location": "Korea"
      }
    }
