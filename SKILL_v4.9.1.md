# LNG市场分析助手 Skill v4.9.1 - Markdown优化版

**版本**: v4.9.1 (Markdown优化版)  
**更新时间**: 2026-04-08 21:40  
**状态**: ✅ 已获授权优化  
**核心**: v4.9固化底座 + markdown-fetch工具优化  

---

## 📝 版本说明

本版本基于 **SKILL v4.9 固化底座**，仅增加工具使用优化，**不修改任何固化内容**。

### v4.9.1 新增内容
- ✅ 集成 **markdown-fetch** 技能
- ✅ 网页抓取Token消耗减少 **80%**
- ✅ 优化助理采集效率

---

## 🔄 与v4.9的差异

| 项目 | v4.9 | v4.9.1 |
|------|------|--------|
| 六阶段流程 | 固化 | 保持一致 |
| 10助理体系 | 固化 | 保持一致 |
| ≥3轮搜索 | 固化 | 保持一致 |
| A/B/C/D置信度 | 固化 | 保持一致 |
| 中孚审核 | 固化 | 保持一致 |
| **工具优化** | web_fetch | **+ markdown-fetch** |
| **Token效率** | 基准 | **-80%** |

---

## 🚀 markdown-fetch 使用指南

### 适用场景
当助理使用 `web_fetch` 工具时，优先使用 **markdown-fetch** 优化：

### 使用方法
在调用 `web_fetch` 时，添加以下 header：

```javascript
{
  "headers": {
    "Accept": "text/markdown, text/html"
  }
}
```

### 响应处理
| Content-Type | 处理方式 | Token节省 |
|--------------|----------|-----------|
| text/markdown | 直接使用Markdown | ~80% |
| text/html | 回退到原有HTML解析 | 0% |

### 示例
```javascript
// 优化前
const result = await web_fetch('https://example.com');

// 优化后（v4.9.1）
const result = await web_fetch('https://example.com', {
  headers: {
    'Accept': 'text/markdown, text/html'
  }
});

// 判断响应格式
if (result.contentType.includes('text/markdown')) {
  // 使用 result.markdown，节省80% Token
} else {
  // 使用 result.html，原有解析逻辑
}
```

---

## 🤖 10位专业助理（保持不变）

| 编号 | 助理 | 职责 | 核心数据源 | 优化建议 |
|------|------|------|-----------|----------|
| 1 | **原油** | Brent/WTI价格 | OilPrice.com, EIA API | 对OilPrice.com使用markdown-fetch |
| 2 | **海明** | JKM/TTF/HH国际价格 | Platts/ICIS | 对Platts使用markdown-fetch |
| 3 | **陆远** | 中国LNG进口/贸易 | Kpler, Bloomberg, 海关总署 | 对新闻网站使用markdown-fetch |
| 4 | **润仓** | 国内LNG价格★必采★ + 浙江专区★必采★ | LNG168, 隆众, Mysteel | 对LNG168使用markdown-fetch |
| 5 | **衡尺** | 价格驱动因素 | 市场新闻, 政策文件 | 对新闻网站使用markdown-fetch |
| 6 | **欧风** | 欧洲市场/库存 | GIE AGSI, Eurostat | API数据，无需优化 |
| 7 | **金算** | 产业链利润 | 成本分析, 利润测算 | 对研报网站使用markdown-fetch |
| 8 | **盾甲** | 投资评级 | 机构研报, 评级数据 | 对研报网站使用markdown-fetch |
| 9 | **镜史** | 历史对比 | 历史数据库 | 根据数据源决定 |
| 10 | **洋基** | 美国LNG产能/库存 | EIA API (A级) | API数据，无需优化 |

---

## 📋 标准化采集协议（保持不变）

### 每助理必须执行
1. **≥3轮搜索**: 逐步扩大搜索范围
2. **多源验证**: 同一指标≥2个来源
3. **差异标注**: 差异>5%时明确标注
4. **时效性检查**: 优先最新数据
5. **置信度评级**: A/B/C/D
6. **【v4.9.1新增】工具优化**: 优先使用markdown-fetch

---

## 🎯 国内LNG价格细化要求（保持不变）

详见 v4.9 SKILL.md

---

## 🎯 浙江专区细化要求（保持不变）

详见 v4.9 SKILL.md

---

## ✅ 中孚审核机制（保持不变）

详见 v4.9 SKILL.md

---

## ✅ 置信度评分标准（保持不变）

详见 v4.9 SKILL.md

---

## 🚫 禁止行为（保持不变）

1. **禁止估算数据** - 没有数据时标注"数据缺失"
2. **禁止编造来源** - 每个数据必须有明确来源
3. **禁止虚高置信度** - 严格按标准评级
4. **禁止绕过助理** - 必须通过10助理采集
5. **禁止单轮搜索** - 至少3轮搜索
6. **禁止自动审核** - 必须由中孚审核
7. **禁止调整底座** - v4.9底座保持不变

---

## 📊 数据质量目标（保持不变）

| 指标 | 目标 | 状态 |
|------|------|------|
| 国内LNG价格完整度 | ≥95% | 液厂+接收站+变动 |
| 浙江专区完整度 | ≥90% | 3接收站+周边+动态 |
| 数据准确度 | ≥90% | 多源验证 |
| 中孚审核通过率 | ≥80% | 评分≥70分 |
| **【v4.9.1新增】Token效率** | **节省80%** | 使用markdown-fetch时 |

---

## 📈 输出要求（保持不变）

1. **Markdown完整版**: 详细数据+分析
2. **HTML网页版**: 可视化展示
3. **国内价格板块**: 细化展示液厂+接收站+变动
4. **浙江专区板块**: 细化展示3接收站+周边+动态+分析
5. **来源标注**: 每个数据必须标注来源和置信度
6. **中孚审核**: 审核报告必须附在最终报告后
7. **【v4.9.1新增】Token日志**: 记录markdown-fetch节省的Token

---

## 🔧 工具使用（v4.9.1优化）

### 基础工具
- **Exa搜索**: 默认搜索工具
- **EIA API**: A级美国数据
- **web_fetch**: 获取网页内容（**+ markdown-fetch优化**）
- **browser**: JS渲染页面 (备用)

### 工具优先级（v4.9.1）
| 数据类型 | 首选 | 次选 | 备用 | 优化策略 |
|----------|------|------|------|----------|
| 国内液厂 | LNG168 | 隆众 | Mysteel | 使用markdown-fetch访问LNG168 |
| 国内接收站 | LNG168 | 隆众 | Mysteel | 使用markdown-fetch访问LNG168 |
| 浙江专区 | LNG168 | 隆众 | 市场询价 | 使用markdown-fetch访问LNG168 |
| 原油价格 | EIA API | OilPrice | Bloomberg | API优先，其次markdown-fetch |
| 国际LNG | Platts | ICIS | CME | 使用markdown-fetch访问 |

---

## ✅ v4.9.1 授权声明

**本SKILL v4.9.1已获用户明确授权优化：**

✅ **授权内容**:
- 集成markdown-fetch技能
- 优化工具使用效率
- 保持v4.9底座不变

✅ **保持不变**:
- 六阶段流程
- 10助理体系
- ≥3轮搜索
- A/B/C/D置信度
- 中孚审核机制
- 所有固化内容

---

## 📚 参考文档

- **底座版本**: SKILL v4.9 (固化底座版)
- **优化技能**: markdown-fetch v1.0.0
- **优化原理**: Cloudflare Markdown for Agents

---

*版本: v4.9.1 | 状态: Markdown优化版 | 更新时间: 2026-04-08 | 底座: v4.9*
