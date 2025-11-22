from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.validators import is_valid_url
from core.runner import run_sqlmap
from pathlib import Path

SQLMAP_SCRIPT = Path(__file__).parent / "sqlmap" / "runner.py"

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
        raise HTTPException(400, detail="URL inválida")

    result = run_sqlmap(url)

    # verifica erro no sqlmap
    if result["returncode"] != 0:
        raise HTTPException(
            500,
            detail={
                "message": "Falha ao executar sqlmap",
                "stderr": result["stderr"],
                "stdout": result["stdout"]
            }
        )

    # retorno para o frontend
    return {
    "status": "success",
    "target_url": url,
    "data": {
    "dbms": result.get("dbms"),
    "injection_points": result.get("injection_points", []),
    "databases": result.get("databases", [])
    
}
    }
