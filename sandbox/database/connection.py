from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://dev:devpw@127.0.0.1:21000/dev"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # 로그에 SQL 문 찍힘
    # connect_args={
    #   "check_same_thread": False  # 이 부분은 SQLite 만 필요
    # }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


# engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL,
#     echo=True,  # 로그에 SQL 문 찍힘
#     connect_args={
#       "check_same_thread": False  # 이 부분은 SQLite 만 필요
#     })
#
# AsyncSessionLocal = async_sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )
#
#
#
# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#   session = AsyncSessionLocal()
#   try:
#     yield session
#   finally:
#     await session.close()

# SQLite 는 async 를 지원하지 않음.

Base = declarative_base()
