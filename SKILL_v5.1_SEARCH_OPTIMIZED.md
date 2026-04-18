# LNG市场分析助手 Skill

**版本**: v5.1-SEARCH-OPTIMIZED (搜索优化版)  
**更新时间**: 2026-04-11 07:50  
**状态**: 🔒 已锁定 - 变更需审批  
**核心**: IEA/EIA标准方法论 + Planner-Generator-Evaluator架构 + 四级数据质量评级 + **三大搜索工具**

---

## ⚠️ 版本控制声明

**本版本(v5.1-SEARCH-OPTIMIZED)已锁定为稳定基础版本**

- ✅ 当前版本经过完整设计和文档化
- 🔒 任何变更都需要通过审批流程 (详见 VERSION.md)
- 📝 所有修改将记录在 CHANGELOG.md 中
- 🔄 支持版本回滚到 v5.1-SEARCH-OPTIMIZED

**变更申请**: 如需调整，请告知变更内容，AI将准备变更申请文档供您审批。

---

## 🆕 v5.1 更新内容（搜索工具优化）

### 新增：三大搜索工具强制使用

| 工具 | 用途 | 优先级 |
|------|------|--------|
| **cn-web-search** | 中文搜索、公众号、百度/搜狗 | 国内数据首选 |
| **web-search-free** (Exa) | AI搜索、国际数据、深度研究 | 国际数据首选 |
| **tavily_search** | Tavily搜索、备用 | 通用搜索 |

### 禁止使用的工具
- ❌ `web_search` (旧版 Tavily) - 已废弃
- ❌ `web_fetch` (直接访问) - 仅作为辅助

---

## 📋 搜索工具使用规范

### 1. cn-web-search（中文搜索）

**适用场景**: 国内LNG价格、公众号文章、中文资讯

**核心数据源**:
- 搜狗微信搜索 (公众号文章)
- 百度搜索
- 360搜索
- 头条搜索

**使用示例**:
```bash
# 公众号搜索
web_fetch(url="https://weixin.sogou.com/weixin?type=2&query=LNG价格", ...)

# 百度搜索
web_fetch(url="https://www.baidu.com/s?wd=浙江LNG接收站价格", ...)
```

**助理分配**:
- 润仓助理（国内价格）- **强制使用**
- 金算助理（产业链利润）- **强制使用**

---

### 2. web-search-free (Exa) - AI搜索

**适用场景**: 国际LNG价格、原油价格、深度研究

**核心工具**:
- `exa.web_search_exa` - 网页搜索
- `exa.get_code_context_exa` - 代码/数据搜索
- `exa.company_research_exa` - 公司研究
- `exa.deep_researcher_start` - 深度研究

**使用示例**:
```bash
# 国际LNG价格
mcporter call exa.web_search_exa(query: "JKM LNG price April 2026 $/MMBtu")

# 原油价格
mcporter call exa.web_search_exa(query: "Brent crude oil price today WTI")

# 深度研究
mcporter call exa.deep_researcher_start(instructions: "Research global LNG market supply demand 2026")
```

**助理分配**:
- 原油助理 - **强制使用**
- 海明助理（国际LNG）- **强制使用**
- 欧风助理（欧洲市场）- **强制使用**
- 洋基助理（美国市场）- **强制使用**

---

### 3. tavily_search（备用搜索）

**适用场景**: 通用搜索、备用方案

**使用示例**:
```python
tavily_search(query="LNG market analysis 2026", max_results=5)
```

**助理分配**:
- 所有助理 - **作为备用**

---

## 🤖 10位专业助理（v5.1搜索工具分配）

| 编号 | 助理 | 职责 | **强制搜索工具** | 数据评级目标 |
|------|------|------|------------------|--------------|
| 1 | **规划者(Planner)** | 制定采集计划、分配任务 | - | - |
| 2 | **原油** | Brent/WTI价格+价差分析 | **Exa (web-search-free)** | A/B级 |
| 3 | **海明** | JKM/TTF/HH+区域价差 | **Exa (web-search-free)** | A/B级 |
| 4 | **陆远** | 中国进口+贸易流分析 | **cn-web-search** + Exa | B/C级 |
| 5 | **润仓** | 国内价格+浙江专区 | **cn-web-search** (首选) | B/C级 |
| 6 | **衡尺** | 五因子驱动因素分析 | **Exa (web-search-free)** | B/C级 |
| 7 | **欧风** | 欧洲库存+供需平衡 | **Exa (web-search-free)** | A/B级 |
| 8 | **金算** | 产业链利润+成本分析 | **cn-web-search** (首选) | B/C级 |
| 9 | **盾甲** | 投资评级+机构观点 | **Exa (web-search-free)** | B/C级 |
| 10 | **镜史** | 历史对比+季节性 | **Exa + cn-web-search** | B/C级 |
| 11 | **洋基** | 美国产能+库存+EIA | **Exa (web-search-free)** | A/B级 |
| 12 | **评估者(Evaluator)** | 数据审核+质量评级 | - | - |

---

## 📊 数据采集流程（v5.1优化版）

### 阶段1: Planner 制定计划
- 确定每个助理使用的搜索工具
- 分配任务优先级

### 阶段2: Generator 并行采集

#### 国内数据组（cn-web-search为主）
```
润仓助理:
  ├─ 搜狗微信搜索: LNG行业信息公众号
  ├─ 百度搜索: 浙江LNG接收站价格
  └─ Exa备用: 国内LNG市场分析

金算助理:
  ├─ 百度搜索: LNG产业链利润
  ├─ 搜狗搜索: 液厂生产利润
  └─ Exa备用: 槽车运输成本
```

#### 国际数据组（Exa为主）
```
原油助理:
  └─ Exa: Brent/WTI现货价格、期货价格

海明助理:
  └─ Exa: JKM/TTF/Henry Hub价格

欧风助理:
  └─ Exa: 欧洲天然气库存、GIE AGSI

洋基助理:
  └─ Exa: 美国LNG产能、EIA库存
```

### 阶段3: Evaluator 审核
- 验证数据来源是否符合工具分配
- 检查数据完整性和质量

---

## 🔍 搜索工具配置

### 已安装工具
```bash
# 中文搜索（已安装）
skillhub install cn-web-search

# Exa免费搜索（已安装）
skillhub install web-search-free

# Tavily搜索（内置）
# 无需安装
```

### Exa配置验证
```bash
mcporter list exa
```

如未配置:
```bash
mcporter config add exa "https://mcp.exa.ai/mcp?tools=web_search_exa,web_search_advanced_exa,get_code_context_exa,crawling_exa,company_research_exa,people_search_exa,deep_researcher_start,deep_researcher_check"
```

---

## ⚡ 快速执行命令

### 启动完整报告生成
```bash
# 使用v5.1执行LNG报告
# AI将自动：
# 1. 启动Planner制定计划
# 2. 并行启动10助理（使用指定搜索工具）
# 3. 启动Evaluator审核
# 4. 生成最终报告
```

---

## 📚 参考文档

- **能源市场专业手册**: `workspace/能源市场研究专业知识手册.md`
- **智能体设计模式**: `workspace/research/ai_agent_design_patterns_report.md`
- **IEA方法论**: https://www.iea.org/data-and-statistics/data-tools
- **EIA方法论**: https://www.eia.gov/opendata/
- **cn-web-search文档**: `/skills/cn-web-search/SKILL.md`
- **web-search-free文档**: `/skills/web-search-free/SKILL.md`

---

*版本: v5.1-SEARCH-OPTIMIZED | 状态: 搜索优化版 | 更新时间: 2026-04-11*  
*架构: Planner-Generator-Evaluator | 搜索工具: cn-web-search + Exa + Tavily*