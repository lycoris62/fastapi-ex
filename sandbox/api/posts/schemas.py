from pydantic import BaseModel


class PostCreate(BaseModel):
  title: str
  content: str
  author_id: int
  board_id: int
 