from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.payloads import ScanPayload
from core.validators import is_valid_url
from core.runner import run_sqlmap

app = FastAPI(
    title="SQL Injection API",
    description="API para análise SQL Injection"
)

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
async def scan_sql(payload: ScanPayload):
    url = payload.url.strip()

    if not is_valid_url(url):
        raise HTTPException(400, "URL inválida ou não permitida.")

    result = run_sqlmap(url)

    if result["returncode"] != 0:
        raise HTTPException(
            500,
            detail={
                "message": "Falha ao executar sqlmap",
                "stderr": result["stderr"],
                "stdout": result["stdout"]
            }
        )

    return {
        "status": "success",
        "target_url": url,
        "output": result["stdout"],
        "databases": result["databases"]
    }
