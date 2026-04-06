# ClawPanel AI助手系统深度分析

**学习时间**: 2026-04-05 21:05-21:15  
**学习来源**: qingchencloud/clawpanel (基于README文档分析)  
**核心目标**: 深入分析AI助手架构，提炼可应用技术

---

## 🎯 系统概述

ClawPanel的AI助手是一个**功能完整的AI Agent系统**，特点：
- ✅ **4种操作模式** - 适应不同安全级别需求
- ✅ **8大内置工具** - 直接操作系统
- ✅ **交互式问答** - 支持单选/多选/文本输入
- ✅ **多模态支持** - 图片识别和分析
- ✅ **人机协作** - AI提问，用户回答后继续

---

## 🏗️ 架构设计

### 1. 四层架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户界面层 (UI)                          │
│  - 模式切换按钮 (聊天/规划/执行/无限)                          │
│  - 工具开关面板                                              │
│  - 对话历史显示                                              │
│  - 图片上传/粘贴                                             │
├─────────────────────────────────────────────────────────────┤
│                      模式控制层 (Mode)                        │
│  - 权限检查器                                                │
│  - 工具过滤器                                                │
│  - 确认对话框管理                                            │
├─────────────────────────────────────────────────────────────┤
│                      工具执行层 (Tools)                       │
│  - 8大工具实现                                               │
│  - 结果格式化                                                │
│  - 错误处理                                                  │
├─────────────────────────────────────────────────────────────┤
│                      系统接口层 (System)                      │
│  - Shell命令执行                                             │
│  - 文件系统操作                                              │
│  - 进程管理                                                  │
│  - 端口检测                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 4种操作模式详解

### 模式1: 聊天模式 (Chat) 💬

**权限配置**:
```javascript
const CHAT_MODE = {
  tools: [],              // 无工具权限
  writeFile: false,       // 禁止写文件
  confirmation: false,    // 无需确认
  color: 'blue',          // UI颜色
  description: '纯问答，不触碰系统'
}
```

**应用场景**:
- 一般性咨询
- 概念解释
- 使用指导

**应用到LNG**:
```python
class LNGChatMode:
    """LNG聊天模式 - 仅回答，不采集数据"""
    def __init__(self):
        self.tools = []
        self.can_collect = False
    
    def handle(self, query: str) -> str:
        # 仅使用已有知识回答
        return self.knowledge_base.answer(query)
```

---

### 模式2: 规划模式 (Plan) 📋

**权限配置**:
```javascript
const PLAN_MODE = {
  tools: ['read_file', 'list_directory', 'get_system_info'],
  writeFile: false,
  confirmation: true,     // 需要用户确认
  color: 'yellow',
  description: '读配置/查日志，输出方案不动文件'
}
```

**应用场景**:
- 系统诊断
- 配置分析
- 方案制定

**应用到LNG**:
```python
class LNGPlanMode:
    """LNG规划模式 - 分析需求，制定采集计划"""
    def __init__(self):
        self.tools = ['read_file', 'list_directory']
        self.can_collect = False
        self.needs_confirmation = True
    
    def handle(self, query: str) -> Plan:
        # 1. 分析用户需求
        intent = self.parse_intent(query)
        
        # 2. 检查已有数据
        existing = self.check_existing_data(intent.date)
        
        # 3. 制定采集计划
        plan = self.create_collection_plan(intent, existing)
        
        # 4. 请求用户确认
        if self.confirm(plan):
            return plan
        else:
            return self.revise_plan(plan)
```

---

### 模式3: 执行模式 (Execute) ⚡

**权限配置**:
```javascript
const EXECUTE_MODE = {
  tools: ['read_file', 'write_file', 'run_command', 'list_directory', 
          'get_system_info', 'list_processes', 'check_port', 'ask_user'],
  writeFile: true,        // 允许写文件
  confirmation: true,     // 危险操作需确认
  color: 'green',
  description: '正常干活，危险操作弹确认'
}
```

**危险操作定义**:
```javascript
const DANGEROUS_OPERATIONS = [
  { pattern: /rm\s+-rf/, description: '强制删除' },
  { pattern: /npm\s+uninstall\s+-g/, description: '全局卸载' },
  { pattern: /drop\s+table/i, description: '删除数据表' },
  { pattern: /delete\s+from/i, description: '删除数据' }
]

function isDangerous(command) {
  return DANGEROUS_OPERATIONS.some(op => op.pattern.test(command))
}
```

**应用到LNG**:
```python
class LNGExecuteMode:
    """LNG执行模式 - 正常采集数据"""
    
    DANGEROUS_OPERATIONS = [
        {'pattern': r'github.*delete', 'desc': '删除GitHub资源'},
        {'pattern': r'rm\s+-rf', 'desc': '强制删除文件'},
    ]
    
    def __init__(self):
        self.tools = ['web_search', 'web_fetch', 'write_file', 'bash']
        self.can_collect = True
        self.needs_confirmation = True
    
    def execute_tool(self, tool: str, args: dict) -> Result:
        # 检查是否为危险操作
        if self.is_dangerous(tool, args):
            if not self.confirm(f"执行危险操作: {args}"):
                return Result.cancelled()
        
        return self.tools[tool].execute(args)
```

---

### 模式4: 无限模式 (Unlimited) ∞

**权限配置**:
```javascript
const UNLIMITED_MODE = {
  tools: ['all'],
  writeFile: true,
  confirmation: false,    // 无需确认
  color: 'red',
  description: '全自动，工具调用不弹窗'
}
```

**应用场景**:
- 自动化脚本
- 定时任务
- 已知安全的批量操作

**应用到LNG**:
```python
class LNGUnlimitedMode:
    """LNG无限模式 - 全自动报告生成"""
    def __init__(self):
        self.tools = ['all']
        self.can_collect = True
        self.needs_confirmation = False
        self.auto_execute = True
    
    def generate_report_auto(self, date: str) -> Report:
        # 全自动流程，无需人工干预
        # 1. 解析意图
        # 2. 并行采集
        # 3. 自动验证
        # 4. 生成报告
        # 5. 推送部署
        return self.full_pipeline(date)
```

---

## 🛠️ 8大工具详解

### 工具1: ask_user (用户交互)

**功能**: 向用户提问，获取输入

**交互类型**:
```javascript
const QUESTION_TYPES = {
  SINGLE_CHOICE: {
    type: 'single',
    options: ['选项A', '选项B', '选项C'],
    allowCustom: true  // 允许输入自定义答案
  },
  MULTI_CHOICE: {
    type: 'multi',
    options: ['组件1', '组件2', '组件3']
  },
  TEXT: {
    type: 'text',
    placeholder: '请输入描述...'
  }
}
```

**应用到LNG**:
```python
class AskUserTool:
    """LNG用户交互工具"""
    
    def ask_data_source(self) -> str:
        """询问数据来源优先级"""
        return self.ask_single_choice(
            question="请选择数据优先级",
            options=["Mysteel优先", "隆众优先", "混合平均"],
            allow_custom=True
        )
    
    def ask_focus_region(self) -> List[str]:
        """询问关注区域"""
        return self.ask_multi_choice(
            question="请选择需要重点关注的区域",
            options=["浙江", "广东", "江苏", "山东", "全国"]
        )
```

---

### 工具2: get_system_info (系统信息)

**功能**: 获取操作系统、架构、主目录等信息

**返回数据**:
```json
{
  "os": "Linux",
  "arch": "x64",
  "home": "/root",
  "shell": "bash",
  "node_version": "22.2.0",
  "workspace": "/root/.openclaw/workspace"
}
```

**应用到LNG**:
```python
class SystemInfoTool:
    """LNG系统信息工具"""
    
    def get_report_env(self) -> dict:
        return {
            'workspace': os.getcwd(),
            'memory_dir': 'memory/reports/LNG',
            'github_repo': 'doou1990/lng-report',
            'available_agents': 12,
            'data_sources': ['exa', 'mysteel', 'lng168']
        }
```

---

### 工具3: run_command (命令执行)

**功能**: 执行Shell命令

**安全处理**:
```javascript
function runCommand(command, timeout = 30000) {
  // 1. 命令白名单检查
  if (!isAllowed(command)) {
    throw new Error('命令不在白名单中')
  }
  
  // 2. 超时设置
  const options = { timeout }
  
  // 3. 执行并捕获输出
  const result = execSync(command, options)
  
  return {
    stdout: result.toString(),
    stderr: '',
    exitCode: 0
  }
}
```

**应用到LNG**:
```python
class RunCommandTool:
    """LNG命令执行工具"""
    
    ALLOWED_COMMANDS = [
        'git', 'npm', 'python', 'pip',
        'curl', 'wget', 'cat', 'ls'
    ]
    
    def execute(self, command: str, timeout: int = 30) -> Result:
        # 安全检查
        if not self.is_allowed(command):
            return Result.error('命令不在白名单中')
        
        # 执行命令
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True,
            timeout=timeout
        )
        
        return Result(
            stdout=result.stdout.decode(),
            stderr=result.stderr.decode(),
            exit_code=result.returncode
        )
```

---

### 工具4: read_file (文件读取)

**功能**: 读取文件内容

**应用到LNG**:
```python
class ReadFileTool:
    """LNG文件读取工具"""
    
    def read_historical_data(self, date: str) -> dict:
        """读取历史数据用于对比"""
        path = f"memory/reports/LNG/daily_estimates/{date}/market_data.json"
        with open(path, 'r') as f:
            return json.load(f)
```

---

### 工具5: write_file (文件写入)

**功能**: 写入文件内容

**应用到LNG**:
```python
class WriteFileTool:
    """LNG文件写入工具"""
    
    def save_report(self, date: str, content: str, format: str):
        """保存报告文件"""
        path = f"memory/reports/LNG/daily_estimates/{date}/"
        os.makedirs(path, exist_ok=True)
        
        if format == 'markdown':
            filename = f"LNG报告_{date}.md"
        elif format == 'html':
            filename = f"LNG报告_{date}.html"
        
        with open(path + filename, 'w') as f:
            f.write(content)
```

---

### 工具6: list_directory (目录浏览)

**功能**: 列出目录内容

**应用到LNG**:
```python
class ListDirectoryTool:
    """LNG目录浏览工具"""
    
    def list_historical_reports(self) -> List[str]:
        """列出历史报告"""
        base_path = "memory/reports/LNG/daily_estimates/"
        return sorted(os.listdir(base_path), reverse=True)
```

---

### 工具7: list_processes (进程查看)

**功能**: 查看运行中的进程

**应用到LNG**:
```python
class ListProcessesTool:
    """LNG进程查看工具"""
    
    def check_agent_status(self) -> dict:
        """检查各助理运行状态"""
        # 检查是否有正在运行的采集任务
        processes = psutil.process_iter(['pid', 'name', 'cmdline'])
        
        active_agents = []
        for proc in processes:
            if 'lng-agent' in proc.info['name']:
                active_agents.append(proc.info)
        
        return {
            'active_agents': len(active_agents),
            'processes': active_agents
        }
```

---

### 工具8: check_port (端口检测)

**功能**: 检测端口占用情况

**应用到LNG**:
```python
class CheckPortTool:
    """LNG端口检测工具"""
    
    def check_gateway_status(self) -> bool:
        """检查Gateway是否运行"""
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 18789))
        sock.close()
        return result == 0
```

---

## 💡 人机协作流程

### 典型交互流程

```
用户: "帮我检查LNG报告系统"
  ↓
AI: [调用 get_system_info] 获取系统信息
  ↓
AI: [调用 list_directory] 查看报告目录
  ↓
AI: [调用 ask_user - SINGLE_CHOICE] 
    "发现以下问题，请选择要修复的：
    1. 昨日报告缺失
    2. 数据完整性低于90%
    3. 取消"
  ↓
用户: 选择 "1. 昨日报告缺失"
  ↓
AI: [调用 run_command] 执行补采脚本
  ↓
AI: "已启动补采任务，预计5分钟完成"
```

---

## 🎨 UI设计亮点

### 1. 模式颜色编码

| 模式 | 颜色 | 心理暗示 |
|------|------|----------|
| 聊天 | 蓝色 | 安全、平静 |
| 规划 | 黄色 | 警告、注意 |
| 执行 | 绿色 | 正常、可执行 |
| 无限 | 红色 | 危险、全自动 |

### 2. 工具开关面板

```
┌─────────────────────────────┐
│  工具权限                    │
├─────────────────────────────┤
│  ☑ 终端命令    ☑ 文件读取   │
│  ☑ 文件写入    ☐ 系统信息   │
│  ☑ 目录浏览    ☐ 进程查看   │
│  ☐ 端口检测                  │
└─────────────────────────────┘
```

### 3. 对话界面

```
┌─────────────────────────────┐
│  💬 聊天模式                  │
├─────────────────────────────┤
│  🤖 检查完成，发现2个问题：   │
│     1. 原油价格数据缺失       │
│     2. 浙江接收站数据异常     │
│                             │
│  请选择要修复的问题：         │
│  [1] 修复原油价格            │
│  [2] 修复浙江数据            │
│  [3] 全部修复                │
│  [4] 跳过                    │
│                             │
│  [输入自定义...]             │
└─────────────────────────────┘
```

---

## 🚀 应用到LNG系统

### 立即实施

1. **模式切换功能**
   ```python
   class LNGModeController:
       MODES = {
           'chat': LNGChatMode(),
           'plan': LNGPlanMode(),
           'execute': LNGExecuteMode(),
           'unlimited': LNGUnlimitedMode()
       }
       
       def switch_mode(self, mode_name: str):
           self.current_mode = self.MODES[mode_name]
   ```

2. **工具权限控制**
   ```python
   class LNGToolController:
       def __init__(self):
           self.tool_switches = {
               'web_search': True,
               'web_fetch': True,
               'write_file': False,  # 默认关闭
               'bash': False
           }
   ```

3. **人机交互优化**
   ```python
   def ask_user(question: str, options: List[str], allow_custom: bool = False):
       """向用户提问并获取回答"""
       # 实现交互式问答
   ```

### 短期实施

4. **图片识别集成**
   - 支持用户上传价格截图
   - AI自动识别并提取数据
   - 用于验证和补充

5. **系统诊断技能**
   - 一键检查数据完整性
   - 自动发现异常
   - 提供修复建议

---

## 📊 总结

| 特性 | ClawPanel | LNG应用 |
|------|-----------|---------|
| 4种模式 | ✅ | 立即实施 |
| 8大工具 | ✅ | 工具库扩展 |
| 人机协作 | ✅ | 交互优化 |
| 颜色编码 | ✅ | UI设计参考 |
| 权限控制 | ✅ | 安全增强 |

---

*学习时间: 2026-04-05 21:05-21:15*  
*核心收获: 4种操作模式、8大工具、人机协作流程*  
*可应用: 5项*
