"use client";

import { FormEvent, useState } from "react";
import { sendFollowUp } from "../lib/api";

export function FollowUpBox({ taskId }: { taskId: number }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const response = await sendFollowUp(taskId, question);
    setAnswer(response.answer);
  }

  return (
    <section>
      <h2>追问</h2>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 8 }}>
        <textarea value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="输入你的问题..." />
        <button type="submit">提问</button>
      </form>
      {answer ? <p>{answer}</p> : null}
    </section>
  );
}
