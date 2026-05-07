from typing import Any

from app.tools.jd_parser import parse_jd
from app.tools.link_classifier import classify_url
from app.tools.search import generate_search_queries, search_ddg
from app.tools.synthesizer import synthesize_research
from app.tools.web_reader import fetch_page_content


def run_research(
    company: str,
    intent: dict[str, Any],
    jd_text: str = "",
    user_links: list[str] | None = None,
) -> dict[str, Any]:
    queries = generate_search_queries(company, intent, jd_text)
    all_results: list[dict[str, str]] = []
    for query in queries:
        results = search_ddg(query)
        all_results.extend(results)

    seen_urls = set()
    unique_results = []
    for r in all_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            unique_results.append(r)

    for link in (user_links or []):
        if link not in seen_urls:
            seen_urls.add(link)
            unique_results.append({"title": "User-provided link", "url": link, "snippet": ""})

    classified = []
    for r in unique_results:
        classified.append({**r, "source_type": classify_url(r["url"])})

    page_contents = []
    for r in classified[:8]:
        page = fetch_page_content(r["url"])
        page_contents.append(page)
        if page.get("error"):
            r["fetch_error"] = page["error"]

    successful = [r for r in classified if not r.get("fetch_error")]
    failed = [r for r in classified if r.get("fetch_error")]

    jd_breakdown = parse_jd(jd_text) if jd_text else {"summary": "", "requirements": [], "responsibilities": []}

    uncertainty_notes = []
    if len(successful) < 3:
        uncertainty_notes.append("Few sources were successfully fetched. Consider providing company links or JD text.")

    research = synthesize_research(successful, page_contents, jd_breakdown, uncertainty_notes)

    return {
        "sources": successful,
        "failed_sources": failed,
        "uncertainty_notes": uncertainty_notes,
        "research": research,
    }
