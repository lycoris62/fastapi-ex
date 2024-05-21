from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.boards.models import Board
from api.boards.schemas import BoardCreate
from database.connection import get_db

board_router = APIRouter(
    tags=["Board"]
)


@board_router.get("")
def get_boards(db: Session = Depends(get_db)):
  boards = db.query(Board).all()
  return boards


@board_router.get("/{id}")
def get_board(id: int, db: Session = Depends((get_db))):
  board = db.query(Board).get(id)
  return board


@board_router.post("")
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
  db_board = Board(name=board.name, public=board.public, creator_id=board.creator_id)
  db.add(db_board)
  db.commit()
  db.refresh(db_board)
  return db_board


@board_router.patch("/{id}")
def update_board(id: int, board: BoardCreate, db: Session = Depends(get_db)):
  db_board = db.query(Board).get(id)
  db_board.name = board.name
  db_board.public = board.public
  db.commit()
  return db_board


@board_router.delete("/{id}")
def update_board(id: int, db: Session = Depends(get_db)):
  db.query(Board).filter(Board.id == id).delete()
  db.commit()
