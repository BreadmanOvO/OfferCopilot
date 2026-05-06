from typing import Any


def recommend_companies(intent: dict[str, Any]) -> list[dict[str, str]]:
    role = intent.get("target_role") or intent.get("role") or "Engineer"
    city = intent.get("city", "your target city")
    field = intent.get("technical_field", "technology")
    company_type = intent.get("company_type", "company")

    return [
        {
            "company_name": f"{city} {field.title()} Labs",
            "reason": f"A {company_type} focused on {field}, likely hiring for {role} roles.",
        },
        {
            "company_name": f"{city} Applied {field.title()}",
            "reason": f"Values hands-on {field} engineers with product focus.",
        },
        {
            "company_name": f"{city} {field.title()} Systems",
            "reason": f"Fast-moving team suitable for {role} candidates.",
        },
    ]
