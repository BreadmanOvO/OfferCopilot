# Frontend Chinese Redesign Spec

## Overview

Redesign the OfferCopilot frontend to be fully in Chinese, improve the landing page UX with a two-card mode selection, and refine form fields based on mainstream Chinese job site patterns.

## Goals

1. All UI text in Chinese
2. Landing page: card-based mode selection (intent vs direct) instead of showing both forms
3. Intent form: all fields optional, city dropdown with Chinese cities, job categories from Boss直聘
4. Direct analysis form: split links into separate fields, remove abbreviations
5. Task detail page and all other pages: Chinese labels

## Page-by-Page Design

### 1. Landing Page (`app/page.tsx`)

Replace the current dual-form layout with two clickable cards:

- **意向推荐** card — blue accent, target icon, "还没确定目标公司？填写求职意向，我来推荐候选公司"
- **直接分析** card — green accent, clipboard icon, "已有目标公司和职位描述？直接开始深度分析"

Clicking a card navigates to `/intent` or `/direct` respectively.

### 2. Intent Form Page (`app/intent/page.tsx`) — NEW

All fields optional. Submit button: "推荐公司"

| Field | Type | Options |
|-------|------|---------|
| 意向城市 | Multi-select dropdown with search | All Chinese prefecture-level cities (地级市) |
| 技术方向 | Single select | 后端开发, 前端开发, 移动开发, AI/算法, 数据开发, 测试, 运维/DevOps, 产品, 设计, 项目管理, 网络安全, 其他 |
| 目标职位 | Text input with suggestions | Based on 技术方向 selection |
| 公司类型 | Multi-select tags | 互联网大厂, 外企, 创业公司, 国企/央企, 上市公司, 不限 |

### 3. Direct Analysis Form Page (`app/direct/page.tsx`) — NEW

Company name required, all other fields optional. Submit button: "开始分析"

| Field | Required | Notes |
|-------|----------|-------|
| 公司名称 | Yes | Text input |
| 职位描述 | No | Textarea |
| 公司官网 | No | URL input |
| 招聘页面链接 | No | URL input |
| 职位描述链接 | No | URL input |
| 其他参考链接 | No | Textarea, one per line |
| 简历摘要 | No | Textarea |
| 关心的问题 | No | Textarea, one per line |

### 4. Task Detail Page (`app/tasks/[taskId]/page.tsx`)

Chinese labels for all report sections:

| English (current) | Chinese (new) |
|-------------------|---------------|
| Company Profile | 公司概况 |
| JD Breakdown | 职位分析 |
| Fit Analysis | 匹配度分析 |
| Skills Gap | 技能差距 |
| Risks | 风险提示 |
| Interview Prep | 面试准备 |
| Action Checklist | 行动清单 |
| Sources | 参考来源 |
| Uncertainty Notes | 不确定性说明 |
| Failure Reason | 失败原因 |

Task status labels:

| English | Chinese |
|---------|---------|
| Pending | 待处理 |
| Researching... | 研究中... |
| Research complete | 研究完成 |
| Analyzing... | 分析中... |
| Completed | 已完成 |
| Partially completed | 部分完成 |
| Needs more information | 需要补充信息 |
| Failed | 失败 |

### 5. Refine Page (`app/tasks/[taskId]/refine/page.tsx`)

- Title: "补充信息"
- Description: "提供额外链接或职位描述以改善分析质量"
- Fields: 公司/职位描述链接 (textarea), 额外职位描述 (textarea)
- Button: "提交并继续分析"

### 6. Follow-up Box (`components/follow-up-box.tsx`)

- Title: "追问"
- Placeholder: "输入你的问题..."
- Button: "提问"

### 7. Company Options (`components/company-options.tsx`)

- Title: "推荐公司"
- Button: "选择这家公司"

### 8. Other Components

- `TaskProgress`: Chinese status labels
- `SourcesView`: Title "参考来源 (N)"
- `ReportSection`: Chinese titles passed from parent

## Technical Changes

### New Files

- `app/intent/page.tsx` — Intent form page
- `app/direct/page.tsx` — Direct analysis form page
- `lib/cities.ts` — Chinese city list (prefecture-level)
- `lib/job-categories.ts` — Job categories and titles from Boss直聘

### Modified Files

- `app/page.tsx` — Replace dual-form with card selection
- `app/tasks/[taskId]/page.tsx` — Chinese labels
- `app/tasks/[taskId]/refine/page.tsx` — Chinese labels
- `components/intent-form.tsx` — Rewrite with dropdowns and Chinese text
- `components/direct-entry-form.tsx` — Split links, Chinese labels
- `components/company-options.tsx` — Chinese labels
- `components/task-progress.tsx` — Chinese status labels
- `components/sources-view.tsx` — Chinese title
- `components/report-section.tsx` — No change (title passed from parent)
- `components/follow-up-box.tsx` — Chinese labels

### Backend Changes

- `app/schemas.py` — Update `CreateTaskRequest` to support new link fields (`company_url`, `recruitment_url`, `jd_url`, `other_urls`)

## Data Model Changes

### CreateTaskRequest

Add new fields for split links:

```python
company_url: str = ""
recruitment_url: str = ""
jd_url: str = ""
other_urls: list[str] = Field(default_factory=list)
```

Keep `user_links` for backward compatibility but populate from the new fields in the frontend.

## Scope

- Frontend-only changes for UI/UX
- Backend: only schema update for new link fields (optional, can reuse `user_links`)
- No changes to search, research, or action logic
- No changes to database schema (links stored as JSON in existing fields)
