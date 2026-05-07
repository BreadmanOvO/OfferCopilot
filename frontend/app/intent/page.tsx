"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { IntentForm } from "../../components/intent-form";
import { CompanyOptions } from "../../components/company-options";
import { createTask } from "../../lib/api";

export default function IntentPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [companyOptions, setCompanyOptions] = useState<
    Array<{ company_name: string; reason: string }> | null
  >(null);

  async function handleSubmit(payload: Record<string, unknown>) {
    setError(null);
    try {
      const result = await createTask(payload);
      const options = (result.report as Record<string, unknown>)
        ?.company_options as
        | Array<{ company_name: string; reason: string }>
        | undefined;

      if (options && options.length > 0) {
        setCompanyOptions(options);
      } else {
        router.push(`/tasks/${result.id}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "提交失败，请重试");
    }
  }

  function handleSelectCompany(companyName: string) {
    router.push(`/direct?company=${encodeURIComponent(companyName)}`);
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
        意向推荐
      </h1>
      <p style={{ color: "#666", fontSize: 16, marginBottom: 32 }}>
        填写求职意向，获取推荐公司
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

      {/* Company options or form */}
      {companyOptions ? (
        <CompanyOptions options={companyOptions} onSelect={handleSelectCompany} />
      ) : (
        <IntentForm onSubmit={handleSubmit} />
      )}
    </main>
  );
}
