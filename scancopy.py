from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import subprocess
import re
import shlex # Para tratamento seguro de strings de comando (embora menos essencial aqui)
from typing import Dict, Any # Usado no retorno para clareza

# === IMPORTAÇÕES DE TERCEIROS (Assumindo que 'validators' é um ficheiro local) ===
# Se 'validators' e 'is_valid_url' são seus, certifique-se de que estão acessíveis.
# Se não existirem, o servidor falhará ao iniciar.
try:
    from validators import is_valid_url
except ImportError:
    # Aviso: Em um ambiente real, você precisa dessa validação
    print("AVISO: Módulo 'validators' não encontrado. URLs não serão validadas.")
    def is_valid_url(url: str): return url.startswith('http') or url.startswith('https')


# --- CONFIGURAÇÃO DA API ---
app = FastAPI(
    title="Hydra SQL Injection Scan API",
    description="API para orquestrar o sqlmap em alvos controlados.",
)

class ScanPayload(BaseModel):
    """Define o formato da entrada JSON da requisição POST."""
    url: str

# --- PONTO DE ENTRADA (ROTAS) ---

@app.get("/")
def welcome_api():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Welcome to Hydra Scan Engine API"}

@app.post("/scan/sql", response_model=None)
async def scan_sql(payload: ScanPayload) -> Dict[str, Any]:
    """Recebe a URL e executa o scan de SQL Injection."""
    target_url = payload.url.strip()

    # CRÍTICA E CORREÇÃO 1: Validação e Segurança
    if not is_valid_url(target_url): 
        raise HTTPException(status_code=400, detail="URL inválida ou não permitida.")
        
    # CRÍTICA 2: O comando deve ser construído DENTRO da função
    # O sqlmap espera que o URL esteja no formato de lista, separado.
    command = [
        "sqlmap",
        "-u", target_url,
        "--dbs",         # Tenta enumerar bases de dados
        "--batch"        # Assume resposta padrão (sim)
    ]

    try: 
        # CRÍTICA 3: Execução do subprocesso
        result = subprocess.run(
            command, 
            capture_output=True,
            text=True,
            timeout=300, # 5 minutos
            check=False  # Não levanta exceção para código de retorno != 0
        )
        
        # O resultado do subprocesso agora está em 'result'
        raw_output = result.stdout.strip()
        raw_error = result.stderr.strip()
        
        # CRÍTICA 4: Tratamento de Erro do sqlmap
        if result.returncode != 0:
            # Se o sqlmap falhar (ex: erro de rede, erro de sintaxe)
            error_message = f"SQLmap falhou com código {result.returncode}. {raw_error}"
            print(f"ERRO SQLMAP: {error_message}")
            return Response(
                content=error_message, 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # CRÍTICA 5: O output e error estavam definidos fora de escopo.
        # Agora eles são retornados no JSON final.
        return {
            "status": "success",
            "url_alvo": target_url,
            "sqlmap_output": raw_output,
            "error_output": raw_error,
            "return_code": result.returncode,
            # Aqui entraria a chamada para a Tarefa 2: parse_sqlmap_output(raw_output)
        }
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="O scan excedeu o tempo limite (300s).")
    
    except FileNotFoundError:
        # Erro que acontece se o 'sqlmap' não estiver no PATH (Não instalado)
        raise HTTPException(status_code=500, detail="Erro de Configuração: Comando 'sqlmap' não encontrado no servidor.")
    
    except Exception as e:
        # Erros inesperados
        print(f"ERRO INESPERADO: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado: {str(e)}")