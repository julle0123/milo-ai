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
    
    
# 감정 요약 결과를 구조화하여 표현하는 Pydantic 모델
# GPT 응답을 JsonOutputParser로 파싱한 후 구조 검증 및 활용에 사용
# Field(...) --> 필수 입력값 (값 반드시 있어야 함)
class EmotionSummary(BaseModel):
    joy: float = Field(..., description="기쁨 점수 (0~1)")              # 하루 대화 중 기쁨 감정의 비율
    sadness: float = Field(..., description="슬픔 점수 (0~1)")          # 하루 대화 중 슬픔 감정의 비율
    anger: float = Field(..., description="분노 점수 (0~1)")            # 하루 대화 중 분노 감정의 비율
    anxiety: float = Field(..., description="불안 점수 (0~1)")          # 하루 대화 중 불안 감정의 비율
    stable: float = Field(..., description="안정 점수 (0~1)")           # 하루 대화 중 안정(평온) 감정의 비율
    summary: str                                                      # 하루 전체 감정 흐름에 대한 요약 서술
    feedback: str                                                     # 사용자의 감정 상태를 기반으로 한 조언/피드백
    encouragement: str                                                # summary와 feedback을 종합한 응원/격려 문장