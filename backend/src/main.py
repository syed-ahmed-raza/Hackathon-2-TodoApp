from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
from .routes import auth, tasks, chat

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins hata dein ya comment kar dein
    allow_origin_regex="https://.*\.vercel\.app",  # <--- Yeh Jadoo karega (Sab Vercel links allowed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)
