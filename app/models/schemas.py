# app/models/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    user_id: str
    input: str
    session_id: Optional[str] = None
    persona: str = "emotional"

class ChatResponse(BaseModel):
    output: str


class ChatRoleplayInput(BaseModel):
    user_id: str
    character_id: int
    input: str
    session_id: Optional[str] = None
    
class ChatLogCreate(BaseModel):
    USER_ID: str
    SENDER: str
    RESPONDER: str

class ChatLogResponse(ChatLogCreate):
    CHAT_ID: int
    CREATED_AT: datetime

    model_config = ConfigDict(from_attributes=True)
    
class MonthlyReportRequest(BaseModel):
    user_id: str