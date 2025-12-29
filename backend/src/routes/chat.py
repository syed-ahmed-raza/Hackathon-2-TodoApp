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

# 👇 Yeh System Instruction Chatbot ki "Shakhsiyat" (Personality) hai
SYSTEM_INSTRUCTION = """
You are a highly intelligent, friendly, and cheerful AI Task Assistant. 🤖✨

**Your Core Personality:**
1.  **Warm & Polite:** Always reply with kindness. If the user says "Salam" or "Assalam-o-Alaikum", reply with "Walaikum Assalam! 🌸 Kese hain aap?". If they say "Hi", reply enthusiastically.
2.  **Emoji Lover:** Use emojis frequently to make the conversation lively (e.g., ✅ for done, 🗑️ for deleted, 📝 for lists).
3.  **Language Adaptability:** If the user speaks in **Roman Urdu/Hindi** (e.g., "Task add kardo"), you MUST reply in **Roman Urdu** (e.g., "Ji zaroor! Task add kar diya hai ✅"). If they speak English, reply in English.
4.  **Smart Helper:** Don't just act like a robot. If the user says "I need to buy milk", understand that this is a task and ask if they want to add it, or just add it and confirm.

**Your Capabilities (Tools):**
- You have access to tools to `add_my_task`, `delete_my_task`, `get_my_tasks`, and `update_my_task`.
- **CRITICAL:** You MUST call the function/tool to perform the action on the database. Do not just say "I did it" without actually calling the tool.

**Response Style:**
- Keep responses concise but friendly.
- When listing tasks, use bullet points.
"""

@router.post("") 
async def chat_agent(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # --- Tool Definitions (Database Actions) ---
    def add_my_task(title: str, description: str = ""):
        """Adds a new task. Example: 'Add buy milk'."""
        cleaned_new_title = title.strip().lower()
        existing_tasks = get_tasks(db, current_user_id)
        for task in existing_tasks:
            if task.title.strip().lower() == cleaned_new_title:
                return "Info: Yeh task pehle se list mein hai! 😅"
        
        final_description = description if description else ""
        create_task(db, title, final_description, current_user_id)
        return f"Done! ✅ Task '{title}' add kar diya gaya hai."

    def delete_my_task(task_identifier: str):
        """Deletes a task by ID or Name."""
        try:
            task_id = int(task_identifier)
            tasks = get_tasks(db, current_user_id)
            task_to_delete = next((task for task in tasks if task.id == task_id), None)
            if task_to_delete and task_to_delete.user_id == current_user_id:
                title = task_to_delete.title
                delete_task(db, task_id, current_user_id)
                return f"Samjho gaya! 🗑️ Task '{title}' delete kar diya."
            else:
                return f"Mujhe ID '{task_identifier}' wala koi task nahi mila. 🧐"
        except ValueError:
            # Name se delete karna
            tasks = get_tasks(db, current_user_id)
            task_to_delete = None
            for task in tasks:
                if task.title.strip().lower() == task_identifier.strip().lower():
                    task_to_delete = task
                    break
            
            if task_to_delete:
                title = task_to_delete.title
                delete_task(db, task_to_delete.id, current_user_id)
                return f"Ho gaya! 🗑️ Task '{title}' delete kar diya."
            else:
                return f"Mujhe '{task_identifier}' naam ka koi task nahi mila. Spelling check karein? 🤔"

    def get_my_tasks():
        """Gets all tasks."""
        tasks = get_tasks(db, current_user_id)
        if not tasks:
            return "Aapki list bilkul khaali hai! 🎈 Koi kaam add karein?"
        
        task_list = "\n".join([f"- **{t.title}** (ID: {t.id}) {'✅' if t.completed else '⏳'}" for t in tasks])
        return f"Yeh rahi aapki tasks list:\n\n{task_list}"

    def update_my_task(task_identifier: str, title: str = None, description: str = None, is_completed: bool = None):
        """Updates a task (mark as done, rename, etc)."""
        task_to_update = None
        # Logic to find task by ID or Name
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
            updated = update_task(db, task_to_update.id, current_user_id, is_completed, title, description)
            if updated:
                status_msg = "complete kar diya ✅" if is_completed else "update kar diya 📝"
                return f"Set hai! Task '{updated.title}' ko {status_msg}."
            else:
                return "Oops! Update mein kuch masla hua. ❌"
        else:
            return "Mujhe yeh task nahi mila. 🤷‍♂️"

    # --- Gemini Setup ---
    tools = [add_my_task, get_my_tasks, delete_my_task, update_my_task]
    
    # Model selection with Fallback
    available_models = ["models/gemini-1.5-flash-latest", "models/gemini-1.5-pro-latest", "models/gemini-pro"]
    
    for model_name in available_models:
        try:
            model = genai.GenerativeModel(
                model_name=model_name, 
                tools=tools, 
                system_instruction=SYSTEM_INSTRUCTION # 👈 The Personality Injection
            )
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(request.message)
            return response.text
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            continue
    
    return "Maazrat! Mere systems abhi thore busy hain. Thodi der baad try karein? 🤖💤"