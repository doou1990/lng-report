# 异常检测自动化规则 v4.0

## 检测规则

### 1. 价格波动异常

```python
# 规则: 单日价格波动超过20%
def check_price_volatility(current_price, previous_price):
    if previous_price == 0:
        return False, "无历史数据"
    
    change_pct = abs(current_price - previous_price) / previous_price * 100
    
    if change_pct > 50:
        return True, f"🔴 严重异常: 价格波动{change_pct:.1f}% (>50%)"
    elif change_pct > 20:
        return True, f"🟡 中度异常: 价格波动{change_pct:.1f}% (20-50%)"
    elif change_pct > 10:
        return True, f"🟢 轻度异常: 价格波动{change_pct:.1f}% (10-20%)"
    else:
        return False, f"正常: 价格波动{change_pct:.1f}% (<10%)"
```

### 2. 多源差异异常

```python
# 规则: 多源数据差异超过10%
def check_source_discrepancy(values, sources):
    if len(values) < 2:
        return False, "单来源，无法对比"
    
    # 转换为数值
    numeric_values = [float(v) for v in values if v is not None]
    
    if len(numeric_values) < 2:
        return False, "有效数据源不足"
    
    max_val = max(numeric_values)
    min_val = min(numeric_values)
    avg_val = sum(numeric_values) / len(numeric_values)
    
    discrepancy_pct = (max_val - min_val) / avg_val * 100
    
    if discrepancy_pct > 20:
        return True, f"🔴 严重差异: 多源差异{discrepancy_pct:.1f}% (>20%)"
    elif discrepancy_pct > 10:
        return True, f"🟡 中度差异: 多源差异{discrepancy_pct:.1f}% (10-20%)"
    elif discrepancy_pct > 5:
        return True, f"🟢 轻度差异: 多源差异{discrepancy_pct:.1f}% (5-10%)"
    else:
        return False, f"正常: 多源差异{discrepancy_pct:.1f}% (<5%)"
```

### 3. 历史对比异常

```python
# 规则: 与历史均值差异超过2个标准差
def check_historical_anomaly(current_value, historical_values):
    if len(historical_values) < 7:
        return False, "历史数据不足(需≥7天)"
    
    mean = sum(historical_values) / len(historical_values)
    variance = sum((x - mean) ** 2 for x in historical_values) / len(historical_values)
    std_dev = variance ** 0.5
    
    if std_dev == 0:
        return False, "历史数据无变化"
    
    z_score = abs(current_value - mean) / std_dev
    
    if z_score > 3:
        return True, f"🔴 严重异常: Z-score={z_score:.2f} (>3σ)"
    elif z_score > 2:
        return True, f"🟡 中度异常: Z-score={z_score:.2f} (2-3σ)"
    else:
        return False, f"正常: Z-score={z_score:.2f} (<2σ)"
```

### 4. 时效性异常

```python
# 规则: 数据过于滞后
def check_data_freshness(data_date, report_date):
    from datetime import datetime
    
    data_dt = datetime.strptime(data_date, "%Y-%m-%d")
    report_dt = datetime.strptime(report_date, "%Y-%m-%d")
    lag_days = (report_dt - data_dt).days
    
    if lag_days > 7:
        return True, f"🔴 严重滞后: 数据滞后{lag_days}天 (>7天)"
    elif lag_days > 3:
        return True, f"🟡 中度滞后: 数据滞后{lag_days}天 (4-7天)"
    elif lag_days > 1:
        return True, f"🟢 轻度滞后: 数据滞后{lag_days}天 (2-3天)"
    else:
        return False, f"正常: 数据滞后{lag_days}天 (≤1天)"
```

---

## 自动化处理流程

```yaml
异常检测流程:
  步骤1_数据采集:
    - 采集原始数据
    - 记录数据来源和时间
  
  步骤2_自动检测:
    - 价格波动检测
    - 多源差异检测
    - 历史对比检测
    - 时效性检测
  
  步骤3_异常分级:
    - 🔴 严重异常: 立即标记，人工审核
    - 🟡 中度异常: 标注警告，纳入报告
    - 🟢 轻度异常: 记录日志，正常报告
  
  步骤4_报告标注:
    - 在报告中显示异常标记
    - 提供异常原因分析
    - 建议后续关注
```

---

## 异常标记格式

```markdown
### 价格数据 (含异常标记)

| 指标 | 数值 | 趋势 | 异常标记 |
|------|------|------|----------|
| Brent原油 | $102.01 | +5% | 🟡 价格波动12% |
| JKM | $18.75 | -2.67% | 正常 |
| 国内均价 | 4,813元/吨 | +3% | 🔴 多源差异15% |

**异常说明**:
- 🟡 Brent原油: 价格较昨日上涨12%，可能受地缘因素影响
- 🔴 国内均价: LNG物联网(4,813)与生意社(5,124)差异15%，需核实
```

---

## 历史异常案例库

```yaml
案例1:
  日期: 2026-03-15
  指标: JKM价格
  异常: 单日上涨50%
  原因: 中东地缘政治紧张
  处理: 标注为异常，但数据有效
  
案例2:
  日期: 2026-04-02
  指标: 国内LNG均价
  异常: 多源差异18%
  原因: 清明假期前后统计口径不同
  处理: 标注差异来源，采用最新数据
  
案例3:
  日期: 2026-03-30
  指标: 浙江接收站价格
  异常: 数据滞后5天
  原因: Mysteel网站维护
  处理: 使用LNG物联网替代
```

---

## 自动化监控仪表板

```markdown
# 异常监控仪表板 - 2026-04-05

## 今日异常统计
- 🔴 严重异常: 0
- 🟡 中度异常: 2
- 🟢 轻度异常: 3

## 异常详情
1. 🟡 国内LNG均价: 多源差异12%
2. 🟡 Henry Hub: 数据滞后2天
3. 🟢 Brent原油: 价格波动8%
4. 🟢 TTF: 价格波动6%
5. 🟢 浙江专区: 部分数据缺失

## 本周趋势
- 异常数量: 较上周减少20%
- 数据质量: 持续提升
- 主要问题: 节假日数据滞后

## 建议行动
1. 配置Mysteel API减少数据缺失
2. 增加节假日自动标注
3. 优化多源差异处理逻辑
```

---

*自动化检测规则 v4.0 | 执行频率: 每次数据采集后*
