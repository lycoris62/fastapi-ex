from typing import Optional, List

from pydantic import BaseModel, EmailStr

from models.events import Event


class User(BaseModel):
  email: EmailStr
  password: str
  events: Optional[List[Event]]

  class Config:
    json_schema_extra = {
      "example": {
        "email": "ex01@planner.com",
        "password": "qwer1234",
        "events": []
      }
    }


class UserSignIn(BaseModel):
  email: EmailStr
  password: str

  class Config:
    json_schema_extra = {
      "example": {
        "email": "ex01@planner.com",
        "password": "qwer1234"
      }
    }
