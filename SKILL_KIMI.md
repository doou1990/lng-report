# LNG市场分析助手 Skill (Kimi Code优化版)

**版本**: v5.0-KIMI  
**适配模型**: Kimi Code (kimi-for-coding)  
**优化目标**: 提升与Kimi Code的兼容性，保持10助理架构

---

## 🚀 Kimi Code 优化特性

### 1. MCP工具化架构
```
┌─────────────────────────────────────────────────────────┐
│                    Kimi Code 主会话                      │
│                   (256K长上下文)                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ 原油MCP │  │ 海明MCP │  │ 润仓MCP │  │ 欧风MCP │   │
│  │  (工具) │  │  (工具) │  │  (工具) │  │  (工具) │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
│       └─────────────┴─────────────┴─────────────┘       │
│                      批量并行调用                        │
│                           │                             │
│                    ┌──────┴──────┐                      │
│                    │  中孚审核   │                      │
│                    │ (Evaluator) │                      │
│                    └──────┬──────┘                      │
│                           │                             │
│                    ┌──────┴──────┐                      │
│                    │  报告生成   │                      │
│                    └─────────────┘                      │
└─────────────────────────────────────────────────────────┘
```

### 2. 关键优化点

| 优化项 | 传统模式 | Kimi优化模式 | 效果 |
|--------|---------|-------------|------|
| **工具调用** | 子代理(新会话) | MCP工具(同会话) | 减少上下文切换 |
| **并行度** | 串行启动 | 批量async.gather | 10助理同时执行 |
| **上下文** | 重复加载 | 长上下文保持 | 减少token消耗 |
| **审核** | 子代理Evaluator | 函数调用中孚 | 快速质量检查 |

### 3. 10位助理MCP工具清单

| 编号 | 助理 | MCP工具名 | 职责 |
|------|------|-----------|------|
| 1 | **规划者** | `batch_collect_all` | 批量协调 |
| 2 | **原油** | `collect_crude_oil_price` | Brent/WTI价格 |
| 3 | **海明** | `collect_lng_international_price` | JKM/TTF/HH |
| 4 | **陆远** | `collect_china_import_data` | 中国进口 |
| 5 | **润仓** | `collect_domestic_lng_price` | 国内价格(浙江必采) |
| 6 | **衡尺** | `collect_market_drivers` | 五因子分析 |
| 7 | **欧风** | `collect_europe_inventory` | 欧洲库存 |
| 8 | **金算** | `collect_industry_profit` | 产业链利润 |
| 9 | **盾甲** | `collect_investment_rating` | 投资评级 |
| 10 | **镜史** | `collect_historical_comparison` | 历史对比 |
| 11 | **洋基** | `collect_us_lng_data` | 美国LNG |
| 12 | **中孚** | `evaluate_data_quality` | 数据审核 |

---

## 📋 使用方式

### 方式1: MCP工具调用（推荐）
```python
# Kimi Code 直接调用MCP工具
results = await asyncio.gather(
    mcp.collect_crude_oil_price(),
    mcp.collect_lng_international_price(),
    mcp.collect_domestic_lng_price(),
    # ... 其他7个助理
)

# 中孚审核
evaluation = await mcp.evaluate_data_quality(results)
```

### 方式2: 批量采集
```python
# 一键采集所有数据
all_data = await mcp.batch_collect_all()
```

---

## ⚙️ Kimi Code 配置参数

```json
{
  "model": "kimi-for-coding",
  "temperature": 0.1,
  "max_tokens": 4000,
  "top_p": 0.9,
  "context_window": 256000,
  "parallel_calls": true,
  "batch_size": 10
}
```

---

## 🔧 文件结构

```
skills/lng-market-analysis/
├── mcp_server/
│   ├── lng_data_server.py      # MCP服务器实现
│   └── mcp_config.json          # MCP配置
├── kimi_optimized_runner.py     # Kimi优化执行器
├── SKILL.md                     # 原版SKILL
└── SKILL_KIMI.md               # Kimi优化版（本文件）
```

---

## ✅ 兼容性保证

- ✅ 保持10助理架构不变
- ✅ 中孚（Evaluator）审核保留
- ✅ 四级数据质量评级
- ✅ IEA/EIA标准9章节报告结构
- ✅ 浙江专区必采要求

---

*版本: v5.0-KIMI | 优化目标: Kimi Code兼容性 | 架构: MCP工具化*
