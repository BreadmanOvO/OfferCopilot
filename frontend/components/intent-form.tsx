"use client";

import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { ALL_CITIES, POPULAR_CITIES } from "../lib/cities";
import {
  COMPANY_TYPES,
  JOB_CATEGORIES,
  getTitlesByCategory,
} from "../lib/job-categories";

/* ------------------------------------------------------------------ */
/*  Styles                                                             */
/* ------------------------------------------------------------------ */

const styles = {
  form: {
    display: "grid",
    gap: 20,
    maxWidth: 560,
    margin: "0 auto",
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  } as React.CSSProperties,
  label: {
    fontSize: 14,
    fontWeight: 600,
    color: "#333",
    marginBottom: 6,
    display: "block",
  } as React.CSSProperties,
  select: {
    width: "100%",
    padding: "8px 12px",
    fontSize: 14,
    border: "1px solid #d1d5db",
    borderRadius: 6,
    backgroundColor: "#fff",
    outline: "none",
    boxSizing: "border-box" as const,
  } as React.CSSProperties,
  textInput: {
    width: "100%",
    padding: "8px 12px",
    fontSize: 14,
    border: "1px solid #d1d5db",
    borderRadius: 6,
    outline: "none",
    boxSizing: "border-box" as const,
  } as React.CSSProperties,
  submitButton: {
    padding: "10px 24px",
    fontSize: 15,
    fontWeight: 600,
    color: "#fff",
    backgroundColor: "#2563eb",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    marginTop: 8,
    transition: "background-color 0.2s",
  } as React.CSSProperties,
  /* --- city dropdown --- */
  cityWrapper: {
    position: "relative" as const,
  } as React.CSSProperties,
  selectedTags: {
    display: "flex",
    flexWrap: "wrap" as const,
    gap: 6,
    minHeight: 36,
    padding: "6px 8px",
    border: "1px solid #d1d5db",
    borderRadius: 6,
    backgroundColor: "#fff",
    cursor: "pointer",
    alignItems: "center",
  } as React.CSSProperties,
  tag: {
    display: "inline-flex",
    alignItems: "center",
    gap: 4,
    padding: "2px 8px",
    fontSize: 13,
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
    borderRadius: 4,
  } as React.CSSProperties,
  tagRemove: {
    cursor: "pointer",
    fontWeight: 700,
    fontSize: 14,
    lineHeight: 1,
    color: "#2563eb",
    background: "none",
    border: "none",
    padding: 0,
  } as React.CSSProperties,
  placeholder: {
    color: "#9ca3af",
    fontSize: 14,
  } as React.CSSProperties,
  dropdownPanel: {
    position: "absolute" as const,
    top: "100%",
    left: 0,
    right: 0,
    marginTop: 4,
    backgroundColor: "#fff",
    border: "1px solid #d1d5db",
    borderRadius: 8,
    boxShadow: "0 4px 16px rgba(0,0,0,0.12)",
    zIndex: 50,
    maxHeight: 280,
    overflowY: "auto" as const,
  } as React.CSSProperties,
  searchInput: {
    width: "100%",
    padding: "8px 12px",
    fontSize: 14,
    border: "none",
    borderBottom: "1px solid #e5e7eb",
    outline: "none",
    boxSizing: "border-box" as const,
  } as React.CSSProperties,
  sectionTitle: {
    fontSize: 12,
    fontWeight: 600,
    color: "#6b7280",
    padding: "8px 12px 4px",
    textTransform: "uppercase" as const,
    letterSpacing: 0.5,
  } as React.CSSProperties,
  cityList: {
    display: "flex",
    flexWrap: "wrap" as const,
    gap: 4,
    padding: "4px 12px 8px",
  } as React.CSSProperties,
  cityChip: {
    padding: "4px 10px",
    fontSize: 13,
    border: "1px solid #e5e7eb",
    borderRadius: 4,
    backgroundColor: "#fff",
    cursor: "pointer",
    transition: "all 0.15s",
  } as React.CSSProperties,
  cityChipActive: {
    padding: "4px 10px",
    fontSize: 13,
    border: "1px solid #2563eb",
    borderRadius: 4,
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
    cursor: "pointer",
  } as React.CSSProperties,
  /* --- tag buttons (company type, role suggestions) --- */
  tagButtonRow: {
    display: "flex",
    flexWrap: "wrap" as const,
    gap: 8,
  } as React.CSSProperties,
  tagBtn: {
    padding: "6px 14px",
    fontSize: 13,
    border: "1px solid #d1d5db",
    borderRadius: 20,
    backgroundColor: "#fff",
    cursor: "pointer",
    transition: "all 0.15s",
  } as React.CSSProperties,
  tagBtnActive: {
    padding: "6px 14px",
    fontSize: 13,
    border: "1px solid #2563eb",
    borderRadius: 20,
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
    fontWeight: 600,
    cursor: "pointer",
  } as React.CSSProperties,
} as const;

/* ------------------------------------------------------------------ */
/*  City multi-select dropdown                                         */
/* ------------------------------------------------------------------ */

function CityDropdown({
  selected,
  onChange,
}: {
  selected: string[];
  onChange: (cities: string[]) => void;
}) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const ref = useRef<HTMLDivElement>(null);

  /* close on outside click */
  useEffect(() => {
    if (!open) return;
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [open]);

  const filtered = query.trim()
    ? ALL_CITIES.filter((c) => c.includes(query.trim()) && !selected.includes(c))
    : ALL_CITIES.filter((c) => !selected.includes(c));

  const popular = POPULAR_CITIES.filter((c) => !selected.includes(c));

  function toggle(city: string) {
    onChange(
      selected.includes(city)
        ? selected.filter((c) => c !== city)
        : [...selected, city]
    );
  }

  return (
    <div ref={ref} style={styles.cityWrapper}>
      {/* trigger */}
      <div style={styles.selectedTags} onClick={() => setOpen(!open)}>
        {selected.length === 0 && (
          <span style={styles.placeholder}>请选择意向城市</span>
        )}
        {selected.map((city) => (
          <span key={city} style={styles.tag}>
            {city}
            <button
              type="button"
              style={styles.tagRemove}
              onClick={(e) => {
                e.stopPropagation();
                toggle(city);
              }}
            >
              x
            </button>
          </span>
        ))}
      </div>

      {/* panel */}
      {open && (
        <div style={styles.dropdownPanel}>
          <input
            style={styles.searchInput}
            placeholder="搜索城市..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          {query.trim() ? (
            <>
              <div style={styles.sectionTitle}>搜索结果</div>
              <div style={styles.cityList}>
                {filtered.length === 0 && (
                  <span style={{ padding: "4px 12px", fontSize: 13, color: "#9ca3af" }}>
                    未找到匹配城市
                  </span>
                )}
                {filtered.map((city) => (
                  <button
                    key={city}
                    type="button"
                    style={
                      selected.includes(city) ? styles.cityChipActive : styles.cityChip
                    }
                    onClick={() => toggle(city)}
                  >
                    {city}
                  </button>
                ))}
              </div>
            </>
          ) : (
            <>
              <div style={styles.sectionTitle}>热门城市</div>
              <div style={styles.cityList}>
                {popular.map((city) => (
                  <button
                    key={city}
                    type="button"
                    style={styles.cityChip}
                    onClick={() => toggle(city)}
                  >
                    {city}
                  </button>
                ))}
              </div>
              <div style={styles.sectionTitle}>全部城市</div>
              <div style={styles.cityList}>
                {filtered.slice(0, 60).map((city) => (
                  <button
                    key={city}
                    type="button"
                    style={styles.cityChip}
                    onClick={() => toggle(city)}
                  >
                    {city}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Main component                                                     */
/* ------------------------------------------------------------------ */

export function IntentForm({
  initialValue,
  onDraftChange,
  onSubmit,
}: {
  initialValue?: {
    cities: string[];
    technicalField: string;
    customField: string;
    targetRoles: string[];
    companyTypes: string[];
  };
  onDraftChange?: (draft: {
    cities: string[];
    technicalField: string;
    customField: string;
    targetRoles: string[];
    companyTypes: string[];
  }) => void;
  onSubmit: (payload: Record<string, unknown>) => Promise<void>;
}) {
  const [cities, setCities] = useState<string[]>(initialValue?.cities ?? []);
  const [technicalField, setTechnicalField] = useState(
    initialValue?.technicalField ?? ""
  );
  const [customField, setCustomField] = useState(initialValue?.customField ?? "");
  const [targetRoles, setTargetRoles] = useState<string[]>(
    initialValue?.targetRoles ?? []
  );
  const [companyTypes, setCompanyTypes] = useState<string[]>(
    initialValue?.companyTypes ?? []
  );

  useEffect(() => {
    onDraftChange?.({
      cities,
      technicalField,
      customField,
      targetRoles,
      companyTypes,
    });
  }, [cities, technicalField, customField, targetRoles, companyTypes, onDraftChange]);

  /* when category changes, clear target roles and custom field */
  const handleCategoryChange = useCallback((label: string) => {
    setTechnicalField(label);
    setTargetRoles([]);
    if (label !== "其他") setCustomField("");
  }, []);

  /* toggle company type tag */
  function toggleCompanyType(type: string) {
    setCompanyTypes((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]
    );
  }

  const roleSuggestions = technicalField ? getTitlesByCategory(technicalField) : [];

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await onSubmit({
      mode: "intent",
      intent: {
        city: cities.join(","),
        technical_field: technicalField === "其他" && customField.trim() ? customField.trim() : technicalField,
        target_role: targetRoles.join(","),
        company_type: companyTypes.join(","),
      },
      company_input: {},
    });
  }

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      {/* ---- 意向城市 ---- */}
      <div>
        <label style={styles.label}>意向城市</label>
        <CityDropdown selected={cities} onChange={setCities} />
      </div>

      {/* ---- 技术方向 ---- */}
      <div>
        <label style={styles.label}>技术方向</label>
        <select
          style={styles.select}
          value={technicalField}
          onChange={(e) => handleCategoryChange(e.target.value)}
        >
          <option value="">请选择技术方向</option>
          {JOB_CATEGORIES.map((cat) => (
            <option key={cat.label} value={cat.label}>
              {cat.label}
            </option>
          ))}
        </select>
        {technicalField === "其他" && (
          <input
            style={{ ...styles.textInput, marginTop: 8 }}
            value={customField}
            onChange={(e) => setCustomField(e.target.value)}
            placeholder="请输入自定义技术方向"
          />
        )}
      </div>

      {/* ---- 目标职位 ---- */}
      <div>
        <label style={styles.label}>目标职位</label>
        {targetRoles.length > 0 && (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 8 }}>
            {targetRoles.map((role) => (
              <span key={role} style={styles.tag}>
                {role}
                <button
                  type="button"
                  style={styles.tagRemove}
                  onClick={() =>
                    setTargetRoles((prev) => prev.filter((r) => r !== role))
                  }
                >
                  x
                </button>
              </span>
            ))}
          </div>
        )}
        {roleSuggestions.length > 0 && (
          <div style={styles.tagButtonRow}>
            {roleSuggestions.map((title) => (
              <button
                key={title}
                type="button"
                style={
                  targetRoles.includes(title) ? styles.tagBtnActive : styles.tagBtn
                }
                onClick={() =>
                  setTargetRoles((prev) =>
                    prev.includes(title)
                      ? prev.filter((r) => r !== title)
                      : [...prev, title]
                  )
                }
              >
                {title}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* ---- 公司类型 ---- */}
      <div>
        <label style={styles.label}>公司类型</label>
        <div style={styles.tagButtonRow}>
          {COMPANY_TYPES.map((type) => (
            <button
              key={type}
              type="button"
              style={
                companyTypes.includes(type)
                  ? styles.tagBtnActive
                  : styles.tagBtn
              }
              onClick={() => toggleCompanyType(type)}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      {/* ---- Submit ---- */}
      <button type="submit" style={styles.submitButton}>
        推荐公司
      </button>
    </form>
  );
}
