import os
import httpx
from dotenv import load_dotenv

# Load environment variables from a .env file if present (project root or CWD)
load_dotenv()


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:latest")


async def generate_response(user_message: str, system_prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt}\n{user_message}",
        "stream": False,
    }

    # Allow longer timeout to accommodate model loading (first request can take a while)
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            resp = await client.post(f"{OLLAMA_HOST}/api/generate", json=payload)
            resp.raise_for_status()
        except httpx.ReadTimeout:
            return "The model is still loading (timeout). Please try again in a moment."
        except httpx.ConnectError:
            return "Could not connect to the model server. Ensure Ollama is running."
        except httpx.HTTPStatusError as e:
            # Surface the status code and message for easier debugging
            return f"Model server returned error: {e.response.status_code} {e.response.text}"

        data = resp.json()
        # Ollama returns {"response": "..."}
        content = data.get("response") or data.get("text") or "I'm here to help."
        return content


