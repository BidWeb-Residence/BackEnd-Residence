from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import subprocess 
from validators import is_valid_url 
from sqlmap import command, target_url_para_scanner
# from typing import Dict, Any (opcional!!)

class ScanPayload(BaseModel):
    url: str

app = FastAPI(
    title="SQL Injection API",
    description="API para receber URLs para análise de vulnerabilidades SQL Injection"
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
    # Em um ambiente controlado, USAR: target_url_para_scanner = target_url
    #teste:
        # return {"url_recebida": target_url}

        output = result.stdout.strip()
        error = result.stderr.strip()


try: 
    result = subprocess.run(
        command, 
        capture_output=True,
        text=True,
        timeout=300,
        check =False 
    )
    
    #Processando resultado
    if result.returncode != 0:
        print(f"Erro ao executar o comando sqlmap: {result.stderr}", 500)
        
        
    raw_output = result.stdout
    print(raw_output)
except subprocess.TimeoutExpired:
    print("O comando sqlmap excedeu o tempo limite.")
except Exception as e:
    print(f"Ocorreu um erro ao executar o comando sqlmap: {e}", 500)


# # falta encaixar o Dict e o Any

# def is_valid_url(url: str) -> bool:
#     return url.startswith("http") or url.startswith("https")
