from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.models.rolecharacter import RoleCharacter

session_histories = {}

def get_session_history(session_id: str):
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]

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

def get_roleplay_chain(prompt_text: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    return RunnableWithMessageHistory(
        prompt | llm,
        lambda session_id: get_session_history(session_id),
        input_messages_key="input",
        history_messages_key="history"
    )
