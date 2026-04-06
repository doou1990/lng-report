# 10助理采集协议文档 v4.0

## 标准化采集协议

所有助理必须遵循以下协议：

```yaml
采集协议_v4.0:
  执行步骤:
    1_预检查: |
      - 检查网络连接
      - 检查搜索工具可用性
      - 如工具不可用，立即返回错误
    
    2_多轮搜索: |
      - 执行≥3轮搜索（核心数据源）
      - 执行≥1轮搜索（备用数据源）
      - 每轮使用不同关键词组合
    
    3_数据提取: |
      - 从搜索结果提取具体数值
      - 记录数据来源和发布时间
      - 标注数据单位
    
    4_交叉验证: |
      - 对比多轮搜索结果
      - 计算数值差异百分比
      - 差异>5%需标注
    
    5_输出格式化: |
      - 返回结构化JSON
      - 包含置信度评估
      - 标注缺失数据
  
  错误处理:
    搜索失败: "更换关键词重试1次"
    提取失败: "尝试备用数据源"
    超时: "返回已采集数据+超时说明"
  
  输出格式:
    indicator: "指标名称"
    unit: "单位"
    values:
      - source: "来源1"
        value: "数值1"
        timestamp: "时间1"
        confidence: "high/medium/low"
      - source: "来源2"
        value: "数值2"
        timestamp: "时间2"
        confidence: "high/medium/low"
    final_value: "最终采用值"
    final_confidence: "A/B/C/D"
    discrepancy: "差异说明或null"
    missing_data: ["缺失项1", "缺失项2"]
    notes: "备注"
```

---

## 1. 原油助理 - 采集协议

### 职责
采集Brent和WTI原油价格

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `Brent crude oil price today [DATE] EIA official` | EIA官方 |
| 2 | `WTI Brent crude oil price today Reuters Bloomberg` | Reuters/Bloomberg |
| 3 | `crude oil price live CNBC TradingEconomics` | CNBC/TradingEconomics |
| 备用 | `oil price today MarketWatch OilPrice.com` | MarketWatch |

### 必采数据
- Brent原油价格（美元/桶）
- WTI原油价格（美元/桶）
- 日涨跌、周涨跌
- 数据来源和更新时间

### 输出示例
```json
{
  "indicator": "Brent/WTI原油价格",
  "unit": "美元/桶",
  "values": [
    {
      "source": "EIA",
      "brent": "102.01",
      "wti": "90.84",
      "timestamp": "2026-04-05",
      "confidence": "high"
    },
    {
      "source": "Reuters",
      "brent": "102.50",
      "wti": "91.20",
      "timestamp": "2026-04-05",
      "confidence": "high"
    }
  ],
  "final_value": "Brent: $102.01, WTI: $90.84",
  "final_confidence": "B",
  "discrepancy": "Reuters数据略高，差异<1%",
  "missing_data": [],
  "notes": "EIA数据为官方数据，优先采用"
}
```

---

## 2. 海明助理 - 采集协议

### 职责
采集JKM、TTF、Henry Hub国际LNG价格

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `JKM LNG spot price today [DATE] Platts ICIS` | Platts/ICIS |
| 2 | `TTF natural gas price Europe today ICE exchange` | ICE交易所 |
| 3 | `Henry Hub natural gas price today EIA CME` | EIA/CME |
| 备用1 | `JKM LNG price today LNGPriceIndex.com` | LNGPriceIndex |
| 备用2 | `TTF gas price today OilPriceAPI TradingNews` | OilPriceAPI |

### 必采数据
- JKM LNG现货价格（$/MMBtu）
- TTF欧洲天然气价格（€/MWh）
- Henry Hub美国天然气价格（$/MMBtu）
- 价格走势（日涨跌）

### 输出示例
```json
{
  "indicator": "国际LNG价格",
  "unit": "$/MMBtu or €/MWh",
  "values": [
    {
      "source": "LNGPriceIndex.com",
      "jkm": "18.75",
      "timestamp": "2026-04-03",
      "confidence": "high"
    },
    {
      "source": "OilPriceAPI",
      "ttf": "54.24",
      "timestamp": "2026-04-01",
      "confidence": "high"
    },
    {
      "source": "EIA",
      "henry_hub": "3.05",
      "timestamp": "2026-03-01",
      "confidence": "medium"
    }
  ],
  "final_value": "JKM: $18.75, TTF: €54.24, HH: $3.05",
  "final_confidence": "B",
  "discrepancy": null,
  "missing_data": [],
  "notes": "Henry Hub数据略滞后"
}
```

---

## 3. 陆远助理 - 采集协议

### 职责
采集中国LNG进口和贸易数据

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `China LNG imports [年月] customs statistics` | 海关总署 |
| 2 | `中国LNG进口量 2026年 海关数据 Bloomberg` | Bloomberg |
| 3 | `China LNG imports Qatar Australia Russia Kpler` | Kpler |
| 备用 | `中国LNG进口 新华社 财新 金联创` | 国内媒体 |

### 必采数据
- 中国LNG进口量（最新月度数据）
- 进口来源国分布
- 关税政策
- 美国LNG进口恢复情况

---

## 4. 润仓助理 - 采集协议（★必采★）

### 职责
采集国内LNG市场价格，含浙江专区

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `LNG工厂价格 Mysteel 隆众资讯 [DATE]` | Mysteel/隆众 |
| 2 | `LNG接收站价格 浙江 宁波 舟山 今日` | 区域价格 |
| 3 | `LNG市场均价 开工率 生意社 百川盈孚` | 生意社/百川 |
| 4 | `中海油宁波 新奥舟山 LNG价格 最新` | 浙江专区 |
| **备用1** | **`LNG价格 今日 lng168.com LNG物联网`** | **LNG物联网⭐** |
| **备用2** | **`天然气价格 金联创 今日`** | **金联创⭐** |

### 必采数据
- LNG全国均价（元/吨）
- 液厂出厂价（分区域）
- **浙江专区接收站价格★★★★★**：
  - 中海油宁波
  - 新奥舟山
  - 宁波北仑
  - 嘉兴平湖
  - 上海五号沟
- 开工率

### 浙江专区专项
```yaml
浙江专区必采:
  中海油宁波:
    优先级: ★★★★★
    关键词: ["中海油宁波 LNG价格 今日", "宁波LNG接收站 最新价格"]
    备用源: LNG物联网、隆众资讯
  
  新奥舟山:
    优先级: ★★★★★
    关键词: ["新奥舟山 LNG价格", "舟山LNG接收站 今日价格"]
    备用源: LNG物联网、隆众资讯
  
  宁波北仑:
    优先级: ★★★★☆
    关键词: ["宁波北仑 LNG接收站价格", "北仑LNG 最新"]
    备用源: Mysteel快讯
  
  嘉兴平湖:
    优先级: ★★★★☆
    关键词: ["嘉兴平湖 LNG价格", "平湖LNG接收站"]
    备用源: Mysteel快讯
  
  上海五号沟:
    优先级: ★★★★☆
    关键词: ["上海五号沟 LNG价格", "上海LNG接收站 最新"]
    备用源: LNG物联网、上海燃气
```

---

## 5. 衡尺助理 - 采集协议

### 职责
采集LNG价格驱动因素

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `LNG market drivers geopolitics Hormuz Qatar 2026` | Reuters/Bloomberg |
| 2 | `global LNG supply disruption 2026` | 国际媒体 |
| 3 | `LNG demand weather heating 2026` | 行业分析 |
| 备用 | `天然气 价格驱动 地缘 财新 华尔街见闻` | 国内媒体 |

---

## 6. 欧风助理 - 采集协议

### 职责
采集欧洲天然气库存和进口数据

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `Europe LNG storage levels [DATE] AGSI GIE` | AGSI/GIE |
| 2 | `EU gas inventory percentage 2026` | Eurostat |
| 3 | `Europe LNG imports record 2026 Bruegel` | Bruegel |
| 备用1 | `European gas price TTF TradingEconomics` | TradingEconomics |
| 备用2 | `Europe LNG Global LNG Hub ICIS` | Global LNG Hub |

---

## 7. 金算助理 - 采集协议

### 职责
采集LNG产业链利润数据

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `Cheniere Energy profit Q1 2026 earnings` | 公司财报 |
| 2 | `LNG companies profit margin 2026` | Yahoo Finance |
| 3 | `Shell TotalEnergies LNG revenue 2026` | SeekingAlpha |
| 备用1 | `Cheniere Energy financials MarketWatch` | MarketWatch |
| 备用2 | `LNG stocks analysis Simply Wall St` | Simply Wall St |

---

## 8. 盾甲助理 - 采集协议

### 职责
采集LNG投资评级和策略建议

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `Cheniere Energy LNG stock rating Strong Buy 2026` | stockanalysis.com |
| 2 | `LNG sector investment outlook analyst rating` | TipRanks |
| 3 | `natural gas LNG price forecast 2026 investment` | MarketBeat |
| 备用1 | `Cheniere Energy stock Zacks rating` | Zacks |
| 备用2 | `LNG investment TheStreet analysis` | TheStreet |

---

## 9. 镜史助理 - 采集协议

### 职责
采集LNG价格历史对比数据

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `LNG price history 2024 2025 2026 comparison EIA` | EIA历史 |
| 2 | `Henry Hub price trend historical World Bank` | World Bank |
| 3 | `JKM LNG price historical data IMF` | IMF |
| 备用 | `natural gas price history Macrotrends` | Macrotrends |

---

## 10. 洋基助理 - 采集协议

### 职责
采集美国LNG出口产能数据

### 搜索矩阵

| 轮次 | 关键词 | 目标数据源 |
|------|--------|-----------|
| 1 | `US LNG export capacity 2026 DOE FERC` | DOE/FERC |
| 2 | `Golden Pass LNG startup 2026` | 公司公告 |
| 3 | `Corpus Christi LNG expansion 2026` | EIA |
| 备用1 | `US LNG projects Energy Central` | Energy Central |
| 备用2 | `LNG export capacity Natural Gas Intelligence` | NGI |

---

## 置信度评分标准 v4.0

| 等级 | 分数 | 标准 | 处理 |
|------|------|------|------|
| A | 90-100 | ≥3来源一致，差异<3%，时效性T日 | 直接采用 |
| B | 75-89 | 2-3来源，差异3-5%，时效性T-1日 | 采用，标注差异 |
| C | 60-74 | 1-2来源，差异5-10%，时效性T-3日 | 采用，标注低可信度 |
| D | <60 | 无数据或差异>10%，时效性>T-7日 | 不采用，标记缺失 |

---

*本文档为10助理采集协议v4.0，所有助理必须严格遵循*
