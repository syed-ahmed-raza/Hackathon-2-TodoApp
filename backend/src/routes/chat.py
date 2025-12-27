import os
import time
import google.generativeai as genai
from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel
from dotenv import load_dotenv
from ..database import get_db
from ..auth import get_current_user_id
from ..crud import create_task, get_tasks, delete_task, get_recent_task_by_title

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/api/chat")
async def chat_agent(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # --- Tool Definitions ---
    def add_my_task(title: str):
        """Adds a new task to the user's list. Be concise."""
        # Clean and normalize the new title for comparison
        cleaned_new_title = title.strip().lower()

        # Fetch all existing tasks for the current user
        existing_tasks = get_tasks(db, current_user_id)
        
        # Check if a task with the exact same title (case-insensitive, trimmed) already exists
        for task in existing_tasks:
            if task.title.strip().lower() == cleaned_new_title:
                return "Error: A task with this exact title already exists."
        
        # Original check for recently created tasks (within 2 seconds)
        if get_recent_task_by_title(db, title, current_user_id):
            return "Error: A task with this exact title already exists."
        
        create_task(db, title, "Pending", current_user_id)
        return f"Success: Task '{title}' added."

    def delete_my_task(task_identifier: str):
        """Deletes a task by its ID or a case-insensitive name search."""
        try:
            task_id = int(task_identifier)
            # We need to find the task to get its title before deleting
            tasks = get_tasks(db, current_user_id)
            task_to_delete = next((task for task in tasks if task.id == task_id), None)
            
            if task_to_delete and task_to_delete.user_id == current_user_id:
                title = task_to_delete.title
                delete_task(db, task_id, current_user_id)
                return f"Successfully deleted '{title}'."
            else:
                return f"Could not find a task with ID '{task_identifier}'."
        except ValueError:
            # It's a string, so search by name
            tasks = get_tasks(db, current_user_id)
            task_to_delete = None
            
            # First, try for an exact case-insensitive match
            for task in tasks:
                if task.title.strip().lower() == task_identifier.strip().lower():
                    task_to_delete = task
                    break
            
            # If no exact match, try for a partial case-insensitive match
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

    # --- Universal Model Discovery and Fallback Logic ---
    tools = [add_my_task, get_my_tasks, delete_my_task]
    system_instruction = "You are a professional, concise, and helpful assistant for a TODO list app. You can add, delete, and list tasks. When deleting a task by name, if the name is not found, inform the user."
    
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
    except Exception as e:
        print(f"🚨 Could not fetch model list from API. Falling back to default list. Error: {e}")
        available_models = ["models/gemini-1.5-flash-latest", "models/gemini-1.5-pro-latest", "models/gemini-pro"]

    # Sort models to prioritize newer versions
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
