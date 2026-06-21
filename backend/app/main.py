from fastapi import FastAPI
from .routes.videos import router as video_router
from .database import engine
from .models import Base
from .routes.users import router as user_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(video_router)

@app.get("/")
def root():
    return {"message": "API Running"}
