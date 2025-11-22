import re

def parse_sqlmap_output(output: str, url: str) -> dict:
    parsed = {
        "target": {
            "os": None,
            "technology": None,
            "dbms": None,
            "url": url
        },
        "databases": [],
        "vulnerabilities": {
            "boolean_based": None,
            "error_based": None,
            "time_based": None,
            "union_based": None
        },
        "raw_output": output
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
    vuln_patterns = {
        "boolean_based": r"Type: boolean-based blind[\s\S]*?Payload: (.+)",
        "error_based":   r"Type: error-based[\s\S]*?Payload: (.+)",
        "time_based":    r"Type: time-based blind[\s\S]*?Payload: (.+)",
        "union_based":   r"Type: UNION query[\s\S]*?Payload: (.+)"
    }

    for key, pattern in vuln_patterns.items():
        match = re.search(pattern, output)
        if match:
            parsed["vulnerabilities"][key] = match.group(1).strip()

    return parsed
