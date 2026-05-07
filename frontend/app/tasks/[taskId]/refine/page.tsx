"use client";

import { useParams, useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { appendInputs, runTask } from "../../../../lib/api";

export default function RefinePage() {
  const params = useParams();
  const router = useRouter();
  const taskId = Number(params.taskId);
  const [userLinks, setUserLinks] = useState("");
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);

    await appendInputs(taskId, {
      user_links: userLinks.split("\n").map((l) => l.trim()).filter(Boolean),
      jd_text: jdText,
    });

    await runTask(taskId);
    router.push(`/tasks/${taskId}`);
  }

  return (
    <main style={{ display: "grid", gap: 24, padding: 32, maxWidth: 800, margin: "0 auto" }}>
      <h1>Supplement Information</h1>
      <p>Provide additional links or JD text to improve the analysis.</p>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
        <textarea value={userLinks} onChange={(e) => setUserLinks(e.target.value)} placeholder="Company/JD links (one per line)" />
        <textarea value={jdText} onChange={(e) => setJdText(e.target.value)} placeholder="Paste additional JD text" />
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Submit and continue analysis"}
        </button>
      </form>
    </main>
  );
}
