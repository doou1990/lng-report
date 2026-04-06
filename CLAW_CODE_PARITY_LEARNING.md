# claw-code-parity 学习总结

**学习时间**: 2026-04-05 20:50-21:00  
**学习来源**: ultraworkers/claw-code-parity  
**核心目标**: 学习Rust实现和Parity（一致性）测试方法

---

## 🎯 项目概述

**claw-code-parity** 是 claw-code 的 **Rust重写版本**，专注于：
- **高性能**: Rust的速度和安全性
- **原生工具执行**: 直接调用系统工具
- **Parity（一致性）**: 与原始系统行为一致
- **Python移植**: 同时维护Python版本

**关键数据**:
- ~20K行Rust代码
- 9个workspace crate
- 50K+ stars（2小时内达成）

---

## 🏗️ Rust架构详解

### Crate结构

```
rust/
├── Cargo.toml              # Workspace根
├── Cargo.lock
└── crates/
    ├── api/                # Anthropic API客户端 + SSE流
    ├── commands/           # 共享slash命令注册表
    ├── compat-harness/     # TS清单提取harness
    ├── mock-anthropic-service/  # 确定性本地mock服务
    ├── plugins/            # 插件注册表和hook连接
    ├── runtime/            # 会话、配置、权限、MCP、prompts
    ├── rusty-claude-cli/   # 主CLI二进制文件 (`claw`)
    ├── telemetry/          # 会话追踪和遥测
    └── tools/              # 内置工具实现
```

### 各Crate职责

| Crate | 职责 | 应用到LNG系统 |
|-------|------|--------------|
| **api** | HTTP客户端、SSE解析、认证 | API调用标准化 |
| **commands** | Slash命令定义 | 交互式命令系统 |
| **runtime** | Agentic循环、配置、会话持久化 | 核心运行时 |
| **tools** | 工具实现(Bash/读写文件/搜索等) | 工具调用框架 |
| **telemetry** | 会话追踪、使用统计 | 成本跟踪 |
| **mock-anthropic-service** | 确定性mock服务 | 测试harness |

---

## 🔧 核心功能实现

### 1. 工具系统 (tools crate)

**内置工具列表**:
```rust
pub enum Tool {
    Bash,           // 执行shell命令
    ReadFile,       // 读取文件
    WriteFile,      // 写入文件
    EditFile,       // 编辑文件
    GlobSearch,     // 文件搜索
    GrepSearch,     // 内容搜索
    WebSearch,      // 网络搜索
    WebFetch,       // 网页获取
    Agent,          // 子Agent调用
    TodoWrite,      // TODO管理
    NotebookEdit,   // 笔记本编辑
    Skill,          // 技能调用
    ToolSearch,     // 工具搜索
}
```

**应用到LNG系统**:
```python
# LNG系统工具映射
TOOLS = {
    'web_search': '海明/润仓等助理使用',
    'web_fetch': '获取价格数据',
    'read_file': '读取历史数据',
    'write_file': '保存报告',
    'bash': '执行数据采集脚本',
    'agent': '12助理并行调用'
}
```

### 2. 运行时系统 (runtime crate)

**核心组件**:
```rust
// ConversationRuntime - Agentic循环
pub struct ConversationRuntime {
    config: Config,
    session: Session,
    permissions: PermissionPolicy,
    mcp_client: MCPClient,
    usage_tracker: UsageTracker,
}

// 关键方法
impl ConversationRuntime {
    pub async fn run_loop(&mut self) -> Result<()> {
        // 1. 加载系统prompt
        // 2. 等待用户输入
        // 3. 调用LLM
        // 4. 执行工具
        // 5. 循环直到完成
    }
}
```

**应用到LNG系统**:
```python
# LNG Runtime设计
class LNGReportRuntime:
    def __init__(self):
        self.config = ConfigLoader()
        self.session = BoulderSession()
        self.permissions = PermissionPolicy()
        self.agents = AgentRegistry()  # 12助理注册表
        self.usage_tracker = UsageTracker()
    
    async def generate_report(self, intent):
        # 1. 解析意图
        # 2. 动态委派
        # 3. 并行采集
        # 4. 多层验证
        # 5. 生成报告
```

### 3. 配置系统

**配置层级** (后加载覆盖前加载):
```
1. ~/.claw.json                    # 全局配置
2. ~/.config/claw/settings.json    # XDG配置
3. /.claw.json                     # 项目配置
4. /.claw/settings.json            # 项目详细配置
5. /.claw/settings.local.json      # 本地覆盖
```

**应用到LNG系统**:
```python
# LNG配置层级
CONFIG_HIERARCHY = [
    '~/.lng-report.json',                    # 全局
    '~/.config/lng-report/settings.json',    # XDG
    'workspace/lng-report.json',             # 项目
    'workspace/lng-report.local.json',       # 本地
]

# 配置内容
CONFIG = {
    'agents': {
        '原油': {'enabled': True, 'priority': 1},
        '海明': {'enabled': True, 'priority': 1},
        # ... 12助理配置
    },
    'data_sources': {
        'mysteel': {'api_key': '***', 'timeout': 30},
        'lng168': {'enabled': True},
    },
    'report': {
        'auto_generate_time': '14:00',
        'github_pages': True,
    }
}
```

### 4. 会话持久化

**会话存储**:
```rust
// 会话保存在 .claw/sessions/
pub struct Session {
    id: String,
    turns: Vec<Turn>,
    metadata: SessionMetadata,
}

// 恢复会话
pub fn resume_session(id: &str) -> Result<Session> {
    let path = format!(".claw/sessions/{}", id);
    Session::load(&path)
}
```

**应用到LNG系统** (Boulder增强):
```python
# 会话存储结构
.claw/
└── sessions/
    ├── 2026-04-05-001/           # 会话ID
    │   ├── state.json            # 状态
    │   ├── turns/                # 对话轮次
    │   └── checkpoints/          # 检查点
    └── latest -> 2026-04-05-001  # 软链接

# 恢复命令
lng-report --resume latest
lng-report --resume 2026-04-05-001
```

### 5. 权限系统

**权限模式**:
```rust
pub enum PermissionMode {
    ReadOnly,           // 只读
    WorkspaceWrite,     // 工作区写入
    DangerFullAccess,   // 完全访问（默认）
}
```

**应用到LNG系统**:
```python
class PermissionPolicy:
    MODES = {
        'read-only': ['web_search', 'web_fetch', 'read_file'],
        'workspace-write': ['write_file', 'edit_file', 'bash'],
        'danger-full-access': ['all_tools']
    }
    
    def check_permission(self, tool: str, mode: str) -> bool:
        return tool in self.MODES.get(mode, [])
```

### 6. 成本跟踪

**使用统计**:
```rust
pub struct UsageTracker {
    input_tokens: u64,
    output_tokens: u64,
    cost_usd: f64,
}

// 显示成本
pub fn show_cost(&self) {
    println!("Input: {} tokens", self.input_tokens);
    println!("Output: {} tokens", self.output_tokens);
    println!("Cost: ${:.4}", self.cost_usd);
}
```

**应用到LNG系统**:
```python
class UsageTracker:
    def __init__(self):
        self.daily_cost = 0.0
        self.monthly_cost = 0.0
        self.token_usage = {}
    
    def track_agent(self, agent_name: str, tokens: int, cost: float):
        self.token_usage[agent_name] = {
            'tokens': tokens,
            'cost': cost
        }
        self.daily_cost += cost
    
    def report(self):
        return {
            'daily_cost': self.daily_cost,
            'monthly_cost': self.monthly_cost,
            'by_agent': self.token_usage
        }
```

---

## 🧪 Parity（一致性）测试方法

### Mock服务

**确定性Mock**:
```rust
// mock-anthropic-service
pub struct MockAnthropicService {
    scenarios: HashMap<String, Scenario>,
}

impl MockAnthropicService {
    pub fn handle_messages(&self, req: Request) -> Response {
        // 返回确定性响应
        // 用于测试CLI行为一致性
    }
}
```

**测试场景**:
```json
// mock_parity_scenarios.json
{
  "scenarios": [
    {"name": "streaming_text", "status": "✅"},
    {"name": "read_file_roundtrip", "status": "✅"},
    {"name": "write_file_allowed", "status": "✅"},
    {"name": "write_file_denied", "status": "✅"},
    {"name": "multi_tool_turn_roundtrip", "status": "✅"},
    {"name": "bash_stdout_roundtrip", "status": "✅"}
  ]
}
```

**应用到LNG系统**:
```python
# LNG Mock服务
class MockDataSource:
    """确定性数据源Mock，用于测试"""
    
    SCENARIOS = {
        'brent_normal': {'price': 109.24, 'change': 0.02},
        'brent_spike': {'price': 120.00, 'change': 0.15},
        'brent_crash': {'price': 80.00, 'change': -0.20},
    }
    
    def get_price(self, scenario: str):
        return self.SCENARIOS.get(scenario)

# 测试用例
def test_price_validation():
    mock = MockDataSource()
    
    # 正常价格
    data = mock.get_price('brent_normal')
    assert verify_price(data) == 'A'
    
    # 异常价格（波动>20%）
    data = mock.get_price('brent_spike')
    assert verify_price(data) == 'C'  # 置信度降级
```

---

## 💡 关键技术洞察

### 1. Rust vs Python 选择

| 特性 | Rust | Python | 适用场景 |
|------|------|--------|----------|
| 性能 | ⭐⭐⭐ | ⭐⭐ | 高频数据采集 |
| 开发速度 | ⭐⭐ | ⭐⭐⭐ | 快速原型 |
| 安全性 | ⭐⭐⭐ | ⭐⭐ | 生产环境 |
| 生态 | ⭐⭐ | ⭐⭐⭐ | 数据科学 |

**LNG系统建议**:
- **数据采集层**: Rust（高频、稳定）
- **业务逻辑层**: Python（灵活、易维护）
- **展示层**: JavaScript（交互）

### 2. 配置驱动架构

**优势**:
- 无需修改代码即可调整行为
- 多环境支持（dev/staging/prod）
- 用户自定义

**LNG配置示例**:
```json
{
  "agents": {
    "润仓": {
      "data_sources": ["lng168", "mysteel", "oilchem"],
      "timeout": 30,
      "retry": 2
    }
  },
  "verification": {
    "auto_check": true,
    "cross_validation": true,
    "anomaly_detection": true
  }
}
```

### 3. 工具注册表模式

**动态工具加载**:
```rust
pub struct ToolRegistry {
    tools: HashMap<String, Box<dyn Tool>>,
}

impl ToolRegistry {
    pub fn register(&mut self, name: &str, tool: Box<dyn Tool>) {
        self.tools.insert(name.to_string(), tool);
    }
    
    pub fn execute(&self, name: &str, args: Args) -> Result<Output> {
        self.tools.get(name)?.execute(args)
    }
}
```

**LNG工具注册表**:
```python
class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.register_default_tools()
    
    def register_default_tools(self):
        self.register('web_search', WebSearchTool())
        self.register('web_fetch', WebFetchTool())
        self.register('data_verify', DataVerificationTool())
        # ... 更多工具
    
    def register_agent_tools(self):
        # 12助理作为工具注册
        for agent in AGENTS:
            self.register(f'agent_{agent.name}', AgentTool(agent))
```

---

## 🚀 应用到LNG系统

### 立即实施 (今晚)

1. **配置系统**
   ```bash
   # 创建配置层级
   mkdir -p ~/.config/lng-report
   touch ~/.config/lng-report/settings.json
   touch workspace/lng-report.json
   ```

2. **成本跟踪**
   ```python
   # 在每次API调用时跟踪
   usage_tracker.track_agent('润仓', tokens=1500, cost=0.03)
   ```

3. **会话恢复**
   ```python
   # 支持--resume参数
   if args.resume:
       boulder.resume(args.resume)
   ```

### 短期实施 (本周)

4. **Mock测试框架**
   - 创建确定性数据源Mock
   - 编写Parity测试用例
   - 自动化测试流程

5. **权限系统**
   - 实现3级权限模式
   - 工具调用前检查权限
   - 敏感操作确认提示

6. **工具注册表**
   - 重构12助理为工具
   - 动态加载新工具
   - 工具版本管理

### 长期规划 (本月)

7. **Rust核心**
   - 调研Rust重写可行性
   - 性能关键路径Rust化
   - 保持Python业务逻辑

8. **遥测系统**
   - 详细使用统计
   - 性能监控
   - 错误追踪

---

## 📊 学习成果总结

| 技术 | claw-code-parity | LNG系统应用 |
|------|-----------------|-------------|
| **Crate架构** | 9个crate分工 | 模块化重构 |
| **配置系统** | 5层配置层级 | 用户自定义 |
| **会话持久化** | .claw/sessions/ | Boulder增强 |
| **权限系统** | 3级权限 | 安全控制 |
| **成本跟踪** | UsageTracker | 预算管理 |
| **Mock测试** | 确定性响应 | 自动化测试 |
| **工具注册表** | 动态加载 | 灵活扩展 |

---

## 📚 参考资源

- [claw-code-parity GitHub](https://github.com/ultraworkers/claw-code-parity)
- [USAGE.md](https://github.com/ultraworkers/claw-code-parity/blob/main/USAGE.md)
- [rust/README.md](https://github.com/ultraworkers/claw-code-parity/blob/main/rust/README.md)

---

*学习时间: 2026-04-05 20:50-21:00*  
*核心收获: Rust架构、Parity测试、配置系统、成本跟踪*  
*可应用技术: 7项*
