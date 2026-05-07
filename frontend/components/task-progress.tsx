export function TaskProgress({ status, stage }: { status: string; stage: string }) {
  const statusLabels: Record<string, string> = {
    pending: "Pending",
    research_running: "Researching...",
    research_done: "Research complete",
    action_running: "Analyzing...",
    completed: "Completed",
    partial_success: "Partially completed",
    needs_input: "Needs more information",
    failed: "Failed",
  };

  return (
    <section>
      <h2>Task Progress</h2>
      <p>Status: {statusLabels[status] || status}</p>
      {stage ? <p>Stage: {stage}</p> : null}
    </section>
  );
}
