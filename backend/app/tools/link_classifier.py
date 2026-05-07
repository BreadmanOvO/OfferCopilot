import re


def classify_url(url: str) -> str:
    url_lower = url.lower()
    if re.search(r"(zhipin|lagou|liepin|boss|51job|智联|前程无忧|linkedin\.com/jobs|indeed\.com)", url_lower):
        return "job_board"
    return "general_web"
