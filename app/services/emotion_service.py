# app/services/emotion_service.py
from typing import List, Dict
import json
import asyncio
from app.models.chat_log import ChatLog
from app.models.user import User
from app.core.client import llm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.models.schemas import EmotionSummary
from app.models.daily_emotion_report import DailyEmotionReport
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate

KST = timezone(timedelta(hours=9))
# 문장 단위 감정 분류용 (6종)
EMOTION_CATEGORIES = ["기쁨", "불안", "분노", "슬픔", "상처", "당황"]

# GPT 기반 감정 라벨링 + 원문 포함 문장 반환
async def analyze_emotion_gpt(user_input: str) -> str:
    prompt = (
        "다음 문장의 대표 감정을 반드시 아래 6개 중 하나로만 한글 한 단어로 출력해줘.\n"
        "기쁨, 불안, 분노, 슬픔, 상처, 당황 중 택1\n"
        f"문장: {user_input}\n감정: "
    )
    result = await llm.ainvoke(prompt)
    emotion = result.content.strip()
    if emotion not in EMOTION_CATEGORIES:
        emotion = "불안"
    return f"[감정: {emotion}] {user_input}"


# 감정 벡터 중 대표 감정을 5종(안정 포함) 기준으로 추출
def extract_emotion_label(user_input: str) -> str:
    prompt = (
        "다음 문장의 대표 감정을 반드시 아래 6개 중 하나로만 한글 한 단어로 출력해줘.\n"
        "기쁨, 불안, 분노, 슬픔, 상처, 당황 중 택1\n"
        f"문장: {user_input}\n감정: "
    )
    emotion = llm.invoke(prompt).content.strip()
    return emotion if emotion in EMOTION_CATEGORIES else "불안"


# 일일 감정 분석용 - 감정 벡터 + 총평 + 피드백 + 응원말 생성
# 감정 벡터 중 대표 감정을 5종(안정 포함) 기준으로 추출
def convert_to_main_emotion(score_dict: Dict[str, float]) -> str:
    five_emotion_scores = {
        "기쁨": score_dict.get("joy", 0.0),
        "슬픔": score_dict.get("sadness", 0.0),
        "분노": score_dict.get("anger", 0.0),
        "불안": score_dict.get("anxiety", 0.0),
        "안정": score_dict.get("stable", 0.0),
    }
    return max(five_emotion_scores.items(), key=lambda x: x[1])[0]

# 하루치 대화 리스트를 GPT에게 넘겨 감정 요약 및 점수 추출
# - 결과는 EmotionSummary 형식으로 구조화됨
# - 반환값은 DB 저장용 dict 형식
async def summarize_day_conversation(messages: List[str], user_id: str, date: str) -> Dict:
    combined_text = "\n".join(messages) # 하루 대화 내용을 한 텍스트로 결합

    parser = JsonOutputParser(pydantic_object=EmotionSummary)  # GPT 응답 구조를 EmotionSummary로 파싱
 
    # 프롬프트 구성 (지침 + 사용자 대화 삽입 + 출력 형식 포함)
    prompt_template = PromptTemplate(
    template="""
너는 감정 분석 전문가야. 아래는 사용자의 하루치 대화 내용이야:

{conversation}

[지침 사항](필수적으로 지켜야함)
- "summary"는 오늘 하루의 감정 흐름을 구체적인 사례와 감정 표현을 중심으로 풍부하게 서술해줘.
  - 단순히 "기뻤다", "불안했다" 로 끝나면 안되고, 무엇 때문에 그런 감정을 느꼈는지도 꼭 포함해줘.
  - 문장 수는 {conversation}양에 따라서 2~5문장 이상으로, 전체 흐름이 느껴지도록 작성해줘.
  - 너무 일반적인 말보다 대화 내용에 맞춘 요약을 해줘야 해.

- "feedback"은 사용자의 상태에 진심으로 도움될만한 현실적인 조언으로 작성해줘. 너무 짧거나 뻔하지 않게 해줘.

- "encouragement"는 summary와 feedback을 기반으로, 오늘을 잘 마무리할 수 있도록 격려하는 말로 1~4문장 내로 따뜻하게 작성해줘.

- 감정 벡터 점수는 오늘 대화의 표현된 정서 강도에 따라 다르게 생성해줘.
- 이전과 비슷하거나 동일한 점수가 반복되면 안되고, 실제 감정 뉘앙스를 반영해 다양한 점수 분포를 보여줘야 해.
- 감정 점수는 떨어질수도있고 오를수도있어.
- 모든 감정 점수는 0.0~1.0 사이로 균형 있게 작성해줘.

{format_instructions}
""",
    input_variables=["conversation"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

    prompt = prompt_template.format(conversation=combined_text)

    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: llm.invoke(prompt))
        parsed_dict = parser.parse(response.content)# EmotionSummary 또는 dict로 파싱

        # 파싱 결과를 DB 저장 형식(dict)으로 재구성
        return {
            "USER_ID": user_id,
            "DATE": date,
            "MAIN_EMOTION": convert_to_main_emotion(parsed_dict),
            "SCORE": max(parsed_dict['joy'], parsed_dict['sadness'], parsed_dict['anger'], parsed_dict['anxiety']),
            "STABLE": parsed_dict['stable'],
            "JOY": parsed_dict['joy'],
            "SADNESS": parsed_dict['sadness'],
            "ANGER": parsed_dict['anger'],
            "ANXIETY": parsed_dict['anxiety'],
            "SUMMARY": parsed_dict['summary'],
            "FEEDBACK": parsed_dict['feedback'],
            "ENCOURAGEMENT": parsed_dict['encouragement']
        }

    except Exception as e:
        print("❌ GPT JSON 파싱 실패:", str(e))
        raise ValueError(f"GPT 응답 파싱 실패: {e}")

    
    
# 최근 감정 흐름 요약 텍스트 반환
# - 주간 일일 리포트를 기반으로 감정 점수 변화 
def get_emotion_trend_text(user_id: str, db: Session) -> str:


    today = datetime.now(KST).date()
    week_ago = today - timedelta(days=6)

    reports = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE >= week_ago,
        DailyEmotionReport.DATE <= today
    ).order_by(DailyEmotionReport.DATE).all()

    if not reports or len(reports) < 2:
        return "최근 감정 변화 데이터가 부족합니다."

    return "\n".join(
        f"{r.DATE} → 기쁨:{r.JOY:.2f}, 슬픔:{r.SADNESS:.2f}, 불안:{r.ANXIETY:.2f}, 안정:{r.STABLE:.2f}, 분노:{r.ANGER:.2f}"
        for r in reports
    )

# 사용자 닉네임 조회
# - 닉네임이 없을 경우 기본값 "사용자님" 반환
def get_user_nickname(user_id: str, db: Session) -> str:
    user = db.query(User).filter(User.USER_ID == user_id).first()
    return user.NICKNAME if user else "사용자"


async def summarize_full_chat_history(user_id: str, db: Session) -> str:
    logs = (
        db.query(ChatLog)
        .filter(ChatLog.USER_ID == user_id)
        .order_by(ChatLog.CREATED_AT.asc())
        .all()[::-1]  # 시간순 정렬
    )
    if not logs:
        return "이전에 나눈 대화 내용이 없습니다."

    full_text = "\n".join(
        f"사용자: {log.SENDER}\n챗봇: {log.RESPONDER}" for log in logs
    )

    summary_prompt = (
        "다음은 사용자와 챗봇 사이의 대화 기록입니다. 이 대화를 한 문단으로 요약해 주세요. "
        "대화의 감정 흐름과 사용자의 고민/상태가 드러나도록 해 주세요.\n\n"
        + full_text
    )

    result = await llm.ainvoke(summary_prompt)
    return result.content if hasattr(result, "content") else str(result)