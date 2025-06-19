from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.models.rolecharacter import RoleCharacter
from app.models.roleplaylog import RolePlayLog
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.orm import Session

# 세션 히스토리 저장소
session_histories = {}

# 역할극 프롬프트 생성
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

# 히스토리 가져오기 (with preload)
def get_session_history(session_id: str, config: dict = None):
    if session_id not in session_histories:
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
def get_roleplay_chain(prompt_text: str, user_id: str, character_id: int, db: Session) -> RunnableWithMessageHistory:
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    return RunnableWithMessageHistory(
        prompt | llm,
        lambda session_id: get_session_history(session_id, {
            "user_id": user_id,
            "character_id": character_id,
            "db": db
        }),
        input_messages_key="input",
        history_messages_key="history"
    )
