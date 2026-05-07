export interface JobCategory {
  label: string;
  titles: string[];
}

export const JOB_CATEGORIES: JobCategory[] = [
  {
    label: '后端开发',
    titles: [
      'Java开发工程师',
      'Go开发工程师',
      'C++开发工程师',
      'Python开发工程师',
      'PHP开发工程师',
      '.NET开发工程师',
      'Rust开发工程师',
    ],
  },
  {
    label: '前端开发',
    titles: [
      '前端开发工程师',
      'React开发工程师',
      'Vue开发工程师',
      'Web前端工程师',
      '小程序开发工程师',
      'Flutter前端工程师',
    ],
  },
  {
    label: '移动开发',
    titles: [
      'Android开发工程师',
      'iOS开发工程师',
      'Flutter开发工程师',
      'React Native开发工程师',
      'HarmonyOS开发工程师',
    ],
  },
  {
    label: 'AI/算法',
    titles: [
      '机器学习工程师',
      '深度学习工程师',
      'NLP算法工程师',
      '计算机视觉算法工程师',
      '推荐算法工程师',
      '大模型算法工程师',
      'AIGC算法工程师',
    ],
  },
  {
    label: '数据开发',
    titles: [
      '数据开发工程师',
      '大数据开发工程师',
      '数据分析师',
      '数据仓库工程师',
      'ETL工程师',
    ],
  },
  {
    label: '测试',
    titles: [
      '测试工程师',
      '自动化测试工程师',
      '性能测试工程师',
      '测试开发工程师',
      'QA工程师',
    ],
  },
  {
    label: '运维/DevOps',
    titles: [
      '运维工程师',
      'DevOps工程师',
      'SRE工程师',
      '云平台工程师',
      'DBA',
    ],
  },
  {
    label: '产品',
    titles: [
      '产品经理',
      '高级产品经理',
      '产品总监',
      '游戏产品经理',
      'AI产品经理',
    ],
  },
  {
    label: '设计',
    titles: [
      'UI设计师',
      'UX设计师',
      '交互设计师',
      '视觉设计师',
      '平面设计师',
    ],
  },
  {
    label: '项目管理',
    titles: [
      '项目经理',
      '敏捷教练',
      '项目总监',
      'PMO',
    ],
  },
  {
    label: '网络安全',
    titles: [
      '安全工程师',
      '渗透测试工程师',
      '安全运维工程师',
      '安全架构师',
      '安全合规工程师',
    ],
  },
  {
    label: '嵌入式/硬件',
    titles: [
      '嵌入式开发工程师',
      'FPGA工程师',
      '硬件工程师',
      '驱动开发工程师',
      '单片机开发工程师',
    ],
  },
  {
    label: '游戏开发',
    titles: [
      'Unity开发工程师',
      'Unreal开发工程师',
      '游戏客户端开发',
      '游戏服务端开发',
      '技术美术',
    ],
  },
  {
    label: '区块链',
    titles: [
      '区块链开发工程师',
      '智能合约工程师',
      'Web3开发工程师',
    ],
  },
  {
    label: '技术管理',
    titles: [
      '技术经理',
      '技术总监',
      'CTO',
      '架构师',
      '解决方案架构师',
    ],
  },
  {
    label: '金融',
    titles: [
      '投资分析师',
      '风控专员',
      '量化分析师',
      '基金经理',
      '证券分析师',
      '银行客户经理',
      '财务分析师',
      '审计师',
    ],
  },
  {
    label: '市场/营销',
    titles: [
      '市场营销经理',
      '品牌经理',
      '新媒体运营',
      '内容运营',
      'SEO/SEM专员',
      '市场策划',
      '商务拓展',
    ],
  },
  {
    label: '销售',
    titles: [
      '销售经理',
      '大客户销售',
      '渠道销售',
      '销售代表',
      '客户成功经理',
    ],
  },
  {
    label: '人力资源',
    titles: [
      'HR经理',
      '招聘专员',
      '薪酬福利专员',
      'HRBP',
      '培训经理',
      '组织发展专员',
    ],
  },
  {
    label: '财务/行政',
    titles: [
      '财务经理',
      '会计',
      '出纳',
      '行政经理',
      '行政专员',
      '法务专员',
    ],
  },
  {
    label: '运营',
    titles: [
      '运营经理',
      '用户运营',
      '活动运营',
      '电商运营',
      '社群运营',
      '直播运营',
    ],
  },
  {
    label: '教育/培训',
    titles: [
      '教师',
      '培训讲师',
      '课程设计师',
      '教育产品经理',
      '教研员',
    ],
  },
  {
    label: '医疗/健康',
    titles: [
      '医生',
      '护士',
      '药剂师',
      '医疗器械工程师',
      '健康管理师',
      '医药代表',
    ],
  },
  {
    label: '其他',
    titles: [
      '售前工程师',
      '技术支持工程师',
      '实施工程师',
      'IT运维',
    ],
  },
];

export const COMPANY_TYPES = [
  '互联网大厂',
  '外企',
  '创业公司',
  '国企/央企',
  '上市公司',
  '不限',
];

export const ALL_JOB_TITLES: string[] = JOB_CATEGORIES.flatMap(
  (category) => category.titles
);

export function getTitlesByCategory(label: string): string[] {
  const category = JOB_CATEGORIES.find((c) => c.label === label);
  return category ? category.titles : [];
}
