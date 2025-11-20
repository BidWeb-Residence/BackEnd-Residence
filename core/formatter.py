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

def format_output(parsed: dict):
    # ------------------------
    # TARGET SECTION
    # ------------------------
    print_section("TARGET INFO")
    t = parsed["target"]
    print_key_value("URL", t["url"])
    print_key_value("OS", t["os"])
    print_key_value("Technology", t["technology"])
    print_key_value("DBMS", t["dbms"])

    # ------------------------
    # DATABASES
    # ------------------------
    print_section("DATABASES ENUMERATED")
    if parsed["databases"]:
        for db in parsed["databases"]:
            print(f" - {Fore.GREEN}{db}")
    else:
        print(f"{Fore.RED}Nenhum banco encontrado.")

    # ------------------------
    # VULNERABILITIES
    # ------------------------
    print_section("VULNERABILITIES")

    vulns = parsed["vulnerabilities"]
    for vtype, info in vulns.items():
        print(f"\n{Fore.MAGENTA}>>> {vtype.upper()} <<<")

        if not info:
            print(f"{Fore.RED}Nenhuma vulnerabilidade detectada.")
            continue

        print(f"{Fore.YELLOW}Title:{Style.RESET_ALL}  {info['title']}")
        print(f"{Fore.YELLOW}Payload:{Style.RESET_ALL} {info['payload']}")
        print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")
