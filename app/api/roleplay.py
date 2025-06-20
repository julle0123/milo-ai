# app/api/roleplay.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.schemas import ChatRoleplayInput, ChatResponse
from app.models.roleplaylog import RolePlayLog
from app.models.rolecharacter import RoleCharacter
from app.services.agent_roleplay import (
    get_roleplay_chain,
    build_prompt_from_character
)

# 라우터 객체 생성 (역할 기반 챗봇 API)
router = APIRouter()

# POST /chat
# 역할 기반 가상대화 실행 및 로그 저장
# 입력: 사용자 ID, 캐릭터 ID, 입력 문장, 세션 ID
# 처리: 캐릭터 정보 조회 → 프롬프트 생성 → GPT 호출 → 응답 저장
@router.post("/chat", response_model=ChatResponse)
def roleplay_chat(req: ChatRoleplayInput, db: Session = Depends(get_db)):
    # 1. 사용자 소유의 역할 캐릭터 정보 조회
    character = db.query(RoleCharacter).filter_by(
        CHARACTER_ID=req.character_id,
        USER_ID=req.user_id
    ).first()
    if not character:
        raise HTTPException(400, detail="해당 사용자의 역할 정보가 없습니다.")

    # 2. 역할 캐릭터 정보 기반 프롬프트 구성
    prompt = build_prompt_from_character(character)

    # 3. 역할극용 LangChain 체인 객체 생성
    chain = get_roleplay_chain(
        prompt_text=prompt,
        user_id=req.user_id,
        character_id=req.character_id,
        db=db
    )

    # 4. 체인 실행 (GPT 응답 생성)
    response = chain.invoke(
        {"input": req.input},
        config={"configurable": {"session_id": req.session_id or req.user_id}},
    )
    bot_reply = response.content.strip()

    # 5. 역할 대화 로그 저장
    db.add(RolePlayLog(
        USER_ID=req.user_id,
        CHARACTER_ID=req.character_id,
        SENDER=req.input,
        RESPONDER=bot_reply
    ))
    db.commit()

    return ChatResponse(output=bot_reply)

