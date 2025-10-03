Param(
  [string]$HostAddress = "127.0.0.1",
  [int]$Port = 8001
)

$ErrorActionPreference = "Stop"

Write-Host "[+] Ensuring virtual environment..."
if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

Write-Host "[+] Activating venv..."
if (Test-Path ".venv\Scripts\Activate.ps1") {
  & .\.venv\Scripts\Activate.ps1
} else {
  Write-Host "[!] Could not activate virtual environment. Please check if Python is installed and .venv was created."
  exit 1
}

Write-Host "[+] Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt

# Load .env if present (python-dotenv reads it in the app, but we set defaults here too)
if (-not $env:OLLAMA_HOST) { $env:OLLAMA_HOST = "http://127.0.0.1:11434" }
if (-not $env:OLLAMA_MODEL) { $env:OLLAMA_MODEL = "mistral:latest" }

Write-Host "[+] Starting API on http://${HostAddress}:${Port} ..."
python -m uvicorn app.main:app --host $HostAddress --port $Port --app-dir backend --log-level info


