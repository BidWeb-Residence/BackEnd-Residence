# 1 Imagem base do Python
FROM python:3.11-slim

# 2. Pasta de trabalho dentro do contêiner
WORKDIR /app

# 3. ATUALIZAR O LINUX E INSTALAR O SQLMAP
# Esta é a etapa que adiciona a ferramenta do Kali ao seu ambiente
RUN apt-get update && \
    apt-get install -y sqlmap && \
    rm -rf /var/lib/apt/lists/*

# 4. Copia o ficheiro de dependências Python
COPY requirements.txt .

# 5. Instala as dependências do Python (FastAPI, Uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o código da aplicação para dentro do contêiner
COPY . .    

# 7. Comando para executar o seu servidor 
CMD ["sh", "-c", "uvicorn scan:app --host 0.0.0.0 --port ${PORT}"]
