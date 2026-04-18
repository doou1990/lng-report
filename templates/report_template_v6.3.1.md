# LNG原油市场日报 - 标准模板（v6.3.1-纵横版）

**报告日期**: {{DATE}}  
**报告版本**: v6.3.1-纵横版  
**审核评分**: {{AUDIT_SCORE}}分 ({{AUDIT_RESULT}})  
**数据完整度**: {{COMPLETENESS}}%  
**执行模式**: 主会话直采 + 纵横分析法

---

## 第一章：执行摘要

### 1.1 核心结论
1. {{CONCLUSION_1}}
2. {{CONCLUSION_2}}
3. {{CONCLUSION_3}}
4. {{CONCLUSION_4}}
5. {{CONCLUSION_5}}

### 1.2 关键数据一览

| 类别 | 指标 | 数值 | 涨跌 | 置信度 |
|------|------|------|------|--------|
| **原油** | Brent | ${{BRENT_PRICE}} | {{BRENT_CHANGE}} | {{BRENT_CONFIDENCE}} |
| | WTI | ${{WTI_PRICE}} | {{WTI_CHANGE}} | {{WTI_CONFIDENCE}} |
| **国际LNG** | JKM | ${{JKM_PRICE}} | {{JKM_CHANGE}} | {{JKM_CONFIDENCE}} |
| | TTF | €{{TTF_PRICE}} | {{TTF_CHANGE}} | {{TTF_CONFIDENCE}} |
| | Henry Hub | ${{HH_PRICE}} | {{HH_CHANGE}} | {{HH_CONFIDENCE}} |
| **国内LNG** | 液厂均价 | {{FACTORY_PRICE}}元/吨 | {{FACTORY_CHANGE}} | {{FACTORY_CONFIDENCE}} |
| | 接收站均价 | {{TERMINAL_PRICE}}元/吨 | {{TERMINAL_CHANGE}} | {{TERMINAL_CONFIDENCE}} |

### 1.3 风险提示
- ⚠️ {{RISK_1}}
- ⚠️ {{RISK_2}}
- ⚠️ {{RISK_3}}

---

## 第二章：市场概况

### 2.1 全球供需格局
{{GLOBAL_SUPPLY_DEMAND_OVERVIEW}}

### 2.2 价格走势回顾
{{PRICE_TREND_REVIEW}}

### 2.3 关键事件影响
| 事件 | 影响 | 持续时间 |
|------|------|----------|
| {{EVENT_1}} | {{IMPACT_1}} | {{DURATION_1}} |
| {{EVENT_2}} | {{IMPACT_2}} | {{DURATION_2}} |
| {{EVENT_3}} | {{IMPACT_3}} | {{DURATION_3}} |

---

## 第三章：原油价格分析

### 3.1 现货价格走势
- **Brent原油**: ${{BRENT_PRICE}}/桶，{{BRENT_CHANGE}}
- **WTI原油**: ${{WTI_PRICE}}/桶，{{WTI_CHANGE}}
- **价差**: Brent-WTI = ${{BRENT_WTI_SPREAD}}/桶

### 3.2 期限结构分析（Backwardation/Contango）
```
期限结构:
近月: ${{FRONT_MONTH_PRICE}}
3个月: ${{M3_PRICE}}
6个月: ${{M6_PRICE}}
12个月: ${{M12_PRICE}}

结构判断: {{TERM_STRUCTURE}} ({{STRUCTURE_INTERPRETATION}})
```

### 3.3 跨区价差分析
| 价差 | 当前值 | 正常范围 | 偏离度 | 解读 |
|------|--------|----------|--------|------|
| Brent-WTI | ${{BRENT_WTI_SPREAD}} | $0-5 | {{BRENT_WTI_DEVIATION}} | {{BRENT_WTI_COMMENT}} |
| Brent-Dubai | ${{BRENT_DUBAI_SPREAD}} | $0-3 | {{BRENT_DUBAI_DEVIATION}} | {{BRENT_DUBAI_COMMENT}} |

### 3.4 驱动因素分析（五因子模型）

| 因子 | 指标 | 当前值 | 影响 | 评分 |
|------|------|--------|------|------|
| **需求因子** | 全球GDP增速 | {{GLOBAL_GDP}} | {{DEMAND_IMPACT}} | {{DEMAND_SCORE}}/25 |
| **供给因子** | OPEC+产量 | {{OPEC_PRODUCTION}} | {{SUPPLY_IMPACT}} | {{SUPPLY_SCORE}}/25 |
| **库存因子** | EIA商业库存 | {{EIA_INVENTORY}} | {{INVENTORY_IMPACT}} | {{INVENTORY_SCORE}}/25 |
| **美元因子** | 美元指数 | {{DXY}} | {{DOLLAR_IMPACT}} | {{DOLLAR_SCORE}}/25 |
| **风险因子** | VIX指数 | {{VIX}} | {{RISK_IMPACT}} | {{RISK_SCORE}}/25 |

---

## 第四章：LNG价格分析

### 4.1 国际LNG价格

| 市场 | 价格 | 单位 | 涨跌 | 置信度 | 来源 |
|------|------|------|------|--------|------|
| JKM | ${{JKM_PRICE}} | 美元/百万英热 | {{JKM_CHANGE}} | {{JKM_CONFIDENCE}} | {{JKM_SOURCE}} |
| TTF | €{{TTF_PRICE}} | 欧元/兆瓦时 | {{TTF_CHANGE}} | {{TTF_CONFIDENCE}} | {{TTF_SOURCE}} |
| Henry Hub | ${{HH_PRICE}} | 美元/百万英热 | {{HH_CHANGE}} | {{HH_CONFIDENCE}} | {{HH_SOURCE}} |

### 4.2 国内LNG价格

#### 液厂价格
- **全国均价**: {{FACTORY_AVG_PRICE}}元/吨
- **价格区间**: {{FACTORY_LOW_PRICE}} - {{FACTORY_HIGH_PRICE}}元/吨
- **开工率**: {{OPERATING_RATE}}%
- **检修情况**: {{MAINTENANCE_INFO}}

#### 接收站价格
- **全国均价**: {{TERMINAL_AVG_PRICE}}元/吨
- **价格区间**: {{TERMINAL_LOW_PRICE}} - {{TERMINAL_HIGH_PRICE}}元/吨
- **最高**: {{TERMINAL_HIGH_NAME}} {{TERMINAL_HIGH_PRICE}}元/吨
- **最低**: {{TERMINAL_LOW_NAME}} {{TERMINAL_LOW_PRICE}}元/吨

### 4.3 浙江专区价格

| 接收站 | 价格(元/吨) | 涨跌 | 日期 | 状态 |
|--------|-------------|------|------|------|
| 宁波中海油 | {{NINGBO_PRICE}} | {{NINGBO_CHANGE}} | {{NINGBO_DATE}} | {{NINGBO_STATUS}} |
| 舟山新奥 | {{ZHOUSHAN_PRICE}} | {{ZHOUSHAN_CHANGE}} | {{ZHOUSHAN_DATE}} | {{ZHOUSHAN_STATUS}} |
| 上海五号沟 | {{SHANGHAI_PRICE}} | {{SHANGHAI_CHANGE}} | {{SHANGHAI_DATE}} | {{SHANGHAI_STATUS}} |
| 浙能温州 | {{WENZHOU_PRICE}} | {{WENZHOU_CHANGE}} | {{WENZHOU_DATE}} | {{WENZHOU_STATUS}} |

### 4.4 区域价差分析

| 价差 | 当前值 | 正常范围 | 解读 |
|------|--------|----------|------|
| JKM-TTF | ${{JKM_TTF_SPREAD}} | $0-2 | {{JKM_TTF_COMMENT}} |
| 液厂-接收站 | {{FACTORY_TERMINAL_SPREAD}}元/吨 | 800-1000 | {{FACTORY_TERMINAL_COMMENT}} |

---

## 第五章：供给分析

### 5.1 全球LNG产能
{{GLOBAL_LNG_CAPACITY}}

### 5.2 主要出口国动态

| 国家 | 产量 | 产能利用率 | 主要项目 | 备注 |
|------|------|------------|----------|------|
| 美国 | {{US_PRODUCTION}} | {{US_UTILIZATION}} | {{US_PROJECTS}} | {{US_NOTES}} |
| 卡塔尔 | {{QA_PRODUCTION}} | {{QA_UTILIZATION}} | {{QA_PROJECTS}} | {{QA_NOTES}} |
| 澳大利亚 | {{AU_PRODUCTION}} | {{AU_UTILIZATION}} | {{AU_PROJECTS}} | {{AU_NOTES}} |
| 俄罗斯 | {{RU_PRODUCTION}} | {{RU_UTILIZATION}} | {{RU_PROJECTS}} | {{RU_NOTES}} |

### 5.3 新增项目投产
{{NEW_PROJECTS}}

### 5.4 供应风险因素
- {{SUPPLY_RISK_1}}
- {{SUPPLY_RISK_2}}
- {{SUPPLY_RISK_3}}

---

## 第六章：需求分析

### 6.1 全球需求趋势
{{GLOBAL_DEMAND_TREND}}

### 6.2 中国进口分析

| 指标 | 数值 | 同比 | 环比 |
|------|------|------|------|
| 月度进口量 | {{CHINA_IMPORT_VOLUME}}万吨 | {{CHINA_IMPORT_YOY}} | {{CHINA_IMPORT_MOM}} |
| 进口均价 | {{CHINA_IMPORT_PRICE}}美元/吨 | {{CHINA_PRICE_YOY}} | {{CHINA_PRICE_MOM}} |

#### 主要来源国
| 国家 | 占比 | 进口量 | 备注 |
|------|------|--------|------|
| 澳大利亚 | {{AUSTRALIA_SHARE}}% | {{AUSTRALIA_VOLUME}} | {{AUSTRALIA_NOTES}} |
| 卡塔尔 | {{QATAR_SHARE}}% | {{QATAR_VOLUME}} | {{QATAR_NOTES}} |
| 马来西亚 | {{MALAYSIA_SHARE}}% | {{MALAYSIA_VOLUME}} | {{MALAYSIA_NOTES}} |
| 俄罗斯 | {{RUSSIA_SHARE}}% | {{RUSSIA_VOLUME}} | {{RUSSIA_NOTES}} |

### 6.3 季节性因素
{{SEASONAL_FACTORS}}

### 6.4 替代能源影响
{{ALTERNATIVE_ENERGY_IMPACT}}

---

## 第七章：库存与平衡

### 7.1 全球库存水平

| 区域 | 库存量 | 库存率 | 同比变化 | 状态 |
|------|--------|--------|----------|------|
| 美国 | {{US_INVENTORY}} | {{US_INVENTORY_RATE}} | {{US_INVENTORY_CHANGE}} | {{US_INVENTORY_STATUS}} |
| 欧洲 | {{EU_INVENTORY}} | {{EU_INVENTORY_RATE}} | {{EU_INVENTORY_CHANGE}} | {{EU_INVENTORY_STATUS}} |
| 中国 | {{CN_INVENTORY}} | {{CN_INVENTORY_RATE}} | {{CN_INVENTORY_CHANGE}} | {{CN_INVENTORY_STATUS}} |

### 7.2 供需平衡表

| 项目 | 2025年 | 2026年(Q1) | 2026年(预测) | 同比变化 |
|------|--------|------------|--------------|----------|
| **供给** | | | | |
| 美国LNG出口 | {{US_SUPPLY_2025}} | {{US_SUPPLY_Q1}} | {{US_SUPPLY_2026}} | {{US_SUPPLY_CHANGE}} |
| 卡塔尔LNG | {{QA_SUPPLY_2025}} | {{QA_SUPPLY_Q1}} | {{QA_SUPPLY_2026}} | {{QA_SUPPLY_CHANGE}} |
| 澳大利亚LNG | {{AU_SUPPLY_2025}} | {{AU_SUPPLY_Q1}} | {{AU_SUPPLY_2026}} | {{AU_SUPPLY_CHANGE}} |
| 俄罗斯LNG | {{RU_SUPPLY_2025}} | {{RU_SUPPLY_Q1}} | {{RU_SUPPLY_2026}} | {{RU_SUPPLY_CHANGE}} |
| 其他 | {{OTHER_SUPPLY_2025}} | {{OTHER_SUPPLY_Q1}} | {{OTHER_SUPPLY_2026}} | {{OTHER_SUPPLY_CHANGE}} |
| **总供给** | {{TOTAL_SUPPLY_2025}} | {{TOTAL_SUPPLY_Q1}} | {{TOTAL_SUPPLY_2026}} | {{TOTAL_SUPPLY_CHANGE}} |
| | | | | |
| **需求** | | | | |
| 中国 | {{CN_DEMAND_2025}} | {{CN_DEMAND_Q1}} | {{CN_DEMAND_2026}} | {{CN_DEMAND_CHANGE}} |
| 日本 | {{JP_DEMAND_2025}} | {{JP_DEMAND_Q1}} | {{JP_DEMAND_2026}} | {{JP_DEMAND_CHANGE}} |
| 韩国 | {{KR_DEMAND_2025}} | {{KR_DEMAND_Q1}} | {{KR_DEMAND_2026}} | {{KR_DEMAND_CHANGE}} |
| 欧洲 | {{EU_DEMAND_2025}} | {{EU_DEMAND_Q1}} | {{EU_DEMAND_2026}} | {{EU_DEMAND_CHANGE}} |
| 其他 | {{OTHER_DEMAND_2025}} | {{OTHER_DEMAND_Q1}} | {{OTHER_DEMAND_2026}} | {{OTHER_DEMAND_CHANGE}} |
| **总需求** | {{TOTAL_DEMAND_2025}} | {{TOTAL_DEMAND_Q1}} | {{TOTAL_DEMAND_2026}} | {{TOTAL_DEMAND_CHANGE}} |
| | | | | |
| **供需缺口** | {{GAP_2025}} | {{GAP_Q1}} | {{GAP_2026}} | {{GAP_CHANGE}} |

### 7.3 库存信号解读
{{INVENTORY_SIGNAL_INTERPRETATION}}

---

## 第八章：风险与展望

### 8.1 地缘政治风险

| 风险因素 | 影响程度 | 概率 | 说明 |
|----------|----------|------|------|
| {{GEOPOLITICAL_RISK_1}} | {{RISK_1_IMPACT}} | {{RISK_1_PROBABILITY}} | {{RISK_1_DESC}} |
| {{GEOPOLITICAL_RISK_2}} | {{RISK_2_IMPACT}} | {{RISK_2_PROBABILITY}} | {{RISK_2_DESC}} |
| {{GEOPOLITICAL_RISK_3}} | {{RISK_3_IMPACT}} | {{RISK_3_PROBABILITY}} | {{RISK_3_DESC}} |

### 8.2 宏观经济风险
{{MACROECONOMIC_RISKS}}

### 8.3 价格预测区间

| 品种 | 短期(1个月) | 中期(3个月) | 长期(6个月) |
|------|-------------|-------------|-------------|
| Brent | {{BRENT_SHORT}} | {{BRENT_MEDIUM}} | {{BRENT_LONG}} |
| JKM | {{JKM_SHORT}} | {{JKM_MEDIUM}} | {{JKM_LONG}} |
| 国内液厂 | {{FACTORY_SHORT}} | {{FACTORY_MEDIUM}} | {{FACTORY_LONG}} |

### 8.4 投资建议
{{INVESTMENT_RECOMMENDATIONS}}

---

## 第九章：数据附录

### 9.1 数据来源说明

| 助理 | 数据类型 | 主要来源 | 备用来源 | 验证来源 |
|------|----------|----------|----------|----------|
| 原油 | 原油价格 | {{CRUDE_PRIMARY_SOURCE}} | {{CRUDE_BACKUP_SOURCE}} | {{CRUDE_VERIFY_SOURCE}} |
| 海明 | 国际气价 | {{INTL_PRIMARY_SOURCE}} | {{INTL_BACKUP_SOURCE}} | {{INTL_VERIFY_SOURCE}} |
| 润仓 | 国内价格 | {{DOMESTIC_PRIMARY_SOURCE}} | {{DOMESTIC_BACKUP_SOURCE}} | {{DOMESTIC_VERIFY_SOURCE}} |
| 欧风 | 欧洲库存 | {{EU_PRIMARY_SOURCE}} | {{EU_BACKUP_SOURCE}} | {{EU_VERIFY_SOURCE}} |
| 洋基 | 美国数据 | {{US_PRIMARY_SOURCE}} | {{US_BACKUP_SOURCE}} | {{US_VERIFY_SOURCE}} |

### 9.2 置信度评级表

| 助理 | 数据类型 | 置信度 | 评分 | 主要依据 |
|------|----------|--------|------|----------|
| 原油 | 原油价格 | {{CRUDE_CONFIDENCE}} | {{CRUDE_SCORE}} | {{CRUDE_SCORE_REASON}} |
| 海明 | 国际气价 | {{INTL_CONFIDENCE}} | {{INTL_SCORE}} | {{INTL_SCORE_REASON}} |
| 润仓 | 国内价格 | {{DOMESTIC_CONFIDENCE}} | {{DOMESTIC_SCORE}} | {{DOMESTIC_SCORE_REASON}} |
| 欧风 | 欧洲库存 | {{EU_CONFIDENCE}} | {{EU_SCORE}} | {{EU_SCORE_REASON}} |
| 洋基 | 美国数据 | {{US_CONFIDENCE}} | {{US_SCORE}} | {{US_SCORE_REASON}} |

### 9.3 审核报告

**审核评分**: {{AUDIT_SCORE}}分  
**审核结论**: {{AUDIT_RESULT}}  
**审核时间**: {{AUDIT_TIME}}

#### 主要问题
{{AUDIT_ISSUES}}

#### 改进建议
{{AUDIT_RECOMMENDATIONS}}

### 9.4 术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| JKM | Japan-Korea Marker | 日韩基准LNG价格 |
| TTF | Title Transfer Facility | 荷兰天然气交易中心 |
| Henry Hub | - | 美国天然气定价基准 |
| Backwardation | - | 现货溢价（近月>远月） |
| Contango | - | 期货溢价（远月>近月） |
| DES | Delivered Ex Ship | 到岸交货 |
| FOB | Free On Board | 离岸交货 |

---

## 🆕 第十章：纵横分析

> **本章基于 AutoClaw 专家共创 Skills「纵横分析法」设计**
> 
> **核心理念**：横向扫描（广度）× 纵向挖掘（深度）= 结构化洞察

---

### 10.1 横向扫描：多维度市场全景

#### 10.1.1 能源比价矩阵
**跨市场对比：原油 / LNG / 煤炭 / 电力**

| 能源品种 | 价格 | 单位 | 热值比价 | LNG替代吸引力 |
|----------|------|------|----------|---------------|
| Brent原油 | ${{BRENT_PRICE}} | 美元/桶 | {{OIL_HEAT_VALUE}} | {{OIL_LNG_ATTRACTION}} |
| JKM LNG | ${{JKM_PRICE}} | 美元/百万英热 | {{LNG_HEAT_VALUE}} | 基准 |
| 纽卡斯尔煤炭 | ${{COAL_PRICE}} | 美元/吨 | {{COAL_HEAT_VALUE}} | {{COAL_LNG_ATTRACTION}} |
| 欧洲电力 | ${{POWER_PRICE}} | 欧元/兆瓦时 | {{POWER_HEAT_VALUE}} | {{POWER_LNG_ATTRACTION}} |

**比价结论**: {{ENERGY_COMPARISON_CONCLUSION}}

---

#### 10.1.2 全球价差地图
**跨地域对比：JKM / TTF / Henry Hub 三角套利**

```
当前价差三角:
                    JKM ${{JKM_PRICE}}
                   /    \
                  /      \
         ${{JKM_TTF_SPREAD}}   ${{JKM_HH_SPREAD}}
                /          \
               /            \
        TTF €{{TTF_PRICE}} ———— Henry Hub ${{HH_PRICE}}
                  ${{TTF_HH_SPREAD}}
```

| 价差路径 | 当前值 | 历史均值 | 偏离度 | 套利机会 |
|----------|--------|----------|--------|----------|
| JKM - TTF | ${{JKM_TTF_SPREAD}} | $1.5 | {{JKM_TTF_DEVIATION}} | {{JKM_TTF_ARBITRAGE}} |
| JKM - HH | ${{JKM_HH_SPREAD}} | $12 | {{JKM_HH_DEVIATION}} | {{JKM_HH_ARBITRAGE}} |
| TTF - HH | ${{TTF_HH_SPREAD}} | $10 | {{TTF_HH_DEVIATION}} | {{TTF_HH_ARBITRAGE}} |

**区域流动方向**: {{REGIONAL_FLOW_DIRECTION}}

---

#### 10.1.3 时间维度对比
**跨时间对比：日 / 周 / 月 / 季 / 年趋势**

| 时间维度 | Brent | JKM | 国内液厂 | 趋势一致性 |
|----------|-------|-----|----------|------------|
| 日环比 | {{BRENT_DAILY}} | {{JKM_DAILY}} | {{FACTORY_DAILY}} | {{DAILY_CONSISTENCY}} |
| 周环比 | {{BRENT_WEEKLY}} | {{JKM_WEEKLY}} | {{FACTORY_WEEKLY}} | {{WEEKLY_CONSISTENCY}} |
| 月环比 | {{BRENT_MONTHLY}} | {{JKM_MONTHLY}} | {{FACTORY_MONTHLY}} | {{MONTHLY_CONSISTENCY}} |
| 季同比 | {{BRENT_QUARTERLY}} | {{JKM_QUARTERLY}} | {{FACTORY_QUARTERLY}} | {{QUARTERLY_CONSISTENCY}} |
| 年同比 | {{BRENT_YEARLY}} | {{JKM_YEARLY}} | {{FACTORY_YEARLY}} | {{YEARLY_CONSISTENCY}} |

**时间维度结论**: {{TIME_DIMENSION_CONCLUSION}}

---

#### 10.1.4 多源数据一致性验证
**同一指标多来源交叉验证**

| 指标 | EIA API | TradingView | 其他来源 | 一致性 | 可信度 |
|------|---------|-------------|----------|--------|--------|
| Brent价格 | ${{BRENT_EIA}} | ${{BRENT_TV}} | ${{BRENT_OTHER}} | {{BRENT_CONSISTENCY}} | {{BRENT_RELIABILITY}} |
| WTI价格 | ${{WTI_EIA}} | ${{WTI_TV}} | ${{WTI_OTHER}} | {{WTI_CONSISTENCY}} | {{WTI_RELIABILITY}} |
| 美国库存 | {{US_INV_EIA}} | {{US_INV_OTHER}} | - | {{US_INV_CONSISTENCY}} | {{US_INV_RELIABILITY}} |
| 国内液厂价 | {{FACTORY_MYSTEEL}} | {{FACTORY_LNG168}} | {{FACTORY_LONGZHONG}} | {{FACTORY_CONSISTENCY}} | {{FACTORY_RELIABILITY}} |

**数据质量评估**: {{DATA_QUALITY_ASSESSMENT}}

---

### 10.2 纵向挖掘：历史与因果

#### 10.2.1 历史周期回溯
**3年 / 5年 / 10年季节性规律**

| 指标 | 当前值 | 3年均值 | 5年均值 | 10年均值 | 历史分位 |
|------|--------|---------|---------|----------|----------|
| Brent | ${{BRENT_PRICE}} | ${{BRENT_3Y_AVG}} | ${{BRENT_5Y_AVG}} | ${{BRENT_10Y_AVG}} | {{BRENT_PERCENTILE}} |
| JKM | ${{JKM_PRICE}} | ${{JKM_3Y_AVG}} | ${{JKM_5Y_AVG}} | ${{JKM_10Y_AVG}} | {{JKM_PERCENTILE}} |
| 国内液厂 | {{FACTORY_PRICE}} | {{FACTORY_3Y_AVG}} | {{FACTORY_5Y_AVG}} | {{FACTORY_10Y_AVG}} | {{FACTORY_PERCENTILE}} |

**季节性规律**:
- **春季(3-5月)**: {{SPRING_PATTERN}}
- **夏季(6-8月)**: {{SUMMER_PATTERN}}
- **秋季(9-11月)**: {{AUTUMN_PATTERN}}
- **冬季(12-2月)**: {{WINTER_PATTERN}}

**历史极端值对比**:
- 当前 vs 历史最高: {{CURRENT_VS_MAX}}
- 当前 vs 历史最低: {{CURRENT_VS_MIN}}
- 当前 vs 疫情前(2019): {{CURRENT_VS_2019}}

---

#### 10.2.2 因果链条拆解
**五因子传导模型：价格 ← 供需 ← 库存 ← 宏观**

```
宏观层: GDP增速 {{GDP_GROWTH}}% → 工业产出 {{INDUSTRIAL_OUTPUT}}%
    ↓
需求层: 全球需求 {{GLOBAL_DEMAND}} → 中国进口 {{CHINA_IMPORT}}
    ↓
供给层: OPEC+产量 {{OPEC_PRODUCTION}} → 美国出口 {{US_EXPORT}}
    ↓
库存层: 美国库存 {{US_INVENTORY}} → 欧洲库存 {{EU_INVENTORY}}
    ↓
价格层: Brent ${{BRENT_PRICE}} → JKM ${{JKM_PRICE}} → 国内 {{FACTORY_PRICE}}
```

**传导时滞分析**:
| 因果链条 | 传导时滞 | 当前状态 | 预测影响 |
|----------|----------|----------|----------|
| 宏观→需求 | 3-6个月 | {{MACRO_DEMAND_STATUS}} | {{MACRO_DEMAND_IMPACT}} |
| 需求→库存 | 1-2个月 | {{DEMAND_INVENTORY_STATUS}} | {{DEMAND_INVENTORY_IMPACT}} |
| 库存→价格 | 即时-2周 | {{INVENTORY_PRICE_STATUS}} | {{INVENTORY_PRICE_IMPACT}} |
| 国际→国内 | 2-4周 | {{INTL_DOMESTIC_STATUS}} | {{INTL_DOMESTIC_IMPACT}} |

---

#### 10.2.3 趋势推演预测
**短期 / 中期 / 长期预测**

| 预测维度 | 驱动因素 | 预测区间 | 置信度 | 关键假设 |
|----------|----------|----------|--------|----------|
| **短期(1个月)** | {{SHORT_DRIVER}} | {{SHORT_RANGE}} | {{SHORT_CONFIDENCE}} | {{SHORT_ASSUMPTION}} |
| **中期(3个月)** | {{MEDIUM_DRIVER}} | {{MEDIUM_RANGE}} | {{MEDIUM_CONFIDENCE}} | {{MEDIUM_ASSUMPTION}} |
| **长期(6个月)** | {{LONG_DRIVER}} | {{LONG_RANGE}} | {{LONG_CONFIDENCE}} | {{LONG_ASSUMPTION}} |

**情景分析**:
| 情景 | 概率 | 价格预测 | 触发条件 |
|------|------|----------|----------|
| 乐观 | {{BULL_PROB}}% | {{BULL_PRICE}} | {{BULL_TRIGGER}} |
| 基准 | {{BASE_PROB}}% | {{BASE_PRICE}} | {{BASE_TRIGGER}} |
| 悲观 | {{BEAR_PROB}}% | {{BEAR_PRICE}} | {{BEAR_TRIGGER}} |

---

#### 10.2.4 关键转折点识别
**异常信号与拐点预警**

| 监测指标 | 当前值 | 阈值 | 偏离度 | 信号强度 |
|----------|--------|------|--------|----------|
| 期限结构 | {{TERM_STRUCTURE}} | 正常/异常 | {{TERM_DEVIATION}} | {{TERM_SIGNAL}} |
| 库存天数 | {{INVENTORY_DAYS}} | 正常范围 | {{INVENTORY_DEVIATION}} | {{INVENTORY_SIGNAL}} |
| 价差极端值 | {{SPREAD_EXTREME}} | 历史区间 | {{SPREAD_DEVIATION}} | {{SPREAD_SIGNAL}} |
| 波动率 | {{VOLATILITY}} | 均值 | {{VOL_DEVIATION}} | {{VOL_SIGNAL}} |

**潜在转折点**:
1. {{TURNING_POINT_1}} (概率: {{TP1_PROB}}%)
2. {{TURNING_POINT_2}} (概率: {{TP2_PROB}}%)
3. {{TURNING_POINT_3}} (概率: {{TP3_PROB}}%)

---

### 10.3 纵横交叉：核心洞察

#### 10.3.1 矛盾点发现
**横向 vs 纵向冲突识别**

| 矛盾点 | 横向信号 | 纵向信号 | 冲突解释 | 优先级 |
|--------|----------|----------|----------|--------|
| {{CONTRADICTION_1}} | {{HORIZONTAL_1}} | {{VERTICAL_1}} | {{EXPLANATION_1}} | {{PRIORITY_1}} |
| {{CONTRADICTION_2}} | {{HORIZONTAL_2}} | {{VERTICAL_2}} | {{EXPLANATION_2}} | {{PRIORITY_2}} |
| {{CONTRADICTION_3}} | {{HORIZONTAL_3}} | {{VERTICAL_3}} | {{EXPLANATION_3}} | {{PRIORITY_3}} |

**矛盾调和结论**: {{CONTRADICTION_RESOLUTION}}

---

#### 10.3.2 确定性排序
**高 / 中 / 低置信度分类**

| 置信度 | 判断 | 依据 | 可执行性 |
|--------|------|------|----------|
| **🔴 高确定性** | {{HIGH_CERTAINTY_1}} | {{HIGH_EVIDENCE_1}} | {{HIGH_ACTION_1}} |
| | {{HIGH_CERTAINTY_2}} | {{HIGH_EVIDENCE_2}} | {{HIGH_ACTION_2}} |
| **🟡 中确定性** | {{MEDIUM_CERTAINTY_1}} | {{MEDIUM_EVIDENCE_1}} | {{MEDIUM_ACTION_1}} |
| | {{MEDIUM_CERTAINTY_2}} | {{MEDIUM_EVIDENCE_2}} | {{MEDIUM_ACTION_2}} |
| **🟢 低确定性** | {{LOW_CERTAINTY_1}} | {{LOW_EVIDENCE_1}} | {{LOW_ACTION_1}} |
| | {{LOW_CERTAINTY_2}} | {{LOW_EVIDENCE_2}} | {{LOW_ACTION_2}} |

---

#### 10.3.3 可执行建议
**基于纵横分析的决策建议**

| 建议类型 | 具体建议 | 适用场景 | 风险提示 |
|----------|----------|----------|----------|
| **采购策略** | {{PROCUREMENT_ADVICE}} | {{PROCUREMENT_SCENARIO}} | {{PROCUREMENT_RISK}} |
| **库存管理** | {{INVENTORY_ADVICE}} | {{INVENTORY_SCENARIO}} | {{INVENTORY_RISK}} |
| **价格对冲** | {{HEDGE_ADVICE}} | {{HEDGE_SCENARIO}} | {{HEDGE_RISK}} |
| **市场时机** | {{TIMING_ADVICE}} | {{TIMING_SCENARIO}} | {{TIMING_RISK}} |

---

### 10.4 纵横分析总结

**核心结论**:
> {{CROSS_ANALYSIS_CORE_CONCLUSION}}

**关键数据支撑**:
- 横向扫描发现: {{HORIZONTAL_FINDING}}
- 纵向挖掘发现: {{VERTICAL_FINDING}}
- 纵横交叉洞察: {{CROSS_INSIGHT}}

**下一步监测重点**:
1. {{MONITORING_PRIORITY_1}}
2. {{MONITORING_PRIORITY_2}}
3. {{MONITORING_PRIORITY_3}}

---

*报告生成时间: {{GENERATION_TIME}}*  
*版本: v6.3.1-纵横版 | 架构: 主会话直采 + 纵横分析法 | 标准: IEA/EIA*  
*数据采集: 12助理并行 | 审核: 自动审核 + 纵横交叉验证*  
*新增: 第十章 纵横分析（基于 AutoClaw 专家共创方法论）*
