"use client";

import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  return (
    <main
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        padding: 32,
      }}
    >
      <h1 style={{ fontSize: 2.5, marginBottom: 4 }}>OfferCopilot</h1>
      <p style={{ color: "#666", fontSize: 1.1, marginBottom: 48 }}>
        求职研究助手 — 帮你分析公司和岗位匹配度
      </p>

      <div
        style={{
          display: "flex",
          gap: 32,
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        {/* Intent Card */}
        <button
          onClick={() => router.push("/intent")}
          style={{
            background: "#fff",
            border: "2px solid #3b82f6",
            borderRadius: 12,
            padding: "40px 32px",
            width: 320,
            textAlign: "left",
            cursor: "pointer",
            transition: "transform 0.2s, box-shadow 0.2s",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "translateY(-4px)";
            e.currentTarget.style.boxShadow = "0 8px 24px rgba(59,130,246,0.2)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          <div style={{ fontSize: 48, marginBottom: 16 }}>🎯</div>
          <h2 style={{ color: "#3b82f6", fontSize: 1.4, marginBottom: 12 }}>
            意向推荐
          </h2>
          <p style={{ color: "#555", fontSize: 1, lineHeight: 1.6, margin: 0 }}>
            还没确定目标公司？填写求职意向，我来推荐候选公司
          </p>
        </button>

        {/* Direct Entry Card */}
        <button
          onClick={() => router.push("/direct")}
          style={{
            background: "#fff",
            border: "2px solid #10b981",
            borderRadius: 12,
            padding: "40px 32px",
            width: 320,
            textAlign: "left",
            cursor: "pointer",
            transition: "transform 0.2s, box-shadow 0.2s",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "translateY(-4px)";
            e.currentTarget.style.boxShadow = "0 8px 24px rgba(16,185,129,0.2)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          <div style={{ fontSize: 48, marginBottom: 16 }}>📋</div>
          <h2 style={{ color: "#10b981", fontSize: 1.4, marginBottom: 12 }}>
            直接分析
          </h2>
          <p style={{ color: "#555", fontSize: 1, lineHeight: 1.6, margin: 0 }}>
            已有目标公司和职位描述？直接开始深度分析
          </p>
        </button>
      </div>
    </main>
  );
}
