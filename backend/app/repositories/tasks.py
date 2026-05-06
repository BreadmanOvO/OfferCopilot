import json

from sqlalchemy.orm import Session

from app.models import TaskRecord
from app.schemas import AppendInputsRequest, CreateTaskRequest, TaskResponse
from app.services.recommendation_service import recommend_companies


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, request: CreateTaskRequest) -> TaskResponse:
        report = {}
        if request.mode == "intent":
            report["company_options"] = recommend_companies(request.intent)

        record = TaskRecord(
            mode=request.mode,
            status="pending",
            current_stage="created",
            intent_payload=json.dumps(request.intent),
            company_payload=json.dumps(request.company_input),
            user_links_payload=json.dumps(request.user_links),
            jd_text=request.jd_text,
            resume_summary=request.resume_summary,
            concern_questions=json.dumps(request.concern_questions),
            report_payload=json.dumps(report),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return self._to_response(record)

    def get(self, task_id: int) -> TaskResponse | None:
        record = self.db.get(TaskRecord, task_id)
        if record is None:
            return None
        return self._to_response(record)

    def update_status(
        self,
        task_id: int,
        *,
        status: str,
        current_stage: str = "",
        search_results: list[dict] | None = None,
        sources: list[dict] | None = None,
        failed_sources: list[dict] | None = None,
        uncertainty_notes: list[str] | None = None,
        research: dict | None = None,
        action: dict | None = None,
        report: dict | None = None,
        failure_reason: str = "",
    ) -> TaskResponse:
        record = self.db.get(TaskRecord, task_id)
        if record is None:
            raise ValueError(f"Task {task_id} not found")

        record.status = status
        if current_stage:
            record.current_stage = current_stage
        if search_results is not None:
            record.search_results_payload = json.dumps(search_results)
        if sources is not None:
            record.sources_payload = json.dumps(sources)
        if failed_sources is not None:
            record.failed_sources_payload = json.dumps(failed_sources)
        if uncertainty_notes is not None:
            record.uncertainty_notes_payload = json.dumps(uncertainty_notes)
        if research is not None:
            record.research_payload = json.dumps(research)
        if action is not None:
            record.action_payload = json.dumps(action)
        if report is not None:
            record.report_payload = json.dumps(report)
        if failure_reason:
            record.failure_reason = failure_reason

        self.db.commit()
        self.db.refresh(record)
        return self._to_response(record)

    def append_inputs(self, task_id: int, request: AppendInputsRequest) -> TaskResponse:
        record = self.db.get(TaskRecord, task_id)
        if record is None:
            raise ValueError(f"Task {task_id} not found")

        existing_links = json.loads(record.user_links_payload)
        record.user_links_payload = json.dumps(existing_links + request.user_links)

        if request.jd_text:
            existing_jd = record.jd_text
            record.jd_text = (existing_jd + "\n" + request.jd_text).strip() if existing_jd else request.jd_text

        if request.resume_summary:
            record.resume_summary = request.resume_summary

        if request.concern_questions:
            existing_q = json.loads(record.concern_questions)
            record.concern_questions = json.dumps(existing_q + request.concern_questions)

        self.db.commit()
        self.db.refresh(record)
        return self._to_response(record)

    def _to_response(self, record: TaskRecord) -> TaskResponse:
        return TaskResponse(
            id=record.id,
            status=record.status,
            current_stage=record.current_stage,
            mode=record.mode,
            intent=json.loads(record.intent_payload),
            company_input=json.loads(record.company_payload),
            jd_text=record.jd_text,
            resume_summary=record.resume_summary,
            concern_questions=json.loads(record.concern_questions),
            user_links=json.loads(record.user_links_payload),
            sources=json.loads(record.sources_payload),
            failed_sources=json.loads(record.failed_sources_payload),
            uncertainty_notes=json.loads(record.uncertainty_notes_payload),
            research=json.loads(record.research_payload),
            action=json.loads(record.action_payload),
            report=json.loads(record.report_payload),
            failure_reason=record.failure_reason,
        )
