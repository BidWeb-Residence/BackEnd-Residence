# 🔍 SQL Injection Scanner API

API desenvolvida em **FastAPI** para detecção automatizada de vulnerabilidades de **SQL Injection**, integrada ao [`sqlmap`](https://sqlmap.org) — o scanner mais avançado da categoria.

> ✅ Projeto seguro para testes educacionais (alvos como `testphp.vulnweb.com`).

---

## 🛠 Pré-requisitos

- [Python 3.9+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

---

## 🚀 Instalação

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente (escolha conforme seu sistema)
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

sudo apt-get update && sudo apt-get install -y sqlmap

# 4. Rodar aplicação
uvicorn scan:app --reload --host 0.0.0.0 --port 8000

```

OBS: Para sair do ambiente virtual rode o seguinte comenado no terminal:

```bash
deactivate
```

# 5. Comando de ataque com sqlmap
python sqlmap.py -u "url" --batch --banner