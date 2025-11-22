from colorama import Fore, Style, init
init(autoreset=True)

def print_section(title):
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.YELLOW}{title.upper()}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

def print_key_value(key, value, color=Fore.GREEN):
    if value:
        print(f"{color}{key}: {Style.RESET_ALL}{value}")
    else:
        print(f"{Fore.RED}{key}: {Style.RESET_ALL}None")

def format_output(parsed):
    print("=== SQLMAP RESULT ===")

    print(f"Target: {parsed['target']}")
    print(f"DBMS: {parsed['dbms']}")

    print("\n--- Injection Points ---")
    for inj in parsed["injection_points"]:
        print(f"Type: {inj['type']}")
        print(f"Payload: {inj['payload']}\n")

    print("\n--- Databases ---")
    for db in parsed["databases"]:
        print(f"- {db}")

    print("\n--- Errors ---")
    for err in parsed["errors"]:
        print(f"* {err}")
        
# não sendo usado no momento