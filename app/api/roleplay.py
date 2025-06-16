# app/api/roleplay.py
from fastapi import APIRouter
from app.models.schemas import ChatRoleplayRequest, ChatResponse
from app.services.agent_roleplay import load_roleplay_prompt, get_roleplay_chain

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def roleplay_chat(req: ChatRoleplayRequest):
    prompt_text = load_roleplay_prompt(
        name=req.name,
        relation=req.relation,
        personality=req.personality,
        speech_style=req.speech_style,
        situation=req.situation
    )
    chain = get_roleplay_chain(prompt_text)
    response = chain.invoke(
        {"input": req.input},
        config={"configurable": {"session_id": req.session_id}}
    )
    return ChatResponse(output=response.content.strip())
