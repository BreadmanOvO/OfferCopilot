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
      <h1>补充信息</h1>
      <p>提供额外链接或职位描述以改善分析质量。</p>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
        <textarea value={userLinks} onChange={(e) => setUserLinks(e.target.value)} placeholder="公司/职位描述链接（每行一个）" />
        <textarea value={jdText} onChange={(e) => setJdText(e.target.value)} placeholder="粘贴额外的职位描述内容" />
        <button type="submit" disabled={loading}>
          {loading ? "处理中..." : "提交并继续分析"}
        </button>
      </form>
    </main>
  );
}
