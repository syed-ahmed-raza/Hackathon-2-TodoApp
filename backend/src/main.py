from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import auth, tasks, chat
from database import create_db_and_tables

load_dotenv()

app = FastAPI()

# 👇 FINAL FIX: Regex use kar rahe hain taake Vercel ke sare domains allow hon
# '*' aur allow_credentials=True ek saath illegal hain, isliye regex zaroori hai.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Vercel ke sab links allow
    allow_origins=["http://localhost:3000"],      # Localhost allow
    allow_credentials=True,                       # Cookies/Tokens allow
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