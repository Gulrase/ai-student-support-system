import os
import httpx
from dotenv import load_dotenv

# Load environment variables from a .env file if present (project root or CWD)
load_dotenv()


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")


async def generate_response(user_message: str, system_prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{OLLAMA_HOST}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        # Expected shape: {"message": {"content": "..."}} or {"choices":[{"message":{"content":"..."}}]}
        message = (
            data.get("message", {}) or data.get("choices", [{}])[0].get("message", {})
        )
        content = message.get("content")
        if not content:
            # Fallback to text fields used by some models
            content = data.get("response") or data.get("text") or "I'm here to help."
        return content


