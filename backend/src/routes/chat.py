import os
import time
import google.generativeai as genai
from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel
from dotenv import load_dotenv
from database import get_db
# 👇 FIX: 'auth' ki jagah 'security' kar diya
from security import get_current_user_id 
from crud import create_task, get_tasks, delete_task, get_recent_task_by_title, update_task

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Router prefix main.py handle kar raha hai, yahan zaroorat nahi
router = APIRouter()

class ChatRequest(BaseModel):
    message: str

# ✅ Route bilkul sahi hai (POST /chat banega)
@router.post("/") 
async def chat_agent(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # ... (Baaki code bilkul same rahega, usme koi change nahi) ...
    # --- Tool Definitions ---
    def add_my_task(title: str, description: str = ""):
        """Adds a new task to the user's list with an optional description. Be concise."""
        cleaned_new_title = title.strip().lower()
        existing_tasks = get_tasks(db, current_user_id)
        
        for task in existing_tasks:
            if task.title.strip().lower() == cleaned_new_title:
                return "Info: A task with this name already exists."
        
        if get_recent_task_by_title(db, title, current_user_id):
            return "Info: A task with this name already exists."
        
        final_description = description if description else ""
        create_task(db, title, final_description, current_user_id)
        return "Success: Task added."

    def delete_my_task(task_identifier: str):
        """Deletes a task by its ID or a case-insensitive name search."""
        try:
            task_id = int(task_identifier)
            tasks = get_tasks(db, current_user_id)
            task_to_delete = next((task for task in tasks if task.id == task_id), None)
            
            if task_to_delete and task_to_delete.user_id == current_user_id:
                title = task_to_delete.title
                delete_task(db, task_id, current_user_id)
                return f"Successfully deleted '{title}'."
            else:
                return f"Could not find a task with ID '{task_identifier}'."
        except ValueError:
            tasks = get_tasks(db, current_user_id)
            task_to_delete = None
            
            for task in tasks:
                if task.title.strip().lower() == task_identifier.strip().lower():
                    task_to_delete = task
                    break
            
            if not task_to_delete:
                for task in tasks:
                    if task_identifier.strip().lower() in task.title.strip().lower():
                        task_to_delete = task
                        break

            if task_to_delete:
                title = task_to_delete.title
                delete_task(db, task_to_delete.id, current_user_id)
                return f"Successfully deleted '{title}'."
            else:
                return f"Could not find a task named '{task_identifier}'. Please check the spelling."

    def get_my_tasks():
        """Gets all of the user's tasks in a clean, bulleted list."""
        tasks = get_tasks(db, current_user_id)
        if not tasks:
            return "You have no tasks."
        return "\n".join([f"- {t.title} (ID: {t.id}, Status: {'Completed' if t.completed else 'Pending'})" for t in tasks])

    def update_my_task(task_identifier: str, title: str = None, description: str = None, is_completed: bool = None):
        """Updates a task's title, description, or status (completed)."""
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
            if not task_to_update:
                for task in tasks:
                    if task_identifier.strip().lower() in task.title.strip().lower():
                        task_to_update = task
                        break

        if task_to_update:
            updated_task = update_task(db, task_to_update.id, current_user_id, is_completed, title, description)
            if updated_task:
                return "Success: Task updated ✅."
            else:
                return "Error: Failed to update task ❌."
        else:
            return "Error: Task not found ❌."

    # --- Universal Model Discovery and Fallback Logic ---
    tools = [add_my_task, get_my_tasks, delete_my_task, update_my_task]
    system_instruction = """You are a smart, friendly, and professional AI Assistant for a Todo App.

**CRITICAL RULE:**
- You **cannot** perform actions just by replying with text. 
- You **MUST** call the provided tools (`add_my_task`, `delete_my_task`, `get_my_tasks`, `update_my_task`) to actually change the database.
- Do not confirm an action unless you have called the tool.

**Guidelines:**
1. **Language Adaptability:**
   - English -> Professional English.
   - Roman Urdu/Hindi -> Reply in Roman Urdu (e.g., "Ji zaroor, task add kar diya ✅").
2. **Personality:** Be polite and use emojis (✅, 🗑️, 📝).
3. **Task Operations:**
   - **Adding:** Call `add_my_task` first. Then say: "Done! ✅ I've added '[Task Name]'."
   - **Deleting:** Call `delete_my_task` with the NAME. Then say: "Deleted '[Task Name]' 🗑️."
   - **Listing:** Call `get_my_tasks`.
   - **Updating (Renaming/Completing):** Call `update_my_task` with the task name or ID, and the new title, description, or `is_completed` status.
4. **Filters:** - If user asks for "Pending" tasks, look at the status in `get_my_tasks` and only show pending ones.
   - If user asks for "Completed" tasks, only show completed ones.

**Tools:**
- Use `add_my_task`, `delete_my_task`, `get_my_tasks`, and `update_my_task`.
"""
    
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
    except Exception as e:
        print(f"🚨 Could not fetch model list from API. Falling back to default list. Error: {e}")
        available_models = ["models/gemini-1.5-flash-latest", "models/gemini-1.5-pro-latest", "models/gemini-pro"]

    def sort_key(model_name):
        if 'gemini-2.0' in model_name: return 0
        if 'gemini-1.5' in model_name: return 1
        return 2

    sorted_models = sorted(available_models, key=sort_key)
    print(f"Discovered models, sorted by preference: {sorted_models}")

    last_error = None
    for model_name in sorted_models:
        try:
            print(f"✅ Attempting to use model: {model_name}")
            model = genai.GenerativeModel(
                model_name=model_name, 
                tools=tools,
                system_instruction=system_instruction
            )
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(request.message)
            
            print(f"🎉 Successfully got response from model: {model_name}")
            return response.text

        except Exception as e:
            last_error = str(e)
            print(f"❌ Model {model_name} failed. Error: {last_error}")
            continue
    
    print(f"🚨 All discovered models failed. Last error: {last_error}")
    return "I'm sorry, all our AI services are currently busy. Please try again later."