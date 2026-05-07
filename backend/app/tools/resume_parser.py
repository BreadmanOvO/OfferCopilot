import re
from typing import Any


def parse_resume_summary(summary: str) -> dict[str, Any]:
    if not summary.strip():
        return {"summary": "", "keywords": [], "years_estimate": 0}

    words = re.findall(r"[a-zA-Z]{2,}|[\u4e00-\u9fff]{2,}", summary)
    keywords = list(dict.fromkeys(w.lower() for w in words if len(w) > 2))

    return {"summary": summary, "keywords": keywords[:30], "years_estimate": 0}
