export type TaskMode = "intent" | "direct";

export type TaskStatus =
  | "pending"
  | "research_running"
  | "research_done"
  | "action_running"
  | "completed"
  | "partial_success"
  | "needs_input"
  | "failed";

export type Source = {
  title: string;
  url: string;
  snippet: string;
  source_type: string;
};

export type TaskResponse = {
  id: number;
  status: TaskStatus;
  current_stage: string;
  mode: TaskMode;
  intent: Record<string, unknown>;
  company_input: Record<string, unknown>;
  jd_text: string;
  resume_summary: string;
  concern_questions: string[];
  user_links: string[];
  sources: Source[];
  failed_sources: Source[];
  uncertainty_notes: string[];
  research: Record<string, unknown>;
  action: Record<string, unknown>;
  report: Record<string, unknown>;
  failure_reason: string;
};
