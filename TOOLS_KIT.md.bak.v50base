# LNG市场分析工具包 - v5.0
# 本文件供12位助理（含Planner和Evaluator）在采集时直接调用
# 更新时间: 2026-04-09
# 版本: v5.0 专业升级版 - IEA/EIA标准 + Planner-Generator-Evaluator架构

---

## 🛠️ 工具调用规范

### 1. 网页抓取工具（按优先级 - v4.9.2优化版）

#### 🥇 第一优先: xcrawl爬虫（如可用）
```javascript
// 适用于: 多页面采集、动态网站、反爬严重的站点
// 优势: 自动遍历、JS渲染、反爬绕过、定时调度
const xcrawlConfig = {
  url: 'https://www.lng168.com/',
  mode: 'crawl',           // crawl/spider/single
  renderJS: true,          // 是否渲染JS
  maxPages: 10,            // 最大采集页数
  interval: 1000,          // 请求间隔(ms)
  headers: {
    'User-Agent': 'Mozilla/5.0 (compatible; LNG-Bot/1.0)'
  }
};

// 使用场景:
// - LNG168多页面价格列表
// - 隆众资讯会员专区
// - Mysteel快讯列表
// - 需要登录的网站
```

#### 🥈 第二优先: markdown-fetch优化
```javascript
// 适用于: 单页面静态内容、博客、新闻
// 优势: 节省80% Token、响应快
const fetchConfig = {
  headers: {
    'Accept': 'text/markdown, text/html'
  }
};

// 判断响应格式
if (response.contentType.includes('text/markdown')) {
  // 使用markdown内容，节省80% Token
  data = response.markdown;
} else {
  // 回退到HTML解析
  data = response.html;
}

// 使用场景:
// - OilPrice.com单篇文章
// - 新闻网站
// - 博客/论坛
// - 文档站点
```

#### 🥉 第三优先: Exa搜索 (mcporter)
```bash
# 适用于: 需要AI搜索、多源聚合、实时信息
# 优势: AI理解意图、自动聚合多源、无需额外API Key

# 使用方法:
mcporter call 'exa.web_search_exa(query: "LNG价格 2026-04-08", numResults: 5)'

# 参数说明:
# - query: 搜索关键词
# - numResults: 返回结果数量 (默认8)
# - type: "auto" | "fast" | "deep" (可选)

# 使用场景:
# - 快速获取多源信息
# - 验证数据交叉
# - 搜索最新资讯
// - 发现新数据源
```

#### 🔧 第四优先: 标准web_fetch
```javascript
// 适用于: 简单静态页面、API端点
// 优势: 简单直接
const response = await web_fetch(url);

// 使用场景:
// - API接口（EIA/GIE）
// - 简单HTML页面
// - 其他工具失败后的兜底
```

#### 🔍 搜索工具使用说明
```bash
# ⚠️ 重要: web_search 工具需要单独配置API Key
# 当前可用搜索方案: mcporter exa (已配置)

# 正确用法:
mcporter call 'exa.web_search_exa(query: "搜索内容", numResults: 5)'

# 错误用法 (会导致失败):
# web_search(query: "搜索内容")  # 未配置API Key
```

#### 🖥️ 最后备用: browser渲染
```javascript
// 适用于: 复杂动态页面、需要交互
// 劣势: 慢、耗资源
const browserConfig = {
  headless: true,
  waitFor: 'networkidle'
};

// 使用场景:
// - 所有其他工具都失败
// - 需要点击/登录等交互
// - 极端复杂的动态页面
```

---

## 📊 助理工具优先级策略（v4.9.2）

### 快速抓取原则
1. **API优先**: 官方API（EIA/GIE）最稳定、最快速
2. **爬虫次之**: xcrawl处理多页面、动态内容
3. **AI搜索**: Exa快速获取多源信息
4. **单页抓取**: markdown-fetch节省Token
5. **最后兜底**: browser处理极端情况

### 各助理工具优先级配置

### 原油助理 ⏱️ 预计耗时: 2-3分钟
```yaml
工具优先级:
  1. EIA API (api) → A级数据，最快速
  2. OilPrice.com (markdown-fetch) → 实时价格
  3. Exa搜索 → 交叉验证
  4. web_fetch → 兜底

数据源:
  - name: EIA API
    url: https://www.eia.gov/
    priority: 1
    confidence: A
    tool: api
    speed: ⭐⭐⭐⭐⭐ (最快)
  
  - name: OilPrice.com
    url: https://oilprice.com/
    priority: 2
    confidence: B
    tool: markdown-fetch
    speed: ⭐⭐⭐⭐ (快)
  
  - name: Bloomberg
    url: https://www.bloomberg.com/
    priority: 3
    confidence: B
    tool: exa-search
    speed: ⭐⭐⭐ (中等)

必采数据:
  - WTI价格
  - Brent价格
  - 日涨跌幅

快速抓取策略:
  - 第1轮: 同时调用EIA API + OilPrice markdown-fetch
  - 第2轮: 如数据差异>5%，使用Exa搜索验证
  - 第3轮: 如仍不一致，使用web_fetch访问第三方数据源
```

### 海明助理 ⏱️ 预计耗时: 3-4分钟
```yaml
工具优先级:
  1. CME Group (xcrawl) → 期货价格多页面
  2. Oil Price API (api) → 实时价格
  3. Investing.com (markdown-fetch) → 市场数据
  4. Exa搜索 → 交叉验证

数据源:
  - name: CME Group
    url: https://www.cmegroup.com/
    priority: 1
    confidence: A
    tool: xcrawl
    speed: ⭐⭐⭐⭐ (快，多页面)
    config:
      pages: ["JKM", "TTF", "Henry Hub"]
  
  - name: Oil Price API
    url: https://oilpriceapi.com/
    priority: 2
    confidence: A
    tool: api
    speed: ⭐⭐⭐⭐⭐ (最快)
  
  - name: Investing.com
    url: https://www.investing.com/
    priority: 3
    confidence: B
    tool: markdown-fetch
    speed: ⭐⭐⭐⭐ (快)

必采数据:
  - JKM价格
  - TTF价格
  - Henry Hub价格

快速抓取策略:
  - 第1轮: xcrawl爬取CME多品种期货价格（一次请求多个）
  - 第2轮: API获取实时价格 + markdown-fetch获取市场分析
  - 第3轮: Exa搜索验证价格差异，获取市场解读
```

### 陆远助理
```yaml
数据源:
  - name: 海关总署
    url: http://www.customs.gov.cn/
    priority: 1
    confidence: A
    tool: markdown-fetch
  
  - name: 华经产业研究院
    url: https://www.huaon.com/
    priority: 2
    confidence: B
    tool: exa-search
  
  - name: 上海石油天然气交易中心
    url: https://www.shpgx.com/
    priority: 3
    confidence: B
    tool: markdown-fetch

必采数据:
  - 年度进口量
  - 月度进口量
  - 主要来源国
  - 进口价格
```

### 润仓助理（★必采项★）⏱️ 预计耗时: 4-5分钟
```yaml
工具优先级:
  1. LNG168.com (xcrawl) → 多页面价格列表，一次抓取全部
  2. 隆众资讯 (xcrawl) → 会员专区数据
  3. Mysteel (markdown-fetch) → 快讯验证
  4. Exa搜索 → 交叉验证

数据源:
  - name: LNG168.com
    url: https://www.lng168.com/
    priority: 1
    confidence: A
    tool: xcrawl
    speed: ⭐⭐⭐⭐ (快，多页面)
    note: 国内LNG价格权威平台
    config:
      pages: ["液厂价格", "接收站价格", "浙江价格", "区域价格"]
      maxPages: 20
  
  - name: 隆众资讯
    url: https://www.oilchem.net/
    priority: 2
    confidence: A
    tool: xcrawl
    speed: ⭐⭐⭐ (中等，需处理登录)
    note: 部分数据需会员
  
  - name: Mysteel
    url: https://www.mysteel.com/
    priority: 3
    confidence: B
    tool: markdown-fetch
    speed: ⭐⭐⭐⭐ (快)

必采数据:
  液厂价格:
    - 全国133家加权均价
    - 区域价格（华北/华东/华南/西南/西北）
    - 最高/最低报价
    - 开工率
    - 检修情况
    - 日环比/周环比/月环比
  
  接收站价格:
    - 全国19家均价
    - 最高/最低报价
  
  浙江专区:
    - 宁波（中海油）
    - 舟山（新奥）
    - 上海（五号沟）
    - 浙能温州 ⭐新增
    - 周边对比（江苏/福建/安徽）

快速抓取策略:
  - 第1轮: xcrawl爬取LNG168全部价格页面（一次请求，多数据）
  - 第2轮: xcrawl尝试隆众资讯（如需要登录则跳过）
  - 第3轮: markdown-fetch获取Mysteel快讯 + Exa搜索验证
  
优化提示:
  - LNG168是核心数据源，务必使用xcrawl完整抓取
  - 浙江专区4个接收站价格要全部获取
  - 环比数据（日/周/月）必须完整
```

### 衡尺助理
```yaml
数据源:
  - name: OilPrice.com
    url: https://oilprice.com/
    priority: 1
    confidence: B
    tool: markdown-fetch
  
  - name: 市场新闻
    tool: exa-search
    query: "LNG 价格驱动因素 2026-04"

必采数据:
  - 供应侧因素
  - 需求侧因素
  - 地缘政治因素
  - 天气因素
  - 政策动态
```

### 欧风助理 ⏱️ 预计耗时: 1-2分钟
```yaml
工具优先级:
  1. GIE AGSI/ALSI API (api) → 官方API，最可靠
  2. Eurostat API (api) → 补充数据
  3. Exa搜索 → 市场动态

数据源:
  - name: GIE AGSI API
    url: https://agsi.gie.eu/api
    priority: 1
    confidence: A
    tool: api
    speed: ⭐⭐⭐⭐⭐ (最快)
  
  - name: GIE ALSI API
    url: https://alsi.gie.eu/api
    priority: 1
    confidence: A
    tool: api
    speed: ⭐⭐⭐⭐⭐ (最快)
  
  - name: Eurostat
    url: https://ec.europa.eu/eurostat
    priority: 2
    confidence: A
    tool: api
    speed: ⭐⭐⭐⭐⭐ (最快)

必采数据:
  - EU整体库存率
  - 主要国家库存
  - TTF价格
  - EU终端LNG库存

快速抓取策略:
  - 第1轮: 同时调用AGSI + ALSI API（并行请求）
  - 第2轮: Eurostat API获取补充统计
  - 第3轮: Exa搜索获取市场解读和预测
  
优化提示:
  - API数据最可靠，优先使用
  - 可同时发起多个API请求，节省时间
  - 注意API限流，如有需要添加间隔
```

### 金算助理
```yaml
数据源:
  - name: 信达证券研报
    tool: exa-search
    query: "LNG产业链利润 成本分析 2026"
  
  - name: 中国交通运输协会
    tool: markdown-fetch
  
  - name: 东方财富
    url: https://www.eastmoney.com/
    tool: markdown-fetch

必采数据:
  - 进口成本测算
  - 产业链各环节利润
  - 成本结构分析
```

### 盾甲助理
```yaml
数据源:
  - name: 中银国际
    tool: exa-search
    query: "昆仑能源 新奥能源 投资评级 2026"
  
  - name: 中金公司
    tool: exa-search
  
  - name: 摩根大通
    tool: exa-search

必采数据:
  - 主要LNG企业投资评级
  - 行业研报观点
  - 机构目标价
```

### 镜史助理
```yaml
数据源:
  - name: 历史数据库
    tool: exa-search
    query: "LNG价格历史 2025 2024 对比"

必采数据:
  - 历史价格对比
  - 季节性规律
  - 同期数据对比
```

### 洋基助理 ⏱️ 预计耗时: 2-3分钟
```yaml
工具优先级:
  1. EIA API (api) → 官方数据，最可靠
  2. Marcellus Drilling (markdown-fetch) → 行业动态
  3. ETF Trends (markdown-fetch) → 市场分析
  4. Exa搜索 → 补充验证

数据源:
  - name: EIA API
    url: https://www.eia.gov/
    priority: 1
    confidence: A
    tool: api
    speed: ⭐⭐⭐⭐⭐ (最快)
  
  - name: Marcellus Drilling
    url: https://marcellusdrilling.com/
    priority: 2
    confidence: B
    tool: markdown-fetch
    speed: ⭐⭐⭐⭐ (快)
  
  - name: ETF Trends
    url: https://www.etftrends.com/
    priority: 3
    confidence: B
    tool: markdown-fetch
    speed: ⭐⭐⭐⭐ (快)

必采数据:
  - LNG出口产能
  - 天然气库存
  - 设施利用率

快速抓取策略:
  - 第1轮: EIA API获取核心数据（库存、产能）
  - 第2轮: markdown-fetch获取行业新闻和分析
  - 第3轮: Exa搜索验证数据，获取市场预测
```

---

## 🔄 采集流程模板

### 每助理必须遵循的3轮搜索

```yaml
Round 1: 精准采集
  - 使用首选数据源
  - 使用markdown-fetch优化
  - 获取核心数据

Round 2: 交叉验证
  - 使用次选数据源
  - 验证Round 1数据
  - 标注差异>5%的指标

Round 3: 补充完善（如需要）
  - 针对缺失数据
  - 使用备用数据源
  - 扩大搜索范围
```

---

## ✅ 置信度评级标准

```yaml
A级 - 官方/多源验证:
  标准: 官方API数据（EIA/GIE）或≥3个独立来源交叉验证
  使用: 直接使用，高可信度

B级 - 权威来源:
  标准: 权威行业网站（LNG168、隆众、Mysteel）或2个来源验证
  使用: 使用，标注来源

C级 - 单一来源:
  标准: 单一来源，无交叉验证，或存在时效性问题
  使用: 使用，标注局限性

D级 - 估算/缺失:
  标准: 基于历史数据估算，或数据缺失
  使用: 标注"数据缺失"，不采用估算值
```

---

## 📁 输出规范

### 文件输出路径
```
reports/lng/daily/YYYY-MM-DD/
├── report.md      # Markdown原始版
├── report.html    # HTML可视化版
└── data.json      # JSON结构化数据
```

### JSON输出格式
```json
{
  "report_metadata": {
    "date": "2026-04-08",
    "version": "v4.9.1",
    "assistant": "助理名称",
    "audit_score": 78,
    "data_completeness": "90%"
  },
  "data": {
    // 各助理采集的数据
  },
  "sources": [
    // 数据来源列表
  ],
  "confidence": {
    // 置信度评级
  }
}
```

---

## 🚨 错误处理（v4.9.2更新）

### 工具调用失败降级流程
```javascript
// 完整降级链: xcrawl → markdown-fetch → exa-search → web_fetch → browser

// 1. xcrawl失败 → 降级到markdown-fetch
if (xcrawlFailed) {
  log("xcrawl失败，降级到markdown-fetch: " + url);
  useMarkdownFetch();
}

// 2. markdown-fetch失败 → 降级到exa-search
if (markdownFetchFailed) {
  log("markdown-fetch失败，降级到exa-search: " + url);
  useExaSearch();
}

// 3. exa-search失败 → 降级到标准web_fetch
if (exaSearchFailed) {
  log("exa-search失败，降级到web_fetch: " + url);
  useStandardFetch();
}

// ⚠️ 注意: web_search 工具未配置，请勿使用
// 所有搜索必须通过 mcporter call exa.web_search_exa 执行

// 4. web_fetch失败 → 最后尝试browser
if (webFetchFailed) {
  log("web_fetch失败，最后尝试browser: " + url);
  useBrowser();
}

// 5. 所有工具失败 → 标注"数据缺失"
if (allToolsFailed) {
  log("所有工具失败，标记数据缺失: " + dataPoint);
  markAsMissing();
}
```

### xcrawl特定错误处理
```javascript
// xcrawl反爬拦截
if (xcrawlResponse.blocked) {
  // 切换代理
  switchProxy();
  retryXcrawl();
}

// xcrawl登录要求
if (xcrawlResponse.requiresLogin) {
  // 跳过，使用其他数据源
  skipToNextSource();
}

// xcrawl页面结构变化
if (xcrawlResponse.parseError) {
  // 使用AI解析原始HTML
  useAIParse(xcrawlResponse.rawHtml);
}
```

### 数据异常处理
```javascript
// 数据差异>5%
if (dataDifference > 5%) {
  标注差异();
  调查原因();
  降低置信度();
}

// 数据超时
if (dataTimeout) {
  使用缓存数据();
  标注时效性问题();
}
```

---

## 📊 四级数据质量评级体系（v5.0新增）

### 评级标准（基于IEA/EIA方法论）

| 等级 | 标准 | 说明 | 使用建议 | 得分权重 |
|------|------|------|----------|----------|
| **A级** | 官方统计，经审计 | EIA/IEA/海关总署等官方数据 | 直接使用，高可信度 | 25分 |
| **B级** | 官方统计，估算成分 | IEA需求预测、OPEC产量 | 使用，标注估算说明 | 20分 |
| **C级** | 行业调查/模型估算 | Platts评估、第三方估算 | 使用，标注局限性 | 15分 |
| **D级** | 单一来源，未验证 | 单一媒体报道、推测数据 | 谨慎使用或标注缺失 | 10分 |

### 质量评分细则（0-100分）

| 维度 | 权重 | 评分标准 | 得分计算 |
|------|------|----------|----------|
| **数据来源** | 25% | A级25分/B级20分/C级15分/D级10分 | ×0.25 |
| **时效性** | 20% | 当日20分/3日内15分/周内10分/过时5分 | ×0.20 |
| **多源验证** | 25% | ≥3源25分/2源20分/1源10分/无验证5分 | ×0.25 |
| **数据完整性** | 20% | 完整20分/基本完整15分/部分缺失10分/严重缺失5分 | ×0.20 |
| **可追溯性** | 10% | 有URL+时间戳10分/有来源5分/无来源0分 | ×0.10 |

**总分 = 各维度得分 × 权重之和**

**评级对应：**
- 90-100分：A级（优秀）
- 75-89分：B级（良好）
- 60-74分：C级（合格）
- <60分：D级（需改进）

### 数据采集标准流程

```bash
# Step 1: 多源采集（至少2个来源）
source1 =采集(首选数据源)
source2 =采集(备用数据源)
source3 =采集(验证数据源) # 可选

# Step 2: 交叉验证
if |source1 - source2| > 5%:
    标注差异()
    调查原因()
    降低置信度()

# Step 3: 质量评分
data_score = calculate_score(来源, 时效性, 验证数, 完整性, 可追溯性)
confidence_level = map_score_to_level(data_score)

# Step 4: MemPalace存储
mempalace store "$data" --category "market_data" --tags=["$type", "$confidence_level"]
```

### 数据质量检查清单（v5.0）

- [ ] 完成≥3轮搜索
- [ ] 同一指标≥2个来源验证（关键数据）
- [ ] 差异>5%的指标已标注原因
- [ ] 所有数据标注来源URL
- [ ] 所有数据标注采集时间戳
- [ ] 所有数据标注置信度等级（A/B/C/D）
- [ ] 所有数据有质量评分（0-100分）
- [ ] 时效性检查通过（优先3日内数据）
- [ ] JSON格式正确
- [ ] 数据完整度≥95%

---

## 🌲 工具选择决策树

```
开始采集
    │
    ├─ 是否有官方API？
    │   ├─ 是 → 使用API（EIA/GIE）→ 最快最可靠
    │   └─ 否 → 继续
    │
    ├─ 是否需要多页面/动态内容？
    │   ├─ 是 → 使用xcrawl → 自动遍历多页面
    │   └─ 否 → 继续
    │
    ├─ 是否需要AI搜索/多源聚合？
    │   ├─ 是 → 使用Exa搜索 → AI理解意图
    │   └─ 否 → 继续
    │
    ├─ 是否为静态单页面？
    │   ├─ 是 → 使用markdown-fetch → 节省80% Token
    │   └─ 否 → 继续
    │
    ├─ 是否为简单静态页面？
    │   ├─ 是 → 使用web_fetch → 简单直接
    │   └─ 否 → 继续
    │
    └─ 使用browser → 最后兜底（慢但万能）
```

## ⏱️ 各助理预计耗时汇总

| 助理 | 预计耗时 | 瓶颈 | 优化建议 |
|------|----------|------|----------|
| 原油 | 2-3分钟 | API响应 | 并行调用多个API |
| 海明 | 3-4分钟 | 多品种价格 | xcrawl一次抓取多个 |
| 陆远 | 3-4分钟 | 多源验证 | 优先使用官方数据 |
| 润仓 | 4-5分钟 | ★核心★多页面 | **必须使用xcrawl** |
| 衡尺 | 3-4分钟 | 新闻分散 | Exa搜索聚合 |
| 欧风 | 1-2分钟 | - | API并行，最快 |
| 金算 | 3-4分钟 | 研报分散 | xcrawl爬取研报库 |
| 盾甲 | 3-4分钟 | 多机构 | Exa搜索聚合评级 |
| 镜史 | 2-3分钟 | 历史数据 | 优先使用数据库 |
| 洋基 | 2-3分钟 | API响应 | 并行调用 |

**整体并行采集预计总耗时: 5-6分钟**（以润仓为准）

## 🔧 工具包更新日志

### v4.9.2 (2026-04-08)
- ✅ **新增xcrawl爬虫工具**（多页面自动采集）
- ✅ **完整工具优先级链**: xcrawl → markdown-fetch → Exa → web_fetch → browser
- ✅ **10位助理个性化工具策略**（含预计耗时）
- ✅ **工具选择决策树**（快速判断用哪个工具）
- ✅ **xcrawl错误处理**（反爬、登录、解析错误）
- ✅ **整体采集优化**: 预计5-6分钟完成全部采集

### v4.9.1 (2026-04-08)
- ✅ 集成markdown-fetch优化（节省80% Token）
- ✅ 新增浙能温州价格采集
- ✅ 优化数据可靠性评价体系
- ✅ 规范报告存储结构（md/html/json）
- ✅ 提供完整工具调用模板

---

## 🧠 MemPalace记忆系统集成（v5.0新增）

### 四层记忆架构

```
┌─────────────────────────────────────────┐
│         L4: Semantic Knowledge          │
│         (语义知识 - 全局真理)            │
│    能源市场基础知识、定价公式、分析方法   │
├─────────────────────────────────────────┤
│         L3: Long-term Memory            │
│         (长期记忆 - 向量数据库)          │
│    历史报告、用户偏好、经验教训          │
├─────────────────────────────────────────┤
│         L2: Short-term Memory           │
│         (短期记忆 - 会话上下文)          │
│    当前会话、近期采集数据、临时状态       │
├─────────────────────────────────────────┤
│         L1: Working Memory              │
│         (工作记忆 - 当前思考)            │
│    活跃上下文、当前任务、推理链          │
└─────────────────────────────────────────┘
```

### 记忆存储规范

```bash
# 存储市场数据
mempalace store "{\"price\": 4876, \"source\": \"LNG168\", \"date\": \"2026-04-09\"}" \
    --category "lng_prices" \
    --tags=["domestic", "factory", "A级"]

# 存储风险因素
mempalace store "霍尔木兹海峡封锁导致供应风险上升" \
    --category "risk_factors" \
    --tags=["geopolitical", "supply", "high_impact"]

# 存储用户偏好
mempalace store "用户重点关注浙江专区价格" \
    --category "user_preferences" \
    --tags=["zhejiang", "priority"]

# 检索相关记忆
mempalace search "供应中断" --category "risk_factors" --limit 5

# 检索历史价格
mempalace search "LNG价格 2026-04" --category "lng_prices"
```

### 记忆使用场景

**场景1: 历史数据对比**
```bash
# 检索历史同期数据
historical_data = mempalace search "LNG价格 2025-04" --category "lng_prices"
# 计算同比变化
yoy_change = (current_price - historical_data.avg) / historical_data.avg
```

**场景2: 风险因素追踪**
```bash
# 检索相关风险
risks = mempalace search "霍尔木兹 卡塔尔" --category "risk_factors"
# 更新风险状态
if risk.resolved:
    mempalace update $risk.id --status "resolved"
```

**场景3: 用户偏好学习**
```bash
# 记录用户反馈
mempalace store "用户反馈: 希望增加库存数据分析" \
    --category "user_feedback" \
    --tags=["feature_request", "inventory"]
# 后续自动增加库存板块
```

---

## 🔧 工具包更新日志

### v5.0 (2026-04-09) - 专业升级版
- ✅ **采用IEA/EIA标准报告结构** - 9章节专业框架
- ✅ **引入Planner-Generator-Evaluator架构** - 三智能体协作
- ✅ **四级数据质量评级体系** - A/B/C/D标准化+评分细则
- ✅ **五因子分析框架** - 需求/供给/库存/宏观/风险
- ✅ **价差分析模块** - 期限结构+跨区价差
- ✅ **供需平衡表** - 标准化供需分析
- ✅ **集成MemPalace记忆系统** - 四层记忆架构
- ✅ **12位助理体系** - 新增Planner和Evaluator

### v4.9.2 (2026-04-08)
- ✅ **新增xcrawl爬虫工具**（多页面自动采集）
- ✅ **完整工具优先级链**: xcrawl → markdown-fetch → Exa → web_fetch → browser
- ✅ **10位助理个性化工具策略**（含预计耗时）
- ✅ **工具选择决策树**（快速判断用哪个工具）
- ✅ **xcrawl错误处理**（反爬、登录、解析错误）
- ✅ **整体采集优化**: 预计5-6分钟完成全部采集

### v4.9.1 (2026-04-08)
- ✅ 集成markdown-fetch优化（节省80% Token）
- ✅ 新增浙能温州价格采集
- ✅ 优化数据可靠性评价体系
- ✅ 规范报告存储结构（md/html/json）
- ✅ 提供完整工具调用模板

---

*本工具包供LNG市场分析12位助理（含Planner和Evaluator）使用*
*版本: v5.0 专业升级版 | 标准: IEA/EIA | 架构: Planner-Generator-Evaluator*
