"use client";

import { useState } from "react";
import { getCompanyJobs } from "../lib/api";
import { CompanyJobsResponse, JobPosition } from "../lib/types";

/* ------------------------------------------------------------------ */
/*  Styles                                                             */
/* ------------------------------------------------------------------ */

const s = {
  section: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  } as React.CSSProperties,
  backButton: {
    background: "none",
    border: "none",
    color: "#3b82f6",
    fontSize: 15,
    cursor: "pointer",
    padding: 0,
    marginBottom: 16,
  } as React.CSSProperties,
  title: {
    fontSize: 22,
    fontWeight: 700,
    marginBottom: 20,
    color: "#1f2937",
  } as React.CSSProperties,
  card: {
    background: "#fff",
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 24,
    marginBottom: 16,
    transition: "box-shadow 0.2s",
  } as React.CSSProperties,
  cardHover: {
    boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
  } as React.CSSProperties,
  companyName: {
    fontSize: 20,
    fontWeight: 700,
    color: "#1f2937",
    marginBottom: 8,
  } as React.CSSProperties,
  reason: {
    fontSize: 14,
    color: "#6b7280",
    lineHeight: 1.6,
    marginBottom: 16,
  } as React.CSSProperties,
  recruitLink: {
    fontSize: 13,
    color: "#3b82f6",
    textDecoration: "none",
    marginBottom: 12,
    display: "inline-block",
  } as React.CSSProperties,
  buttonRow: {
    display: "flex",
    gap: 10,
    flexWrap: "wrap" as const,
  } as React.CSSProperties,
  viewJobsBtn: {
    padding: "8px 18px",
    fontSize: 14,
    fontWeight: 600,
    color: "#3b82f6",
    backgroundColor: "#eff6ff",
    border: "1px solid #bfdbfe",
    borderRadius: 8,
    cursor: "pointer",
    transition: "all 0.15s",
  } as React.CSSProperties,
  selectBtn: {
    padding: "8px 18px",
    fontSize: 14,
    fontWeight: 600,
    color: "#fff",
    backgroundColor: "#2563eb",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    transition: "background-color 0.15s",
  } as React.CSSProperties,
  /* Position list */
  positionListWrapper: {
    marginTop: 16,
    borderTop: "1px solid #e5e7eb",
    paddingTop: 16,
  } as React.CSSProperties,
  positionListTitle: {
    fontSize: 16,
    fontWeight: 600,
    color: "#374151",
    marginBottom: 12,
  } as React.CSSProperties,
  positionItem: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "12px 16px",
    border: "1px solid #e5e7eb",
    borderRadius: 8,
    marginBottom: 8,
    cursor: "pointer",
    transition: "all 0.15s",
    backgroundColor: "#fff",
  } as React.CSSProperties,
  positionItemHover: {
    borderColor: "#3b82f6",
    backgroundColor: "#f0f7ff",
  } as React.CSSProperties,
  positionTitle: {
    fontSize: 15,
    fontWeight: 600,
    color: "#1f2937",
  } as React.CSSProperties,
  positionMeta: {
    fontSize: 13,
    color: "#6b7280",
    marginTop: 2,
  } as React.CSSProperties,
  positionArrow: {
    fontSize: 18,
    color: "#9ca3af",
    flexShrink: 0,
  } as React.CSSProperties,
  backToListBtn: {
    background: "none",
    border: "none",
    color: "#3b82f6",
    fontSize: 14,
    cursor: "pointer",
    padding: "8px 0",
    marginTop: 8,
  } as React.CSSProperties,
  /* Job detail */
  detailOverlay: {
    position: "fixed" as const,
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0,0,0,0.3)",
    zIndex: 100,
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
    paddingTop: 60,
    overflowY: "auto" as const,
  } as React.CSSProperties,
  detailCard: {
    background: "#fff",
    borderRadius: 12,
    padding: 32,
    maxWidth: 640,
    width: "90%",
    maxHeight: "80vh",
    overflowY: "auto" as const,
    boxShadow: "0 20px 60px rgba(0,0,0,0.15)",
  } as React.CSSProperties,
  detailTitle: {
    fontSize: 20,
    fontWeight: 700,
    color: "#1f2937",
    marginBottom: 12,
  } as React.CSSProperties,
  detailMeta: {
    fontSize: 14,
    color: "#6b7280",
    marginBottom: 8,
  } as React.CSSProperties,
  detailLink: {
    display: "inline-block",
    marginTop: 16,
    padding: "8px 18px",
    fontSize: 14,
    fontWeight: 600,
    color: "#fff",
    backgroundColor: "#2563eb",
    borderRadius: 8,
    textDecoration: "none",
  } as React.CSSProperties,
  loading: {
    textAlign: "center" as const,
    padding: 24,
    color: "#6b7280",
    fontSize: 14,
  } as React.CSSProperties,
  emptyHint: {
    textAlign: "center" as const,
    padding: 24,
    color: "#9ca3af",
    fontSize: 14,
  } as React.CSSProperties,
  statusMessage: {
    fontSize: 13,
    color: "#6b7280",
    backgroundColor: "#f9fafb",
    border: "1px solid #e5e7eb",
    borderRadius: 8,
    padding: "10px 12px",
    marginTop: 14,
    marginBottom: 12,
    lineHeight: 1.5,
  } as React.CSSProperties,
};

/* ------------------------------------------------------------------ */
/*  Job Detail Modal                                                   */
/* ------------------------------------------------------------------ */

function JobDetailOverlay({
  position,
  companyName,
  onClose,
}: {
  position: JobPosition;
  companyName: string;
  onClose: () => void;
}) {
  return (
    <div style={s.detailOverlay} onClick={onClose}>
      <div style={s.detailCard} onClick={(e) => e.stopPropagation()}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
          <h3 style={s.detailTitle}>{position.title}</h3>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "none",
              fontSize: 24,
              cursor: "pointer",
              color: "#9ca3af",
              padding: 0,
              lineHeight: 1,
            }}
          >
            x
          </button>
        </div>

        <p style={s.detailMeta}>
          <strong>公司:</strong> {companyName}
        </p>
        {position.location && (
          <p style={s.detailMeta}>
            <strong>城市:</strong> {position.location}
          </p>
        )}
        {position.department && (
          <p style={s.detailMeta}>
            <strong>部门:</strong> {position.department}
          </p>
        )}

        {position.description && (
          <p style={s.detailMeta}>
            <strong>岗位描述:</strong> {position.description}
          </p>
        )}
        {position.requirements && (
          <p style={s.detailMeta}>
            <strong>岗位要求:</strong> {position.requirements}
          </p>
        )}
        {position.source && (
          <p style={s.detailMeta}>
            <strong>信息来源:</strong> {position.source}
          </p>
        )}

        {position.url ? (
          <a
            href={position.url}
            target="_blank"
            rel="noopener noreferrer"
            style={s.detailLink}
          >
            查看完整岗位描述
          </a>
        ) : (
          <p style={{ ...s.detailMeta, marginTop: 16 }}>
            暂无详细链接，请访问招聘官网查看具体要求。
          </p>
        )}

        <button
          onClick={onClose}
          style={{
            ...s.backToListBtn,
            marginTop: 20,
            display: "block",
          }}
        >
          返回职位列表
        </button>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Position List                                                      */
/* ------------------------------------------------------------------ */

function PositionList({
  positions,
  onSelect,
  onBack,
}: {
  positions: JobPosition[];
  onSelect: (pos: JobPosition) => void;
  onBack: () => void;
}) {
  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);

  if (positions.length === 0) {
    return (
      <div style={s.positionListWrapper}>
        <p style={s.emptyHint}>暂未找到在招职位，请访问招聘官网查看。</p>
        <button onClick={onBack} style={s.backToListBtn}>
          返回公司列表
        </button>
      </div>
    );
  }

  return (
    <div style={s.positionListWrapper}>
      <h4 style={s.positionListTitle}>在招职位 ({positions.length})</h4>
      {positions.map((pos, idx) => (
        <div
          key={`${pos.title}-${idx}`}
          style={{
            ...s.positionItem,
            ...(hoveredIdx === idx ? s.positionItemHover : {}),
          }}
          onClick={() => onSelect(pos)}
          onMouseEnter={() => setHoveredIdx(idx)}
          onMouseLeave={() => setHoveredIdx(null)}
        >
          <div>
            <div style={s.positionTitle}>{pos.title}</div>
            <div style={s.positionMeta}>
              {[pos.location, pos.department].filter(Boolean).join(" | ")}
            </div>
          </div>
          <span style={s.positionArrow}>&gt;</span>
        </div>
      ))}
      <button onClick={onBack} style={s.backToListBtn}>
        返回公司列表
      </button>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Company Card                                                       */
/* ------------------------------------------------------------------ */

function CompanyCard({
  option,
  isExpanded,
  jobsData,
  isLoading,
  selectedPosition,
  error,
  onExpand,
  onCollapse,
  onSelectPosition,
  onClearSelectedPosition,
  onSelectCompany,
}: {
  option: { company_name: string; reason: string };
  isExpanded: boolean;
  jobsData: CompanyJobsResponse | undefined;
  isLoading: boolean;
  selectedPosition: JobPosition | null;
  error: string;
  onExpand: () => void;
  onCollapse: () => void;
  onSelectPosition: (pos: JobPosition) => void;
  onClearSelectedPosition: () => void;
  onSelectCompany: () => void;
}) {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      style={{
        ...s.card,
        ...(hovered ? s.cardHover : {}),
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <h3 style={s.companyName}>{option.company_name}</h3>
      <p style={s.reason}>{option.reason}</p>

      {isExpanded && jobsData?.recruit_url && (
        <a
          href={jobsData.recruit_url}
          target="_blank"
          rel="noopener noreferrer"
          style={s.recruitLink}
        >
          招聘官网: {jobsData.recruit_url}
        </a>
      )}

      <div style={s.buttonRow}>
        {isExpanded ? (
          <button onClick={onCollapse} style={s.viewJobsBtn}>
            收起职位
          </button>
        ) : (
          <button onClick={onExpand} style={s.viewJobsBtn}>
            查看职位
          </button>
        )}
        <button onClick={onSelectCompany} style={s.selectBtn}>
          选择这家公司
        </button>
      </div>

      {/* Position list (expanded) */}
      {isExpanded && (
        <>
          {isLoading ? (
            <div style={s.loading}>正在加载职位信息...</div>
          ) : error ? (
            <div style={s.emptyHint}>{error}</div>
          ) : jobsData ? (
            <>
              {jobsData.message && (
                <p style={s.statusMessage}>
                  {jobsData.message}
                  {jobsData.confidence && `（可信度: ${jobsData.confidence}）`}
                </p>
              )}
              <PositionList
                positions={jobsData.positions}
                onSelect={onSelectPosition}
                onBack={onCollapse}
              />
            </>
          ) : null}
        </>
      )}

      {/* Job detail overlay */}
      {selectedPosition && (
        <JobDetailOverlay
          position={selectedPosition}
          companyName={option.company_name}
          onClose={onClearSelectedPosition}
        />
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Main Component                                                     */
/* ------------------------------------------------------------------ */

export function CompanyOptions({
  options,
  onSelect,
  onBack,
}: {
  options: Array<{ company_name: string; reason: string }>;
  onSelect: (companyName: string) => void;
  onBack?: () => void;
}) {
  const [expandedCompany, setExpandedCompany] = useState<string | null>(null);
  const [selectedPosition, setSelectedPosition] = useState<JobPosition | null>(null);
  const [jobsData, setJobsData] = useState<Record<string, CompanyJobsResponse>>({});
  const [loadingJobs, setLoadingJobs] = useState<Record<string, boolean>>({});
  const [jobsError, setJobsError] = useState<Record<string, string>>({});

  async function handleExpand(companyName: string) {
    // Toggle if already expanded
    if (expandedCompany === companyName) {
      setExpandedCompany(null);
      setSelectedPosition(null);
      return;
    }

    setExpandedCompany(companyName);
    setSelectedPosition(null);

    // Fetch jobs if not cached
    if (!jobsData[companyName]) {
      setLoadingJobs((prev) => ({ ...prev, [companyName]: true }));
      try {
        const data = await getCompanyJobs(companyName);
        setJobsData((prev) => ({ ...prev, [companyName]: data }));
        setJobsError((prev) => ({ ...prev, [companyName]: "" }));
      } catch (err) {
        setJobsError((prev) => ({
          ...prev,
          [companyName]: "职位信息加载失败，请稍后重试",
        }));
      } finally {
        setLoadingJobs((prev) => ({ ...prev, [companyName]: false }));
      }
    }
  }

  function handleSelectPosition(pos: JobPosition) {
    setSelectedPosition(pos);
  }

  if (!options.length) return null;

  return (
    <section style={s.section}>
      {onBack && (
        <button onClick={onBack} style={s.backButton}>
          &larr; 返回上一步
        </button>
      )}
      <h2 style={s.title}>推荐公司</h2>
      {options.map((option) => (
        <CompanyCard
          key={option.company_name}
          option={option}
          isExpanded={expandedCompany === option.company_name}
          jobsData={jobsData[option.company_name]}
          isLoading={loadingJobs[option.company_name] ?? false}
          selectedPosition={
            expandedCompany === option.company_name ? selectedPosition : null
          }
          error={jobsError[option.company_name] ?? ""}
          onExpand={() => handleExpand(option.company_name)}
          onCollapse={() => {
            setExpandedCompany(null);
            setSelectedPosition(null);
          }}
          onSelectPosition={handleSelectPosition}
          onClearSelectedPosition={() => setSelectedPosition(null)}
          onSelectCompany={() => onSelect(option.company_name)}
        />
      ))}
    </section>
  );
}
