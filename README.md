AI Powered Students Support System (Prototype)

Overview

This prototype provides a minimal FastAPI backend for:

- Chat-based student support using a local LLM via Ollama (e.g., mistral, llama3, or an open-source Groq-compatible model).
- Simple dropout/mental-health risk scoring from survey-like features with a lightweight model.

Getting Started

Prerequisites

- Python 3.10+
- pip
- (Optional) Ollama installed and a local model pulled (e.g., `ollama pull mistral`)

Setup

1. Create and activate a virtual environment

   macOS/Linux:
   
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install backend dependencies

   ```bash
   pip install -r backend/requirements.txt
   ```

3. Run the API

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 --app-dir backend
   ```

Windows (PowerShell) quick start

```powershell
cd <path-to>/ai-student-support-system
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
./run.ps1 -HostAddress 127.0.0.1 -Port 8001
```

macOS/Linux quick start

```bash
cd <path-to>/ai-student-support-system
bash ./run.sh
```

Endpoints

- POST /api/chat
  - body: `{ "message": "I feel overwhelmed" }`
  - returns: LLM response with supportive guidance

- POST /api/risk/score
  - body: `{"features": {"attendance_rate": 0.8, "gpa": 2.5, "missed_assignments": 5}}`
  - returns: `{ "risk": 0..1 }`

Examples

```bash
# Health check
curl -s http://localhost:8001/health | jq

# Chat
curl -s -X POST http://localhost:8001/api/chat/ \
  -H 'Content-Type: application/json' \
  -d '{"message":"I feel overwhelmed by exams"}' | jq

# Risk score
curl -s -X POST http://localhost:8001/api/risk/score \
  -H 'Content-Type: application/json' \
  -d '{"features":{"attendance_rate":0.8,"gpa":2.5,"missed_assignments":5}}' | jq
```

Config

- Environment variables:
  - `OLLAMA_MODEL` (default: `mistral`)
  - `OLLAMA_HOST` (default: `http://127.0.0.1:11434`)
  - You can create a `.env` file with these values; the server loads it automatically.

Notes

- This is a prototype and not intended for clinical use.
- Replace the simple risk model with your trained artifacts when available.


