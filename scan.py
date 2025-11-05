from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import subprocess 
from validators import is_valid_url 
# from typing import Dict, Any

def is_valid_url(url: str) -> bool:
    return url.startswith("http") or url.startswith("https")

class ScanPayload(BaseModel):
    url: str

app = FastAPI(
    title = "SQL Injection  API",
    description = "API para receber URLS para análise"
)
 
@app.get("/")               
async def welcomeAPI():
    return "<p>Welcome to SQL Injection Tester</p>"


@app.post("/scan/sql")
async def scan_sql(payload: ScanPayload):
    target_url = payload.url.strip()
    if not is_valid_url(target_url):
       raise HTTPException(status_code=400, detail="URL inválida ou não permitida.")
    # Em um ambiente controlado, USAR: target_url_para_scanner = target_url
    #teste:
    # target_url_para_scanner = "http://testphp.vulnweb.com/listproducts.php?cat=1"
    return {"url_recebida": target_url}

command = [
    "sqlmap",
    "-u",
    # target_url_para_scanner,
    "http://testphp.vulnweb.com/listproducts.php?cat=1",
    "--dbs"
    "--batch",
    "--risk=1"
]

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

    

# problema para resolver: definir o target_url_para_scanner dentro do escopo command
# encaixar o Dict e o Any















# APP.POST ANTIGO
# def scan_sql():

#     data = request.get_json()
#     if not data or "url" not in data:
#         return jsonify({"error": "O corpo da requisição deve conter a chave 'url'."}), 400
#     target_url = data["url"].strip()
#     if not is_valid_url(target_url):
#         return jsonify({"error": "URL inválida ou não permitida."}), 400
#     print(target_url)
#     return jsonify({"url_recebida": target_url})
