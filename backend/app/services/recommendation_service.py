from __future__ import annotations

import logging
from typing import Any

from app.tools.llm_client import llm

logger = logging.getLogger(__name__)


# Mock company database grouped by type (fallback)
_COMPANIES: dict[str, list[dict[str, str]]] = {
    "互联网大厂": [
        {"name": "字节跳动", "desc": "全球化的科技公司，旗下有抖音、今日头条等产品"},
        {"name": "腾讯", "desc": "社交与游戏领域的巨头，微信生态核心"},
        {"name": "阿里巴巴", "desc": "电商与云计算领军企业"},
        {"name": "美团", "desc": "本地生活服务领域的领先平台"},
        {"name": "京东", "desc": "以自营电商和物流体系著称"},
        {"name": "百度", "desc": "搜索引擎与AI技术驱动的科技公司"},
        {"name": "网易", "desc": "游戏、音乐、教育多元化互联网公司"},
        {"name": "拼多多", "desc": "社交电商领域的快速崛起者"},
    ],
    "外企": [
        {"name": "微软 (Microsoft)", "desc": "全球领先的软件与云服务公司"},
        {"name": "谷歌 (Google)", "desc": "搜索、广告与AI技术的全球领导者"},
        {"name": "亚马逊 (Amazon)", "desc": "电商与云计算巨头"},
        {"name": "苹果 (Apple)", "desc": "消费电子与生态系统的标杆"},
        {"name": "Meta", "desc": "社交与元宇宙领域的探索者"},
        {"name": "高盛 (Goldman Sachs)", "desc": "全球顶级投资银行"},
    ],
    "创业公司": [
        {"name": "月之暗面 (Moonshot AI)", "desc": "大模型领域的明星创业公司"},
        {"name": "智谱AI", "desc": "专注大模型研发的AI公司"},
        {"name": "MiniMax", "desc": "多模态大模型创业公司"},
        {"name": "SHEIN", "desc": "全球化快时尚电商平台"},
        {"name": "小红书", "desc": "生活方式社区与电商平台"},
    ],
    "国企/央企": [
        {"name": "中国移动", "desc": "最大的移动通信运营商"},
        {"name": "中国银行", "desc": "四大国有银行之一"},
        {"name": "国家电网", "desc": "全球最大的公用事业企业"},
        {"name": "中国石油", "desc": "综合性能源央企"},
        {"name": "中国电信", "desc": "综合智能信息服务运营商"},
    ],
    "上市公司": [
        {"name": "小米", "desc": "智能硬件与IoT生态链公司"},
        {"name": "比亚迪", "desc": "新能源汽车与电池技术领导者"},
        {"name": "宁德时代", "desc": "全球动力电池龙头企业"},
        {"name": "海尔智家", "desc": "全球化家电与智慧家居品牌"},
        {"name": "中芯国际", "desc": "国内领先的芯片代工企业"},
    ],
}

_DEFAULT_COMPANIES = [
    {"name": "字节跳动", "desc": "全球化的科技公司，旗下有抖音、今日头条等产品"},
    {"name": "腾讯", "desc": "社交与游戏领域的巨头，微信生态核心"},
    {"name": "阿里巴巴", "desc": "电商与云计算领军企业"},
    {"name": "微软 (Microsoft)", "desc": "全球领先的软件与云服务公司"},
    {"name": "小米", "desc": "智能硬件与IoT生态链公司"},
]


def recommend_companies(intent: dict[str, Any]) -> list[dict[str, str]]:
    """Return company recommendations based on user intent.

    Uses LLM when configured, falls back to hardcoded database.
    """
    # Try LLM-powered recommendations first
    if llm.is_configured:
        try:
            return _llm_recommend(intent)
        except Exception as e:
            logger.warning("LLM recommendation failed, falling back to database: %s", e)

    # Fallback: hardcoded database
    return _fallback_recommend(intent)


def _llm_recommend(intent: dict[str, Any]) -> list[dict[str, str]]:
    company_type = intent.get("company_type", "")
    field = intent.get("technical_field", "")
    role = intent.get("target_role", "")
    city = intent.get("city", "")

    context_parts: list[str] = []
    if field:
        context_parts.append(f"技术方向: {field}")
    if role:
        context_parts.append(f"目标职位: {role}")
    if company_type:
        context_parts.append(f"期望公司类型: {company_type}")
    if city:
        context_parts.append(f"意向城市: {city}")

    context_str = "\n".join(context_parts) if context_parts else "无特定偏好"

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个资深的求职顾问。根据用户的求职意向，推荐5家适合的公司。\n"
                "请用JSON格式返回，结构如下：\n"
                "{\n"
                '  "companies": [\n'
                '    {"company_name": "公司名称", "reason": "推荐理由（50-100字）"}\n'
                "  ]\n"
                "}\n"
                "推荐理由要具体说明为什么这家公司适合用户的背景和意向。\n"
                "只返回JSON，不要其他文字。用中文回答。"
            ),
        },
        {
            "role": "user",
            "content": f"我的求职意向：\n{context_str}",
        },
    ]

    result = llm.chat_json(messages, max_tokens=1024)
    companies = result.get("companies", [])

    if not companies:
        raise RuntimeError("LLM returned empty company list")

    return companies[:5]


def _fallback_recommend(intent: dict[str, Any]) -> list[dict[str, str]]:
    company_type = intent.get("company_type", "")
    field = intent.get("technical_field", "")
    role = intent.get("target_role", "")
    city = intent.get("city", "")

    candidates: list[dict[str, str]] = []
    types = [t.strip() for t in company_type.split(",") if t.strip()] if company_type else []

    for t in types:
        if t in _COMPANIES:
            candidates.extend(_COMPANIES[t])

    if not candidates:
        candidates = list(_DEFAULT_COMPANIES)

    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for c in candidates:
        if c["name"] not in seen:
            seen.add(c["name"])
            unique.append(c)

    context_parts: list[str] = []
    if field:
        context_parts.append(f"{field}")
    if role:
        context_parts.append(f"{role}")
    if city:
        context_parts.append(f"意向城市: {city}")
    context_str = "，".join(context_parts) if context_parts else ""

    results: list[dict[str, str]] = []
    for c in unique[:5]:
        reason = c["desc"]
        if context_str:
            reason += f"。适合{context_str}方向的求职者。"
        results.append({
            "company_name": c["name"],
            "reason": reason,
        })

    return results
