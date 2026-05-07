"use client";

import { FormEvent, useState } from "react";

export function IntentForm({ onSubmit }: { onSubmit: (payload: Record<string, unknown>) => Promise<void> }) {
  const [city, setCity] = useState("");
  const [technicalField, setTechnicalField] = useState("");
  const [targetRole, setTargetRole] = useState("");
  const [companyType, setCompanyType] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await onSubmit({
      mode: "intent",
      intent: { city, technical_field: technicalField, target_role: targetRole, company_type: companyType },
      company_input: {},
    });
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
      <h2>Job Intent</h2>
      <input value={city} onChange={(e) => setCity(e.target.value)} placeholder="Target city" />
      <input value={technicalField} onChange={(e) => setTechnicalField(e.target.value)} placeholder="Technical field" />
      <input value={targetRole} onChange={(e) => setTargetRole(e.target.value)} placeholder="Target role" />
      <input value={companyType} onChange={(e) => setCompanyType(e.target.value)} placeholder="Preferred company type" />
      <button type="submit">Get company options</button>
    </form>
  );
}
