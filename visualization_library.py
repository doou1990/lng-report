# 可视化图表库 - v4.4增强版

**实现日期**: 2026-04-06  
**功能**: 8种图表类型，自动选择，交互增强

---

from typing import Dict, List, Literal, Optional
import json

class LNGVisualizationLibrary:
    """LNG数据可视化图表库"""
    
    def __init__(self):
        self.chart_types = {
            "line": self.create_line_chart,
            "bar": self.create_bar_chart,
            "candlestick": self.create_candlestick_chart,
            "area": self.create_area_chart,
            "scatter": self.create_scatter_chart,
            "heatmap": self.create_heatmap_chart,
            "gauge": self.create_gauge_chart,
            "combo": self.create_combo_chart
        }
    
    def auto_select_chart(self, data: List[Dict], intent: Dict) -> str:
        """
        根据数据特征自动选择最佳图表类型
        
        选择逻辑:
        1. 时间序列 + 多维度 → 折线图/面积图
        2. 对比分析 → 柱状图
        3. 价格OHLC数据 → K线图
        4. 双变量关系 → 散点图
        5. 矩阵数据 → 热力图
        6. 单一关键指标 → 仪表盘
        7. 多指标组合 → 组合图
        """
        # 判断数据特征
        has_date = any("date" in str(k).lower() for k in data[0].keys()) if data else False
        has_ohlc = all(k in data[0] for k in ["open", "high", "low", "close"]) if data else False
        data_count = len(data)
        field_count = len(data[0]) if data else 0
        
        # 根据意图和数据特征选择
        if intent.get("action") == "trend":
            if data_count > 30:
                return "area"  # 大数据量用面积图
            return "line"  # 趋势用折线图
        
        elif intent.get("action") == "compare":
            return "bar"  # 对比用柱状图
        
        elif has_ohlc:
            return "candlestick"  # OHLC数据用K线图
        
        elif field_count == 2 and has_date:
            return "scatter"  # 双变量用散点图
        
        elif field_count > 5:
            return "heatmap"  # 多维度用热力图
        
        elif data_count == 1 and field_count <= 3:
            return "gauge"  # 单一指标用仪表盘
        
        elif field_count >= 4:
            return "combo"  # 多指标用组合图
        
        return "line"  # 默认折线图
    
    # ============ 1. 折线图 (Line Chart) ============
    
    def create_line_chart(
        self,
        data: List[Dict],
        x_field: str = "date",
        y_fields: List[str] = None,
        title: str = "价格趋势",
        subtitle: str = "",
        colors: List[str] = None
    ) -> Dict:
        """
        创建折线图 - 适合时间序列趋势展示
        
        示例: 展示Brent和WTI原油价格30天走势
        """
        if y_fields is None:
            y_fields = ["price"]
        
        if colors is None:
            colors = ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de"]
        
        x_data = [str(row.get(x_field, "")) for row in data]
        
        series = []
        for i, field in enumerate(y_fields):
            series.append({
                "name": field.replace("_", " ").title(),
                "type": "line",
                "data": [row.get(field) for row in data],
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 6,
                "lineStyle": {"width": 2},
                "itemStyle": {"color": colors[i % len(colors)]},
                "areaStyle": {
                    "opacity": 0.1,
                    "color": {
                        "type": "linear",
                        "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": colors[i % len(colors)]},
                            {"offset": 1, "color": "rgba(255,255,255,0)"}
                        ]
                    }
                }
            })
        
        return {
            "chart_type": "line",
            "title": {"text": title, "subtext": subtitle, "left": "center"},
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "cross"},
                "formatter": self._create_tooltip_formatter(y_fields)
            },
            "legend": {"data": [s["name"] for s in series], "bottom": 0},
            "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
            "xAxis": {
                "type": "category",
                "boundaryGap": False,
                "data": x_data,
                "axisLabel": {"rotate": 45 if len(x_data) > 10 else 0}
            },
            "yAxis": {"type": "value", "name": "价格", "axisLabel": {"formatter": "{value}"}},
            "dataZoom": [
                {"type": "inside", "start": 0, "end": 100},
                {"type": "slider", "start": 0, "end": 100, "bottom": 30}
            ],
            "toolbox": {
                "feature": {
                    "saveAsImage": {"title": "保存图片"},
                    "dataView": {"title": "数据视图", "readOnly": True},
                    "restore": {"title": "还原"},
                    "zoom": {"title": {"zoom": "区域缩放", "back": "缩放还原"}}
                }
            },
            "series": series
        }
    
    # ============ 2. 柱状图 (Bar Chart) ============
    
    def create_bar_chart(
        self,
        data: List[Dict],
        x_field: str = "category",
        y_field: str = "value",
        title: str = "数据对比",
        subtitle: str = "",
        horizontal: bool = False
    ) -> Dict:
        """
        创建柱状图 - 适合类别对比
        
        示例: 对比不同地区LNG价格
        """
        x_data = [str(row.get(x_field, "")) for row in data]
        y_data = [row.get(y_field, 0) for row in data]
        
        # 渐变色
        color_gradient = {
            "type": "linear",
            "x": 0, "y": 0, "x2": 0, "y2": 1,
            "colorStops": [
                {"offset": 0, "color": "#83bff6"},
                {"offset": 0.5, "color": "#188df0"},
                {"offset": 1, "color": "#188df0"}
            ]
        }
        
        return {
            "chart_type": "bar",
            "title": {"text": title, "subtext": subtitle, "left": "center"},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
            "xAxis": {
                "type": "category" if not horizontal else "value",
                "data": x_data if not horizontal else None,
                "axisTick": {"alignWithLabel": True},
                "axisLabel": {"interval": 0, "rotate": 30 if len(x_data) > 6 else 0}
            },
            "yAxis": {
                "type": "value" if not horizontal else "category",
                "data": None if not horizontal else x_data,
                "name": "数值"
            },
            "series": [{
                "name": y_field,
                "type": "bar",
                "barWidth": "60%",
                "data": y_data,
                "itemStyle": {
                    "color": color_gradient,
                    "borderRadius": [5, 5, 0, 0] if not horizontal else [0, 5, 5, 0]
                },
                "label": {
                    "show": True,
                    "position": "top" if not horizontal else "right",
                    "formatter": "{c}"
                }
            }],
            "dataZoom": [{"type": "inside"}] if len(x_data) > 10 else [],
            "toolbox": {
                "feature": {
                    "saveAsImage": {},
                    "dataView": {},
                    "magicType": {"type": ["line", "bar"]},
                    "restore": {}
                }
            }
        }
    
    # ============ 3. K线图 (Candlestick Chart) ============
    
    def create_candlestick_chart(
        self,
        data: List[Dict],
        title: str = "价格K线",
        subtitle: str = ""
    ) -> Dict:
        """
        创建K线图 - 适合展示价格波动
        
        示例: 展示LNG期货价格OHLC数据
        """
        # 提取OHLC数据
        dates = [row.get("date", "") for row in data]
        candle_data = []
        for row in data:
            candle_data.append([
                row.get("open", 0),
                row.get("close", 0),
                row.get("low", 0),
                row.get("high", 0)
            ])
        
        # 计算MA5和MA10
        ma5 = self._calculate_ma(candle_data, 5)
        ma10 = self._calculate_ma(candle_data, 10)
        
        return {
            "chart_type": "candlestick",
            "title": {"text": title, "subtext": subtitle, "left": "center"},
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "cross"},
                "formatter": self._candlestick_formatter
            },
            "legend": {"data": ["K线", "MA5", "MA10"], "bottom": 0},
            "grid": {"left": "10%", "right": "10%", "bottom": "15%"},
            "xAxis": {
                "type": "category",
                "data": dates,
                "scale": True,
                "boundaryGap": False,
                "axisLine": {"onZero": False},
                "splitLine": {"show": False},
                "min": "dataMin",
                "max": "dataMax"
            },
            "yAxis": {
                "scale": True,
                "splitArea": {"show": True}
            },
            "dataZoom": [
                {"type": "inside", "start": 50, "end": 100},
                {"show": True, "type": "slider", "top": "90%", "start": 50, "end": 100}
            ],
            "series": [
                {
                    "name": "K线",
                    "type": "candlestick",
                    "data": candle_data,
                    "itemStyle": {
                        "color": "#ef232a",  # 涨 - 红色
                        "color0": "#14b143",  # 跌 - 绿色
                        "borderColor": "#ef232a",
                        "borderColor0": "#14b143"
                    }
                },
                {
                    "name": "MA5",
                    "type": "line",
                    "data": ma5,
                    "smooth": True,
                    "lineStyle": {"opacity": 0.5}
                },
                {
                    "name": "MA10",
                    "type": "line",
                    "data": ma10,
                    "smooth": True,
                    "lineStyle": {"opacity": 0.5}
                }
            ]
        }
    
    def _calculate_ma(self, data: List[List], period: int) -> List[Optional[float]]:
        """计算移动平均线"""
        result = []
        for i in range(len(data)):
            if i < period - 1:
                result.append(None)
            else:
                avg = sum(data[j][1] for j in range(i - period + 1, i + 1)) / period
                result.append(round(avg, 2))
        return result
    
    # ============ 4. 面积图 (Area Chart) ============
    
    def create_area_chart(
        self,
        data: List[Dict],
        x_field: str = "date",
        y_fields: List[str] = None,
        title: str = "累积趋势"
    ) -> Dict:
        """
        创建面积图 - 适合展示累积趋势
        
        示例: 展示LNG库存累积变化
        """
        base_chart = self.create_line_chart(data, x_field, y_fields, title)
        
        # 增强面积效果
        for series in base_chart["series"]:
            series["areaStyle"] = {
                "opacity": 0.3,
                "color": {
                    "type": "linear",
                    "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": series["itemStyle"]["color"]},
                        {"offset": 1, "color": "rgba(255,255,255,0.1)"}
                    ]
                }
            }
            series["lineStyle"] = {"width": 1}
        
        base_chart["chart_type"] = "area"
        return base_chart
    
    # ============ 5. 散点图 (Scatter Chart) ============
    
    def create_scatter_chart(
        self,
        data: List[Dict],
        x_field: str,
        y_field: str,
        size_field: Optional[str] = None,
        title: str = "相关性分析"
    ) -> Dict:
        """
        创建散点图 - 适合展示双变量关系
        
        示例: 展示原油价格与LNG价格的相关性
        """
        scatter_data = []
        for row in data:
            point = [row.get(x_field), row.get(y_field)]
            if size_field:
                point.append(row.get(size_field, 5))
            scatter_data.append(point)
        
        return {
            "chart_type": "scatter",
            "title": {"text": title, "left": "center"},
            "tooltip": {
                "trigger": "item",
                "formatter": f"{x_field}: {{c[0]}}\n{y_field}: {{c[1]}}"
            },
            "xAxis": {"type": "value", "name": x_field, "scale": True},
            "yAxis": {"type": "value", "name": y_field, "scale": True},
            "series": [{
                "type": "scatter",
                "symbolSize": lambda val: val[2] if len(val) > 2 else 10,
                "data": scatter_data,
                "itemStyle": {
                    "color": {
                        "type": "radial",
                        "x": 0.4, "y": 0.3, "r": 1,
                        "colorStops": [
                            {"offset": 0, "color": "#f6efa6"},
                            {"offset": 1, "color": "#d88273"}
                        ]
                    }
                }
            }]
        }
    
    # ============ 6. 热力图 (Heatmap) ============
    
    def create_heatmap_chart(
        self,
        data: List[List],
        x_labels: List[str],
        y_labels: List[str],
        title: str = "热力图"
    ) -> Dict:
        """
        创建热力图 - 适合展示矩阵数据
        
        示例: 展示不同地区不同时间的LNG价格热力图
        """
        # 转换数据格式
        heatmap_data = []
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                heatmap_data.append([j, i, value])
        
        return {
            "chart_type": "heatmap",
            "title": {"text": title, "left": "center"},
            "tooltip": {"position": "top"},
            "grid": {"height": "50%", "top": "10%"},
            "xAxis": {
                "type": "category",
                "data": x_labels,
                "splitArea": {"show": True}
            },
            "yAxis": {
                "type": "category",
                "data": y_labels,
                "splitArea": {"show": True}
            },
            "visualMap": {
                "min": min(min(row) for row in data),
                "max": max(max(row) for row in data),
                "calculable": True,
                "orient": "horizontal",
                "left": "center",
                "bottom": "15%",
                "inRange": {
                    "color": ["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", 
                              "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
                }
            },
            "series": [{
                "name": "数值",
                "type": "heatmap",
                "data": heatmap_data,
                "label": {"show": True},
                "emphasis": {
                    "itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}
                }
            }]
        }
    
    # ============ 7. 仪表盘 (Gauge Chart) ============
    
    def create_gauge_chart(
        self,
        value: float,
        title: str = "关键指标",
        min_val: float = 0,
        max_val: float = 100,
        unit: str = ""
    ) -> Dict:
        """
        创建仪表盘 - 适合展示单一关键指标
        
        示例: 展示当前LNG库存水平
        """
        # 根据值确定颜色
        if value < max_val * 0.3:
            color = "#ef4444"  # 红色 - 低
        elif value < max_val * 0.7:
            color = "#f59e0b"  # 黄色 - 中
        else:
            color = "#10b981"  # 绿色 - 高
        
        return {
            "chart_type": "gauge",
            "title": {"text": title, "left": "center"},
            "series": [{
                "type": "gauge",
                "startAngle": 180,
                "endAngle": 0,
                "min": min_val,
                "max": max_val,
                "splitNumber": 8,
                "axisLine": {
                    "lineStyle": {
                        "width": 6,
                        "color": [
                            [0.25, "#ef4444"],
                            [0.5, "#f59e0b"],
                            [0.75, "#3b82f6"],
                            [1, "#10b981"]
                        ]
                    }
                },
                "pointer": {
                    "icon": "path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",
                    "length": "12%",
                    "width": 20,
                    "offsetCenter": [0, "-60%"],
                    "itemStyle": {"color": "auto"}
                },
                "axisTick": {"length": 12, "lineStyle": {"color": "auto", "width": 2}},
                "splitLine": {"length": 20, "lineStyle": {"color": "auto", "width": 5}},
                "axisLabel": {
                    "color": "#464646",
                    "fontSize": 14,
                    "distance": -60,
                    "formatter": "{value}" + unit
                },
                "title": {"offsetCenter": [0, "-20%"], "fontSize": 20},
                "detail": {
                    "fontSize": 30,
                    "offsetCenter": [0, "0%"],
                    "valueAnimation": True,
                    "formatter": "{value}" + unit,
                    "color": "auto"
                },
                "data": [{"value": value, "name": title}]
            }]
        }
    
    # ============ 8. 组合图 (Combo Chart) ============
    
    def create_combo_chart(
        self,
        data: List[Dict],
        x_field: str = "date",
        line_fields: List[str] = None,
        bar_fields: List[str] = None,
        title: str = "多指标分析"
    ) -> Dict:
        """
        创建组合图 - 适合展示多指标对比
        
        示例: 同时展示价格(折线)和库存(柱状)
        """
        if line_fields is None:
            line_fields = []
        if bar_fields is None:
            bar_fields = []
        
        x_data = [str(row.get(x_field, "")) for row in data]
        
        series = []
        colors = ["#5470c6", "#91cc75", "#fac858", "#ee6666"]
        
        # 添加折线系列
        for i, field in enumerate(line_fields):
            series.append({
                "name": field,
                "type": "line",
                "yAxisIndex": 0,
                "data": [row.get(field) for row in data],
                "smooth": True,
                "itemStyle": {"color": colors[i % len(colors)]}
            })
        
        # 添加柱状系列
        for i, field in enumerate(bar_fields):
            series.append({
                "name": field,
                "type": "bar",
                "yAxisIndex": 1 if line_fields else 0,
                "data": [row.get(field) for row in data],
                "itemStyle": {"color": colors[(i + len(line_fields)) % len(colors)]}
            })
        
        y_axes = [{"type": "value", "name": "价格", "position": "left"}]
        if bar_fields:
            y_axes.append({"type": "value", "name": "数量", "position": "right"})
        
        return {
            "chart_type": "combo",
            "title": {"text": title, "left": "center"},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {"data": [s["name"] for s in series], "bottom": 0},
            "xAxis": {"type": "category", "data": x_data, "axisPointer": {"type": "shadow"}},
            "yAxis": y_axes,
            "series": series,
            "toolbox": {
                "feature": {
                    "magicType": {"show": True, "type": ["line", "bar", "stack"]},
                    "restore": {"show": True}
                }
            }
        }
    
    # ============ 辅助方法 ============
    
    def _create_tooltip_formatter(self, fields: List[str]) -> str:
        """创建tooltip格式化函数"""
        return "function(params) { return params.map(p => p.marker + p.seriesName + ': ' + p.value).join('<br/>'); }"
    
    def _candlestick_formatter(self, params):
        """K线图tooltip格式化"""
        param = params[0]
        return f"""
        日期: {param.name}<br/>
        开盘: {param.data[1]}<br/>
        收盘: {param.data[2]}<br/>
        最低: {param.data[3]}<br/>
        最高: {param.data[4]}
        """
    
    def render_chart(self, chart_config: Dict, container_id: str = "chart") -> str:
        """
        渲染图表为HTML
        
        返回完整的HTML代码，可直接在浏览器中打开
        """
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{chart_config.get('title', {}).get('text', 'Chart')}</title>
            <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
            <style>
                body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; }}
                #{container_id} {{ width: 100%; height: 500px; }}
            </style>
        </head>
        <body>
            <div id="{container_id}"></div>
            <script>
                var chart = echarts.init(document.getElementById('{container_id}'));
                var option = {json.dumps(chart_config, ensure_ascii=False, indent=2)};
                chart.setOption(option);
                window.addEventListener('resize', function() {{ chart.resize(); }});
            </script>
        </body>
        </html>
        """
        return html_template


# ============ 使用示例 ============

if __name__ == "__main__":
    viz = LNGVisualizationLibrary()
    
    # 示例数据
    sample_data = [
        {"date": "2026-04-01", "brent": 106.5, "wti": 108.2},
        {"date": "2026-04-02", "brent": 107.2, "wti": 109.1},
        {"date": "2026-04-03", "brent": 108.4, "wti": 110.3},
        {"date": "2026-04-04", "brent": 109.0, "wti": 111.5},
        {"date": "2026-04-05", "brent": 108.4, "wti": 110.3},
        {"date": "2026-04-06", "brent": 108.4, "wti": 110.3}
    ]
    
    # 创建折线图
    line_chart = viz.create_line_chart(
        data=sample_data,
        x_field="date",
        y_fields=["brent", "wti"],
        title="原油价格趋势"
    )
    print("折线图配置已生成")
    
    # 自动选择图表类型
    intent = {"action": "trend"}
    chart_type = viz.auto_select_chart(sample_data, intent)
    print(f"自动选择图表类型: {chart_type}")
    
    # 渲染为HTML
    html = viz.render_chart(line_chart, "crude_price_chart")
    with open("/tmp/crude_price_chart.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML文件已保存: /tmp/crude_price_chart.html")
