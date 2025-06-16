# app/models/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChatRequest(BaseModel):
    input: str
    session_id: str = "default"
    persona: str = "emotional"

class ChatResponse(BaseModel):
    output: str

class ChatRoleplayRequest(BaseModel):
    name: str
    relation: str
    personality: str
    speech_style: str
    situation: str
    input: str
    session_id: str = "default"

class ChatLogCreate(BaseModel):
    USER_ID: str
    SENDER: str
    RESPONDER: str

class ChatLogResponse(ChatLogCreate):
    CHAT_ID: int
    CREATED_AT: datetime

    model_config = ConfigDict(from_attributes=True)