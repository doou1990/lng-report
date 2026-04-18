# LNG市场分析助手 Skill v4.2 - AI助手增强版

**更新时间**: 2026-04-05 21:15  
**更新内容**: 融合ClawPanel AI助手4模式、ClawTeam多Agent协作、claw-code工具系统

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

### L4: 人工审核
```python
def l4_manual_audit(data: dict, l1_l2_l3_results: dict) -> AuditResult:
    """第四层：人工审核（置信度<D时触发）"""
    if l1_l2_l3_results['confidence'] == 'D':
        # 触发人工审核
        return request_human_audit(data)
    return AuditResult(approved=True)
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

## ⚠️ 重要规则 (v4.2 固化)

1. **4种模式**: 根据用户需求自动选择或询问
2. **12助理**: 易经八卦+两仪扩展，动态委派
3. **Tool Registry**: 统一工具管理，可开关
4. **4层验证**: L1自动→L2交叉→L3异常→L4人工
5. **置信度评分**: A/B/C/D四级，D级不采用
6. **Boulder会话**: 断点续传，崩溃恢复
7. **成本跟踪**: 按助理跟踪API成本
8. **人机协作**: 关键决策询问用户
9. **定时任务**: 每天14:00无限模式自动生成
10. **GitHub推送**: 自动推送到 https://doou1990.github.io/lng-report/

---

## 📁 文件结构 (v4.2)

```
skills/lng-market-analysis/
├── SKILL.md                    # 本文件
├── agents/                     # 12助理配置
│   ├── 原油.yml
│   ├── 海明.yml
│   ├── ...
│   ├── 期货.yml               # 新增
│   └── 库存.yml               # 新增
├── tools/                      # 工具实现
│   ├── registry.py
│   ├── web_search.py
│   ├── web_fetch.py
│   └── ...
├── modes/                      # 4种模式
│   ├── chat.py
│   ├── plan.py
│   ├── execute.py
│   └── unlimited.py
├── verification/               # 4层验证
│   ├── l1_auto_check.py
│   ├── l2_cross_validation.py
│   ├── l3_anomaly_detection.py
│   └── l4_manual_audit.py
├── templates/                  # 报告模板
│   ├── markdown.template
│   └── html.template
└── config/
    └── default.yml
```

---

## 🎓 学习来源

本v4.2版本融合以下项目的最佳实践：

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

*Skill版本: v4.2*  
*更新日期: 2026-04-05*  
*学习时长: 4小时15分钟*  
*融合项目: 10个*
