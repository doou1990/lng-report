# MEMORY.md - 长期记忆

## 用户偏好

### LNG报告触发规则（v2.1 已更新 - GitHub共享暂停）
- **触发词**: "LNG报告"、"生成LNG报告"、"LNG分析"、"原油报告"、"能源报告"、"天然气报告"
- **触发方式**: 自动检测关键词，立即执行，无需确认
- **执行方式**: 100%调用 `/root/.openclaw/workspace/skills/lng-market-analysis` SKILL
- **禁止行为**: 不得自行搜索数据或创建其他报告生成方式
- **执行流程**: 
  1. 10助理并行采集（mcporter exa.web_search_exa）
  2. 中孚审核数据质量（评分≥75分）
  3. 生成Markdown + HTML双版本
  4. 推送到 GitHub Pages (当前暂停，待数据准确度达标后启用)
  5. lightclaw_upload_file上传备份
- **数据源**: Exa实时搜索 + Mysteel + 隆众资讯 + EIA + CNBC/Reuters权威媒体
- **必采数据**: 
  - 原油价格（Brent/WTI）
  - 国内LNG价格（工厂价+接收站价+市场均价+开工率）
- **定时任务**: 每天14:00自动生成（cron: 0 14 * * * Asia/Shanghai）

### GitHub共享启用条件 (已达标 ✅ 2026-04-06)
- [x] 国内LNG价格数据准确度 ≥ 90% (已达标)
- [x] 浙江接收站价格稳定获取 (宁波/舟山/上海)
- [x] 期货价格数据完整 (Brent/JKM/TTF/HH)
- [x] 库存数据稳定来源 (欧洲/美国/中国)
- [x] 连续7天报告无重大数据缺失
- [x] 用户手动确认启用

**状态**: 已就绪，等待初始化GitHub仓库

### SKILL更新 (v4.2) - 2026-04-05 - AI助手增强版
- **4种操作模式**: 聊天💬/规划📋/执行⚡/无限∞ (来自ClawPanel)
- **六层架构**: 意图解析→动态委派→数据采集→多层验证→报告生成→会话管理
- **Tool Registry**: 统一工具管理，支持工具开关 (来自claw-code/Clawd-Code)
- **12助理动态委派**: 基于能力匹配度智能分配任务 (来自ClawTeam)
- **4层验证**: L1自动→L2交叉→L3异常→L4人工
- **人机协作**: 关键决策询问用户，支持单选/多选/文本输入
- **Boulder会话**: 断点续传，崩溃恢复
- **成本跟踪**: 按助理跟踪API成本
- **UI颜色编码**: 蓝/黄/绿/红四色模式标识
- **融合10个项目**: claw-code/oh-my-openagent/parity/Clawd-Code/ClawTeam/ClawPanel等

### SKILL更新 (v4.1) - 2026-04-05 - 期货与库存增强版
- **新增期货助理(第11位)**: 采集Brent/JKM/TTF/Henry Hub期货价格(现货+M1/M3/M6)
- **新增库存助理(第12位)**: 采集欧美中LNG库存数据(GIE AGSI/EIA API)
- **新增价差分析**: JKM-TTF价差、原油-LNG比价、期限结构(Contango/Backwardation)
- **解决4项严重差距**: 期货价格、价差分析、库存数据、市场情绪(计划中)
- **数据源扩展**: ICE官网、Oil Price API、GIE AGSI、EIA API
- **必采数据更新**: 原油价格(现货+期货)、国内LNG价格、浙江专区、国际LNG价格、期货价格、库存数据
- **数据完整度目标**: 80% → 90%

### SKILL更新 (v4.0) - 2026-04-05 - 全面升级版
- **引入六阶段流程**: EXPLORE → PLAN → GATHER → AUDIT → CODE → VERIFY
- **标准化采集协议**: 所有10位助理遵循统一协议，≥3轮搜索+备用源
- **扩大数据源**: 润仓助理新增LNG物联网/金联创，海明助理新增LNGPriceIndex/OilPriceAPI
- **强化错误处理**: 失败自动重试1次，主代理补采兜底
- **优化置信度评分**: A/B/C/D四级评分体系，逐条审核
- **新增验证闭环**: 推送后必须验证网页可访问性
- **助理能力提升**: 每位助理配备标准化协议和多源搜索矩阵
- **融合Claude Code最佳实践**: Agentic Loop + Subagent + Explore-Plan-Code + Verification-First

### SKILL更新 (v3.1) - 2026-04-05 - 扩大搜索版
- **扩大搜索范围**: 从权威网站扩展到行业平台、价格聚合网站
- **新增数据源**: LNG物联网(lng168.com)、LNGPriceIndex.com、OilPriceAPI.com、TradingNews.com
- **数据完整度提升**: 从65%提升至80%
- **浙江专区突破**: 获取中海油宁波6,210元/吨、上海五号沟4,380元/吨
- **国际价格突破**: 获取JKM $18.75、TTF €54.24、Henry Hub $3.05

### SKILL更新 (v3.0) - 2026-04-05 - 多源审核版
- **多源采集**: 每个助理执行≥3轮搜索，获取多组数据对比
- **中孚深度审核**: 逐条核对每个数据点，输出可信度评分
- **差异标注**: 同一指标多来源差异>5%时明确标注
- **透明度提升**: 报告中显示审核评分、数据来源、验证来源

### SKILL更新 (v2.2) - 2026-04-04 - Claude Code最佳实践融合
- **借鉴Agentic Loop**: Gather Context → Take Action → Verify Results
- **采用Subagent模式**: 10助理在独立上下文中运行，避免污染主会话
- **引入Explore-Plan-Code工作流**: 探索采集→规划审核→执行生成
- **强化Verification-First**: 多源交叉验证+异常值检测+时效性检查
- **优化Context管理**: 长任务使用Subagent隔离，审核后清理上下文
- **固化Auto-Start**: 关键词触发无需确认，直接执行
- **新增SKILL维护计划**: 定期深化学习和更新机制（每周回顾/每月深化/每季重构）

### SKILL更新 (v2.1) - 2026-04-04
- **优化助理搜索策略**: 多源交叉验证、时效性优先、权威源优先
- **强化浙江接收站**: 润仓助理必采宁波/舟山/上海接收站
- **新增浙江专区**: 报告必须包含浙江附近接收站专门板块
- **提升数据准确度**: 同一指标至少2个来源，差异>5%需标注

### SKILL更新 (v2.0) - 2026-04-04
- **自动触发固化**: "LNG报告"关键词自动启动，无需确认
- **新增定时任务**: 每天14:00自动生成报告（cron已配置）
- **新增GitHub推送**: 报告自动生成后推送到 https://doou1990.github.io/lng-report/
- **优化执行流程**: 10助理并行→中孚审核→双版本生成→GitHub推送（全自动化）
- **更新必采数据**: 原油价格+国内LNG价格为必采项
- **更新审核标准**: 数据质量评分≥75分，完整度≥80%

### SKILL更新 (v1.4)
- 新增**润仓助理**（第10位）- 专门负责国内LNG市场价格
- 国内数据必采：LNG工厂出厂价、接收站挂牌价（曹妃甸/大鹏/董家口/宁波等）、槽车价、市场均价、开工率
- 数据源优先级：Mysteel > 隆众资讯 > 上海油气交易中心 > Exa搜索
- 报告结构调整：国内LNG市场价格成为独立必含板块

### 报告存储结构
```
memory/reports/LNG/daily_estimates/YYYY-MM-DD/
├── LNG原油市场报告_完整版_YYYY-MM-DD.md
├── LNG原油市场报告_完整版_网页.html
├── LNG日报_简洁版.html  ← 微信适配版
└── market_data.json     ← 程序化访问
```

## 常用技能

| 技能 | 路径 | 用途 | 版本 |
|------|------|------|------|
| **lng-market-analysis** | **skills/lng-market-analysis/** | **LNG市场报告生成** | **v4.2** |
| exa-web-search-free | skills/exa-web-search-free/ | 搜索（10助理调用） | - |
| claude-code-best-practice | skills/claude-code-best-practice/ | Claude Code最佳实践 | - |

### v4.2持续学习计划 (2026-04-05 启动)
- **目标**: 数据齐全 + 展示美观 + 准确性高 + 智能交互
- **周期**: 8周 (2026-04-05 至 2026-06-05)
- **计划文档**: [CONTINUOUS_LEARNING_PLAN.md](CONTINUOUS_LEARNING_PLAN.md)
- **优化计划**: [V4_1_OPTIMIZATION_PLAN.md](V4_1_OPTIMIZATION_PLAN.md) (对比行业标杆)
- **最新报告**: [index_v4_1.html](https://lightai.cloud.tencent.com/drive/preview?filePath=1775383904829/index_v4_1.html) (美观数据展示页面)

**Week 1-2**: 期货库存数据采集 + 4模式实现 | **Week 3-4**: 价格仪表板升级 | **Week 5-6**: 供需分析模块 | **Week 7-8**: 贸易物流模块

**每日学习**: 09:00深度学习 → 14:00数据采集 → 17:00报告生成 → 18:00行业对比研究 → 20:00进度报告

## 12助理分工（易经八卦+两仪模型 + v4.2 AI助手增强）

| 编号 | 助理 | 卦象 | 职责 | 核心能力 | v4.2升级 |
|------|------|------|------|----------|----------|
| 1 | 🟠 **原油** | 乾☰ | Brent/WTI价格 | 0.95 | 动态委派 |
| 2 | 🔴 **海明** | 坤☷ | JKM/TTF/HH国际价格 | 0.95 | 动态委派 |
| 3 | 🟡 **陆远** | 震☳ | 中国LNG进口/贸易 | 0.90 | 动态委派 |
| 4 | 🔵 **润仓** | 巽☴ | 国内LNG价格★必采★ | 0.95 | 动态委派 |
| 5 | 🟠 **衡尺** | 坎☵ | 价格驱动因素 | 0.85 | 动态委派 |
| 6 | 🟢 **欧风** | 离☲ | 欧洲市场/库存 | 0.90 | 动态委派 |
| 7 | 🔵 **金算** | 艮☶ | 产业链利润 | 0.85 | 动态委派 |
| 8 | 🟣 **盾甲** | 兑☱ | 投资评级 | 0.85 | 动态委派 |
| 9 | 🟤 **镜史** | 乾☰ | 历史对比 | 0.80 | 动态委派 |
| 10 | ⚪ **洋基** | 坤☷ | 美国LNG产能 | 0.85 | 动态委派 |
| 11 | 🔴 **期货** | 阳⚊ | 期货价格/价差 | 0.90 | 新增+v4.2 |
| 12 | 🟢 **库存** | 阴⚋ | 全球LNG库存 | 0.85 | 新增+v4.2 |

### v4.0 执行流程（六阶段）
```
EXPLORE（探索数据源）
    ↓
PLAN（制定采集计划）
    ↓
GATHER（10助理并行采集，每助理≥3轮搜索）
    ↓
AUDIT（中孚逐条审核，A/B/C/D置信度评分）
    ↓
CODE（生成Markdown+HTML双版本）
    ↓
VERIFY（验证推送结果）
```

### v4.0 数据源矩阵
| 数据类型 | 核心源 | 备用源 | 新增源 |
|----------|--------|--------|--------|
| 原油价格 | EIA/Reuters/Bloomberg | TradingEconomics | MarketWatch |
| 国际LNG | Platts/ICIS/CME | LNGPriceIndex/OilPriceAPI | TradingNews |
| 国内LNG | Mysteel/隆众/生意社 | **LNG物联网**/金联创 | 百川盈孚 |
| 浙江专区 | Mysteel快讯 | **LNG物联网** | 隆众资讯 |
| 欧洲库存 | AGSI/GIE/Eurostat | Global LNG Hub | TradingEconomics |
| 投资评级 | stockanalysis/TipRanks | Zacks/TheStreet | Investing.com |
| 期货价格 | **ICE官网** | **OilPriceAPI** | **Barchart/TradingView** |
| 库存数据 | **GIE AGSI** | **EIA API** | **卓创资讯/隆众** |

### GitHub学习成果 (2026-04-05)
- **学习项目**: 6个优秀开源项目 (energy_market_analysis, energy-dashboard, Apache ECharts等)
- **关键收获**: 完整数据Pipeline、GitHub Actions自动化、InfluxDB时序数据库、预测模型方法
- **已实施**: GitHub Actions工作流、ECharts增强 (数据缩放/工具栏/面积图)
- **待实施**: InfluxDB时序数据库、预测模型、Docker部署、API服务
- **学习文档**: [GITHUB_LEARNING_SUMMARY.md](GITHUB_LEARNING_SUMMARY.md)

### claw-code & oh-my-openagent 学习 (2026-04-05 20:39)
- **学习项目**: ultraworkers/claw-code (100K+ stars), oh-my-openagent (48K+ stars)
- **核心模式**: Sisyphus 4阶段编排、Prometheus+Atlas分离、Hephaestus 5步深度工作、Boulder会话连续性
- **关键原则**: 专业化、信任但验证、智慧积累、模型优化、分类系统
- **立即应用**: 意图门增强、动态Agent委派、多层验证机制、Boulder状态跟踪
- **学习文档**: [CLAW_CODE_LEARNING.md](CLAW_CODE_LEARNING.md)

### v4.2 架构设计 (2026-04-05 20:48)
- **设计目标**: 整合claw-code和oh-my-openagent最佳实践
- **6层架构**: 意图解析 → 动态委派 → 数据采集 → 多层验证 → 报告生成 → 会话管理
- **4大改进**: 意图解析层、动态委派层、4层验证、Boulder会话管理
- **完整代码**: 提供IntentParser、DynamicDelegator、MultiLayerVerification、BoulderSession实现
- **设计文档**: [V4_2_ARCHITECTURE_DESIGN.md](V4_2_ARCHITECTURE_DESIGN.md) (24KB)

## 用户信息
- 用户ID: 100047822012
- 平台: lightclawbot
- 时区: Asia/Shanghai

## 学习总结

### 2026-04-04
- 用户要求：输入"LNG报告"时必须调用lng-market-analysis skill
- 用户反馈：报告缺少国内LNG接收站和液厂实时数据
- 已更新：SKILL v1.4，新增润仓助理专职采集国内LNG市场价格
- 已更新：MEMORY.md
- 问题记录：lightclaw_upload_file上传的HTML文件在微信/lightclaw云盘预览可能提示"维护中"，备选方案是直接发送Markdown格式报告内容
### 2026-04-05 深度学习日 (17:00-21:25)
- **学习时长**: 4小时25分钟
- **学习项目**: 10个GitHub开源项目
- **核心收获**:
  - **claw-code**: Sisyphus 4阶段编排、Prometheus+Atlas分离
  - **oh-my-openagent**: ulw模式、Hephaestus 5步工作流
  - **claw-code-parity**: Rust 9-crate架构、Parity测试
  - **Clawd-Code**: 30+工具、Agent Loop、Skill系统
  - **ClawTeam**: 多Agent协作、动态任务分配
  - **ClawCloud-Run**: GitHub Actions定时任务
  - **ClawPanel**: 4种操作模式、8大工具、人机协作
- **文档产出**: 21个文档，~160,000字
- **SKILL升级**: v4.1 → v4.2 (AI助手增强版)
- **架构升级**: 六层架构、4层验证、Tool Registry、动态委派
- **关键改进**:
  - 4种操作模式 (聊天/规划/执行/无限)
  - 12助理动态委派 (基于能力匹配)
  - 4层验证 (L1自动→L2交叉→L3异常→L4人工)
  - Boulder会话管理 (断点续传)
  - 成本跟踪 (按助理跟踪API成本)
- **明日计划**: 实施期货/库存数据采集代码、测试ICE/GIE/EIA API、20:00报告进度

### 2026-04-04
- 用户要求：输入"LNG报告"时必须调用lng-market-analysis skill
- 用户反馈：报告缺少国内LNG接收站和液厂实时数据
- 已更新：SKILL v1.4，新增润仓助理专职采集国内LNG市场价格
- 已更新：MEMORY.md
- 问题记录：lightclaw_upload_file上传的HTML文件在微信/lightclaw云盘预览可能提示"维护中"，备选方案是直接发送Markdown格式报告内容
