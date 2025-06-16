# ✅ emotion_service.py
from typing import List, Dict
import json
from app.core.client import llm

# ----------------------
# 문장 단위 감정 분류용 (6종)
# ----------------------

EMOTION_CATEGORIES = ["기쁨", "불안", "분노", "슬픔", "상처", "당황"]

def analyze_emotion_gpt(user_input: str) -> str:
    """
    사용자 입력 문장을 GPT를 이용해 6가지 감정 중 하나로 분류한 뒤,
    [감정: OO] 문장 형태로 반환
    """
    prompt = (
        "다음 문장의 대표 감정을 반드시 아래 6개 중 하나로만 한글 한 단어로 출력해줘.\n"
        "기쁨, 불안, 분노, 슬픔, 상처, 당황 중 택1\n"
        f"문장: {user_input}\n감정: "
    )
    emotion = llm.invoke(prompt).content.strip()
    if emotion not in EMOTION_CATEGORIES:
        emotion = "불안"
    return f"[감정: {emotion}] {user_input}"

def extract_emotion_label(user_input: str) -> str:
    """
    감정 태그만 반환하는 버전
    """
    prompt = (
        "다음 문장의 대표 감정을 반드시 아래 6개 중 하나로만 한글 한 단어로 출력해줘.\n"
        "기쁨, 불안, 분노, 슬픔, 상처, 당황 중 택1\n"
        f"문장: {user_input}\n감정: "
    )
    emotion = llm.invoke(prompt).content.strip()
    return emotion if emotion in EMOTION_CATEGORIES else "불안"

# ----------------------
# 하루치 감정 분석 리포트용 (6종 분석 → 대표 감정 5종 변환)
# ----------------------

def convert_to_main_emotion(score_dict: Dict[str, float]) -> str:
    five_emotion_scores = {
        "기쁨": score_dict.get("joy", 0.0),
        "슬픔": score_dict.get("sadness", 0.0),
        "분노": score_dict.get("anger", 0.0),
        "불안": score_dict.get("anxiety", 0.0),
        "안정": score_dict.get("stable", 0.0),
    }
    return max(five_emotion_scores.items(), key=lambda x: x[1])[0]

def summarize_day_conversation(messages: List[str], user_id: str, date: str) -> Dict:
    combined_text = "\n".join(messages)

    prompt = f"""
너는 감정 분석 전문가야. 아래는 사용자의 하루치 대화 내용이야:

{combined_text}

다음 정보를 생성해줘 (JSON 형식으로 정확하게 출력해 소수점 2째자리까지 나타내줘):
- joy: 기쁨 점수 (0~1)
- sadness: 슬픔 점수 (0~1)
- anger: 분노 점수 (0~1)
- anxiety: 불안 점수 (0~1)
- stable: 안정감 점수 (0~1)
- summary: 하루 전체 대화 요약
- feedback: GPT가 제공하는 회복 가이드
- encouragement: 짧은 응원 메시지
"""

    response = llm.invoke(prompt)

    try:
        parsed = json.loads(response.content)

        main_emotion = convert_to_main_emotion(parsed)

        return {
            "USER_ID": user_id,
            "DATE": date,
            "MAIN_EMOTION": main_emotion,
            "SCORE": max(parsed["joy"], parsed["sadness"], parsed["anger"], parsed["anxiety"]),
            "STABLE": parsed["stable"],
            "JOY": parsed["joy"],
            "ANGER": parsed["anger"],
            "ANXIETY": parsed["anxiety"],
            "SUMMARY": parsed["summary"],
            "FEEDBACK": parsed["feedback"],
            "ENCOURAGEMENT": parsed["encouragement"]
        }
    except Exception as e:
        raise ValueError(f"GPT 응답 파싱 실패: {e}")
