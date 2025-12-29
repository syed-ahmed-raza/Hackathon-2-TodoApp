from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import auth, tasks, chat
from database import create_db_and_tables

load_dotenv()

app = FastAPI()

# 👇 ALLOW ALL ORIGINS (Taake Vercel ke naye links block na hon)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Wildcard: Sab allowed hain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo App Backend is Running!"}