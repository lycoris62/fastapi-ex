from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

import crud
from api.boards.router import board_router
from api.posts.router import post_router
from api.users.router import user_router
from database.connection import engine, Base, get_db

origins = [
  "http://127.0.0.1:8000",
  "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,  # 더 자세한 정보는 여기에. https://fastapi.tiangolo.com/ko/tutorial/cors/
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users")
app.include_router(board_router, prefix="/boards")
app.include_router(post_router, prefix="/posts")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
  return PlainTextResponse("이건 검증 핸들러로 한 거지롱~~~ : " + str(exc), status_code=400)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
  return PlainTextResponse("이건 http 핸들러로 한 거지롱~~~ : " + str(exc.detail), status_code=exc.status_code)


@app.on_event("startup")
def init_db():
  Base.metadata.create_all(bind=engine)


@app.get("/users")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  users = crud.get_users(db, skip=skip, limit=limit)
  return users
