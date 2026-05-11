from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.tasks import TaskRepository
from app.schemas import AppendInputsRequest, CompanyJobsResponse, CreateTaskRequest, TaskResponse
from app.workflows.task_workflow import run_task_workflow

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/jobs/{company_name}", response_model=CompanyJobsResponse)
def get_company_jobs(company_name: str) -> CompanyJobsResponse:
    from app.services.job_listing_service import fetch_company_jobs

    result = fetch_company_jobs(company_name)
    return CompanyJobsResponse(**result)


@router.post("", response_model=TaskResponse)
def create_task(request: CreateTaskRequest, db: Session = Depends(get_db)) -> TaskResponse:
    repository = TaskRepository(db)
    return repository.create(request)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    repository = TaskRepository(db)
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{task_id}/inputs", response_model=TaskResponse)
def append_inputs(task_id: int, request: AppendInputsRequest, db: Session = Depends(get_db)) -> TaskResponse:
    repository = TaskRepository(db)
    try:
        return repository.append_inputs(task_id, request)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/run", response_model=TaskResponse)
def run_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    repository = TaskRepository(db)
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    repository.update_status(task_id, status="research_running", current_stage="researching")

    task_data = {
        "company_input": task.company_input,
        "intent": task.intent,
        "jd_text": task.jd_text,
        "user_links": task.user_links,
        "resume_summary": task.resume_summary,
        "concern_questions": task.concern_questions,
    }

    try:
        result = run_task_workflow(task_id, task_data)
    except Exception as e:
        repository.update_status(task_id, status="failed", failure_reason=str(e))
        return repository.get(task_id)

    return repository.update_status(
        task_id,
        status=result["status"],
        current_stage=result.get("current_stage", ""),
        sources=result.get("sources"),
        failed_sources=result.get("failed_sources"),
        uncertainty_notes=result.get("uncertainty_notes"),
        research=result.get("research"),
        action=result.get("action"),
        report=result.get("report"),
        failure_reason=result.get("failure_reason", ""),
    )
