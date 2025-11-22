def format_output(parsed: dict):
    print("=== SQLMAP RESULT ===")

    # Valores principais com fallback
    url = parsed.get("url", "None")
    dbms = parsed.get("dbms", "None")
    os = parsed.get("os", "None")
    tech = parsed.get("technology", "None")

    print(f"URL: {url}")
    print(f"DBMS: {dbms}")
    print(f"OS: {os}")
    print(f"Technology: {tech}")
    print()

    print("============================================================")
    print("INJECTION POINTS")
    print("============================================================")

    injections = parsed.get("injection_points", [])
    if not injections:
        print("Nenhum injection point detectado.")
    else:
        for inj in injections:
            print(f"- {inj}")

    print()
    print("============================================================")
    print("DATABASES")
    print("============================================================")

    dbs = parsed.get("databases", [])
    if not dbs:
        print("Nenhum database encontrado.")
    else:
        for db in dbs:
            print(f"- {db}")

    print()
    print("============================================================")
    print("ERRORS / WARNINGS")
    print("============================================================")

    errors = parsed.get("errors", [])
    if not errors:
        print("Nenhum erro encontrado.")
    else:
        for err in errors:
            print(f"- {err}")

    print()
    print("============================================================")
    print("RAW OUTPUT")
    print("============================================================")

    raw = parsed.get("raw", "")
    print(f"raw_output_length: {len(raw)} chars")
