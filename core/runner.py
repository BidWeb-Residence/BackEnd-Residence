from core.parser import parse_sqlmap_output
from core.formatter import format_output
import subprocess

def run_sqlmap(url: str):
    command = [
        "sqlmap",
        "-u", url,
        "--dbs",
        "--batch",
        "--risk=2",
        "--threads=2",
        "--timeout=30",
        "--flush-session"
    ]

    result = subprocess.run(
        command,
        text=True,
        capture_output=True
    )

    # Parse do stdout
    parsed = parse_sqlmap_output(result.stdout, url)

    # Adiciona informações do processo
    parsed["returncode"] = result.returncode
    parsed["stdout"] = result.stdout
    parsed["stderr"] = result.stderr

    return parsed


if __name__ == "__main__":
    run_sqlmap("http://testphp.vulnweb.com/listproducts.php?cat=1")
