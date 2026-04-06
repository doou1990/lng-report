# LNG MCP Server 设计文档

**设计日期**: 2026-04-06  
**参考项目**: mcp-agent, claude-data-analysis, OpenClaw-Skill  
**版本**: v1.0

---

## 1. 架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                     LNG MCP Server                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Tools     │  │  Resources  │  │   Prompts   │         │
│  │  (工具)     │  │  (资源)     │  │  (提示模板)  │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         └─────────────────┼─────────────────┘               │
│                           ▼                                 │
│              ┌─────────────────────┐                        │
│              │   12 Assistant Core │                        │
│              │   (12助理核心)       │                        │
│              └─────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Prices  │  │  Reports │  │ History  │  │ Metadata │   │
│  │  价格数据 │  │  报告    │  │ 历史数据 │  │ 元数据   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 核心组件

| 组件 | 说明 | 对应MCP概念 |
|------|------|------------|
| **Tools** | 执行特定任务的函数 | MCP Tools |
| **Resources** | 可读取的数据资源 | MCP Resources |
| **Prompts** | 预定义的提示模板 | MCP Prompts |
| **12 Assistant Core** | 12助理并行采集核心 | 内部实现 |

---

## 2. Tools 设计

### 2.1 价格查询工具

```python
@mcp.tool()
def get_crude_oil_price(
    date: str = None,
    oil_type: Literal["brent", "wti", "both"] = "both"
) -> dict:
    """
    获取原油价格
    
    Args:
        date: 日期 (YYYY-MM-DD)，默认为今天
        oil_type: 原油类型 (brent/wti/both)
    
    Returns:
        {
            "date": "2026-04-06",
            "brent": {"price": 108.4, "unit": "USD/桶", "change": -0.55},
            "wti": {"price": 110.3, "unit": "USD/桶", "change": -1.15},
            "source": "OilPrice.com",
            "confidence": "A"
        }
    """
    pass

@mcp.tool()
def get_lng_price(
    date: str = None,
    benchmark: Literal["jkm", "ttf", "henry_hub", "all"] = "all"
) -> dict:
    """
    获取LNG价格
    
    Args:
        date: 日期 (YYYY-MM-DD)，默认为今天
        benchmark: 基准价格 (jkm/ttf/henry_hub/all)
    
    Returns:
        {
            "date": "2026-04-06",
            "jkm": {"price": 18.75, "unit": "USD/MMBtu"},
            "ttf": {"price": 54.24, "unit": "EUR/MWh"},
            "henry_hub": {"price": 3.05, "unit": "USD/MMBtu"},
            "source": "Global LNG Hub",
            "confidence": "A"
        }
    """
    pass

@mcp.tool()
def get_china_lng_price(
    date: str = None,
    region: Literal["north", "east", "south", "all"] = "all"
) -> dict:
    """
    获取中国LNG价格
    
    Args:
        date: 日期 (YYYY-MM-DD)，默认为今天
        region: 区域 (north/east/south/all)
    
    Returns:
        {
            "date": "2026-04-06",
            "factory_avg": 4813,  # 液厂均价
            "terminal_avg": 5824,  # 接收站均价
            "unit": "元/吨",
            "operating_rate": "47%",
            "sources": ["LNG物联网", "隆众资讯"],
            "confidence": "A"
        }
    """
    pass
```

### 2.2 报告生成工具

```python
@mcp.tool()
def generate_lng_report(
    date: str = None,
    report_type: Literal["daily", "weekly", "monthly"] = "daily",
    format: Literal["markdown", "html", "json"] = "markdown",
    sections: list = None
) -> dict:
    """
    生成LNG市场分析报告
    
    Args:
        date: 报告日期 (YYYY-MM-DD)，默认为今天
        report_type: 报告类型 (daily/weekly/monthly)
        format: 输出格式 (markdown/html/json)
        sections: 包含的章节列表，默认全部
    
    Returns:
        {
            "report_id": "lng-2026-04-06",
            "date": "2026-04-06",
            "format": "markdown",
            "content": "# LNG原油市场分析报告...",
            "file_path": "/reports/LNG/daily/2026-04-06.md",
            "data_completeness": "92%",
            "confidence": "A-",
            "generated_at": "2026-04-06T16:03:00Z"
        }
    """
    pass

@mcp.tool()
def generate_price_chart(
    data_type: Literal["crude", "lng", "china_lng"],
    start_date: str,
    end_date: str,
    chart_type: Literal["line", "bar", "candlestick"] = "line"
) -> dict:
    """
    生成价格走势图
    
    Args:
        data_type: 数据类型 (crude/lng/china_lng)
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        chart_type: 图表类型 (line/bar/candlestick)
    
    Returns:
        {
            "chart_id": "chart-001",
            "chart_type": "line",
            "data_points": 30,
            "image_url": "/charts/lng_price_2026-03-06_2026-04-06.png",
            "html_embed": "<div id='chart-001'>..."
        }
    """
    pass
```

### 2.3 自然语言查询工具

```python
@mcp.tool()
def natural_language_query(
    query: str,
    context: dict = None
) -> dict:
    """
    自然语言查询LNG数据
    
    Args:
        query: 自然语言查询，如"本周LNG价格趋势如何？"
        context: 上下文信息
    
    Returns:
        {
            "query": "本周LNG价格趋势如何？",
            "sql": "SELECT * FROM lng_prices WHERE date BETWEEN ...",
            "result": {...},
            "visualization": {...},
            "analysis": "本周LNG价格呈现上涨趋势..."
        }
    """
    pass
```

---

## 3. Resources 设计

### 3.1 价格资源

```python
@mcp.resource("lng://prices/{date}")
def get_prices_resource(date: str) -> str:
    """
    获取指定日期的所有价格数据
    URI: lng://prices/2026-04-06
    """
    pass

@mcp.resource("lng://prices/crude/latest")
def get_latest_crude_price() -> str:
    """
    获取最新原油价格
    URI: lng://prices/crude/latest
    """
    pass

@mcp.resource("lng://prices/china/{region}/{date}")
def get_china_regional_price(region: str, date: str) -> str:
    """
    获取中国区域价格
    URI: lng://prices/china/east/2026-04-06
    """
    pass
```

### 3.2 报告资源

```python
@mcp.resource("lng://reports/{type}/{date}")
def get_report_resource(type: str, date: str) -> str:
    """
    获取报告
    URI: lng://reports/daily/2026-04-06
    """
    pass

@mcp.resource("lng://reports/latest")
def get_latest_report() -> str:
    """
    获取最新报告
    URI: lng://reports/latest
    """
    pass
```

### 3.3 历史数据资源

```python
@mcp.resource("lng://history/prices/{data_type}/{start_date}/{end_date}")
def get_price_history(data_type: str, start_date: str, end_date: str) -> str:
    """
    获取历史价格数据
    URI: lng://history/prices/jkm/2026-01-01/2026-04-06
    """
    pass
```

---

## 4. Prompts 设计

### 4.1 分析报告提示

```python
@mcp.prompt()
def price_analysis_prompt(
    data_type: str,
    date_range: str
) -> str:
    """
    价格分析专家提示模板
    """
    return f"""
    你是一位专业的LNG市场分析师。请基于以下数据进行分析：
    
    数据类型: {data_type}
    时间范围: {date_range}
    
    请提供：
    1. 价格走势分析
    2. 关键驱动因素
    3. 与历史数据对比
    4. 未来趋势预测
    5. 风险提示
    
    请以专业、客观的角度进行分析。
    """

@mcp.prompt()
def market_summary_prompt(date: str) -> str:
    """
    市场总结提示模板
    """
    return f"""
    请生成{date}的LNG市场日报执行摘要：
    
    要求：
    - 3-5条核心结论
    - 每条结论配有关键数据支撑
    - 区分事实与判断
    - 突出重要变化
    """
```

### 4.2 自然语言查询提示

```python
@mcp.prompt()
def nl_to_sql_prompt(user_query: str) -> str:
    """
    自然语言转SQL提示模板
    """
    return f"""
    将用户的自然语言查询转换为SQL查询。
    
    用户查询: {user_query}
    
    可用表：
    - crude_prices (原油价格): date, brent_price, wti_price, source
    - lng_prices (LNG价格): date, jkm_price, ttf_price, henry_hub_price, source
    - china_lng_prices (中国LNG): date, region, factory_price, terminal_price, source
    - reports (报告): date, type, content, completeness
    
    请生成：
    1. SQL查询语句
    2. 查询意图解释
    3. 预期结果格式
    """
```

---

## 5. 实现代码

### 5.1 服务器主文件

```python
# lng_mcp_server.py

from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
import json

# 创建MCP服务器
mcp = FastMCP("LNG Market Analysis Server")

# ============ Tools ============

@mcp.tool()
def get_crude_oil_price(date: str = None, oil_type: str = "both") -> dict:
    """获取原油价格"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 调用原油助理(乾☰)采集数据
    # 这里简化实现，实际应调用12助理流程
    result = {
        "date": date,
        "brent": {"price": 108.4, "unit": "USD/桶", "change": -0.55},
        "wti": {"price": 110.3, "unit": "USD/桶", "change": -1.15},
        "source": "OilPrice.com",
        "confidence": "A",
        "collected_by": "助理1-原油(乾☰)"
    }
    
    if oil_type == "brent":
        return {k: v for k, v in result.items() if k in ["date", "brent", "source", "confidence"]}
    elif oil_type == "wti":
        return {k: v for k, v in result.items() if k in ["date", "wti", "source", "confidence"]}
    
    return result

@mcp.tool()
def get_lng_price(date: str = None, benchmark: str = "all") -> dict:
    """获取LNG价格"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 调用海明助理(坤☷)采集数据
    result = {
        "date": date,
        "jkm": {"price": 18.75, "unit": "USD/MMBtu", "change": -2.67},
        "ttf": {"price": 54.24, "unit": "EUR/MWh", "change": 0},
        "henry_hub": {"price": 3.05, "unit": "USD/MMBtu", "change": -0.67},
        "source": "Global LNG Hub",
        "confidence": "A",
        "collected_by": "助理2-海明(坤☷)"
    }
    
    if benchmark != "all":
        return {
            "date": date,
            benchmark: result[benchmark],
            "source": result["source"],
            "confidence": result["confidence"]
        }
    
    return result

@mcp.tool()
def get_china_lng_price(date: str = None, region: str = "all") -> dict:
    """获取中国LNG价格"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 调用润仓助理(巽☴)采集数据
    result = {
        "date": date,
        "factory_avg": 4813,
        "terminal_avg": 5824,
        "unit": "元/吨",
        "operating_rate": "47%",
        "total_factories": 133,
        "maintenance": 70,
        "region_data": {
            "north": {"factory": 5050, "terminal": 5300},
            "east": {"factory": 4900, "terminal": 5600},
            "south": {"factory": 4800, "terminal": 6400}
        },
        "sources": ["LNG物联网", "隆众资讯"],
        "confidence": "A",
        "collected_by": "助理4-润仓(巽☴)"
    }
    
    return result

@mcp.tool()
def generate_lng_report(
    date: str = None,
    report_type: str = "daily",
    format: str = "markdown"
) -> dict:
    """生成LNG市场分析报告"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 调用12助理并行采集
    # 实际实现应使用asyncio.gather并行调用
    
    report_id = f"lng-{date}"
    file_path = f"/reports/LNG/{report_type}/{date}.md"
    
    return {
        "report_id": report_id,
        "date": date,
        "type": report_type,
        "format": format,
        "file_path": file_path,
        "data_completeness": "92%",
        "confidence": "A-",
        "generated_at": datetime.now().isoformat(),
        "collected_by": "12助理协作系统",
        "web_url": f"https://lightai.cloud.tencent.com/drive/preview?filePath={report_id}/index.html"
    }

@mcp.tool()
def natural_language_query(query: str, context: dict = None) -> dict:
    """自然语言查询LNG数据"""
    
    # 1. 解析查询意图
    # 2. 生成SQL
    # 3. 执行查询
    # 4. 生成可视化
    # 5. 输出分析
    
    return {
        "query": query,
        "intent": "price_trend_analysis",
        "sql": "SELECT * FROM lng_prices WHERE date BETWEEN ...",
        "result": {"rows": 30, "data": [...]},
        "visualization": {
            "type": "line_chart",
            "title": "LNG价格趋势",
            "data": [...]
        },
        "analysis": "根据查询结果，本周LNG价格呈现上涨趋势...",
        "confidence": "A"
    }

# ============ Resources ============

@mcp.resource("lng://prices/{date}")
def get_prices_resource(date: str) -> str:
    """获取指定日期的所有价格数据"""
    data = {
        "crude": get_crude_oil_price(date),
        "lng": get_lng_price(date),
        "china": get_china_lng_price(date)
    }
    return json.dumps(data, indent=2, ensure_ascii=False)

@mcp.resource("lng://reports/latest")
def get_latest_report() -> str:
    """获取最新报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    report = generate_lng_report(today)
    return json.dumps(report, indent=2, ensure_ascii=False)

# ============ Prompts ============

@mcp.prompt()
def price_analysis_prompt(data_type: str = "LNG", date_range: str = "本周") -> str:
    """价格分析专家提示"""
    return f"""
    你是一位专业的{data_type}市场分析师。请基于{date_range}的数据进行分析：
    
    请提供：
    1. 价格走势分析
    2. 关键驱动因素
    3. 与历史数据对比
    4. 未来趋势预测
    5. 风险提示
    """

# ============ Main ============

if __name__ == "__main__":
    # 启动MCP服务器
    mcp.run(transport='stdio')
```

---

## 6. 客户端使用示例

### 6.1 Python客户端

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置服务器参数
server_params = StdioServerParameters(
    command="python",
    args=["lng_mcp_server.py"]
)

async def use_lng_mcp():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()
            
            # 获取原油价格
            crude_price = await session.call_tool(
                "get_crude_oil_price",
                {"date": "2026-04-06", "oil_type": "both"}
            )
            print(f"原油价格: {crude_price}")
            
            # 生成报告
            report = await session.call_tool(
                "generate_lng_report",
                {"date": "2026-04-06", "format": "html"}
            )
            print(f"报告已生成: {report['web_url']}")
            
            # 自然语言查询
            result = await session.call_tool(
                "natural_language_query",
                {"query": "本周LNG价格趋势如何？"}
            )
            print(f"查询结果: {result['analysis']}")
            
            # 读取资源
            prices = await session.read_resource("lng://prices/2026-04-06")
            print(f"价格数据: {prices}")
```

### 6.2 Claude Code集成

```json
// .claude/mcp.json
{
  "mcpServers": {
    "lng-market": {
      "command": "python",
      "args": ["/path/to/lng_mcp_server.py"],
      "env": {
        "LNG_DATA_PATH": "/data/lng"
      }
    }
  }
}
```

使用方式：
```
Claude: 帮我查询今天的LNG价格
→ 自动调用 lng-market.get_lng_price()

Claude: 生成本周的LNG市场报告
→ 自动调用 lng-market.generate_lng_report()

Claude: 比较本周和上周的原油价格
→ 自动调用 lng-market.natural_language_query()
```

---

## 7. 部署配置

### 7.1 Docker部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY lng_mcp_server.py .
COPY skills/ ./skills/

EXPOSE 8000

CMD ["python", "lng_mcp_server.py"]
```

### 7.2 环境变量

```bash
# .env
LNG_DATA_PATH=/data/lng
LNG_REPORT_PATH=/reports/lng
MCP_LOG_LEVEL=INFO
ENABLE_12_ASSISTANTS=true
DEFAULT_TIMEOUT=180
```

---

## 8. 下一步计划

| 阶段 | 任务 | 时间 |
|------|------|------|
| 1 | 实现基础Tools (价格查询) | 本周 |
| 2 | 集成12助理核心 | 下周 |
| 3 | 实现自然语言查询 | 下周 |
| 4 | 添加可视化功能 | 第3周 |
| 5 | 部署测试 | 第4周 |

---

*设计完成时间: 2026-04-06 19:00*
