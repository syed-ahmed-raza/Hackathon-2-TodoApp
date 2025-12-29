import os
import google.generativeai as genai
from fastapi import APIRouter, Depends
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

# 👇 FIX: Empty string ("") taake URL /chat bane, na ke /chat/
@router.post("") 
async def chat_agent(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    
    
    # Tool Definitions (Yahan paste karne ki zaroorat nahi, aapka purana code theek hai)
    # Bas upar wala @router.post("") change zaroori hai.
    # Agar aap chahein toh puraana logic yahan neeche waisa hi rakhein.
    
    # --- Tool Definitions ---
    def add_my_task(title: str, description: str = ""):
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
        tasks = get_tasks(db, current_user_id)
        if not tasks:
            return "You have no tasks."
        return "\n".join([f"- {t.title} (ID: {t.id}, Status: {'Completed' if t.completed else 'Pending'})" for t in tasks])

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

    tools = [add_my_task, get_my_tasks, delete_my_task, update_my_task]
    system_instruction = """You are a smart AI Assistant for a Todo App. You MUST call tools to perform actions."""
    
    available_models = ["models/gemini-1.5-flash-latest", "models/gemini-1.5-pro-latest"]
    
    # Try finding models dynamically
    try:
        found_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if found_models: available_models = found_models
    except:
        pass

    for model_name in available_models:
        try:
            model = genai.GenerativeModel(model_name=model_name, tools=tools, system_instruction=system_instruction)
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(request.message)
            return response.text
        except:
            continue
    
    return "I'm sorry, AI services are busy."