# app/services/agent_roleplay.py
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.models.rolecharacter import RoleCharacter
from app.models.roleplaylog import RolePlayLog
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.orm import Session

# 역할극 대화 기능 전용 세션 메모리 저장소
# - session_id 기준으로 사용자-캐릭터 간 대화 히스토리 관리
# - LangChain 메모리 연동을 위해 구조 통일
session_histories = {}

# 역할극 프롬프트 생성
# - 입력: 사용자 정의 RoleCharacter 객체
# - 처리: 역할극용 프롬프트 템플릿을 불러와 캐릭터 속성으로 format
# - 출력: 시스템 프롬프트 문자열
def build_prompt_from_character(character: RoleCharacter) -> str:
    with open("app/prompt/roleplay_prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()
    return template.format(
        name=character.NAME,
        relation=character.RELATIONSHIP,
        personality=character.PERSONALITY,
        speech_style=character.TONE,
        situation=character.SITUATION
    )

# DB → 히스토리 로딩
# - 입력: session_id, user_id, character_id, db 세션
# - 처리: 해당 캐릭터와 유저의 과거 역할극 로그를 시간순으로 조회
#         → LangChain 형식의 메모리 구조로 변환
# - 결과: session_histories[session_id] 에 ChatMessageHistory 저장
def preload_roleplay_history(session_id: str, user_id: str, character_id: int, db: Session):
    logs = (
        db.query(RolePlayLog)
        .filter(RolePlayLog.USER_ID == user_id)
        .filter(RolePlayLog.CHARACTER_ID == character_id)
        .order_by(RolePlayLog.CREATED_AT.asc())
        .all()
    )
    history = ChatMessageHistory()
    for log in logs:
        history.add_user_message(HumanMessage(content=log.SENDER))
        history.add_ai_message(AIMessage(content=log.RESPONDER))
    session_histories[session_id] = history

# 세션 ID 기준으로 히스토리 반환
# - 입력: session_id, config(dict)
# - 처리:
#   (1) 세션 히스토리 존재 시 반환
#   (2) 없을 경우, user_id + character_id + db 포함된 config 기반으로 preload 수행
# - 결과: ChatMessageHistory 반환 (LangChain 메모리 사용 목적)
def get_session_history(session_id: str, config: dict = None, reset: bool = False):
    if reset or session_id not in session_histories:
        if config and "user_id" in config and "character_id" in config and "db" in config:
            preload_roleplay_history(
                session_id,
                user_id=config["user_id"],
                character_id=config["character_id"],
                db=config["db"]
            )
        else:
            session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]


# 역할극 체인 생성
# - 입력: 프롬프트 텍스트, 유저/캐릭터 식별자, DB 세션
# - 구성:
#   1. 시스템 프롬프트 + 히스토리 + 사용자 입력 메시지 구조로 LangChain PromptTemplate 생성
#   2. GPT 모델 연결 (ChatOpenAI)
#   3. RunnableWithMessageHistory 로 메모리 포함 체인 구성
# - 출력: RunnableWithMessageHistory 객체 반환
def get_roleplay_chain(prompt_text: str, user_id: str, character_id: int, db: Session, force_reset: bool = False) -> RunnableWithMessageHistory:
    session_id = f"{user_id}_{character_id}"
    if force_reset:
        reset_session_history(session_id)

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

    def history_loader(sid):
        return get_session_history(sid, {
            "user_id": user_id,
            "character_id": character_id,
            "db": db
        }, reset=force_reset)  # 🔥 여기에 reset 플래그 반영

    return RunnableWithMessageHistory(
        prompt | llm,
        history_loader,
        input_messages_key="input",
        history_messages_key="history"
    )

def reset_session_history(session_id: str):
    if session_id in session_histories:
        del session_histories[session_id]