"use client";

import { FormEvent, useEffect, useState } from "react";

export function DirectEntryForm({
  onSubmit,
  initialCompany = "",
}: {
  onSubmit: (payload: Record<string, unknown>) => Promise<void>;
  initialCompany?: string;
}) {
  const [company, setCompany] = useState(initialCompany);
  const [jd, setJd] = useState("");
  const [userLinks, setUserLinks] = useState("");
  const [resumeSummary, setResumeSummary] = useState("");
  const [concernQuestions, setConcernQuestions] = useState("");

  useEffect(() => { setCompany(initialCompany); }, [initialCompany]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await onSubmit({
      mode: "direct",
      intent: {},
      company_input: { company },
      jd_text: jd,
      user_links: userLinks.split("\n").map((l) => l.trim()).filter(Boolean),
      resume_summary: resumeSummary,
      concern_questions: concernQuestions.split("\n").map((q) => q.trim()).filter(Boolean),
    });
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
      <h2>Direct Analysis</h2>
      <input value={company} onChange={(e) => setCompany(e.target.value)} placeholder="Company name" />
      <textarea value={jd} onChange={(e) => setJd(e.target.value)} placeholder="Paste job description" />
      <textarea value={userLinks} onChange={(e) => setUserLinks(e.target.value)} placeholder="Company/JD links (one per line)" />
      <textarea value={resumeSummary} onChange={(e) => setResumeSummary(e.target.value)} placeholder="Resume summary" />
      <textarea value={concernQuestions} onChange={(e) => setConcernQuestions(e.target.value)} placeholder="Concern questions (one per line)" />
      <button type="submit">Run analysis</button>
    </form>
  );
}
