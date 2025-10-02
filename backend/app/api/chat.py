from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ml.ollama_client import generate_response


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest) -> ChatResponse:
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    system_prompt = (
        "You are a supportive, non-clinical student wellbeing assistant. "
        "Offer empathetic, practical guidance, suggest campus resources, and encourage help-seeking. "
        "Avoid giving medical or legal advice. Keep responses under 150 words."
    )
    reply_text = await generate_response(user_message=body.message, system_prompt=system_prompt)
    return ChatResponse(reply=reply_text)


