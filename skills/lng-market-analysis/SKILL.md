# LNG市场分析助手 Skill v4.4 - 自然语言查询与可视化增强版

**更新时间**: 2026-04-06 19:06  
**更新内容**: 自然语言查询、8种可视化图表、MCP服务器设计

---

## 🚨 v4.3 关键优化

### 1. 超时机制优化
| 任务类型 | v4.2超时 | v4.3超时 | 优化效果 |
|---------|---------|---------|---------|
| 简单搜索 | 120s | 120s | 保持不变 |
| 复杂采集 | 120s | **180s** | **+50%** |
| 审核任务 | 120s | **90s** | **简化流程** |

### 2. 搜索策略优化
```yaml
# v4.2: 每助理≥3轮搜索，无上限
# v4.3: 分层搜索，硬性限制3轮

search_strategy:
  round_1: 精准关键词，高置信源
  round_2: 补充验证，交叉核对  
  round_3: 仅当差异>5%时执行
  max_rounds: 3  # 硬性限制
```

### 3. 分层审核优化
```yaml
# v4.2: 中孚作为独立助理，易超时
# v4.3: L1-L3主代理自动执行，L4按需触发

layer_4_verification:
  l1_auto_check: 主代理执行(自动规则)
  l2_cross_validation: 主代理执行(多源对比)
  l3_anomaly_detection: 主代理执行(统计检测)
  l4_manual_audit: 仅当置信度<C时触发
```

### 4. 数据源优先级配置
```yaml
agent_3_luyuan:
  primary: ["Kpler", "Bloomberg"]
  fallback: ["E-Gas", "主代理知识库"]
  timeout: 180s

agent_12_kucun:
  primary: ["EIA周报", "GIE"]
  fallback: ["Eurostat"]
  timeout: 180s
```

### 5. 自然语言查询 (v4.4新增)

**功能**: 用户直接用中文查询LNG数据，系统自动生成SQL、可视化图表和分析报告

**使用示例**:
```
用户: "本周LNG价格趋势如何？"
系统: 
  - 意图识别: trend, lng, this_week
  - 生成SQL: SELECT * FROM lng_prices WHERE date BETWEEN ...
  - 自动可视化: 折线图展示JKM/TTF/Henry Hub趋势
  - 生成分析: "本周LNG价格呈现上涨趋势，JKM上涨2.3%..."
```

**实现模块**:
- `nl_query_engine.py` - 自然语言查询引擎
- 意图识别 → SQL生成 → 数据查询 → 可视化 → 分析生成

### 6. 可视化增强 (v4.4新增)

**图表类型**:
| 图表类型 | 适用场景 | 自动选择条件 |
|---------|---------|-------------|
| **折线图** | 时间序列趋势 | 时间跨度>7天 |
| **柱状图** | 对比分析 | 类别对比数据 |
| **K线图** | 价格波动 | 高频价格数据 |
| **面积图** | 累积趋势 | 展示总量变化 |
| **散点图** | 相关性分析 | 双变量关系 |
| **热力图** | 矩阵数据 | 多维度对比 |
| **仪表盘** | 关键指标 | 单一重要数值 |
| **组合图** | 多指标对比 | 价格+库存+利润 |

**交互功能**:
- 数据缩放 (DataZoom)
- 工具栏 (Toolbox): 保存、刷新、数据视图
- 悬停提示 (Tooltip)
- 图例切换 (Legend)
- 区域缩放 (Brush)

---

## 🎯 核心理念升级

基于今日学习成果，融合以下最佳实践：

### 1. ClawPanel AI助手模式
```
💬 聊天模式 → 纯问答，不触碰系统
📋 规划模式 → 分析需求，制定采集计划
⚡ 执行模式 → 正常采集，危险操作确认
∞ 无限模式 → 全自动报告生成
```

### 2. ClawTeam多Agent协作
```
Planner (意图解析器) → Executor (12助理) → Reviewer (中孚) → Coordinator (主控)
```

### 3. claw-code工具系统
```
Tool Registry → Agent Loop → Verification → Output
```

---

## 🤖 12位专业助理（v4.2 易经八卦+两仪扩展）

| 编号 | 助理 | 卦象 | 职责 | 核心能力 |
|------|------|------|------|----------|
| 1 | 原油 | 乾☰ | Brent/WTI价格 | 0.95 |
| 2 | 海明 | 坤☷ | JKM/TTF/HH国际价格 | 0.95 |
| 3 | 陆远 | 震☳ | 中国LNG进口/贸易 | 0.90 |
| 4 | 润仓 | 巽☴ | 国内LNG价格★必采★ | 0.95 |
| 5 | 衡尺 | 坎☵ | 价格驱动因素 | 0.85 |
| 6 | 欧风 | 离☲ | 欧洲市场/库存 | 0.90 |
| 7 | 金算 | 艮☶ | 产业链利润 | 0.85 |
| 8 | 盾甲 | 兑☱ | 投资评级 | 0.85 |
| 9 | 镜史 | 乾☰ | 历史对比 | 0.80 |
| 10 | 洋基 | 坤☷ | 美国LNG产能 | 0.85 |
| **11** | **期货** | **阳⚊** | **期货价格/价差** | **0.90** |
| **12** | **库存** | **阴⚋** | **全球LNG库存** | **0.85** |

---

## 🏗️ v4.2 六层架构

基于今日学习的DeepFlow 2.0 + claw-code + ClawPanel + ClawTeam融合设计：

```
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 1: INTENT PARSER (意图解析层)                                   │
│  ├── 模式识别: 聊天/规划/执行/无限                                     │
│  ├── 需求澄清: 询问用户具体需求                                        │
│  └── 任务分解: 生成子任务清单                                          │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 2: DYNAMIC DELEGATOR (动态委派层)                               │
│  ├── 能力匹配: 根据数据类型选择最佳助理                                 │
│  ├── 并行分组: 每组5个助理同时执行                                     │
│  └── 备用计划: 每个Agent的fallback方案                                 │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 3: DATA COLLECTION (数据采集层)                                 │
│  ├── 12助理并行采集                                                   │
│  ├── Tool Registry统一工具管理                                        │
│  └── 失败自动重试 + 主代理补采                                         │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 4: MULTI-LAYER VERIFICATION (多层验证层)                        │
│  ├── L1: 自动检查 (数值范围/非空/时效性)                               │
│  ├── L2: 交叉验证 (≥2来源，差异<5%)                                   │
│  ├── L3: 异常检测 (3σ/IQR/Isolation Forest)                           │
│  └── L4: 人工审核 (置信度<D时触发)                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 5: REPORT GENERATION (报告生成层)                               │
│  ├── Markdown完整版                                                   │
│  ├── HTML网页版 (ECharts可视化)                                        │
│  ├── 数据JSON (程序化访问)                                             │
│  └── GitHub Pages自动推送                                              │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 6: SESSION MANAGEMENT (会话管理层)                              │
│  ├── Boulder状态跟踪 (boulder.json)                                    │
│  ├── 断点续传机制                                                      │
│  └── 成本跟踪 (UsageTracker)                                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 4种操作模式详解

### 模式1: 聊天模式 💬
```yaml
mode: chat
tools: []                    # 无工具权限
can_collect: false           # 禁止数据采集
confirmation: false          # 无需确认
color: blue
description: 纯问答，不触碰系统

应用场景:
  - "什么是LNG?"
  - "解释一下JKM价格"
  - "今天有什么重要新闻?"
```

### 模式2: 规划模式 📋
```yaml
mode: plan
tools: [read_file, list_directory, get_system_info]
can_collect: false           # 禁止采集
confirmation: true           # 需要确认
color: yellow
description: 分析需求，制定采集计划

应用场景:
  - "帮我规划明天的报告采集"
  - "检查现有数据完整性"
  - "分析需要补充哪些数据源"

执行流程:
  1. 解析用户需求
  2. 检查历史数据可用性
  3. 识别缺失数据源
  4. 制定采集计划
  5. 询问用户确认
```

### 模式3: 执行模式 ⚡
```yaml
mode: execute
tools: [web_search, web_fetch, read_file, write_file, bash]
can_collect: true            # 允许采集
confirmation: true           # 危险操作需确认
color: green
description: 正常采集，危险操作确认

dangerous_operations:
  - pattern: github.*delete
    desc: 删除GitHub资源
  - pattern: rm\s+-rf
    desc: 强制删除文件
  - pattern: price.*change.*>.*20%
    desc: 价格波动>20%

应用场景:
  - "生成今天的LNG报告"
  - "采集原油价格数据"
  - "更新浙江接收站价格"
```

### 模式4: 无限模式 ∞
```yaml
mode: unlimited
tools: [all]
can_collect: true            # 允许采集
confirmation: false          # 无需确认
auto_execute: true           # 自动执行
color: red
description: 全自动报告生成

应用场景:
  - 定时任务 (每天14:00)
  - 已知安全的批量操作
  - 自动化脚本

执行流程:
  1. 自动解析意图
  2. 动态委派12助理
  3. 并行采集数据
  4. 多层验证
  5. 自动生成报告
  6. 自动推送到GitHub
  7. 自动验证
```

---

## 🛠️ Tool Registry (工具注册表)

基于claw-code和Clawd-Code的工具系统设计：

```python
class LNGToolRegistry:
    """LNG工具注册表 - 统一管理所有工具"""
    
    def __init__(self):
        self._tools = {}
        self._register_builtin_tools()
        self._register_agent_tools()
    
    def _register_builtin_tools(self):
        """注册内置工具"""
        self.register('web_search', WebSearchTool())
        self.register('web_fetch', WebFetchTool())
        self.register('read_file', ReadFileTool())
        self.register('write_file', WriteFileTool())
        self.register('bash', BashTool())
        self.register('data_verify', DataVerificationTool())
    
    def _register_agent_tools(self):
        """注册12助理作为工具"""
        for agent in LNG_AGENTS:
            self.register(f'agent_{agent.name}', AgentTool(agent))
    
    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """执行工具"""
        tool = self._tools.get(tool_name)
        if not tool:
            return ToolResult.error(f"Tool {tool_name} not found")
        return tool.execute(**kwargs)
```

### 8大核心工具

| 工具 | 功能 | 应用到LNG |
|------|------|-----------|
| **web_search** | 网络搜索 | 助理数据采集 |
| **web_fetch** | 网页获取 | 价格数据提取 |
| **read_file** | 文件读取 | 读取历史数据 |
| **write_file** | 文件写入 | 保存报告 |
| **bash** | 命令执行 | 执行脚本 |
| **data_verify** | 数据验证 | 多层验证 |
| **ask_user** | 用户交互 | 询问需求 |
| **check_port** | 端口检测 | Gateway状态 |

---

## 🤖 12助理动态委派

基于ClawTeam的任务分配策略：

```python
class LNGTaskAllocator:
    """LNG任务分配器 - 基于能力匹配"""
    
    AGENT_CAPABILITIES = {
        '原油': {'brent': 0.95, 'wti': 0.95, 'brent_futures': 0.90},
        '海明': {'jkm': 0.95, 'ttf': 0.90, 'hh': 0.85, 'jkm_futures': 0.85},
        '润仓': {'国内': 0.95, '浙江': 0.95, '液厂': 0.90},
        '期货': {'brent_futures': 0.90, 'jkm_futures': 0.85, 'ttf_futures': 0.85},
        '库存': {'eu_inventory': 0.85, 'us_inventory': 0.90, 'china_inventory': 0.70}
    }
    
    def allocate(self, data_type: str) -> str:
        """根据数据类型分配最佳助理"""
        scores = {}
        for agent, caps in self.AGENT_CAPABILITIES.items():
            scores[agent] = caps.get(data_type, 0)
        
        # 选择得分最高的助理
        best_agent = max(scores, key=scores.get)
        
        # 检查负载，如过载则选择次优
        if self._is_overloaded(best_agent):
            scores.pop(best_agent)
            best_agent = max(scores, key=scores.get)
        
        return best_agent
```

---

## 🔍 多层验证 (4层)

基于今日学习的验证机制：

### L1: 自动检查
```python
def l1_auto_check(data: dict) -> CheckResult:
    """第一层：自动规则检查"""
    errors = []
    
    # 数值范围检查
    if not (0 < data['price'] < 10000):
        errors.append(f"价格超出合理范围: {data['price']}")
    
    # 非空检查
    if not data.get('source'):
        errors.append("缺少数据来源")
    
    # 时效性检查
    if data['date'] < datetime.now() - timedelta(days=7):
        errors.append("数据过期")
    
    return CheckResult(passed=len(errors)==0, errors=errors)
```

### L2: 交叉验证
```python
def l2_cross_validation(sources: List[dict]) -> ValidationResult:
    """第二层：多源交叉验证"""
    if len(sources) < 2:
        return ValidationResult(confidence='B', note='单来源')
    
    values = [s['value'] for s in sources]
    avg = sum(values) / len(values)
    max_diff = max(abs(v - avg) / avg for v in values)
    
    if max_diff < 0.03:
        return ValidationResult(confidence='A', note='多源一致')
    elif max_diff < 0.05:
        return ValidationResult(confidence='B', note=f'差异{max_diff:.1%}')
    else:
        return ValidationResult(confidence='C', note=f'差异较大{max_diff:.1%}')
```

### L3: 异常检测
```python
def l3_anomaly_detection(current: float, history: List[float]) -> AnomalyResult:
    """第三层：统计异常检测"""
    # 3σ检测
    mean = np.mean(history)
    std = np.std(history)
    z_score = abs(current - mean) / std
    
    if z_score > 3:
        return AnomalyResult(is_anomaly=True, method='3σ', severity='high')
    
    # IQR检测
    q1, q3 = np.percentile(history, [25, 75])
    iqr = q3 - q1
    if current < q1 - 1.5*iqr or current > q3 + 1.5*iqr:
        return AnomalyResult(is_anomaly=True, method='IQR', severity='medium')
    
    return AnomalyResult(is_anomaly=False)
```

### L4: 分层审核 (v4.3优化)

```python
# v4.3: 分层审核，主代理执行L1-L3，L4按需触发
def layer_4_verification(data: dict, agent_results: list) -> AuditReport:
    """第四层：多层验证"""
    
    # L1: 自动检查 (主代理执行)
    l1_result = l1_auto_check(data)
    if not l1_result.passed:
        return AuditReport(confidence='D', errors=l1_result.errors)
    
    # L2: 交叉验证 (主代理执行)
    l2_result = l2_cross_validation(agent_results)
    if l2_result.confidence == 'C':
        return AuditReport(confidence='C', note=l2_result.note)
    
    # L3: 异常检测 (主代理执行)
    l3_result = l3_anomaly_detection(data)
    if l3_result.is_anomaly and l3_result.severity == 'high':
        return AuditReport(confidence='C', note=f"3σ异常: {l3_result.method}")
    
    # L4: 人工审核 (仅当置信度<C时触发，避免超时)
    if l2_result.confidence in ['C', 'D']:
        return request_human_audit(data)
    
    return AuditReport(
        confidence=l2_result.confidence,
        l1_passed=True,
        l2_result=l2_result,
        l3_result=l3_result
    )
```

---

## 📊 置信度评分 (v4.2)

| 等级 | 分数 | L1 | L2 | L3 | L4 | 处理 |
|------|------|----|----|----|----|------|
| A | 90-100 | ✅ | ≥2源<3% | 无异常 | 免审 | 直接采用 |
| B | 75-89 | ✅ | 2源3-5% | 无异常 | 免审 | 采用，标注差异 |
| C | 60-74 | ✅ | 1-2源5-10% | 轻微异常 | 抽查 | 采用，标注低可信度 |
| D | <60 | ❌ | 单源>10% | 严重异常 | 必审 | 不采用，标记缺失 |

---

## 🎨 UI设计升级

基于ClawPanel的颜色编码和交互设计：

### 模式颜色
```css
--mode-chat: #3b82f6;      /* 蓝色 - 安全 */
--mode-plan: #eab308;      /* 黄色 - 警告 */
--mode-execute: #22c55e;   /* 绿色 - 正常 */
--mode-unlimited: #ef4444; /* 红色 - 危险 */
```

### 置信度徽章
```html
<span class="badge badge-a">A</span> <!-- 绿色 -->
<span class="badge badge-b">B</span> <!-- 蓝色 -->
<span class="badge badge-c">C</span> <!-- 黄色 -->
<span class="badge badge-d">D</span> <!-- 红色 -->
```

---

## 🚀 执行流程 (v4.2)

```
用户输入
    ↓
[Layer 1] 意图解析 → 识别模式(聊天/规划/执行/无限)
    ↓
[Layer 2] 动态委派 → 选择相关助理
    ↓
[Layer 3] 并行采集 → 12助理同时工作
    ↓
[Layer 4] 多层验证 → L1→L2→L3→L4
    ↓
[Layer 5] 报告生成 → Markdown + HTML + JSON
    ↓
[Layer 6] 会话管理 → Boulder保存 + 成本跟踪
    ↓
输出结果
```

---

## ⚙️ 超时与搜索策略配置 (v4.3新增)

### 超时配置
```yaml
# config/timeout.yml
agent_timeout:
  simple_task: 120s      # 简单搜索(原油、期货)
  complex_task: 180s     # 复杂采集(进口、库存)
  audit_task: 90s        # 审核任务(简化流程)

# 按助理配置
agent_specific:
  agent_3_luyuan: 180s   # 中国进口数据复杂
  agent_12_kucun: 180s   # 全球库存多源采集
  others: 120s           # 其他助理默认
```

### 搜索策略配置
```yaml
# config/search_strategy.yml
search_rules:
  max_rounds: 3          # 硬性限制3轮
  
  round_1:
    description: "精准关键词，高置信源"
    sources: ["Exa", "官方API", "权威媒体"]
    required: true
    
  round_2:
    description: "补充验证，交叉核对"
    condition: "R1数据不完整或差异>3%"
    required: conditional
    
  round_3:
    description: "仅当差异>5%时执行"
    condition: "R1+R2差异>5%"
    required: conditional
    
  stop_conditions:
    - "已获得≥2个独立来源"
    - "数据差异<5%"
    - "达到max_rounds限制"
```

### 数据源优先级
```yaml
# config/data_sources.yml
agents:
  agent_1_crude:
    primary: ["OilPrice.com", "Energy Intelligence"]
    fallback: ["Trading Economics", "Bloomberg"]
    
  agent_2_international:
    primary: ["lngpriceindex.com", "CME", "Global LNG Hub"]
    fallback: ["TradingView", "Investing.com"]
    
  agent_3_luyuan:
    primary: ["Kpler", "Bloomberg", "海关总署"]
    fallback: ["E-Gas", "Reuters"]
    
  agent_4_runcang:
    primary: ["LNG物联网(lng168.com)", "隆众资讯"]
    fallback: ["Mysteel", "百川盈孚"]
    
  agent_6_oufeng:
    primary: ["GIE AGSI", "Eurostat"]
    fallback: ["EIA周报引用", "行业研报"]
    
  agent_12_kucun:
    primary: ["EIA", "GIE AGSI"]
    fallback: ["EIA周报", "Eurostat"]
```

---

## ⚠️ 重要规则 (v4.3 更新)

1. **4种模式**: 根据用户需求自动选择或询问
2. **12助理**: 易经八卦+两仪扩展，动态委派
3. **超时配置**: 简单120s/复杂180s/审核90s
4. **搜索策略**: 硬性限制3轮，分层执行
5. **4层验证**: L1-L3主代理自动，L4按需触发
6. **置信度评分**: A/B/C/D四级，D级不采用
7. **Boulder会话**: 断点续传，崩溃恢复
8. **成本跟踪**: 按助理跟踪API成本
9. **定时任务**: 每天14:00无限模式自动生成
10. **GitHub推送**: 自动推送到 https://doou1990.github.io/lng-report/ (已启用 ✅ 2026-04-06)

### GitHub共享启用条件 (已达标 ✅ 2026-04-06)
- [x] 国内LNG价格数据准确度 ≥ 90%
- [x] 浙江接收站价格稳定获取
- [x] 期货价格数据完整
- [x] 库存数据稳定来源
- [x] 连续7天报告无重大数据缺失
- [x] 用户手动确认启用

**状态**: 已就绪，等待初始化GitHub仓库

---

## 📁 文件结构 (v4.4)

```
skills/lng-market-analysis/
├── SKILL.md                    # 本文件 (v4.4)
├── agents/                     # 12助理配置
│   ├── 原油.yml                # timeout: 120s
│   ├── 海明.yml                # timeout: 120s
│   ├── 陆远.yml                # timeout: 180s
│   ├── 润仓.yml                # timeout: 120s
│   ├── ...
│   ├── 期货.yml
│   └── 库存.yml                # timeout: 180s
├── tools/                      # 工具实现
│   ├── registry.py
│   ├── web_search.py
│   ├── web_fetch.py
│   ├── timeout_manager.py
│   ├── nl_query_engine.py      # 新增 (v4.4) - 自然语言查询
│   └── visualization_library.py # 新增 (v4.4) - 可视化库
├── modes/                      # 4种模式
│   ├── chat.py
│   ├── plan.py
│   ├── execute.py
│   └── unlimited.py
├── visualization/              # 可视化配置 (v4.4新增)
│   ├── charts/                 # 8种图表类型配置
│   ├── themes/                 # 主题样式
│   └── templates/              # 图表模板
├── docs/
│   ├── LNG_MCP_Server_Design.md    # 新增 (v4.4) - MCP服务器设计
│   ├── v4.2_超时问题分析.md
│   ├── v4.3_优化方案.md
│   └── v4.4_新特性说明.md          # 新增 (v4.4)
└── ...
│   ├── plan.py
│   ├── execute.py
│   └── unlimited.py
├── verification/               # 4层验证 (v4.3优化)
│   ├── l1_auto_check.py        # 主代理执行
│   ├── l2_cross_validation.py  # 主代理执行
│   ├── l3_anomaly_detection.py # 主代理执行
│   └── l4_manual_audit.py      # 按需触发
├── config/                     # 配置 (v4.3新增)
│   ├── default.yml
│   ├── timeout.yml             # 超时配置
│   ├── search_strategy.yml     # 搜索策略
│   └── data_sources.yml        # 数据源优先级
├── templates/                  # 报告模板
│   ├── markdown.template
│   └── html.template
└── docs/
    ├── v4.2_超时问题分析.md     # 问题总结
    └── v4.3_优化方案.md         # 优化记录
```

---

## 📝 版本历史

| 版本 | 日期 | 主要更新 |
|------|------|---------|
| v4.3 | 2026-04-06 | 超时优化、搜索策略、分层审核 |
| v4.2 | 2026-04-05 | AI助手增强、4模式、动态委派 |
| v4.1 | 2026-04-05 | 期货助理、库存助理、价差分析 |
| v4.0 | 2026-04-05 | 六阶段流程、标准化采集 |
| v3.1 | 2026-04-05 | 扩大搜索范围、多源审核 |
| v3.0 | 2026-04-05 | 多源采集、深度审核 |
| v2.2 | 2026-04-04 | Claude Code最佳实践 |
| v2.1 | 2026-04-04 | 优化搜索策略、浙江专区 |
| v2.0 | 2026-04-04 | 自动触发、定时任务 |
| v1.4 | 2026-04-04 | 润仓助理、国内LNG价格 |

## 🎓 学习来源

本v4.3版本融合以下项目的最佳实践：

| 项目 | 核心贡献 |
|------|----------|
| claw-code | Sisyphus编排、Prometheus+Atlas分离 |
| oh-my-openagent | ulw模式、Hephaestus工作流 |
| claw-code-parity | 9个crate架构、Parity测试 |
| Clawd-Code | 30+工具、Agent Loop |
| ClawTeam | 多Agent协作、任务分配 |
| ClawCloud-Run | GitHub Actions定时任务 |
| ClawPanel | 4种模式、8大工具、人机协作 |

---

*Skill版本: v4.3*  
*更新日期: 2026-04-06*  
*优化内容: 超时机制、搜索策略、分层审核*  
*解决v4.2问题: 3个助理超时*  
*预期提升: 成功率83%→95%+，执行时间-25%*
