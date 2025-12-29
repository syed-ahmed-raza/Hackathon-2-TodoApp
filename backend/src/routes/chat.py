import os
import google.generativeai as genai
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from dotenv import load_dotenv
from database import get_db
from security import get_current_user_id 
from crud import create_task, get_tasks, delete_task, get_recent_task_by_title, update_task

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

# 👇 Language & Personality Settings
SYSTEM_INSTRUCTION = """
You are a smart and helpful AI Task Assistant for a Todo App. 🤖

**LANGUAGE RULES (CRITICAL):**
1.  **DEFAULT:** Always reply in **ENGLISH** by default.
2.  **ADAPTABILITY:** If (and ONLY if) the user speaks in **Roman Urdu** or **Hindi** (e.g., "Kaise ho?", "Task add kardo"), then you **MUST** switch to **Roman Urdu**.
    - User: "Add a task to buy milk." -> You: "Done! I've added the task 'Buy milk' ✅."
    - User: "Doodh lane ka task add karo." -> You: "Ji zaroor! 'Doodh lana' task add kar diya hai ✅."

**Personality:**
- Be friendly, professional, and concise.
- Use emojis to make the chat lively (✅, 📝, 🗑️).

**Your Tools:**
- You can Add, Delete, View, and Update tasks.
- You MUST call the tool/function to perform the action. Do not just say you did it.
"""

@router.post("") 
async def chat_agent(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # --- Tool Definitions ---
    def add_my_task(title: str, description: str = ""):
        cleaned_new_title = title.strip().lower()
        existing_tasks = get_tasks(db, current_user_id)
        for task in existing_tasks:
            if task.title.strip().lower() == cleaned_new_title:
                return "Info: Task already exists."
        final_description = description if description else ""
        create_task(db, title, final_description, current_user_id)
        return f"Success: Task '{title}' added ✅."

    def delete_my_task(task_identifier: str):
        try:
            task_id = int(task_identifier)
            tasks = get_tasks(db, current_user_id)
            task_to_delete = next((task for task in tasks if task.id == task_id), None)
            if task_to_delete and task_to_delete.user_id == current_user_id:
                title = task_to_delete.title
                delete_task(db, task_id, current_user_id)
                return f"Success: Deleted '{title}' 🗑️."
        except ValueError:
            tasks = get_tasks(db, current_user_id)
            task_to_delete = None
            for task in tasks:
                if task.title.strip().lower() == task_identifier.strip().lower():
                    task_to_update = task
                    break
            if not task_to_delete:
                 for task in tasks:
                    if task_identifier.strip().lower() in task.title.strip().lower():
                        task_to_delete = task
                        break
            if task_to_delete:
                title = task_to_delete.title
                delete_task(db, task_to_delete.id, current_user_id)
                return f"Success: Deleted '{title}' 🗑️."
            return f"Error: Task '{task_identifier}' not found."

    def get_my_tasks():
        tasks = get_tasks(db, current_user_id)
        if not tasks:
            return "Your task list is empty."
        return "\n".join([f"- {t.title} (ID: {t.id}) {'✅' if t.completed else '⏳'}" for t in tasks])

    def update_my_task(task_identifier: str, title: str = None, description: str = None, is_completed: bool = None):
        task_to_update = None
        try:
            task_id = int(task_identifier)
            tasks = get_tasks(db, current_user_id)
            task_to_update = next((task for task in tasks if task.id == task_id), None)
        except ValueError:
            tasks = get_tasks(db, current_user_id)
            for task in tasks:
                if task.title.strip().lower() == task_identifier.strip().lower():
                    task_to_update = task
                    break
        
        if task_to_update:
            update_task(db, task_to_update.id, current_user_id, is_completed, title, description)
            return f"Success: Task updated ✅."
        return "Error: Task not found."

    tools = [add_my_task, get_my_tasks, delete_my_task, update_my_task]
    
    # 👇 SMART MODEL SELECTION (No more guessing)
    # Hum pehle standard models try karenge, agar wo nahi chale to API se pochenge
    model_list = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    
    # Koshish karein ke live models bhi list kar lein (Agar API allow kare)
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                name = m.name.replace("models/", "")
                if name not in model_list:
                    model_list.append(name)
    except:
        pass # Agar list_models fail ho jaye (permission issue), to standard list use karein

    last_error = "No models available"

    # Jo bhi pehla chal jaye, wo winner 🏆
    for model_name in model_list:
        try:
            model = genai.GenerativeModel(
                model_name=model_name, 
                tools=tools, 
                system_instruction=SYSTEM_INSTRUCTION
            )
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(request.message)
            return response.text # Agar success, to yahi return kardo aur loop khatam
        except Exception as e:
            last_error = str(e)
            continue # Agar fail, to agla model try karo
    
    # Agar sab fail ho jayen
    return f"Sorry, I am having trouble connecting to AI. Error: {last_error}"