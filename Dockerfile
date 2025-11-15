# 1 Imagem base do Python
FROM python:3.11-slim

# 2. Pasta de trabalho dentro do contêiner
WORKDIR /app

# 3. ATUALIZAR O LINUX E INSTALAR O SQLMAP
# Esta é a etapa que adiciona a ferramenta do Kali ao seu ambiente
RUN apt-get update && \
    apt-get install -y sqlmap && \
    rm -rf /var/lib/apt/lists/*

# 4. Copie o seu ficheiro de dependências Python
COPY requirements.txt .

# 5. Instale as dependências do Python (FastAPI, Uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copie todo o resto do seu código (ex: scan.py)
COPY . .

# 7. Comando para executar o seu servidor FastAPI na porta 8080
# O Back4App exige que a sua aplicação ouça na porta 8080
CMD ["uvicorn", "scan:app", "--host", "0.0.0.0", "--port", "8080"]