from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes import auth, tasks, chat
from database import create_db_and_tables

load_dotenv()

app = FastAPI()

# 👇 YEH HAI FIX: Vercel ka exact URL list mein dalein
origins = [
    "*", # Testing ke liye sab allowed
    "https://hackathon-2-todo-acwvp8t2c-syed-ahmed-razas-projects.vercel.app", # Aapka Vercel URL
    "https://hackathon-2-todoapp.vercel.app" # Backup main URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Updated origins list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Routes setup
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo App Backend is Running!"}