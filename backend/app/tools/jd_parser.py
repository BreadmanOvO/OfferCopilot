import re
from typing import Any


def parse_jd(jd_text: str) -> dict[str, Any]:
    if not jd_text.strip():
        return {"summary": "", "requirements": [], "responsibilities": []}

    lines = [line.strip() for line in jd_text.split("\n") if line.strip()]
    requirements = []
    responsibilities = []

    for line in lines:
        line_lower = line.lower()
        if any(kw in line_lower for kw in ["require", "qualif", "must have", "skill", "experience", "熟悉", "掌握", "具备", "要求"]):
            requirements.append(line)
        elif any(kw in line_lower for kw in ["responsib", "duty", "work on", "build", "develop", "负责", "参与"]):
            responsibilities.append(line)

    if not requirements and not responsibilities:
        requirements = lines[:5] if len(lines) > 5 else lines

    return {"summary": jd_text[:500], "requirements": requirements, "responsibilities": responsibilities}
