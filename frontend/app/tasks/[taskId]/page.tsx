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
      <h1>分析报告 #{task.id}</h1>
      <TaskProgress status={task.status} stage={task.current_stage} />
      <SourcesView sources={task.sources} />
      <ReportSection title="公司概况" data={task.report.company_profile} />
      <ReportSection title="职位分析" data={task.report.jd_breakdown} />
      <ReportSection title="匹配度分析" data={task.report.fit_analysis} />
      <ReportSection title="技能差距" data={task.report.skills_gap_summary} />
      <ReportSection title="风险提示" data={task.report.risks} />
      <ReportSection title="面试准备" data={task.report.interview_prep} />
      <ReportSection title="行动清单" data={task.report.action_checklist} />
      {task.uncertainty_notes.length > 0 ? (
        <ReportSection title="不确定性说明" data={task.uncertainty_notes} />
      ) : null}
      {task.failure_reason ? (
        <section>
          <h2>失败原因</h2>
          <p style={{ color: "red" }}>{task.failure_reason}</p>
        </section>
      ) : null}
      <FollowUpBox taskId={task.id} />
    </main>
  );
}
