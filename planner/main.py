import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from database.connection_mongo import Settings
from routes.events import event_router
from routes.users import user_router

app = FastAPI()
settings = Settings()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# @app.on_event("startup")
# def on_startup():
#   conn()

@app.on_event("startup")
async def init_db():
  await settings.initialize_database()


@app.get("/")
async def home():
  return RedirectResponse(url="/event/")


if __name__ == "__main__":
  uvicorn.run("main.app", host="127.0.0.1", port=8000, reload=True)
