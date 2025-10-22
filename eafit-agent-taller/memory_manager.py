import os
from supabase import create_client, Client
from langchain_core.messages import HumanMessage, AIMessage

# Cargar claves desde .env (ya debe estar hecho por agent_core)
SUPABASE_URL = os.getenv("https://qtsbwvbxgdkaynkwrwcl.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0c2J3dmJ4Z2RrYXlua3dyd2NsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExNDEzODgsImV4cCI6MjA3NjcxNzM4OH0.g0-1p9FLmgrEJyX7i81M0V7lc1uPshKfyfV4UOKcrY0")

# Inicializar cliente de Supabase
supabase: Client = create_client(https://qtsbwvbxgdkaynkwrwcl.supabase.co, eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0c2J3dmJ4Z2RrYXlua3dyd2NsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExNDEzODgsImV4cCI6MjA3NjcxNzM4OH0.g0-1p9FLmgrEJyX7i81M0V7lc1uPshKfyfV4UOKcrY0)

def get_chat_history(user_id):
    """
    Obtiene el historial de chat para un user_id y lo formatea para LangChain.
    """
    response = (
        supabase
        .table("chat_history")
        .select("*")
        .eq("user_id", str(user_id))
        .order("timestamp", desc=False)
        .execute()
    )

    messages = []
    if response.data:
        for record in response.data:
            if record["sender_role"] == "user":
                messages.append(HumanMessage(content=record["message"]))
            elif record["sender_role"] == "ai":
                messages.append(AIMessage(content=record["message"]))

    return messages

def add_message_to_history(user_id, sender_role, message):
    """
    Añade un nuevo mensaje (de 'user' o 'ai') a la base de datos.
    """
    try:
        supabase.table("chat_history").insert({
            "user_id": str(user_id),
            "sender_role": sender_role,
            "message": message
        }).execute()
    except Exception as e:
        print(f"Error al guardar en Supabase: {e}")

