# LNG市场分析助手 Skill

**版本**: v5.1-NO-WEBFETCH (无web_fetch版)  
**更新时间**: 2026-04-11 07:58  
**状态**: 🔒 已锁定  
**核心**: IEA/EIA标准 + Planner-Generator-Evaluator + **仅mcporter搜索工具**

---

## ⚠️ 重要变更（v5.1）

### 删除的工具
- ❌ `web_fetch` - **已删除，不再使用**
- ❌ `web_search` - **已删除，不再使用**

### 仅使用的工具
| 工具 | 调用方式 | 用途 |
|------|----------|------|
| **cn-web-search** | `mcporter call cn-web-search.search` | 中文搜索、公众号 |
| **web-search-free** (Exa) | `mcporter call exa.web_search_exa` | 国际搜索、AI搜索 |
| **tavily_search** | `tavily_search(...)` | 备用搜索 |

---

## 🤖 10位助理工具分配（v5.1）

| 助理 | 职责 | 强制工具 | 备用工具 |
|------|------|----------|----------|
| **润仓** | 国内价格+浙江专区 | `mcporter cn-web-search` | `tavily_search` |
| **原油** | Brent/WTI | `mcporter exa` | `tavily_search` |
| **海明** | JKM/TTF/HH | `mcporter exa` | `tavily_search` |
| **陆远** | 中国进口 | `mcporter cn-web-search` | `mcporter exa` |
| **衡尺** | 五因子分析 | `mcporter exa` | `tavily_search` |
| **欧风** | 欧洲库存 | `mcporter exa` | `tavily_search` |
| **金算** | 产业链利润 | `mcporter cn-web-search` | `tavily_search` |
| **盾甲** | 投资评级 | `mcporter exa` | `tavily_search` |
| **镜史** | 历史对比 | `mcporter exa` | `mcporter cn-web-search` |
| **洋基** | 美国产能 | `mcporter exa` | `tavily_search` |

---

## 🔧 工具使用示例

### cn-web-search（国内数据）
```bash
# 国内LNG价格
mcporter call cn-web-search.search query="LNG价格 2026年4月"

# 浙江接收站
mcporter call cn-web-search.search query="浙江宁波 LNG接收站价格"

# 公众号
mcporter call cn-web-search.search query="LNG行业信息 公众号"
```

### Exa（国际数据）
```bash
# 原油价格
mcporter call exa.web_search_exa query="Brent crude oil price today"

# 国际LNG
mcporter call exa.web_search_exa query="JKM LNG price April 2026"

# 欧洲库存
mcporter call exa.web_search_exa query="Europe natural gas storage GIE"
```

### Tavily（备用）
```python
tavily_search(query="LNG market news", max_results=5)
```

---

## 🚫 禁止行为

1. **禁止使用 `web_fetch`** - 只使用 mcporter 调用搜索工具
2. **禁止使用 `web_search`** - 使用 `tavily_search` 或 mcporter
3. **禁止直接访问URL** - 所有搜索通过 mcporter 工具

---

*版本: v5.1-NO-WEBFETCH | 更新时间: 2026-04-11*