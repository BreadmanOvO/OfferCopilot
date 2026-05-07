"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { CompanyOptions } from "../components/company-options";
import { DirectEntryForm } from "../components/direct-entry-form";
import { IntentForm } from "../components/intent-form";
import { createTask } from "../lib/api";

export default function HomePage() {
  const router = useRouter();
  const [companyOptions, setCompanyOptions] = useState<Array<{ company_name: string; reason: string }>>([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(payload: Record<string, unknown>) {
    setError("");
    try {
      const task = await createTask(payload);
      const options = task.report.company_options as Array<{ company_name: string; reason: string }> | undefined;

      if (options?.length) {
        setCompanyOptions(options);
        setSelectedCompany("");
        return;
      }

      router.push(`/tasks/${task.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    }
  }

  return (
    <main style={{ display: "grid", gap: 24, padding: 32, maxWidth: 800, margin: "0 auto" }}>
      <h1>OfferCopilot</h1>
      {error ? <p style={{ color: "red" }}>{error}</p> : null}
      <IntentForm onSubmit={handleSubmit} />
      <CompanyOptions options={companyOptions} onSelect={setSelectedCompany} />
      <DirectEntryForm onSubmit={handleSubmit} initialCompany={selectedCompany} />
    </main>
  );
}
