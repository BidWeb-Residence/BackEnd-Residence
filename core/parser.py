# core/parser.py
import re
from typing import Dict, List


def _extract_injection_points(output: str) -> List[Dict]:
 
    findings = []
    
    pattern = re.compile(
        r"Type:\s*(.+?)\s*\n\s*Title:\s*(.+?)\s*\n\s*Payload:\s*(.+?)(?=\n\s*\n|\n---|\Z)",
        re.IGNORECASE | re.DOTALL,
    )

    for m in pattern.finditer(output):
        t = m.group(1).strip()
        title = m.group(2).strip()
        payload = m.group(3).strip()
        findings.append({"type": t, "title": title, "payload": payload})
    return findings


def _extract_databases(output: str) -> List[str]:

    dbs = []
    
    block_match = re.search(r"available databases\s*\[\d+\]:\s*(.*?)(?:\n\n|\Z)", output, re.IGNORECASE | re.DOTALL)
    if block_match:
        block = block_match.group(1)
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        for ln in lines:
            m = re.match(r"\[\*\]\s*(.+)", ln)
            if m:
                name = m.group(1).strip()
                if not re.match(r"(starting|ending|fetched data)", name, re.IGNORECASE):
                    dbs.append(name)
    else:
        # Fallback: pega todas as linhas [*] <nome> e filtra
        all_matches = re.findall(r"\[\*\]\s*([A-Za-z0-9_\-]+)", output)
        for name in all_matches:
            if not re.match(r"(starting|ending|fetched|your sqlmap version)", name, re.IGNORECASE):
                dbs.append(name)
    # remove duplicados mantendo ordem
    seen = set()
    res = []
    for d in dbs:
        if d not in seen:
            seen.add(d)
            res.append(d)
    return res


def _extract_dbms(output: str) -> str:
    m = re.search(r"back-end DBMS[:\s]*([^\n]+)", output, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # fallback: procurar "the back-end DBMS is <name>"
    m2 = re.search(r"the back-end DBMS is\s*([^\n]+)", output, re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    return None


def _extract_os_and_tech(output: str) -> Dict[str, str]:
    os_val = None
    tech_val = None
    m_os = re.search(r"web server operating system:\s*([^\n]+)", output, re.IGNORECASE)
    if m_os:
        os_val = m_os.group(1).strip()
    m_tech = re.search(r"web application technology:\s*([^\n]+)", output, re.IGNORECASE)
    if m_tech:
        tech_val = m_tech.group(1).strip()
    return {"os": os_val, "technology": tech_val}


def _extract_errors(output: str) -> List[str]:
    errs = []
    for m in re.finditer(r"\[(CRITICAL|ERROR|WARNING)\]\s*(.+)", output, re.IGNORECASE):
        level = m.group(1).upper()
        msg = m.group(2).strip()
        errs.append(f"[{level}] {msg}")
    return errs


def parse_sqlmap_output(output: str, url: str) -> Dict:
    parsed = {
        "target": {
            "os": None,
            "technology": None,
            "dbms": None,
            "url": url
        },
        "injection_points": [],
        "databases": [],
        "errors": [],
        "raw_output": output
    }

    # DBMS, OS, technology
    parsed["target"]["dbms"] = _extract_dbms(output)
    meta = _extract_os_and_tech(output)
    parsed["target"]["os"] = meta.get("os")
    parsed["target"]["technology"] = meta.get("technology")

    # injection points
    parsed["injection_points"] = _extract_injection_points(output)

    # databases
    parsed["databases"] = _extract_databases(output)

    # errors/warnings
    parsed["errors"] = _extract_errors(output)

    return parsed
