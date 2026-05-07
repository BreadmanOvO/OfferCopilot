# Frontend Chinese Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the OfferCopilot frontend to be fully Chinese with improved UX for mode selection and form fields.

**Architecture:** Replace the dual-form landing page with a card-based mode selection that navigates to separate intent/direct form pages. Create new data files for Chinese cities and job categories. Update all components and pages with Chinese labels.

**Tech Stack:** Next.js 14, React 18, TypeScript

---

## File Structure

### New Files
- `frontend/lib/cities.ts` — Chinese prefecture-level city list
- `frontend/lib/job-categories.ts` — Job categories and titles
- `frontend/app/intent/page.tsx` — Intent form page
- `frontend/app/direct/page.tsx` — Direct analysis form page

### Modified Files
- `frontend/app/page.tsx` — Card-based mode selection
- `frontend/components/intent-form.tsx` — Rewrite with dropdowns
- `frontend/components/direct-entry-form.tsx` — Split links, Chinese labels
- `frontend/components/company-options.tsx` — Chinese labels
- `frontend/components/task-progress.tsx` — Chinese status labels
- `frontend/components/sources-view.tsx` — Chinese title
- `frontend/components/follow-up-box.tsx` — Chinese labels
- `frontend/app/tasks/[taskId]/page.tsx` — Chinese report section titles
- `frontend/app/tasks/[taskId]/refine/page.tsx` — Chinese labels

---

### Task 1: Create City Data File

**Files:**
- Create: `frontend/lib/cities.ts`

- [ ] **Step 1: Create the city list file**

```typescript
// Chinese prefecture-level cities grouped by province
export const CITIES_BY_PROVINCE: Record<string, string[]> = {
  "北京": ["北京市"],
  "上海": ["上海市"],
  "天津": ["天津市"],
  "重庆": ["重庆市"],
  "广东": ["广州市", "深圳市", "珠海市", "汕头市", "佛山市", "东莞市", "中山市", "惠州市", "江门市", "湛江市", "肇庆市", "茂名市", "梅州市", "揭阳市", "清远市", "韶关市", "河源市", "云浮市", "潮州市", "阳江市", "汕尾市"],
  "浙江": ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市"],
  "江苏": ["南京市", "苏州市", "无锡市", "常州市", "南通市", "徐州市", "盐城市", "扬州市", "镇江市", "泰州市", "连云港市", "淮安市", "宿迁市"],
  "山东": ["济南市", "青岛市", "烟台市", "潍坊市", "临沂市", "淄博市", "济宁市", "泰安市", "聊城市", "威海市", "枣庄市", "德州市", "日照市", "滨州市", "菏泽市", "东营市"],
  "四川": ["成都市", "绵阳市", "德阳市", "宜宾市", "南充市", "达州市", "泸州市", "乐山市", "内江市", "遂宁市", "攀枝花市", "眉山市", "广安市", "资阳市", "自贡市", "广元市", "雅安市", "巴中市", "凉山彝族自治州"],
  "湖北": ["武汉市", "宜昌市", "襄阳市", "荆州市", "黄冈市", "十堰市", "孝感市", "荆门市", "咸宁市", "鄂州市", "随州市", "黄石市", "恩施土家族苗族自治州"],
  "湖南": ["长沙市", "岳阳市", "株洲市", "衡阳市", "湘潭市", "常德市", "邵阳市", "郴州市", "娄底市", "永州市", "益阳市", "怀化市", "张家界市", "湘西土家族苗族自治州"],
  "河南": ["郑州市", "洛阳市", "南阳市", "许昌市", "周口市", "新乡市", "信阳市", "商丘市", "驻马店市", "焦作市", "平顶山市", "安阳市", "开封市", "濮阳市", "鹤壁市", "漯河市", "三门峡市"],
  "河北": ["石家庄市", "唐山市", "保定市", "邯郸市", "廊坊市", "沧州市", "邢台市", "衡水市", "承德市", "张家口市", "秦皇岛市"],
  "福建": ["福州市", "厦门市", "泉州市", "漳州市", "莆田市", "龙岩市", "三明市", "南平市", "宁德市"],
  "安徽": ["合肥市", "芜湖市", "蚌埠市", "阜阳市", "安庆市", "六安市", "马鞍山市", "淮南市", "淮北市", "铜陵市", "宣城市", "黄山市", "滁州市", "亳州市", "宿州市", "池州市"],
  "辽宁": ["沈阳市", "大连市", "鞍山市", "锦州市", "营口市", "盘锦市", "抚顺市", "丹东市", "朝阳市", "本溪市", "辽阳市", "葫芦岛市", "阜新市", "铁岭市"],
  "陕西": ["西安市", "咸阳市", "宝鸡市", "渭南市", "汉中市", "延安市", "安康市", "榆林市", "商洛市", "铜川市"],
  "江西": ["南昌市", "赣州市", "九江市", "宜春市", "吉安市", "上饶市", "抚州市", "景德镇市", "萍乡市", "新余市", "鹰潭市"],
  "黑龙江": ["哈尔滨市", "大庆市", "齐齐哈尔市", "牡丹江市", "绥化市", "佳木斯市", "鸡西市", "双鸭山市", "鹤岗市", "黑河市", "伊春市", "七台河市", "大兴安岭地区"],
  "广西": ["南宁市", "柳州市", "桂林市", "玉林市", "梧州市", "百色市", "贵港市", "河池市", "钦州市", "北海市", "防城港市", "来宾市", "贺州市", "崇左市"],
  "云南": ["昆明市", "曲靖市", "大理白族自治州", "红河哈尼族彝族自治州", "玉溪市", "文山壮族苗族自治州", "楚雄彝族自治州", "普洱市", "昭通市", "保山市", "丽江市", "临沧市"],
  "贵州": ["贵阳市", "遵义市", "毕节市", "黔南布依族苗族自治州", "黔东南苗族侗族自治州", "铜仁市", "六盘水市", "黔西南布依族苗族自治州", "安顺市"],
  "山西": ["太原市", "运城市", "临汾市", "大同市", "长治市", "晋城市", "忻州市", "晋中市", "朔州市", "吕梁市", "阳泉市"],
  "吉林": ["长春市", "吉林市", "四平市", "延边朝鲜族自治州", "通化市", "松原市", "白城市", "白山市", "辽源市"],
  "甘肃": ["兰州市", "天水市", "庆阳市", "酒泉市", "平凉市", "白银市", "张掖市", "武威市", "定西市", "陇南市", "金昌市", "嘉峪关市", "临夏回族自治州", "甘南藏族自治州"],
  "内蒙古": ["呼和浩特市", "包头市", "鄂尔多斯市", "赤峰市", "通辽市", "呼伦贝尔市", "巴彦淖尔市", "乌兰察布市", "兴安盟", "锡林郭勒盟", "乌海市", "阿拉善盟"],
  "新疆": ["乌鲁木齐市", "昌吉回族自治州", "伊犁哈萨克自治州", "阿克苏地区", "喀什地区", "哈密市", "吐鲁番市", "巴音郭楞蒙古自治州", "塔城地区", "和田地区", "阿勒泰地区", "克拉玛依市", "博尔塔拉蒙古自治州", "克孜勒苏柯尔克孜自治州"],
  "海南": ["海口市", "三亚市", "儋州市"],
  "宁夏": ["银川市", "吴忠市", "石嘴山市", "固原市", "中卫市"],
  "青海": ["西宁市", "海东市", "海西蒙古族藏族自治州", "海南藏族自治州", "海北藏族自治州", "黄南藏族自治州", "果洛藏族自治州", "玉树藏族自治州"],
  "西藏": ["拉萨市", "日喀则市", "林芝市", "昌都市", "山南市", "那曲市", "阿里地区"],
  "台湾": ["台北市", "新北市", "桃园市", "台中市", "台南市", "高雄市"],
  "香港": ["香港特别行政区"],
  "澳门": ["澳门特别行政区"],
};

// Flat list of all cities for search
export const ALL_CITIES: string[] = Object.values(CITIES_BY_PROVINCE).flat();

// Popular cities for quick selection
export const POPULAR_CITIES = [
  "北京市", "上海市", "广州市", "深圳市", "杭州市", "成都市",
  "武汉市", "南京市", "苏州市", "西安市", "重庆市", "天津市",
];
```

- [ ] **Step 2: Verify the file compiles**

Run: `cd frontend && npx tsc --noEmit lib/cities.ts`
Expected: No errors

- [ ] **Step 3: Commit**

```bash
git add frontend/lib/cities.ts
git commit -m "feat: add Chinese city data file"
```

---

### Task 2: Create Job Categories Data File

**Files:**
- Create: `frontend/lib/job-categories.ts`

- [ ] **Step 1: Create the job categories file**

```typescript
// Job categories based on Boss直聘 classification
export interface JobCategory {
  label: string;
  titles: string[];
}

export const JOB_CATEGORIES: JobCategory[] = [
  {
    label: "后端开发",
    titles: ["Java开发工程师", "Python开发工程师", "Go开发工程师", "C++开发工程师", "PHP开发工程师", ".NET开发工程师", "Node.js开发工程师", "Ruby开发工程师", "Rust开发工程师", "Scala开发工程师"],
  },
  {
    label: "前端开发",
    titles: ["前端开发工程师", "Web前端开发", "React开发工程师", "Vue开发工程师", "小程序开发工程师", "H5开发工程师", "全栈开发工程师"],
  },
  {
    label: "移动开发",
    titles: ["Android开发工程师", "iOS开发工程师", "Flutter开发工程师", "React Native开发工程师", "跨平台开发工程师"],
  },
  {
    label: "AI/算法",
    titles: ["算法工程师", "机器学习工程师", "深度学习工程师", "NLP算法工程师", "计算机视觉工程师", "推荐算法工程师", "语音识别工程师", "AI研究员", "大模型工程师"],
  },
  {
    label: "数据开发",
    titles: ["数据分析师", "数据工程师", "大数据开发工程师", "ETL工程师", "数据仓库工程师", "BI工程师", "数据科学家"],
  },
  {
    label: "测试",
    titles: ["测试工程师", "自动化测试工程师", "性能测试工程师", "测试开发工程师", "安全测试工程师", "质量管理工程师"],
  },
  {
    label: "运维/DevOps",
    titles: ["运维工程师", "DevOps工程师", "SRE工程师", "系统管理员", "网络工程师", "DBA", "云架构师"],
  },
  {
    label: "产品",
    titles: ["产品经理", "产品总监", "产品运营", "用户研究员", "需求分析师", "商业分析师"],
  },
  {
    label: "设计",
    titles: ["UI设计师", "UX设计师", "交互设计师", "视觉设计师", "平面设计师", "品牌设计师", "动效设计师"],
  },
  {
    label: "项目管理",
    titles: ["项目经理", "项目总监", "Scrum Master", "敏捷教练", "PMO"],
  },
  {
    label: "网络安全",
    titles: ["安全工程师", "渗透测试工程师", "安全运维工程师", "安全架构师", "安全研究员", "合规工程师"],
  },
  {
    label: "其他",
    titles: ["技术总监", "CTO", "架构师", "技术经理", "IT支持"],
  },
];

// Company types
export const COMPANY_TYPES = [
  "互联网大厂",
  "外企",
  "创业公司",
  "国企/央企",
  "上市公司",
  "不限",
];

// Get all job titles flat
export const ALL_JOB_TITLES: string[] = JOB_CATEGORIES.flatMap((cat) => cat.titles);

// Get titles by category label
export function getTitlesByCategory(label: string): string[] {
  return JOB_CATEGORIES.find((cat) => cat.label === label)?.titles ?? [];
}
```

- [ ] **Step 2: Verify the file compiles**

Run: `cd frontend && npx tsc --noEmit lib/job-categories.ts`
Expected: No errors

- [ ] **Step 3: Commit**

```bash
git add frontend/lib/job-categories.ts
git commit -m "feat: add job categories data file"
```

---

### Task 3: Rewrite Landing Page

**Files:**
- Modify: `frontend/app/page.tsx`

- [ ] **Step 1: Rewrite the landing page with card selection**

Replace the entire content of `frontend/app/page.tsx` with:

```tsx
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
        gap: 32,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1 style={{ fontSize: 32, marginBottom: 8 }}>OfferCopilot</h1>
        <p style={{ color: "#6b7280", fontSize: 16 }}>
          求职研究助手 — 帮你分析公司和岗位匹配度
        </p>
      </div>

      <div style={{ display: "flex", gap: 24, flexWrap: "wrap", justifyContent: "center" }}>
        <button
          onClick={() => router.push("/intent")}
          style={{
            border: "2px solid #3b82f6",
            borderRadius: 12,
            padding: "32px 40px",
            width: 280,
            cursor: "pointer",
            background: "#eff6ff",
            textAlign: "left",
            transition: "transform 0.2s, box-shadow 0.2s",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "translateY(-2px)";
            e.currentTarget.style.boxShadow = "0 4px 12px rgba(59,130,246,0.15)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          <div style={{ fontSize: 32, marginBottom: 12 }}>&#127919;</div>
          <h2 style={{ fontSize: 20, marginBottom: 8, color: "#1e40af" }}>意向推荐</h2>
          <p style={{ color: "#6b7280", fontSize: 14, lineHeight: 1.5 }}>
            还没确定目标公司？
            <br />
            填写求职意向，我来推荐候选公司
          </p>
        </button>

        <button
          onClick={() => router.push("/direct")}
          style={{
            border: "2px solid #10b981",
            borderRadius: 12,
            padding: "32px 40px",
            width: 280,
            cursor: "pointer",
            background: "#ecfdf5",
            textAlign: "left",
            transition: "transform 0.2s, box-shadow 0.2s",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "translateY(-2px)";
            e.currentTarget.style.boxShadow = "0 4px 12px rgba(16,185,129,0.15)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          <div style={{ fontSize: 32, marginBottom: 12 }}>&#128203;</div>
          <h2 style={{ fontSize: 20, marginBottom: 8, color: "#065f46" }}>直接分析</h2>
          <p style={{ color: "#6b7280", fontSize: 14, lineHeight: 1.5 }}>
            已有目标公司和职位描述？
            <br />
            直接开始深度分析
          </p>
        </button>
      </div>
    </main>
  );
}
```

- [ ] **Step 2: Test the page renders**

Run: `cd frontend && npm run build 2>&1 | head -20`
Expected: Build succeeds

- [ ] **Step 3: Commit**

```bash
git add frontend/app/page.tsx
git commit -m "feat: rewrite landing page with card-based mode selection"
```

---

### Task 4: Rewrite Intent Form Component

**Files:**
- Modify: `frontend/components/intent-form.tsx`

- [ ] **Step 1: Rewrite the intent form with dropdowns and Chinese text**

Replace the entire content of `frontend/components/intent-form.tsx` with:

```tsx
"use client";

import { FormEvent, useState } from "react";
import { ALL_CITIES, POPULAR_CITIES } from "../lib/cities";
import { JOB_CATEGORIES, COMPANY_TYPES, getTitlesByCategory } from "../lib/job-categories";

export function IntentForm({
  onSubmit,
}: {
  onSubmit: (payload: Record<string, unknown>) => Promise<void>;
}) {
  const [selectedCities, setSelectedCities] = useState<string[]>([]);
  const [citySearch, setCitySearch] = useState("");
  const [showCityDropdown, setShowCityDropdown] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [targetRole, setTargetRole] = useState("");
  const [selectedCompanyTypes, setSelectedCompanyTypes] = useState<string[]>([]);

  const filteredCities = ALL_CITIES.filter(
    (city) => city.includes(citySearch) && !selectedCities.includes(city)
  ).slice(0, 20);

  const suggestedTitles = selectedCategory ? getTitlesByCategory(selectedCategory) : [];

  function toggleCity(city: string) {
    setSelectedCities((prev) =>
      prev.includes(city) ? prev.filter((c) => c !== city) : [...prev, city]
    );
  }

  function toggleCompanyType(type: string) {
    setSelectedCompanyTypes((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]
    );
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await onSubmit({
      mode: "intent",
      intent: {
        city: selectedCities.join(","),
        technical_field: selectedCategory,
        target_role: targetRole,
        company_type: selectedCompanyTypes.join(","),
      },
      company_input: {},
    });
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: 20 }}>
      {/* City selector */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          意向城市
        </label>
        <div style={{ position: "relative" }}>
          <div
            style={{
              border: "1px solid #d1d5db",
              borderRadius: 8,
              padding: "8px 12px",
              background: "white",
              display: "flex",
              flexWrap: "wrap",
              gap: 6,
              minHeight: 40,
              alignItems: "center",
              cursor: "text",
            }}
            onClick={() => setShowCityDropdown(true)}
          >
            {selectedCities.length > 0 ? (
              selectedCities.map((city) => (
                <span
                  key={city}
                  style={{
                    background: "#eff6ff",
                    color: "#3b82f6",
                    padding: "2px 8px",
                    borderRadius: 4,
                    fontSize: 13,
                    display: "flex",
                    alignItems: "center",
                    gap: 4,
                  }}
                >
                  {city}
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleCity(city);
                    }}
                    style={{
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                      padding: 0,
                      color: "#3b82f6",
                      fontSize: 16,
                    }}
                  >
                    ×
                  </button>
                </span>
              ))
            ) : (
              <span style={{ color: "#9ca3af" }}>请选择城市（可多选）</span>
            )}
          </div>

          {showCityDropdown && (
            <div
              style={{
                position: "absolute",
                top: "100%",
                left: 0,
                right: 0,
                background: "white",
                border: "1px solid #d1d5db",
                borderRadius: 8,
                marginTop: 4,
                maxHeight: 300,
                overflow: "auto",
                zIndex: 10,
                boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
              }}
            >
              <div style={{ padding: 8, borderBottom: "1px solid #e5e7eb" }}>
                <input
                  type="text"
                  value={citySearch}
                  onChange={(e) => setCitySearch(e.target.value)}
                  placeholder="搜索城市..."
                  style={{
                    width: "100%",
                    border: "1px solid #d1d5db",
                    borderRadius: 6,
                    padding: "6px 10px",
                    fontSize: 14,
                    outline: "none",
                  }}
                />
              </div>

              {/* Popular cities */}
              {citySearch === "" && (
                <div style={{ padding: "8px 12px", borderBottom: "1px solid #e5e7eb" }}>
                  <div style={{ fontSize: 12, color: "#9ca3af", marginBottom: 6 }}>热门城市</div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                    {POPULAR_CITIES.map((city) => (
                      <button
                        key={city}
                        type="button"
                        onClick={() => toggleCity(city)}
                        style={{
                          background: selectedCities.includes(city) ? "#3b82f6" : "#f3f4f6",
                          color: selectedCities.includes(city) ? "white" : "#374151",
                          border: "none",
                          borderRadius: 16,
                          padding: "4px 12px",
                          fontSize: 13,
                          cursor: "pointer",
                        }}
                      >
                        {city}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Filtered cities */}
              <div style={{ padding: 4 }}>
                {filteredCities.map((city) => (
                  <div
                    key={city}
                    onClick={() => toggleCity(city)}
                    style={{
                      padding: "8px 12px",
                      cursor: "pointer",
                      borderRadius: 6,
                      fontSize: 14,
                      background: selectedCities.includes(city) ? "#eff6ff" : "transparent",
                      color: selectedCities.includes(city) ? "#3b82f6" : "#374151",
                    }}
                  >
                    {city}
                  </div>
                ))}
              </div>

              <div
                style={{
                  padding: "8px 12px",
                  borderTop: "1px solid #e5e7eb",
                  textAlign: "center",
                }}
              >
                <button
                  type="button"
                  onClick={() => setShowCityDropdown(false)}
                  style={{
                    background: "none",
                    border: "none",
                    color: "#3b82f6",
                    cursor: "pointer",
                    fontSize: 14,
                  }}
                >
                  关闭
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Technical field */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          技术方向
        </label>
        <select
          value={selectedCategory}
          onChange={(e) => {
            setSelectedCategory(e.target.value);
            setTargetRole("");
          }}
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
            background: "white",
          }}
        >
          <option value="">请选择技术方向</option>
          {JOB_CATEGORIES.map((cat) => (
            <option key={cat.label} value={cat.label}>
              {cat.label}
            </option>
          ))}
        </select>
      </div>

      {/* Target role */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          目标职位
        </label>
        <input
          type="text"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
          placeholder="输入或选择具体职位"
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
          }}
        />
        {suggestedTitles.length > 0 && (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 }}>
            {suggestedTitles.map((title) => (
              <button
                key={title}
                type="button"
                onClick={() => setTargetRole(title)}
                style={{
                  background: targetRole === title ? "#3b82f6" : "#f3f4f6",
                  color: targetRole === title ? "white" : "#374151",
                  border: "none",
                  borderRadius: 16,
                  padding: "4px 12px",
                  fontSize: 13,
                  cursor: "pointer",
                }}
              >
                {title}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Company type */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          公司类型
        </label>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {COMPANY_TYPES.map((type) => (
            <button
              key={type}
              type="button"
              onClick={() => toggleCompanyType(type)}
              style={{
                background: selectedCompanyTypes.includes(type) ? "#3b82f6" : "#f3f4f6",
                color: selectedCompanyTypes.includes(type) ? "white" : "#374151",
                border: "none",
                borderRadius: 16,
                padding: "6px 16px",
                fontSize: 14,
                cursor: "pointer",
              }}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      <button
        type="submit"
        style={{
          width: "100%",
          padding: 12,
          background: "#3b82f6",
          color: "white",
          border: "none",
          borderRadius: 8,
          fontSize: 16,
          cursor: "pointer",
          marginTop: 8,
        }}
      >
        推荐公司
      </button>
    </form>
  );
}
```

- [ ] **Step 2: Test the component compiles**

Run: `cd frontend && npm run build 2>&1 | head -20`
Expected: Build succeeds

- [ ] **Step 3: Commit**

```bash
git add frontend/components/intent-form.tsx
git commit -m "feat: rewrite intent form with Chinese dropdowns"
```

---

### Task 5: Create Intent Page

**Files:**
- Create: `frontend/app/intent/page.tsx`

- [ ] **Step 1: Create the intent page**

```tsx
"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { IntentForm } from "../../components/intent-form";
import { CompanyOptions } from "../../components/company-options";
import { createTask } from "../../lib/api";

export default function IntentPage() {
  const router = useRouter();
  const [companyOptions, setCompanyOptions] = useState<
    Array<{ company_name: string; reason: string }>
  >([]);
  const [error, setError] = useState("");

  async function handleSubmit(payload: Record<string, unknown>) {
    setError("");
    try {
      const task = await createTask(payload);
      const options = task.report.company_options as
        | Array<{ company_name: string; reason: string }>
        | undefined;

      if (options?.length) {
        setCompanyOptions(options);
        return;
      }

      router.push(`/tasks/${task.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "请求失败");
    }
  }

  function handleSelectCompany(companyName: string) {
    router.push(`/direct?company=${encodeURIComponent(companyName)}`);
  }

  return (
    <main
      style={{
        display: "grid",
        gap: 24,
        padding: 32,
        maxWidth: 600,
        margin: "0 auto",
      }}
    >
      <div>
        <button
          onClick={() => router.push("/")}
          style={{
            background: "none",
            border: "none",
            color: "#3b82f6",
            cursor: "pointer",
            fontSize: 14,
            padding: 0,
          }}
        >
          ← 返回首页
        </button>
        <h1 style={{ marginTop: 12 }}>意向推荐</h1>
        <p style={{ color: "#6b7280" }}>填写求职意向，获取推荐公司</p>
      </div>

      {error && <p style={{ color: "#ef4444" }}>{error}</p>}

      <IntentForm onSubmit={handleSubmit} />

      {companyOptions.length > 0 && (
        <CompanyOptions options={companyOptions} onSelect={handleSelectCompany} />
      )}
    </main>
  );
}
```

- [ ] **Step 2: Test the page compiles**

Run: `cd frontend && npm run build 2>&1 | head -20`
Expected: Build succeeds

- [ ] **Step 3: Commit**

```bash
git add frontend/app/intent/page.tsx
git commit -m "feat: add intent page with company recommendation flow"
```

---

### Task 6: Rewrite Direct Entry Form Component

**Files:**
- Modify: `frontend/components/direct-entry-form.tsx`

- [ ] **Step 1: Rewrite the form with split links and Chinese labels**

Replace the entire content of `frontend/components/direct-entry-form.tsx` with:

```tsx
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
  const [recruitmentUrl, setRecruitmentUrl] = useState("");
  const [jdUrl, setJdUrl] = useState("");
  const [otherUrls, setOtherUrls] = useState("");
  const [resumeSummary, setResumeSummary] = useState("");
  const [concernQuestions, setConcernQuestions] = useState("");

  useEffect(() => {
    setCompany(initialCompany);
  }, [initialCompany]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    // Combine all links into user_links for backward compatibility
    const userLinks = [companyUrl, recruitmentUrl, jdUrl]
      .map((l) => l.trim())
      .filter(Boolean)
      .concat(
        otherUrls
          .split("\n")
          .map((l) => l.trim())
          .filter(Boolean)
      );

    await onSubmit({
      mode: "direct",
      intent: {},
      company_input: { company_name: company },
      jd_text: jd,
      user_links: userLinks,
      resume_summary: resumeSummary,
      concern_questions: concernQuestions
        .split("\n")
        .map((q) => q.trim())
        .filter(Boolean),
    });
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: 16 }}>
      {/* Company name - required */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          公司名称 <span style={{ color: "#ef4444" }}>*</span>
        </label>
        <input
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="如：字节跳动、阿里巴巴"
          required
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
          }}
        />
      </div>

      {/* Job description */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          职位描述
        </label>
        <textarea
          value={jd}
          onChange={(e) => setJd(e.target.value)}
          placeholder="粘贴职位描述内容..."
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
            minHeight: 100,
          }}
        />
      </div>

      {/* Company URL */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          公司官网
        </label>
        <input
          value={companyUrl}
          onChange={(e) => setCompanyUrl(e.target.value)}
          placeholder="https://..."
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
          }}
        />
      </div>

      {/* Recruitment URL */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          招聘页面链接
        </label>
        <input
          value={recruitmentUrl}
          onChange={(e) => setRecruitmentUrl(e.target.value)}
          placeholder="招聘信息页面地址"
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
          }}
        />
      </div>

      {/* JD URL */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          职位描述链接
        </label>
        <input
          value={jdUrl}
          onChange={(e) => setJdUrl(e.target.value)}
          placeholder="具体岗位的页面地址"
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
          }}
        />
      </div>

      {/* Other URLs */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          其他参考链接
        </label>
        <textarea
          value={otherUrls}
          onChange={(e) => setOtherUrls(e.target.value)}
          placeholder="如：公司评价、新闻报道等（每行一个）"
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
            minHeight: 60,
          }}
        />
      </div>

      {/* Resume summary */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          简历摘要
        </label>
        <textarea
          value={resumeSummary}
          onChange={(e) => setResumeSummary(e.target.value)}
          placeholder="简要描述你的技能和经验..."
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
            minHeight: 80,
          }}
        />
      </div>

      {/* Concern questions */}
      <div>
        <label style={{ display: "block", fontWeight: 600, marginBottom: 6, fontSize: 14 }}>
          关心的问题
        </label>
        <textarea
          value={concernQuestions}
          onChange={(e) => setConcernQuestions(e.target.value)}
          placeholder="如：团队规模？技术栈？加班情况？（每行一个）"
          style={{
            width: "100%",
            border: "1px solid #d1d5db",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14,
            minHeight: 60,
          }}
        />
      </div>

      <button
        type="submit"
        style={{
          width: "100%",
          padding: 12,
          background: "#10b981",
          color: "white",
          border: "none",
          borderRadius: 8,
          fontSize: 16,
          cursor: "pointer",
          marginTop: 8,
        }}
      >
        开始分析
      </button>
    </form>
  );
}
```

- [ ] **Step 2: Test the component compiles**

Run: `cd frontend && npm run build 2>&1 | head -20`
Expected: Build succeeds

- [ ] **Step 3: Commit**

```bash
git add frontend/components/direct-entry-form.tsx
git commit -m "feat: rewrite direct entry form with split links and Chinese labels"
```

---

### Task 7: Create Direct Analysis Page

**Files:**
- Create: `frontend/app/direct/page.tsx`

- [ ] **Step 1: Create the direct analysis page**

```tsx
"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { DirectEntryForm } from "../../components/direct-entry-form";
import { createTask } from "../../lib/api";

export default function DirectPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialCompany = searchParams.get("company") || "";
  const [error, setError] = useState("");

  async function handleSubmit(payload: Record<string, unknown>) {
    setError("");
    try {
      const task = await createTask(payload);
      router.push(`/tasks/${task.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "请求失败");
    }
  }

  return (
    <main
      style={{
        display: "grid",
        gap: 24,
        padding: 32,
        maxWidth: 600,
        margin: "0 auto",
      }}
    >
      <div>
        <button
          onClick={() => router.push("/")}
          style={{
            background: "none",
            border: "none",
            color: "#3b82f6",
            cursor: "pointer",
            fontSize: 14,
            padding: 0,
          }}
        >
          ← 返回首页
        </button>
        <h1 style={{ marginTop: 12 }}>直接分析</h1>
        <p style={{ color: "#6b7280" }}>填写岗位信息，开始深度分析</p>
      </div>

      {error && <p style={{ color: "#ef4444" }}>{error}</p>}

      <DirectEntryForm onSubmit={handleSubmit} initialCompany={initialCompany} />
    </main>
  );
}
```

- [ ] **Step 2: Test the page compiles**

Run: `cd frontend && npm run build 2>&1 | head -20`
Expected: Build succeeds

- [ ] **Step 3: Commit**

```bash
git add frontend/app/direct/page.tsx
git commit -m "feat: add direct analysis page"
```

---

### Task 8: Update Task Progress Component

**Files:**
- Modify: `frontend/components/task-progress.tsx`

- [ ] **Step 1: Update status labels to Chinese**

Replace the entire content of `frontend/components/task-progress.tsx` with:

```tsx
export function TaskProgress({ status, stage }: { status: string; stage: string }) {
  const statusLabels: Record<string, string> = {
    pending: "待处理",
    research_running: "研究中...",
    research_done: "研究完成",
    action_running: "分析中...",
    completed: "已完成",
    partial_success: "部分完成",
    needs_input: "需要补充信息",
    failed: "失败",
  };

  return (
    <section>
      <h2>任务进度</h2>
      <p>状态：{statusLabels[status] || status}</p>
      {stage ? <p>阶段：{stage}</p> : null}
    </section>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/task-progress.tsx
git commit -m "feat: update task progress to Chinese labels"
```

---

### Task 9: Update Sources View Component

**Files:**
- Modify: `frontend/components/sources-view.tsx`

- [ ] **Step 1: Update title to Chinese**

Replace the entire content of `frontend/components/sources-view.tsx` with:

```tsx
import { Source } from "../lib/types";

export function SourcesView({ sources }: { sources: Source[] }) {
  if (!sources.length) return null;

  return (
    <section>
      <h2>参考来源 ({sources.length})</h2>
      <ul>
        {sources.map((source) => (
          <li key={source.url}>
            <a href={source.url} target="_blank" rel="noopener noreferrer">
              {source.title || source.url}
            </a>
            {source.snippet ? <p>{source.snippet}</p> : null}
          </li>
        ))}
      </ul>
    </section>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/sources-view.tsx
git commit -m "feat: update sources view to Chinese"
```

---

### Task 10: Update Follow-up Box Component

**Files:**
- Modify: `frontend/components/follow-up-box.tsx`

- [ ] **Step 1: Update labels to Chinese**

Replace the entire content of `frontend/components/follow-up-box.tsx` with:

```tsx
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
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="输入你的问题..."
        />
        <button type="submit">提问</button>
      </form>
      {answer ? <p>{answer}</p> : null}
    </section>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/follow-up-box.tsx
git commit -m "feat: update follow-up box to Chinese"
```

---

### Task 11: Update Company Options Component

**Files:**
- Modify: `frontend/components/company-options.tsx`

- [ ] **Step 1: Update labels to Chinese**

Replace the entire content of `frontend/components/company-options.tsx` with:

```tsx
export function CompanyOptions({
  options,
  onSelect,
}: {
  options: Array<{ company_name: string; reason: string }>;
  onSelect: (companyName: string) => void;
}) {
  if (!options.length) return null;

  return (
    <section>
      <h2>推荐公司</h2>
      <ul>
        {options.map((option) => (
          <li key={option.company_name}>
            <strong>{option.company_name}</strong>
            <p>{option.reason}</p>
            <button type="button" onClick={() => onSelect(option.company_name)}>
              选择这家公司
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/company-options.tsx
git commit -m "feat: update company options to Chinese"
```

---

### Task 12: Update Task Detail Page

**Files:**
- Modify: `frontend/app/tasks/[taskId]/page.tsx`

- [ ] **Step 1: Update report section titles to Chinese**

Replace the entire content of `frontend/app/tasks/[taskId]/page.tsx` with:

```tsx
import { getTask } from "../../../lib/api";
import { ReportSection } from "../../../components/report-section";
import { SourcesView } from "../../../components/sources-view";
import { TaskProgress } from "../../../components/task-progress";
import { FollowUpBox } from "../../../components/follow-up-box";

export default async function TaskPage({
  params,
}: {
  params: Promise<{ taskId: string }>;
}) {
  const { taskId } = await params;
  const task = await getTask(taskId);

  return (
    <main
      style={{
        display: "grid",
        gap: 24,
        padding: 32,
        maxWidth: 900,
        margin: "0 auto",
      }}
    >
      <h1>分析报告 #{task.id}</h1>
      <TaskProgress status={task.status} stage={task.current_stage} />
      <SourcesView sources={task.sources} />
      <ReportSection title="公司概况" data={task.report.company_profile} />
      <ReportSection title="职位分析" data={task.report.jd_breakdown} />
      <ReportSection title="匹配度分析" data={task.report.fit_analysis} />
      <ReportSection title="技能差距" data={task.report.skills_gap_summary} />
      <ReportSection title="风险提示" data={task.report.risks} />
      <ReportSection title="面试准备" data={task.report.interview_prep} />
      <ReportSection title="行动清单" data={task.report.action_checklist} />
      {task.uncertainty_notes.length > 0 ? (
        <ReportSection title="不确定性说明" data={task.uncertainty_notes} />
      ) : null}
      {task.failure_reason ? (
        <section>
          <h2>失败原因</h2>
          <p style={{ color: "#ef4444" }}>{task.failure_reason}</p>
        </section>
      ) : null}
      <FollowUpBox taskId={task.id} />
    </main>
  );
}
```

- [ ] **Step 2: Test the page compiles**

Run: `cd frontend && npm run build 2>&1 | head -20`
Expected: Build succeeds

- [ ] **Step 3: Commit**

```bash
git add frontend/app/tasks/[taskId]/page.tsx
git commit -m "feat: update task detail page to Chinese"
```

---

### Task 13: Update Refine Page

**Files:**
- Modify: `frontend/app/tasks/[taskId]/refine/page.tsx`

- [ ] **Step 1: Update labels to Chinese**

Replace the entire content of `frontend/app/tasks/[taskId]/refine/page.tsx` with:

```tsx
"use client";

import { useParams, useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { appendInputs, runTask } from "../../../../lib/api";

export default function RefinePage() {
  const params = useParams();
  const router = useRouter();
  const taskId = Number(params.taskId);
  const [userLinks, setUserLinks] = useState("");
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);

    await appendInputs(taskId, {
      user_links: userLinks
        .split("\n")
        .map((l) => l.trim())
        .filter(Boolean),
      jd_text: jdText,
    });

    await runTask(taskId);
    router.push(`/tasks/${taskId}`);
  }

  return (
    <main
      style={{
        display: "grid",
        gap: 24,
        padding: 32,
        maxWidth: 800,
        margin: "0 auto",
      }}
    >
      <h1>补充信息</h1>
      <p>提供额外链接或职位描述以改善分析质量。</p>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
        <textarea
          value={userLinks}
          onChange={(e) => setUserLinks(e.target.value)}
          placeholder="公司/职位描述链接（每行一个）"
        />
        <textarea
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
          placeholder="粘贴额外的职位描述内容"
        />
        <button type="submit" disabled={loading}>
          {loading ? "处理中..." : "提交并继续分析"}
        </button>
      </form>
    </main>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/app/tasks/[taskId]/refine/page.tsx
git commit -m "feat: update refine page to Chinese"
```

---

### Task 14: Final Build Verification

- [ ] **Step 1: Run full build**

Run: `cd frontend && npm run build`
Expected: Build succeeds with no errors

- [ ] **Step 2: Run dev server and test manually**

Run: `cd frontend && npm run dev`
Open http://localhost:3000 and verify:
- Landing page shows two cards in Chinese
- Clicking "意向推荐" navigates to /intent
- Clicking "直接分析" navigates to /direct
- Intent form has all Chinese labels and dropdowns
- Direct form has split link fields
- Task detail page shows Chinese report sections

- [ ] **Step 3: Commit any fixes if needed**

```bash
git add -A
git commit -m "fix: final polish for Chinese frontend"
```
