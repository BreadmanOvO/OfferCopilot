from typing import Any, Literal

from pydantic import BaseModel, Field


TaskMode = Literal["intent", "direct"]
TaskStatus = Literal[
    "pending",
    "research_running",
    "research_done",
    "action_running",
    "completed",
    "partial_success",
    "needs_input",
    "failed",
]


class CreateTaskRequest(BaseModel):
    mode: TaskMode
    intent: dict[str, Any] = Field(default_factory=dict)
    company_input: dict[str, Any] = Field(default_factory=dict)
    jd_text: str = ""
    resume_summary: str = ""
    concern_questions: list[str] = Field(default_factory=list)
    user_links: list[str] = Field(default_factory=list)


class AppendInputsRequest(BaseModel):
    user_links: list[str] = Field(default_factory=list)
    jd_text: str = ""
    resume_summary: str = ""
    concern_questions: list[str] = Field(default_factory=list)


class TaskResponse(BaseModel):
    id: int
    status: TaskStatus
    current_stage: str
    mode: TaskMode
    intent: dict[str, Any]
    company_input: dict[str, Any]
    jd_text: str
    resume_summary: str
    concern_questions: list[str]
    user_links: list[str]
    sources: list[dict[str, Any]]
    failed_sources: list[dict[str, Any]]
    uncertainty_notes: list[str]
    research: dict[str, Any]
    action: dict[str, Any]
    report: dict[str, Any]
    failure_reason: str
