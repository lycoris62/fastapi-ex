from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from database.connection import engine, Base, SessionLocal

app = FastAPI()


@app.on_event("startup")
def init_db():
  Base.metadata.create_all(bind=engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.get("/users")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  users = crud.get_users(db, skip=skip, limit=limit)
  return users
