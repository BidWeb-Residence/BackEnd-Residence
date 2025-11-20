# 1. Imagem base
FROM python:3.11-slim

# 2. Diretório de trabalho
WORKDIR /app

# 3. Update e instalar sqlmap
RUN apt-get update && \
    apt-get install -y sqlmap && \
    rm -rf /var/lib/apt/lists/*

# 4. Copiar dependências
COPY requirements.txt .

# 5. Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar código da aplicação
COPY . .

# 7. “Dentro do container, tudo será executado no diretório /app
ENV PYTHONPATH="/app"

# 8. Expor porta (opcional mas recomendado)
EXPOSE 8000

# 9. Rodar o servidor
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]
CMD ["--port", "8000"]
