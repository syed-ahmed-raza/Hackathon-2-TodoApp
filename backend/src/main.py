from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes import auth, tasks, chat
from database import create_db_and_tables

# Environment variables load karein
load_dotenv()

app = FastAPI()

# CORS Fix: Taake Vercel (Frontend) aur Render (Backend) aapas mein baat kar sakein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Production mein ise specific Vercel URL par set karna behtar hai
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Database tables create karein
    create_db_and_tables()

# Routes Fix: Prefix aur Tags add kiye hain taake frontend calls (/auth, /tasks) sahi se kaam karein
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo App Backend is Running!"}