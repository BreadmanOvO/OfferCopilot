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
      <h2>Follow-up</h2>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 8 }}>
        <textarea value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ask a follow-up question" />
        <button type="submit">Ask</button>
      </form>
      {answer ? <p>{answer}</p> : null}
    </section>
  );
}
