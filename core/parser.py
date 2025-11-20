import re

def parse_sqlmap_output(output: str, url: str) -> dict:
    parsed = {
        "target": {
            "os": [],
            "technology": [],
            "dbms": [],
            "url": url
        },
        "databases": [],
        "vulnerabilities": {
            "boolean_based": [],
            "error_based": [],
            "time_based": [],
            "union_based": []
        }
    }

    # ------------------------------- OS -------------------------------
    os_match = re.search(r"web server operating system: ([^\n]+)", output)
    if os_match:
        parsed["target"]["os"] = os_match.group(1).strip()

    # ------------------------------- TECHNOLOGY -------------------------------
    tech_match = re.search(r"web application technology: ([^\n]+)", output)
    if tech_match:
        parsed["target"]["technology"] = tech_match.group(1).strip()

    # ------------------------------- DBMS -------------------------------
    dbms_match = re.search(r"back-end DBMS is ([^\n]+)", output)
    if dbms_match:
        parsed["target"]["dbms"] = dbms_match.group(1).strip()

    # ------------------------------- DATABASES -------------------------------
    db_matches = re.findall(r"\[\*\] (.+)", output)
    parsed["databases"] = db_matches or []

    # ------------------------------- VULNERABILIDADES -------------------------------
    vuln_blocks = {
        "boolean_based": r"(Type: boolean-based blind[\s\S]*?)(?=Type:|\Z)",
        "error_based":   r"(Type: error-based[\s\S]*?)(?=Type:|\Z)",
        "time_based":    r"(Type: time-based blind[\s\S]*?)(?=Type:|\Z)",
        "union_based":   r"(Type: UNION query[\s\S]*?)(?=Type:|\Z)"
    }

    for key, pattern in vuln_blocks.items():
        block = re.search(pattern, output)
        if block:
            text = block.group(1)

            title = re.search(r"Title:\s*(.+)", text)
            payload = re.search(r"Payload:\s*(.+)", text)

            parsed["vulnerabilities"][key] = {
                "title": title.group(1).strip() if title else None,
                "payload": payload.group(1).strip() if payload else None
            }

    return parsed
