# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

from core.validators import is_valid_url
from core.runner import run_sqlmap

app = FastAPI(
    title="SQL Injection API",
    description="API para análise SQL Injection"
)

class ScanRequest(BaseModel):
    url: str

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def welcome_api():
    return {"message": "Welcome to SQL Injection Tester"}

@app.post("/scan/sql")
async def scan_url(data: ScanRequest):
    url = data.url

    # validação
    if not is_valid_url(url):
        raise HTTPException(status_code=400, detail="URL inválida")

    result = run_sqlmap(url)

    # verifica erro no sqlmap (se precisar diferenciar)
    if result.get("returncode", 1) != 0:
        # encaminha stderr para diagnosticar, mas ainda retorna parsed se existir
        parsed = result.get("parsed", {})
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Falha ao executar sqlmap",
                "stderr": result.get("stderr"),
                "stdout": result.get("stdout"),
                "parsed": parsed
            }
        )

    parsed = result.get("parsed", {})

    return {
        "status": "success",
        "target_url": url,
        "data": {
            "target": parsed.get("target", {}),
            "dbms": parsed.get("target", {}).get("dbms"),
            "injection_points": parsed.get("injection_points", []),
            "databases": parsed.get("databases", []),
            "errors": parsed.get("errors", [])
        }
    }
