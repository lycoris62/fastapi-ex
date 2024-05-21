from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.posts.models import Post
from api.posts.schemas import PostCreate
from database.connection import get_db

post_router = APIRouter(
    tags=["Post"]
)


@post_router.get("")
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(Post).all()
  return posts


@post_router.get("/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
  post = db.query(Post).get(id)
  return post


@post_router.post("")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
  db_post = Post(title=post.title, content=post.content, board_id=post.board_id, author_id=post.author_id)
  db.add(db_post)
  db.commit()
  db.refresh(db_post)
  return db_post


@post_router.patch("/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
  db_post = db.query(Post).get(id)
  db_post.title = post.title
  db_post.content = post.content
  db.commit()
  db.refresh(db_post)
  return db_post


@post_router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
  db.query(Post).filter(Post.id == id).delete()
  db.commit()
