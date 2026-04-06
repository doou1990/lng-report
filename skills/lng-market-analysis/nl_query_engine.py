# 自然语言查询功能原型

**实现日期**: 2026-04-06  
**参考项目**: claude-data-analysis, mcp-agent  
**版本**: v1.0

---

## 1. 核心架构

```
用户自然语言查询
       ↓
┌─────────────────┐
│  意图识别模块   │  ← 解析用户想做什么
└────────┬────────┘
         ↓
┌─────────────────┐
│  SQL生成模块    │  ← 将意图转为SQL
└────────┬────────┘
         ↓
┌─────────────────┐
│  数据查询模块   │  ← 执行SQL获取数据
└────────┬────────┘
         ↓
┌─────────────────┐
│  可视化模块     │  ← 自动选择图表类型
└────────┬────────┘
         ↓
┌─────────────────┐
│  分析生成模块   │  ← 生成文字分析
└─────────────────┘
         ↓
    完整结果返回
```

---

## 2. 实现代码

```python
# nl_query_engine.py

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Literal
import sqlite3
from dataclasses import dataclass

@dataclass
class QueryIntent:
    """查询意图"""
    action: str  # query, compare, trend, predict
    data_type: str  # crude, lng, china_lng
    metric: str  # price, volume, inventory
    time_range: Dict[str, str]  # {start: "2026-04-01", end: "2026-04-06"}
    filters: Dict[str, any]  # {region: "east", benchmark: "jkm"}
    aggregation: Optional[str]  # avg, sum, max, min

@dataclass
class QueryResult:
    """查询结果"""
    query: str
    intent: QueryIntent
    sql: str
    data: List[Dict]
    visualization: Dict
    analysis: str
    confidence: str

class NLQueryEngine:
    """自然语言查询引擎"""
    
    def __init__(self, db_path: str = "lng_data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
    # ============ 1. 意图识别 ============
    
    def parse_intent(self, user_query: str) -> QueryIntent:
        """
        解析用户查询意图
        
        示例:
        - "本周LNG价格趋势" → action: trend, data_type: lng, time_range: this_week
        - "比较Brent和WTI价格" → action: compare, data_type: crude
        - "华东地区LNG价格" → action: query, data_type: china_lng, filters: {region: east}
        """
        query = user_query.lower()
        
        # 识别action
        if any(word in query for word in ["趋势", "走势", "变化", "trend"]):
            action = "trend"
        elif any(word in query for word in ["比较", "对比", "vs", "compare"]):
            action = "compare"
        elif any(word in query for word in ["预测", "forecast", "predict"]):
            action = "predict"
        else:
            action = "query"
        
        # 识别data_type
        if any(word in query for word in ["原油", "crude", "brent", "wti", "石油"]):
            data_type = "crude"
        elif any(word in query for word in ["中国", "国内", "china", "液厂", "接收站"]):
            data_type = "china_lng"
        else:
            data_type = "lng"
        
        # 识别metric
        if any(word in query for word in ["库存", "inventory", "storage"]):
            metric = "inventory"
        elif any(word in query for word in ["进口", "import", "贸易"]):
            metric = "volume"
        else:
            metric = "price"
        
        # 识别time_range
        time_range = self._parse_time_range(query)
        
        # 识别filters
        filters = self._parse_filters(query, data_type)
        
        # 识别aggregation
        aggregation = self._parse_aggregation(query)
        
        return QueryIntent(
            action=action,
            data_type=data_type,
            metric=metric,
            time_range=time_range,
            filters=filters,
            aggregation=aggregation
        )
    
    def _parse_time_range(self, query: str) -> Dict[str, str]:
        """解析时间范围"""
        today = datetime.now()
        
        # 本周
        if any(word in query for word in ["本周", "这周", "this week"]):
            start = today - timedelta(days=today.weekday())
            end = today
            return {"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")}
        
        # 本月
        if any(word in query for word in ["本月", "这个月", "this month"]):
            start = today.replace(day=1)
            end = today
            return {"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")}
        
        # 今年
        if any(word in query for word in ["今年", "this year", "2026"]):
            return {"start": "2026-01-01", "end": today.strftime("%Y-%m-%d")}
        
        # 最近7天/30天
        if "7天" in query or "一周" in query:
            start = today - timedelta(days=7)
            return {"start": start.strftime("%Y-%m-%d"), "end": today.strftime("%Y-%m-%d")}
        
        if "30天" in query or "一个月" in query:
            start = today - timedelta(days=30)
            return {"start": start.strftime("%Y-%m-%d"), "end": today.strftime("%Y-%m-%d")}
        
        # 默认今天
        return {"start": today.strftime("%Y-%m-%d"), "end": today.strftime("%Y-%m-%d")}
    
    def _parse_filters(self, query: str, data_type: str) -> Dict[str, any]:
        """解析过滤条件"""
        filters = {}
        
        # 区域过滤
        if data_type == "china_lng":
            if any(word in query for word in ["华东", "东部", "east"]):
                filters["region"] = "east"
            elif any(word in query for word in ["华北", "北部", "north"]):
                filters["region"] = "north"
            elif any(word in query for word in ["华南", "南部", "south"]):
                filters["region"] = "south"
        
        # 基准价格过滤
        if data_type == "lng":
            if any(word in query for word in ["jkm", "亚洲", "日韩"]):
                filters["benchmark"] = "jkm"
            elif any(word in query for word in ["ttf", "欧洲", "荷兰"]):
                filters["benchmark"] = "ttf"
            elif any(word in query for word in ["henry hub", "美国", "hh"]):
                filters["benchmark"] = "henry_hub"
        
        # 原油类型过滤
        if data_type == "crude":
            if "brent" in query:
                filters["oil_type"] = "brent"
            elif "wti" in query:
                filters["oil_type"] = "wti"
        
        return filters
    
    def _parse_aggregation(self, query: str) -> Optional[str]:
        """解析聚合方式"""
        if any(word in query for word in ["平均", "均值", "avg", "average"]):
            return "avg"
        elif any(word in query for word in ["最高", "最大", "max", "maximum"]):
            return "max"
        elif any(word in query for word in ["最低", "最小", "min", "minimum"]):
            return "min"
        elif any(word in query for word in ["总和", "总计", "sum", "total"]):
            return "sum"
        return None
    
    # ============ 2. SQL生成 ============
    
    def generate_sql(self, intent: QueryIntent) -> str:
        """根据意图生成SQL"""
        
        # 选择表
        table_map = {
            "crude": "crude_prices",
            "lng": "lng_prices",
            "china_lng": "china_lng_prices"
        }
        table = table_map.get(intent.data_type, "lng_prices")
        
        # 选择字段
        if intent.data_type == "crude":
            fields = ["date", "brent_price", "wti_price", "source"]
        elif intent.data_type == "lng":
            fields = ["date", "jkm_price", "ttf_price", "henry_hub_price", "source"]
        else:  # china_lng
            fields = ["date", "region", "factory_price", "terminal_price", "source"]
        
        # 构建WHERE条件
        conditions = [f"date BETWEEN '{intent.time_range['start']}' AND '{intent.time_range['end']}'"]
        
        for key, value in intent.filters.items():
            if key == "region":
                conditions.append(f"region = '{value}'")
            elif key == "benchmark":
                # 对于LNG，选择特定基准
                pass
            elif key == "oil_type":
                # 对于原油，选择特定类型
                pass
        
        where_clause = " AND ".join(conditions)
        
        # 构建聚合
        if intent.aggregation:
            agg_fields = []
            for field in fields:
                if field not in ["date", "region", "source"]:
                    agg_fields.append(f"{intent.aggregation}({field}) as {field}")
            fields = ["date"] + agg_fields
        
        # 构建ORDER BY
        order_by = "date ASC"
        
        # 组装SQL
        sql = f"""
        SELECT {', '.join(fields)}
        FROM {table}
        WHERE {where_clause}
        ORDER BY {order_by}
        """.strip()
        
        return sql
    
    # ============ 3. 数据查询 ============
    
    def execute_query(self, sql: str) -> List[Dict]:
        """执行SQL查询"""
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        # 转换为字典列表
        result = []
        for row in rows:
            result.append({key: row[key] for key in row.keys()})
        
        return result
    
    # ============ 4. 可视化生成 ============
    
    def generate_visualization(self, data: List[Dict], intent: QueryIntent) -> Dict:
        """
        根据数据特征自动生成可视化
        
        规则:
        - 时间序列数据 → 折线图
        - 对比数据 → 柱状图
        - 分布数据 → 饼图/环形图
        """
        if not data:
            return {"type": "none", "reason": "no_data"}
        
        # 判断数据类型
        has_date = "date" in data[0]
        has_multiple_series = len(data[0]) > 3  # date + 2+ price fields
        
        # 选择图表类型
        if intent.action == "trend" or (has_date and len(data) > 5):
            chart_type = "line"
            title = f"{intent.data_type.upper()}价格趋势"
        elif intent.action == "compare" or has_multiple_series:
            chart_type = "bar"
            title = f"{intent.data_type.upper()}价格对比"
        else:
            chart_type = "table"
            title = f"{intent.data_type.upper()}价格数据"
        
        # 生成ECharts配置
        if chart_type == "line":
            option = self._generate_line_chart(data, intent)
        elif chart_type == "bar":
            option = self._generate_bar_chart(data, intent)
        else:
            option = None
        
        return {
            "type": chart_type,
            "title": title,
            "data_points": len(data),
            "echarts_option": option,
            "recommendation": self._get_chart_recommendation(intent, chart_type)
        }
    
    def _generate_line_chart(self, data: List[Dict], intent: QueryIntent) -> Dict:
        """生成折线图配置"""
        dates = [row["date"] for row in data]
        
        series = []
        if intent.data_type == "crude":
            series = [
                {
                    "name": "Brent",
                    "type": "line",
                    "data": [row.get("brent_price") for row in data],
                    "smooth": True
                },
                {
                    "name": "WTI",
                    "type": "line",
                    "data": [row.get("wti_price") for row in data],
                    "smooth": True
                }
            ]
        elif intent.data_type == "lng":
            series = [
                {
                    "name": "JKM",
                    "type": "line",
                    "data": [row.get("jkm_price") for row in data],
                    "smooth": True
                },
                {
                    "name": "TTF",
                    "type": "line",
                    "data": [row.get("ttf_price") for row in data],
                    "smooth": True
                },
                {
                    "name": "Henry Hub",
                    "type": "line",
                    "data": [row.get("henry_hub_price") for row in data],
                    "smooth": True
                }
            ]
        
        return {
            "xAxis": {"type": "category", "data": dates},
            "yAxis": {"type": "value", "name": "价格"},
            "series": series,
            "tooltip": {"trigger": "axis"},
            "legend": {"bottom": 0}
        }
    
    def _generate_bar_chart(self, data: List[Dict], intent: QueryIntent) -> Dict:
        """生成柱状图配置"""
        # 简化实现
        return {
            "xAxis": {"type": "category", "data": [row["date"] for row in data]},
            "yAxis": {"type": "value"},
            "series": [{"type": "bar", "data": [row.get("price") for row in data]}]
        }
    
    def _get_chart_recommendation(self, intent: QueryIntent, chart_type: str) -> str:
        """获取图表推荐说明"""
        recommendations = {
            "line": "折线图适合展示时间序列数据的趋势变化",
            "bar": "柱状图适合对比不同类别或时间点的数据",
            "pie": "饼图适合展示数据的占比分布",
            "table": "表格适合展示详细的原始数据"
        }
        return recommendations.get(chart_type, "")
    
    # ============ 5. 分析生成 ============
    
    def generate_analysis(self, data: List[Dict], intent: QueryIntent) -> str:
        """
        基于数据生成文字分析
        
        使用模板 + 数据填充的方式
        """
        if not data:
            return "暂无数据可供分析。"
        
        # 计算基础统计
        analysis_parts = []
        
        # 1. 数据概览
        analysis_parts.append(f"查询期间共获取{len(data)}条数据记录。")
        
        # 2. 价格变化
        if len(data) >= 2:
            first = data[0]
            last = data[-1]
            
            if intent.data_type == "crude":
                brent_change = last.get("brent_price", 0) - first.get("brent_price", 0)
                wti_change = last.get("wti_price", 0) - first.get("wti_price", 0)
                
                analysis_parts.append(
                    f"Brent原油价格从{first.get('brent_price')}美元/桶"
                    f"变化至{last.get('brent_price')}美元/桶，"
                    f"{'上涨' if brent_change > 0 else '下跌'}了{abs(brent_change):.2f}美元。"
                )
                
                analysis_parts.append(
                    f"WTI原油价格从{first.get('wti_price')}美元/桶"
                    f"变化至{last.get('wti_price')}美元/桶，"
                    f"{'上涨' if wti_change > 0 else '下跌'}了{abs(wti_change):.2f}美元。"
                )
            
            elif intent.data_type == "lng":
                jkm_change = last.get("jkm_price", 0) - first.get("jkm_price", 0)
                analysis_parts.append(
                    f"JKM价格从{first.get('jkm_price')}美元/MMBtu"
                    f"变化至{last.get('jkm_price')}美元/MMBtu，"
                    f"{'上涨' if jkm_change > 0 else '下跌'}了{abs(jkm_change):.2f}美元。"
                )
        
        # 3. 趋势判断
        if intent.action == "trend":
            analysis_parts.append("整体呈现" + self._judge_trend(data, intent) + "趋势。")
        
        # 4. 关键观察
        analysis_parts.append(self._generate_key_observation(data, intent))
        
        return "\n\n".join(analysis_parts)
    
    def _judge_trend(self, data: List[Dict], intent: QueryIntent) -> str:
        """判断趋势"""
        if len(data) < 2:
            return "平稳"
        
        # 简化：比较首尾
        first = data[0]
        last = data[-1]
        
        # 获取价格字段
        price_field = None
        if intent.data_type == "crude":
            price_field = "brent_price"
        elif intent.data_type == "lng":
            price_field = "jkm_price"
        elif intent.data_type == "china_lng":
            price_field = "factory_price"
        
        if price_field:
            change = last.get(price_field, 0) - first.get(price_field, 0)
            if change > 0:
                return "上涨"
            elif change < 0:
                return "下跌"
        
        return "平稳"
    
    def _generate_key_observation(self, data: List[Dict], intent: QueryIntent) -> str:
        """生成关键观察"""
        observations = []
        
        # 找最高/最低
        if intent.data_type == "crude":
            prices = [row.get("brent_price", 0) for row in data if row.get("brent_price")]
            if prices:
                max_price = max(prices)
                min_price = min(prices)
                observations.append(f"期间最高价格为{max_price}美元/桶，最低为{min_price}美元/桶。")
        
        # 添加一般性观察
        observations.append("建议关注地缘政治风险和供需变化对价格的影响。")
        
        return " ".join(observations)
    
    # ============ 主入口 ============
    
    def query(self, user_query: str) -> QueryResult:
        """
        主查询入口
        
        完整流程：意图识别 → SQL生成 → 数据查询 → 可视化 → 分析生成
        """
        # 1. 意图识别
        intent = self.parse_intent(user_query)
        
        # 2. SQL生成
        sql = self.generate_sql(intent)
        
        # 3. 数据查询
        data = self.execute_query(sql)
        
        # 4. 可视化生成
        visualization = self.generate_visualization(data, intent)
        
        # 5. 分析生成
        analysis = self.generate_analysis(data, intent)
        
        return QueryResult(
            query=user_query,
            intent=intent,
            sql=sql,
            data=data,
            visualization=visualization,
            analysis=analysis,
            confidence="A" if len(data) > 0 else "C"
        )


# ============ 使用示例 ============

if __name__ == "__main__":
    # 初始化引擎
    engine = NLQueryEngine()
    
    # 测试查询
    test_queries = [
        "本周LNG价格趋势如何？",
        "比较Brent和WTI原油价格",
        "华东地区LNG价格",
        "最近7天JKM价格变化",
        "本月中国LNG市场概况"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"用户查询: {query}")
        print(f"{'='*60}")
        
        result = engine.query(query)
        
        print(f"\n意图识别:")
        print(f"  Action: {result.intent.action}")
        print(f"  Data Type: {result.intent.data_type}")
        print(f"  Time Range: {result.intent.time_range}")
        print(f"  Filters: {result.intent.filters}")
        
        print(f"\n生成SQL:")
        print(f"  {result.sql}")
        
        print(f"\n查询结果:")
        print(f"  数据条数: {len(result.data)}")
        print(f"  置信度: {result.confidence}")
        
        print(f"\n可视化:")
        print(f"  类型: {result.visualization['type']}")
        print(f"  标题: {result.visualization['title']}")
        
        print(f"\n分析结论:")
        print(f"  {result.analysis}")
```

---

## 3. 集成到LNG MCP Server

```python
# 在 lng_mcp_server.py 中添加

@mcp.tool()
def natural_language_query(query: str, context: dict = None) -> dict:
    """
    自然语言查询LNG数据
    
    示例:
    - "本周LNG价格趋势如何？"
    - "比较Brent和WTI价格"
    - "华东地区LNG价格"
    """
    from nl_query_engine import NLQueryEngine
    
    engine = NLQueryEngine()
    result = engine.query(query)
    
    return {
        "query": result.query,
        "intent": {
            "action": result.intent.action,
            "data_type": result.intent.data_type,
            "time_range": result.intent.time_range,
            "filters": result.intent.filters
        },
        "sql": result.sql,
        "data": result.data,
        "visualization": result.visualization,
        "analysis": result.analysis,
        "confidence": result.confidence
    }
```

---

## 4. 测试用例

| 用户查询 | 预期意图 | 预期SQL | 预期图表 |
|---------|---------|---------|---------|
| "本周LNG价格趋势" | trend, lng, this_week | SELECT * FROM lng_prices WHERE date BETWEEN ... | 折线图 |
| "比较Brent和WTI" | compare, crude | SELECT * FROM crude_prices | 柱状图/折线图 |
| "华东地区价格" | query, china_lng, east | SELECT * FROM china_lng_prices WHERE region='east' | 表格/柱状图 |
| "最近7天JKM" | trend, lng, 7days | SELECT * FROM lng_prices WHERE date BETWEEN ... | 折线图 |
| "本月平均价格" | query, avg | SELECT AVG(price) ... | 指标卡 |

---

*原型完成时间: 2026-04-06 19:00*
