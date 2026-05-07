"use client";

import { FormEvent, useEffect, useState } from "react";

export function DirectEntryForm({
  onSubmit,
  initialCompany = "",
}: {
  onSubmit: (payload: Record<string, unknown>) => Promise<void>;
  initialCompany?: string;
}) {
  const [company, setCompany] = useState(initialCompany);
  const [jd, setJd] = useState("");
  const [companyUrl, setCompanyUrl] = useState("");
  const [recruitUrl, setRecruitUrl] = useState("");
  const [jdUrl, setJdUrl] = useState("");
  const [otherUrls, setOtherUrls] = useState("");
  const [resumeSummary, setResumeSummary] = useState("");
  const [concernQuestions, setConcernQuestions] = useState("");

  useEffect(() => {
    setCompany(initialCompany);
  }, [initialCompany]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const links = [companyUrl, recruitUrl, jdUrl]
      .map((l) => l.trim())
      .filter(Boolean);
    const extra = otherUrls
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);
    await onSubmit({
      mode: "direct",
      intent: {},
      company_input: { company_name: company },
      jd_text: jd,
      user_links: [...links, ...extra],
      resume_summary: resumeSummary,
      concern_questions: concernQuestions
        .split("\n")
        .map((q) => q.trim())
        .filter(Boolean),
    });
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
      <div>
        <label style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
          公司名称 *
        </label>
        <input
          required
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="如：字节跳动、阿里巴巴"
          style={inputStyle}
        />
      </div>

      <div>
        <label style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
          职位描述
        </label>
        <textarea
          value={jd}
          onChange={(e) => setJd(e.target.value)}
          placeholder="粘贴职位描述内容..."
          style={{ ...inputStyle, minHeight: 120 }}
        />
      </div>

      <div>
        <label style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
          公司官网
        </label>
        <input
          type="url"
          value={companyUrl}
          onChange={(e) => setCompanyUrl(e.target.value)}
          placeholder="https://..."
          style={inputStyle}
        />
      </div>

      <div>
        <label style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
          招聘页面链接
        </label>
        <input
          type="url"
          value={recruitUrl}
          onChange={(e) => setRecruitUrl(e.target.value)}
          placeholder="招聘信息页面地址"
          style={inputStyle}
        />
      </div>

      <div>
        <label style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
          职位描述链接
        </label>
        <input
          type="url"
          value={jdUrl}
          onChange={(e) => setJdUrl(e.target.value)}
          placeholder="具体岗位的页面地址"
          style={inputStyle}
        />
      </div>

      <div>
        <label style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
          其他参考链接
        </label>
        <textarea
          value={otherUrls}
          onChange={(e) => setOtherUrls(e.target.value)}
          placeholder="如：公司评价、新闻报道等（每行一个）"
          style={{ ...inputStyle, minHeight: 80 }}
        />
      </div>

      <div>
        <label style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
          简历摘要
        </label>
        <textarea
          value={resumeSummary}
          onChange={(e) => setResumeSummary(e.target.value)}
          placeholder="简要描述你的技能和经验..."
          style={{ ...inputStyle, minHeight: 80 }}
        />
      </div>

      <div>
        <label style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
          关心的问题
        </label>
        <textarea
          value={concernQuestions}
          onChange={(e) => setConcernQuestions(e.target.value)}
          placeholder="如：团队规模？技术栈？加班情况？（每行一个）"
          style={{ ...inputStyle, minHeight: 80 }}
        />
      </div>

      <button
        type="submit"
        style={{
          ...inputStyle,
          backgroundColor: "#10b981",
          color: "#fff",
          border: "none",
          cursor: "pointer",
          fontWeight: 600,
          padding: "10px 16px",
          fontSize: 15,
        }}
      >
        开始分析
      </button>
    </form>
  );
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "8px 12px",
  border: "1px solid #d1d5db",
  borderRadius: 6,
  fontSize: 14,
  boxSizing: "border-box",
};
