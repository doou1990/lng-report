# Clawd-Code (Python版) 学习总结

**学习时间**: 2026-04-05 20:53-21:00  
**学习来源**: GPT-AGI/Clawd-Code  
**核心目标**: 学习Python实现的Agent系统，提炼可应用技术

---

## 🎯 项目概述

**Clawd-Code** 是 Claude Code 的 **完整Python重实现**，特点：
- ✅ **真实可用**: 不是代码片段，是完整CLI工具
- ✅ **基于源码**: 从真实TypeScript源码移植
- ✅ **架构保真**: 保留原始设计模式
- ✅ **Python原生**: 干净、符合Python习惯的代码
- ✅ **多Provider**: 支持Anthropic/OpenAI/GLM
- ✅ **完整工具**: 30+工具，Agent Loop完整实现

**技术栈**:
- Python 3.11+
- 完整类型提示
- 现代Python特性
- uv包管理

---

## 🏗️ 核心架构

### 目录结构

```
Clawd-Code/
├── src/
│   ├── cli.py              # CLI入口
│   ├── providers/          # LLM提供商 (Anthropic/OpenAI/GLM)
│   ├── repl/               # 交互式REPL
│   ├── skills/             # SKILL.md加载与创建
│   └── tool_system/        # 工具注册、循环、验证
├── tests/                  # 核心测试套件
├── .clawd/
│   └── skills/             # 项目级自定义技能
└── FEATURE_LIST.md         # 功能状态跟踪
```

### 核心模块

| 模块 | 文件 | 功能 | 应用到LNG |
|------|------|------|-----------|
| **cli.py** | 入口 | 命令解析、启动REPL | 主入口设计 |
| **providers/** | 多目录 | 多模型抽象层 | 多模型支持 |
| **repl/** | 多文件 | 交互式REPL | 交互体验 |
| **skills/** | skill加载 | Markdown技能系统 | SKILL.md优化 |
| **tool_system/** | 30+工具 | 工具注册、Agent Loop | 核心工具框架 |

---

## 🔧 关键技术详解

### 1. 多Provider抽象层

**设计模式**:
```python
# providers/base.py
class BaseProvider(ABC):
    @abstractmethod
    def chat(self, messages: list) -> Iterator[str]:
        """流式聊天接口"""
        pass
    
    @abstractmethod
    def get_models(self) -> list[str]:
        """获取可用模型列表"""
        pass

# providers/anthropic.py
class AnthropicProvider(BaseProvider):
    def chat(self, messages):
        # Anthropic特定实现
        pass

# providers/openai.py
class OpenAIProvider(BaseProvider):
    def chat(self, messages):
        # OpenAI特定实现
        pass
```

**配置管理**:
```json
// ~/.clawd/config.json
{
  "default_provider": "glm",
  "providers": {
    "anthropic": {
      "api_key": "base64-encoded-key",
      "base_url": "https://api.anthropic.com",
      "default_model": "claude-sonnet-4-20250514"
    },
    "openai": {
      "api_key": "base64-encoded-key",
      "base_url": "https://api.openai.com/v1",
      "default_model": "gpt-4"
    },
    "glm": {
      "api_key": "base64-encoded-key",
      "base_url": "https://open.bigmodel.cn/api/paas/v4",
      "default_model": "glm-4.5"
    }
  }
}
```

**应用到LNG系统**:
```python
# LNG多模型支持
class LNGProviderManager:
    PROVIDERS = {
        'exa': ExaProvider(),      # 搜索
        'mysteel': MysteelProvider(),  # 国内数据
        'lng168': LNG168Provider(),    # LNG物联网
    }
    
    def get_data(self, source: str, query: str):
        provider = self.PROVIDERS.get(source)
        return provider.fetch(query)
```

---

### 2. 工具系统 (Tool System)

**工具基类**:
```python
# tool_system/base.py
class BaseTool(ABC):
    name: str
    description: str
    parameters: dict  # JSON Schema
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        pass

# 工具结果
@dataclass
class ToolResult:
    success: bool
    output: str
    error: Optional[str] = None
```

**30+工具实现**:

| 类别 | 工具 | 状态 | 应用到LNG |
|------|------|------|-----------|
| 文件操作 | FileReadTool | ✅ | 读取历史数据 |
| 文件操作 | FileWriteTool | ✅ | 保存报告 |
| 文件操作 | FileEditTool | ✅ | 更新数据 |
| 文件操作 | GlobTool | ✅ | 批量文件处理 |
| 文件操作 | GrepTool | ✅ | 内容搜索 |
| 系统操作 | BashTool | ✅ | 执行脚本 |
| 网络工具 | WebFetchTool | ✅ | 获取网页 |
| 网络工具 | WebSearchTool | ✅ | 搜索数据 |
| 交互工具 | AskUserQuestionTool | ✅ | 用户确认 |
| 任务管理 | TodoWriteTool | ✅ | 任务跟踪 |
| 任务管理 | TaskManager | ✅ | 任务管理 |
| Agent工具 | AgentTool | ✅ | 子Agent调用 |
| Agent工具 | BriefTool | ✅ | 任务简报 |
| Agent工具 | TeamTool | ✅ | 团队协调 |
| 配置工具 | ConfigTool | ✅ | 配置管理 |
| 计划模式 | PlanModeTool | ✅ | 计划模式 |
| 定时任务 | CronTool | ✅ | 定时报告 |
| MCP工具 | MCPTool | ✅ | MCP集成 |
| 技能系统 | SkillTool | ✅ | 技能调用 |
| 工具搜索 | ToolSearchTool | ✅ | 工具发现 |

**工具注册表**:
```python
# tool_system/registry.py
class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        return list(self._tools.keys())
    
    def execute(self, name: str, **kwargs) -> ToolResult:
        tool = self.get(name)
        if not tool:
            return ToolResult(success=False, error=f"Tool {name} not found")
        return tool.execute(**kwargs)
```

**应用到LNG系统**:
```python
# LNG工具注册表
class LNGToolRegistry:
    def __init__(self):
        self.registry = ToolRegistry()
        self._register_lng_tools()
    
    def _register_lng_tools(self):
        # 注册12助理作为工具
        for agent in LNG_AGENTS:
            self.registry.register(AgentTool(agent))
        
        # 注册数据工具
        self.registry.register(WebSearchTool())
        self.registry.register(WebFetchTool())
        self.registry.register(DataVerificationTool())
    
    async def collect_data(self, agent_name: str, query: str):
        return await self.registry.execute(
            f'agent_{agent_name}',
            query=query
        )
```

---

### 3. Agent Loop (核心循环)

**实现模式**:
```python
# tool_system/agent_loop.py
class AgentLoop:
    def __init__(self, provider: BaseProvider, tools: ToolRegistry):
        self.provider = provider
        self.tools = tools
        self.messages = []
    
    async def run(self, user_input: str) -> str:
        """运行Agent循环直到完成"""
        self.messages.append({"role": "user", "content": user_input})
        
        while True:
            # 1. 调用LLM
            response = await self._call_llm()
            
            # 2. 检查是否有工具调用
            if not response.tool_calls:
                # 无工具调用，直接返回结果
                return response.content
            
            # 3. 执行工具
            for tool_call in response.tool_calls:
                result = await self._execute_tool(tool_call)
                
                # 4. 将结果添加回对话
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result.output
                })
    
    async def _call_llm(self) -> LLMResponse:
        """调用LLM获取响应"""
        return await self.provider.chat(self.messages)
    
    async def _execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """执行单个工具"""
        return self.tools.execute(
            tool_call.name,
            **tool_call.arguments
        )
```

**应用到LNG系统**:
```python
# LNG Agent Loop
class LNGReportLoop:
    def __init__(self):
        self.intent_parser = IntentParser()
        self.delegator = DynamicDelegator()
        self.verifier = MultiLayerVerification()
        self.tools = LNGToolRegistry()
    
    async def generate_report(self, user_input: str):
        # 1. 解析意图
        intent = self.intent_parser.parse(user_input)
        
        # 2. 动态委派
        plan = self.delegator.delegate(intent)
        
        # 3. 并行执行工具（12助理）
        results = await asyncio.gather(*[
            self.tools.collect_data(agent, intent)
            for agent in plan['selected_agents']
        ])
        
        # 4. 多层验证
        verified = self.verifier.verify(results)
        
        # 5. 生成报告
        return self._generate_output(verified)
```

---

### 4. Skill系统 (SKILL.md)

**Skill定义格式**:
```markdown
---
description: 解释代码，使用类比和图表
when_to_use: 当用户问"这段代码怎么工作？"时使用
allowed-tools:
  - Read
  - Grep
  - Glob
arguments: [path]
---

请解释 $path 的实现：先给一个类比，再画一个结构示意图。
```

**Skill加载器**:
```python
# skills/loader.py
class SkillLoader:
    SKILL_DIRS = [
        '~/.clawd/skills/',           # 用户级技能
        './.clawd/skills/',           # 项目级技能
    ]
    
    def load_skills(self) -> Dict[str, Skill]:
        skills = {}
        for dir_path in self.SKILL_DIRS:
            for skill_file in Path(dir_path).glob('*/SKILL.md'):
                skill = self._parse_skill(skill_file)
                skills[skill.name] = skill
        return skills
    
    def _parse_skill(self, file_path: Path) -> Skill:
        """解析SKILL.md文件"""
        content = file_path.read_text()
        
        # 解析YAML frontmatter
        frontmatter, body = self._split_frontmatter(content)
        config = yaml.safe_load(frontmatter)
        
        return Skill(
            name=file_path.parent.name,
            description=config['description'],
            allowed_tools=config.get('allowed-tools', []),
            arguments=config.get('arguments', []),
            template=body
        )
```

**应用到LNG系统**:
```markdown
# skills/lng-report/SKILL.md
---
description: 生成LNG市场分析报告
when_to_use: 当用户需要LNG价格数据或市场分析时
allowed-tools:
  - agent_原油
  - agent_海明
  - agent_润仓
  - agent_期货
  - agent_库存
arguments: [date, focus]
---

生成 $date 的LNG市场分析报告。

重点关注: $focus

执行步骤:
1. 调用相关助理采集数据
2. 验证数据准确性
3. 生成Markdown和HTML报告
4. 推送到GitHub Pages
```

---

### 5. REPL交互系统

**Slash命令**:

| 命令 | 功能 | 应用到LNG |
|------|------|-----------|
| `/` | 显示所有命令和技能 | 帮助系统 |
| `/help` | 显示帮助 | 帮助系统 |
| `/save` | 保存会话 | Boulder保存 |
| `/load <id>` | 加载会话 | Boulder恢复 |
| `/multiline` | 多行输入 | 复杂查询 |
| `/clear` | 清空历史 | 重置会话 |
| `/exit` | 退出REPL | 退出系统 |

**实现模式**:
```python
# repl/slash_commands.py
class SlashCommandRegistry:
    def __init__(self):
        self._commands: Dict[str, Callable] = {}
    
    def register(self, name: str, handler: Callable):
        self._commands[name] = handler
    
    def execute(self, command: str, args: list) -> str:
        handler = self._commands.get(command)
        if handler:
            return handler(*args)
        return f"Unknown command: {command}"

# 注册命令
registry = SlashCommandRegistry()
registry.register('/save', lambda: save_session())
registry.register('/load', lambda id: load_session(id))
```

---

## 📊 功能状态对比

### Clawd-Code vs LNG系统

| 功能 | Clawd-Code | LNG系统 | 差距 |
|------|-----------|---------|------|
| **多Provider** | ✅ Anthropic/OpenAI/GLM | ⚠️ Exa/Mysteel等 | 类似 |
| **工具系统** | ✅ 30+工具 | ✅ 12助理 | 相当 |
| **Agent Loop** | ✅ 完整实现 | ✅ 六阶段流程 | 相当 |
| **Skill系统** | ✅ SKILL.md | ✅ SKILL.md | 相当 |
| **会话持久化** | ✅ 保存/加载 | ✅ Boulder | 相当 |
| **REPL** | ✅ 交互式 | ❌ 无 | 可添加 |
| **权限系统** | 🟡 框架存在 | ✅ 4层验证 | LNG更优 |
| **成本跟踪** | 🚫 暂无 | ✅ UsageTracker | LNG更优 |
| **上下文构建** | 🟡 基础版 | ✅ 完整 | LNG更优 |

---

## 🚀 可应用技术

### 立即应用 (今晚)

1. **Skill系统优化**
   ```python
   # 优化SKILL.md解析
   class SkillLoader:
       def load(self, skill_path: str) -> Skill:
           # 支持变量替换
           # 支持条件执行
           # 支持工具限制
   ```

2. **工具注册表**
   ```python
   # 统一工具管理
   registry = ToolRegistry()
   registry.register_agent_tools(LNG_AGENTS)
   ```

3. **REPL命令**
   ```python
   # 添加交互式命令
   /save - 保存当前会话
   /status - 显示采集进度
   /cost - 显示API成本
   ```

### 短期应用 (本周)

4. **多Provider配置**
   ```json
   // ~/.lng-report/config.json
   {
     "data_sources": {
       "mysteel": {"api_key": "***", "priority": 1},
       "lng168": {"enabled": true, "timeout": 30}
     }
   }
   ```

5. **Agent Loop优化**
   ```python
   # 参考Clawd-Code的循环实现
   # 优化错误处理
   # 添加重试机制
   ```

6. **测试框架**
   ```python
   # 添加工具对等性测试
   # 添加Agent Loop测试
   ```

---

## 📚 参考资源

- [Clawd-Code GitHub](https://github.com/GPT-AGI/Clawd-Code)
- [FEATURE_LIST.md](https://github.com/GPT-AGI/Clawd-Code/blob/main/FEATURE_LIST.md)
- [SETUP_GUIDE.md](https://github.com/GPT-AGI/Clawd-Code/blob/main/docs/guide/SETUP_GUIDE.md)

---

*学习时间: 2026-04-05 20:53-21:00*  
*核心收获: Python Agent系统实现、30+工具、Agent Loop、Skill系统*  
*可应用技术: 6项*
