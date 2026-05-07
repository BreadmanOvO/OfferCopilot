"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { DirectEntryForm } from "../../components/direct-entry-form";
import { createTask } from "../../lib/api";

export default function DirectPage() {
  return (
    <Suspense>
      <DirectPageContent />
    </Suspense>
  );
}

function DirectPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialCompany = searchParams.get("company") || "";
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(payload: Record<string, unknown>) {
    setError(null);
    try {
      const result = await createTask(payload);
      router.push(`/tasks/${result.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "提交失败，请重试");
    }
  }

  return (
    <main
      style={{
        maxWidth: 720,
        margin: "0 auto",
        padding: "40px 24px",
      }}
    >
      {/* Back button */}
      <button
        onClick={() => router.push("/")}
        style={{
          background: "none",
          border: "none",
          color: "#3b82f6",
          fontSize: 15,
          cursor: "pointer",
          padding: 0,
          marginBottom: 24,
        }}
      >
        ← 返回首页
      </button>

      {/* Title */}
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>
        直接分析
      </h1>
      <p style={{ color: "#666", fontSize: 16, marginBottom: 32 }}>
        填写岗位信息，开始深度分析
      </p>

      {/* Error message */}
      {error && (
        <div
          style={{
            color: "#dc2626",
            backgroundColor: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: 8,
            padding: "12px 16px",
            marginBottom: 24,
            fontSize: 14,
          }}
        >
          {error}
        </div>
      )}

      {/* Direct entry form */}
      <DirectEntryForm onSubmit={handleSubmit} initialCompany={initialCompany} />
    </main>
  );
}
