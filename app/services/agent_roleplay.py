# app/services/agent_roleplay.py
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import os

# 세션 저장소
session_histories = {}

def get_session_history(session_id: str):
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]

def load_roleplay_prompt(name: str, relation: str, personality: str, speech_style: str, situation: str) -> str:
    with open("app/prompt/roleplay_prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()
    return template.format(
        name=name,
        relation=relation,
        personality=personality,
        speech_style=speech_style,
        situation=situation
    )

def get_roleplay_chain(prompt_text: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    chain = prompt | llm
    return RunnableWithMessageHistory(
        chain,
        lambda session_id: get_session_history(session_id),
        input_messages_key="input",
        history_messages_key="history"
    )
