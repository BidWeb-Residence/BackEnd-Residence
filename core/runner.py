from core.parser import parse_sqlmap_output
from core.formatter import format_output
import subprocess
from typing import Dict, List


def run_sqlmap(url: str) -> dict:
    command = [
        "sqlmap",
        "-u", url,
        "--dbs",
        "--batch",
        "--risk=3",
        "--level=3",
        "--threads=2",
        "--timeout=30",
        "--flush-session"
    ]

    result = subprocess.run(
        command,
        text=True,
        capture_output=True
    )

    stdout = result.stdout or ""
    stderr = result.stderr or ""
    returncode = result.returncode

    # Parse do stdout
    parsed = parse_sqlmap_output(stdout, url)

    # Log seguro no terminal
    if isinstance(parsed, dict):
        format_output(parsed)
    else:
        print("Erro: sqlmap retornou um formato inesperado.")

    # Retorno completo para API ou CLI
    return {
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
        "parsed": parsed
    }


if __name__ == "__main__":
    import sys
    test_url = "http://testphp.vulnweb.com/listproducts.php?cat=1"
    if len(sys.argv) > 1:
        test_url = sys.argv[1]

    res = run_sqlmap(test_url)

    print("\n=== RETURN ===")
    print(f"returncode: {res['returncode']}")
    print(f"databases: {res['parsed'].get('databases')}")
