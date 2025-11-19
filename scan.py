from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
from typing import Dict, Any
import os
import re
from pathlib import Path

SQLMAP_SCRIPT = Path(__file__).parent / "sqlmap" / "sqlmap.py"
def is_valid_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")

class ScanPayload(BaseModel):
    url: str

app = FastAPI(
    title="SQL Injection API",
    description="API para receber URLs para análise de vulnerabilidades SQL Injection"
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
    print(SQLMAP_SCRIPT)
    return {"message": "Welcome to SQL Injection Tester"}

@app.post("/scan/sql")
async def scan_sql(payload: ScanPayload) -> Dict[str, Any]:
    target_url = payload.url.strip()

    if not is_valid_url(target_url):
        raise HTTPException(status_code=400, detail="URL inválida ou não permitida.")

    command = [
        "python",                  # ← executável do Python
        str(SQLMAP_SCRIPT),        # ← caminho para sqlmap.py
        "-u", target_url,          # ← URL alvo
        "--dbs",                   # ← opções do sqlmap
        "--batch",
        "--risk=2",
        "--threads=2",
        "--timeout=30"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,  # Timeout total de 5 minutos
            check=False  # Não levanta exceção automaticamente
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode != 0:
            return {
                "status": "error",
                "message": "Falha ao executar sqlmap",
                "stderr": error,
                "stdout": output
            }

        return {
            "status": "success",
            "target_url": target_url,
            "output": output,
            "detected_databases": parse_databases_from_output(output)  
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Tempo limite excedido durante o scan.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")


def parse_databases_from_output(output: str) -> list:
    databases = []
    lines = output.splitlines()
    for line in lines:
        line = line.strip()
        # Procura linhas que começam com [*] e têm conteúdo após
        if line.startswith("[*]") and len(line) > 3:
            # Remove "[*]" e limpa espaços
            db_name = line[3:].strip()
            # Filtra linhas irrelevantes (ex: mensagens do sqlmap)
            if db_name and not db_name.startswith(("starting", "ending", "legal", "https")):
                databases.append(db_name)
    return databases