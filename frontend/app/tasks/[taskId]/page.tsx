import { getTask } from "../../../lib/api";
import { ReportSection } from "../../../components/report-section";
import { SourcesView } from "../../../components/sources-view";
import { TaskProgress } from "../../../components/task-progress";
import { FollowUpBox } from "../../../components/follow-up-box";

export default async function TaskPage({ params }: { params: Promise<{ taskId: string }> }) {
  const { taskId } = await params;
  const task = await getTask(taskId);

  return (
    <main style={{ display: "grid", gap: 24, padding: 32, maxWidth: 900, margin: "0 auto" }}>
      <h1>Task #{task.id}</h1>
      <TaskProgress status={task.status} stage={task.current_stage} />
      <SourcesView sources={task.sources} />
      <ReportSection title="Company Profile" data={task.report.company_profile} />
      <ReportSection title="JD Breakdown" data={task.report.jd_breakdown} />
      <ReportSection title="Fit Analysis" data={task.report.fit_analysis} />
      <ReportSection title="Skills Gap" data={task.report.skills_gap_summary} />
      <ReportSection title="Risks" data={task.report.risks} />
      <ReportSection title="Interview Prep" data={task.report.interview_prep} />
      <ReportSection title="Action Checklist" data={task.report.action_checklist} />
      {task.uncertainty_notes.length > 0 ? (
        <ReportSection title="Uncertainty Notes" data={task.uncertainty_notes} />
      ) : null}
      {task.failure_reason ? (
        <section>
          <h2>Failure Reason</h2>
          <p style={{ color: "red" }}>{task.failure_reason}</p>
        </section>
      ) : null}
      <FollowUpBox taskId={task.id} />
    </main>
  );
}
