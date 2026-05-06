from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.tasks import TaskRepository
from app.schemas import AppendInputsRequest, CreateTaskRequest, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


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
