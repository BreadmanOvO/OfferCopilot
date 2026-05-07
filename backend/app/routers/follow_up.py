import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import TaskRecord

router = APIRouter(tags=["follow-up"])


class FollowUpRequest(BaseModel):
    question: str


@router.post("/tasks/{task_id}/follow-up")
def create_follow_up(task_id: int, request: FollowUpRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    record = db.get(TaskRecord, task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")

    report = json.loads(record.report_payload)
    action = json.loads(record.action_payload)
    checklist = action.get("action_checklist", report.get("action_checklist", ["Review the report"]))
    first_step = checklist[0] if checklist else "Review the report"
    return {
        "answer": f"Based on the existing analysis, start with: {first_step}. Question received: {request.question}"
    }
