# BackEnd-Residence

Backend do projeto Residence, desenvolvido com **Flask**. Este projeto serve como API para gerenciar funcionalidades relacionadas ao Residence.

---

## 🔹 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

- Python 3.10 ou superior
- pip (gerenciador de pacotes do Python)
- Ambiente virtual opcional (recomendado)

---

## 🔹 Configuração do ambiente

1. Crie e ative o ambiente virtual:

```bash
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

2. Instale as dependências

```bash
pip install -r requirements.txt
```

3. Inicialize o servidor

```bash
python -m flask --app scan run
```

OBS: Para sair do ambiente virtual rode o seguinte comenado no terminal:

```bash
deactivate
```


# Dentro da sua rota /scan/sql
import subprocess

# 1. Obter o URL alvo da requisição
target_url = request.json.get('url')

# 2. Montar o comando a ser executado no terminal do Kali
# O --batch garante que o sqlmap não faça perguntas interativas
command = [
    "sqlmap",
    "-u", target_url,
    "--dbs",          # Tenta enumerar os bancos de dados
    "--batch"
]

# 3. Executar o comando e capturar a saída
try:
    # A magia acontece aqui!
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=300  # Define um tempo limite de 5 minutos
    )

    # 'result.stdout' contém a saída de texto do sqlmap
    raw_output = result.stdout

    # O próximo passo é enviar 'raw_output' para a função da Tarefa 2
    # ...

except subprocess.TimeoutExpired:
    # Lidar com o caso de o scan demorar muito
    return {"error": "O scan excedeu o tempo limite."}, 500
except Exception as e:
    # Lidar com outros erros
    return {"error": str(e)}, 500

