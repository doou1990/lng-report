# LNG报告生成 - 快速参考卡片

## 🚀 一键触发
```
用户输入: "LNG报告"
系统自动: 执行六阶段流程，生成报告并推送
```

## 📋 六阶段流程

| 阶段 | 名称 | 耗时 | 输出 |
|------|------|------|------|
| 1 | EXPLORE | 1-2min | 数据源可用性报告 |
| 2 | PLAN | 1min | 执行计划 |
| 3 | GATHER | 5-10min | 10助理采集数据 |
| 4 | AUDIT | 2-3min | 中孚审核报告 |
| 5 | CODE | 2-3min | Markdown + HTML |
| 6 | VERIFY | 1min | 验证报告 |

**总计**: 约15-20分钟

---

## 🤖 10助理速查

| 助理 | 核心数据 | 新增备用源 |
|------|----------|-----------|
| 🟠 原油 | Brent/WTI | TradingEconomics |
| 🔴 海明 | JKM/TTF/HH | **LNGPriceIndex/OilPriceAPI** |
| 🟡 陆远 | 中国进口 | 金联创 |
| 🔵 **润仓** | **国内价格+浙江** | **LNG物联网⭐** |
| 🟠 衡尺 | 驱动因素 | 金十数据 |
| 🟢 欧风 | 欧洲库存 | Global LNG Hub |
| 🔵 金算 | 产业链利润 | Simply Wall St |
| 🟣 盾甲 | 投资评级 | Zacks |
| 🟤 镜史 | 历史对比 | Macrotrends |
| ⚪ 洋基 | 美国产能 | Energy Central |

---

## 🎯 浙江专区必采

| 接收站 | 优先级 | 核心数据源 |
|--------|--------|-----------|
| 中海油宁波 | ★★★★★ | **LNG物联网** / 隆众 |
| 新奥舟山 | ★★★★★ | **LNG物联网** / 隆众 |
| 宁波北仑 | ★★★★☆ | Mysteel快讯 |
| 嘉兴平湖 | ★★★★☆ | Mysteel快讯 |
| 上海五号沟 | ★★★★☆ | **LNG物联网** |

---

## 📊 置信度评分

```
A (90-100): ≥3来源一致，差异<3% → 直接采用
B (75-89):  2-3来源，差异3-5% → 采用，标注差异
C (60-74):  1-2来源，差异5-10% → 采用，标注低可信度
D (<60):    无数据或差异>10% → 不采用
```

---

## 🔧 故障排除

| 问题 | 解决方案 |
|------|----------|
| Subagent超时 | 主代理自动补采 |
| 搜索工具失效 | 更换备用关键词 |
| 数据缺失 | 扩大搜索到非权威平台 |
| GitHub推送失败 | 上传至云盘备份 |

---

## 📁 文件位置

```
skills/lng-market-analysis/
├── SKILL.md              # 主Skill文档
├── AGENT_PROTOCOLS.md    # 10助理采集协议
└── QUICK_REFERENCE.md    # 本快速参考

memory/reports/LNG/daily_estimates/YYYY-MM-DD/
├── explore_report.md
├── execution_plan.md
├── audit_report_v4.0.md
├── index.html
└── market_data.json
```

---

## 🌐 报告地址

- **GitHub Pages**: https://doou1990.github.io/lng-report/
- **云盘备份**: 每次生成后自动上传

---

## ⚡ 快捷命令

```bash
# 手动触发报告生成
# 输入: "LNG报告"

# 查看历史报告
ls /root/.openclaw/workspace/memory/reports/LNG/daily_estimates/

# 查看最新审核报告
cat /memory/reports/LNG/daily_estimates/$(date +%Y-%m-%d)/audit_report_v4.0.md
```

---

*版本: v4.0 | 更新时间: 2026-04-05*
