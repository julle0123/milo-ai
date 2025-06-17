# emotion_service.py
from typing import List, Dict
import json
from app.core.client import llm

# ----------------------
# 문장 단위 감정 분류용 (6종)
# ----------------------

EMOTION_CATEGORIES = ["기쁨", "불안", "분노", "슬픔", "상처", "당황"]

def analyze_emotion_gpt(user_input: str) -> str:
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

다음 정보를 JSON 형식으로 정확하게 출력해줘 (key는 영문, 값은 소수점 둘째자리까지):

예시:
{{
  "joy": 0.83,
  "sadness": 0.15,
  "anger": 0.10,
  "anxiety": 0.62,
  "stable": 0.33,
  "summary": "하루 동안 불안이 많이 느껴졌고, 직업에 대한 걱정이 컸습니다.",
  "feedback": "불안할 땐 호흡을 가다듬고 잠시 산책을 해보세요.",
  "encouragement": "오늘도 잘 버텨주셔서 고마워요."
}}
"""

    response = llm.invoke(prompt)
    raw_output = response.content.strip()
    print("🧠 GPT 응답 원문:\n", raw_output)

    if raw_output.startswith("```json"):
        raw_output = raw_output.lstrip("```json").rstrip("```").strip()
    elif raw_output.startswith("```"):
        raw_output = raw_output.lstrip("```").rstrip("```").strip()

    try:
        parsed = json.loads(raw_output)

        main_emotion = convert_to_main_emotion(parsed)

        return {
            "USER_ID": user_id,
            "DATE": date,
            "MAIN_EMOTION": main_emotion,
            "SCORE": max(parsed["joy"], parsed["sadness"], parsed["anger"], parsed["anxiety"]),
            "STABLE": parsed["stable"],
            "JOY": parsed["joy"],
            "SADNESS": parsed["sadness"],
            "ANGER": parsed["anger"],
            "ANXIETY": parsed["anxiety"],
            "SUMMARY": parsed["summary"],
            "FEEDBACK": parsed["feedback"],
            "ENCOURAGEMENT": parsed["encouragement"]
        }
    except Exception as e:
        print("GPT JSON 파싱 실패:", str(e))
        raise ValueError(f"GPT 응답 파싱 실패: {e}")