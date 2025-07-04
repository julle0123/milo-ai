# app/graph/prompts.py (신규 파일 생성 권장)

PROMPT_PATH = {
    "emotional": "app/prompt/emotion_prompt_emotional.txt",
    "practical": "app/prompt/emotion_prompt_practical.txt",
}

def load_prompt_template(persona: str) -> str:
    path = PROMPT_PATH.get(persona, PROMPT_PATH["emotional"])
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
