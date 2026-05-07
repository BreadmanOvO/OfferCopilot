export function ReportSection({ title, data }: { title: string; data: unknown }) {
  if (!data) return null;

  return (
    <section>
      <h2>{title}</h2>
      <pre style={{ whiteSpace: "pre-wrap", background: "#f9fafb", padding: 16, borderRadius: 8 }}>
        {typeof data === "string" ? data : JSON.stringify(data, null, 2)}
      </pre>
    </section>
  );
}
