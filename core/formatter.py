# core/formatter.py
from colorama import Fore, Style, init
init(autoreset=True)

def print_section(title):
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.YELLOW}{title.upper()}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

def print_key_value(key, value, color=Fore.GREEN):
    if value is None or (isinstance(value, (list, str)) and len(value) == 0):
        print(f"{Fore.RED}{key}:{Style.RESET_ALL} None")
    else:
        print(f"{color}{key}:{Style.RESET_ALL} {value}")

def format_output(parsed: dict):
    """
    Imprime uma versão amigável do parsed no terminal.
    Esta função é segura para ser chamada mesmo que campos estejam faltando.
    """
    print("=== SQLMAP RESULT ===")

    target = parsed.get("target", {})
    print_key_value("URL", target.get("url"))
    print_key_value("DBMS", target.get("dbms"))
    print_key_value("OS", target.get("os"))
    print_key_value("Technology", target.get("technology"))

    print_section("Injection Points")
    inj = parsed.get("injection_points", [])
    if not inj:
        print(f"{Fore.YELLOW}Nenhum injection point detectado.")
    else:
        for i in inj:
            t = i.get("type", "N/A")
            title = i.get("title", None)
            payload = i.get("payload", None)
            print(f"{Fore.MAGENTA}- Type: {t}{Style.RESET_ALL}")
            if title:
                print(f"  {Fore.YELLOW}Title:{Style.RESET_ALL} {title}")
            if payload:
                print(f"  {Fore.YELLOW}Payload:{Style.RESET_ALL} {payload}")
            print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")

    print_section("Databases")
    dbs = parsed.get("databases", [])
    if not dbs:
        print(f"{Fore.YELLOW}Nenhum database encontrado.")
    else:
        for db in dbs:
            print(f"- {Fore.GREEN}{db}{Style.RESET_ALL}")

    print_section("Errors / Warnings")
    errs = parsed.get("errors", [])
    if not errs:
        print(f"{Fore.GREEN}Nenhuma mensagem de erro/aviso detectada.")
    else:
        for e in errs:
            print(f"- {Fore.RED}{e}{Style.RESET_ALL}")

    # opcional: manter raw_output curto (não printar todo, apenas tamanho)
    raw = parsed.get("raw_output", "")
    print_section("Raw output")
    if raw:
        print(f"raw_output_length: {len(raw)} chars")
    else:
        print("Sem raw_output")
