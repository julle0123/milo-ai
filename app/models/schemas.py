# app/models/schemas.py
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

# 챗봇 대화 요청 입력 스키마
class ChatRequest(BaseModel):
    user_id: str                 # 사용자 ID
    input: str                   # 사용자 입력 문장
    session_id: Optional[str] = None  # 세션 ID (없으면 서버에서 생성)
    persona: str = "emotional"        # 프롬프트 타입 (emotional 또는 practical)
    force_summary: Optional[bool] = False  # 요약 강제 여부 (기본값: False)
    
# 챗봇 대화 응답 스키마
class ChatResponse(BaseModel):
    output: str                  # 챗봇 응답 문장


# 역할극 대화 요청 입력 스키마
class ChatRoleplayInput(BaseModel):
    user_id: str
    character_id: int
    input: str
    session_id: Optional[str] = None


# 대화 로그 저장용 입력 스키마
class ChatLogCreate(BaseModel):
    USER_ID: str
    SENDER: str
    RESPONDER: str

# 대화 로그 조회용 출력 스키마
class ChatLogResponse(ChatLogCreate):
    CHAT_ID: int
    CREATED_AT: datetime

    model_config = ConfigDict(from_attributes=True)  # ORM 객체 변환 허용


# 월간 리포트 생성 요청 스키마
class MonthlyReportRequest(BaseModel):
    user_id: str
    
    
# 감정 요약 응답 구조
class EmotionSummary(BaseModel):
    joy: float = Field(..., description="기쁨 점수 (0~1)")
    sadness: float = Field(..., description="슬픔 점수 (0~1)")
    anger: float = Field(..., description="분노 점수 (0~1)")
    anxiety: float = Field(..., description="불안 점수 (0~1)")
    stable: float = Field(..., description="안정 점수 (0~1)")
    summary: str
    feedback: str
    encouragement: str