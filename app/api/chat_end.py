# app/api/chat_end.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

# DB 세션 의존성 주입 함수 (SQLAlchemy)
from app.core.db import get_db

# 감정 리포트 관련 서비스 함수
from app.services.report_service import get_day_conversations, save_or_update_daily_report
from app.services.emotion_service import summarize_day_conversation

# 라우터 객체 생성 (챗봇 세션 관련 API 등록 용도)
router = APIRouter()

# 챗봇 세션 종료 시 감정 리포트를 자동 생성 및 저장하는 API
# - 경로: POST /session/end
# - 사용 목적: 하루 대화 세션이 끝났을 때, 감정 요약 및 DB 기록 수행
# - 세션 의미:
#    사용자 입장에서는 "오늘의 대화 세션 종료"
#    시스템 입장에서는 "하루 단위로 정서 기록 저장 트리거"
# - 호출 위치: 프론트엔드에서 대화 종료 시점

@router.post("/session/end")
async def end_session(user_id: str, db: Session = Depends(get_db)):
    # 오늘 날짜를 'YYYY-MM-DD' 형식으로 생성
    today = datetime.now().strftime("%Y-%m-%d")

    # 오늘 하루 동안 사용자(user_id)의 대화 내역 불러오기
    #    - chat_log_TB에서 user_id + 오늘 날짜 기준으로 필터링
    messages = get_day_conversations(user_id, today, db)

    # 대화가 존재하면 감정 요약 및 분석 진행
    if messages:
        try:
            # GPT 모델 기반으로 오늘 대화 전체 감정 요약/분석 수행
            result = await summarize_day_conversation(messages, user_id, today)

            # 감정 리포트 저장에 필요한 모든 필수 키가 있는지 검증
            required_keys = {
                "MAIN_EMOTION", "SCORE", "STABLE", "JOY", "SADNESS", "ANGER",
                "ANXIETY", "SUMMARY", "FEEDBACK", "ENCOURAGEMENT"
            }
            missing_keys = required_keys - result.keys()
            if missing_keys:
                raise ValueError(f"누락된 키 존재: {missing_keys}")

            # 리포트를 DB에 저장 (이미 있으면 업데이트)
            #    - 테이블: daily_emotion_report_TB
            await save_or_update_daily_report(db, user_id, today, result)

            # 정상 저장된 경우 상태 및 대표 감정 반환
            return {"status": "saved", "main_emotion": result["MAIN_EMOTION"]}

        except Exception as e:
            # 분석 또는 저장 중 에러 발생 시 예외 처리
            msg = f"{e}"
            return {"status": "error", "message": msg}
    else:
        # 오늘 대화 내역이 없는 경우
        return {"status": "no_messages"}
