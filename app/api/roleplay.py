from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.schemas import ChatRoleplayInput, ChatResponse
from app.models.role_play_log import role_play_log_TB
from app.models.rolecharacter import RoleCharacter
from app.services.agent_roleplay import (
    get_roleplay_chain,
    build_prompt_from_character
)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def roleplay_chat(req: ChatRoleplayInput, db: Session = Depends(get_db)):
    # 1. 역할 정보 DB에서 조회
    character = db.query(RoleCharacter).filter_by(
        CHARACTER_ID=req.character_id,
        USER_ID=req.user_id
    ).first()
    if not character:
        raise HTTPException(400, detail="해당 사용자의 역할 정보가 없습니다.")

    # 2. 프롬프트 구성
    prompt = build_prompt_from_character(character)

    # 3. GPT 응답 생성
    chain = get_roleplay_chain(prompt)
    response = chain.invoke(
        {"input": req.input},
        config={"configurable": {"session_id": req.session_id or req.user_id}},
    )
    bot_reply = response.content.strip()

    # 4. 로그 저장
    db.add(role_play_log_TB(
        USER_ID=req.user_id,
        CHARACTER_ID=req.character_id,
        SENDER=req.input,
        RESPONDER=bot_reply
    ))
    db.commit()

    return ChatResponse(output=bot_reply)
