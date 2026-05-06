from sqlalchemy import Column, Integer, String, Text

from app.db import Base


class TaskRecord(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    mode = Column(String(32), nullable=False)
    status = Column(String(32), nullable=False, default="pending")
    current_stage = Column(String(32), nullable=False, default="")
    intent_payload = Column(Text, nullable=False, default="{}")
    company_payload = Column(Text, nullable=False, default="{}")
    user_links_payload = Column(Text, nullable=False, default="[]")
    jd_text = Column(Text, nullable=False, default="")
    resume_summary = Column(Text, nullable=False, default="")
    concern_questions = Column(Text, nullable=False, default="[]")
    search_results_payload = Column(Text, nullable=False, default="[]")
    sources_payload = Column(Text, nullable=False, default="[]")
    failed_sources_payload = Column(Text, nullable=False, default="[]")
    uncertainty_notes_payload = Column(Text, nullable=False, default="[]")
    research_payload = Column(Text, nullable=False, default="{}")
    action_payload = Column(Text, nullable=False, default="{}")
    report_payload = Column(Text, nullable=False, default="{}")
    failure_reason = Column(Text, nullable=False, default="")
