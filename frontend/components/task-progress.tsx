export function TaskProgress({ status, stage }: { status: string; stage: string }) {
  const statusLabels: Record<string, string> = {
    pending: "待处理",
    research_running: "研究中...",
    research_done: "研究完成",
    action_running: "分析中...",
    completed: "已完成",
    partial_success: "部分完成",
    needs_input: "需要补充信息",
    failed: "失败",
  };

  return (
    <section>
      <h2>任务进度</h2>
      <p>状态：{statusLabels[status] || status}</p>
      {stage ? <p>阶段：{stage}</p> : null}
    </section>
  );
}
