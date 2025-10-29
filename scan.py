from flask import Flask, request, jsonify
import subprocess
from validators import is_valid_url 

app = Flask(__name__)
 
@app.get("/")               
def welcomeAPI():
    return "<p>Welcome to SQL Injection Tester</p>"


@app.post("/scan/sql")
def scan_sql():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "O corpo da requisição deve conter a chave 'url'."}), 400
    target_url = data["url"].strip()
    if not is_valid_url(target_url):
        return jsonify({"error": "URL inválida ou não permitida."}), 400
    print(target_url)
    return jsonify({"url_recebida": target_url})
