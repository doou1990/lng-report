# LNG原油市场日报 - 全融合模板（v6.3.1-FULL）
# 纵横分析法贯穿全报告

**报告日期**: {{DATE}}  
**报告版本**: v6.3.1-FULL（纵横全融合版）  
**审核评分**: {{AUDIT_SCORE}}分 ({{AUDIT_RESULT}})  
**数据完整度**: {{COMPLETENESS}}%  
**执行模式**: 主会话直采 + 纵横分析法（全融合）

---

## 第一章：执行摘要（纵横概览）

### 1.1 核心结论
1. {{CONCLUSION_1}}
2. {{CONCLUSION_2}}
3. {{CONCLUSION_3}}
4. {{CONCLUSION_4}}
5. {{CONCLUSION_5}}

### 1.2 纵横视角速览

#### 横向扫描（广度）
| 维度 | 关键发现 | 异常信号 |
|------|----------|----------|
| 跨市场 | {{CROSS_MARKET_FINDING}} | {{CROSS_MARKET_ALERT}} |
| 跨地域 | {{CROSS_REGION_FINDING}} | {{CROSS_REGION_ALERT}} |
| 跨时间 | {{CROSS_TIME_FINDING}} | {{CROSS_TIME_ALERT}} |

#### 纵向挖掘（深度）
| 维度 | 关键发现 | 趋势判断 |
|------|----------|----------|
| 历史周期 | {{HISTORICAL_FINDING}} | {{HISTORICAL_TREND}} |
| 因果传导 | {{CAUSAL_FINDING}} | {{CAUSAL_TREND}} |
| 预测推演 | {{FORECAST_FINDING}} | {{FORECAST_TREND}} |

### 1.3 关键数据一览

| 类别 | 指标 | 数值 | 涨跌 | 置信度 |
|------|------|------|------|--------|
| **原油** | Brent | ${{BRENT_PRICE}} | {{BRENT_CHANGE}} | {{BRENT_CONFIDENCE}} |
| | WTI | ${{WTI_PRICE}} | {{WTI_CHANGE}} | {{WTI_CONFIDENCE}} |
| **国际LNG** | JKM | ${{JKM_PRICE}} | {{JKM_CHANGE}} | {{JKM_CONFIDENCE}} |
| | TTF | €{{TTF_PRICE}} | {{TTF_CHANGE}} | {{TTF_CONFIDENCE}} |
| | Henry Hub | ${{HH_PRICE}} | {{HH_CHANGE}} | {{HH_CONFIDENCE}} |
| **国内LNG** | 液厂均价 | {{FACTORY_PRICE}}元/吨 | {{FACTORY_CHANGE}} | {{FACTORY_CONFIDENCE}} |
| | 接收站均价 | {{TERMINAL_PRICE}}元/吨 | {{TERMINAL_CHANGE}} | {{TERMINAL_CONFIDENCE}} |

### 1.4 风险提示
- ⚠️ {{RISK_1}}
- ⚠️ {{RISK_2}}
- ⚠️ {{RISK_3}}

---

## 第二章：市场概况（纵横全景）

### 2.1 横向：全球多市场对比

#### 2.1.1 能源市场联动
| 市场 | 当前价格 | 周变化 | 月变化 | 与LNG相关性 |
|------|----------|--------|--------|-------------|
| Brent原油 | ${{BRENT_PRICE}} | {{BRENT_WEEKLY}} | {{BRENT_MONTHLY}} | {{BRENT_CORRELATION}} |
| JKM LNG | ${{JKM_PRICE}} | {{JKM_WEEKLY}} | {{JKM_MONTHLY}} | 1.00 |
| 纽卡斯尔煤炭 | ${{COAL_PRICE}} | {{COAL_WEEKLY}} | {{COAL_MONTHLY}} | {{COAL_CORRELATION}} |
| 欧洲电力 | ${{POWER_PRICE}} | {{POWER_WEEKLY}} | {{POWER_MONTHLY}} | {{POWER_CORRELATION}} |

**联动分析**: {{MARKET_LINKAGE_ANALYSIS}}

#### 2.1.2 地域市场对比
| 区域 | 基准价格 | 溢价/折价 | 驱动因素 |
|------|----------|-----------|----------|
| 亚洲 | JKM ${{JKM_PRICE}} | 基准 | {{ASIA_DRIVER}} |
| 欧洲 | TTF €{{TTF_PRICE}} | {{EUROPE_PREMIUM}} | {{EUROPE_DRIVER}} |
| 北美 | HH ${{HH_PRICE}} | {{NORTH_AMERICA_DISCOUNT}} | {{NA_DRIVER}} |
| 中国 | 液厂{{FACTORY_PRICE}} | {{CHINA_PREMIUM}} | {{CHINA_DRIVER}} |

### 2.2 纵向：历史演变脉络

#### 2.2.1 年度趋势回顾
```
价格演变（近5年）:
2021: Brent $70 → JKM $15 → 国内 4500
2022: Brent $95 → JKM $25 → 国内 6800 (俄乌冲突)
2023: Brent $82 → JKM $18 → 国内 5200
2024: Brent $79 → JKM $16 → 国内 4800
2025: Brent {{BRENT_2025}} → JKM {{JKM_2025}} → 国内 {{FACTORY_2025}}
当前: Brent ${{BRENT_PRICE}} → JKM ${{JKM_PRICE}} → 国内 {{FACTORY_PRICE}}
```

#### 2.2.2 周期位置判断
| 指标 | 当前值 | 周期位置 | 历史分位 | 趋势方向 |
|------|--------|----------|----------|----------|
| Brent | ${{BRENT_PRICE}} | {{BRENT_CYCLE}} | {{BRENT_PERCENTILE}} | {{BRENT_DIRECTION}} |
| JKM | ${{JKM_PRICE}} | {{JKM_CYCLE}} | {{JKM_PERCENTILE}} | {{JKM_DIRECTION}} |
| 国内液厂 | {{FACTORY_PRICE}} | {{FACTORY_CYCLE}} | {{FACTORY_PERCENTILE}} | {{FACTORY_DIRECTION}} |

### 2.3 关键事件影响
| 事件 | 影响 | 持续时间 | 纵横评估 |
|------|------|----------|----------|
| {{EVENT_1}} | {{IMPACT_1}} | {{DURATION_1}} | {{EVENT_1_CROSS}} |
| {{EVENT_2}} | {{IMPACT_2}} | {{DURATION_2}} | {{EVENT_2_CROSS}} |
| {{EVENT_3}} | {{IMPACT_3}} | {{DURATION_3}} | {{EVENT_3_CROSS}} |

---

## 第三章：原油价格分析（纵横深度）

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

#### 3.2.1 纵向：期限结构历史演变
| 时间 | 近月 | 3月 | 6月 | 12月 | 结构类型 |
|------|------|-----|-----|------|----------|
| 当前 | ${{FRONT_MONTH_PRICE}} | ${{M3_PRICE}} | ${{M6_PRICE}} | ${{M12_PRICE}} | {{TERM_STRUCTURE}} |
| 1月前 | ${{FRONT_MONTH_PRICE_1M}} | ${{M3_PRICE_1M}} | ${{M6_PRICE_1M}} | ${{M12_PRICE_1M}} | {{TERM_STRUCTURE_1M}} |
| 3月前 | ${{FRONT_MONTH_PRICE_3M}} | ${{M3_PRICE_3M}} | ${{M6_PRICE_3M}} | ${{M12_PRICE_3M}} | {{TERM_STRUCTURE_3M}} |
| 1年前 | ${{FRONT_MONTH_PRICE_1Y}} | ${{M3_PRICE_1Y}} | ${{M6_PRICE_1Y}} | ${{M12_PRICE_1Y}} | {{TERM_STRUCTURE_1Y}} |

**演变趋势**: {{TERM_STRUCTURE_TREND}}

### 3.3 横向：跨区价差与跨能源比价

#### 3.3.1 跨区价差
| 价差 | 当前值 | 正常范围 | 偏离度 | 解读 |
|------|--------|----------|--------|------|
| Brent-WTI | ${{BRENT_WTI_SPREAD}} | $0-5 | {{BRENT_WTI_DEVIATION}} | {{BRENT_WTI_COMMENT}} |
| Brent-Dubai | ${{BRENT_DUBAI_SPREAD}} | $0-3 | {{BRENT_DUBAI_DEVIATION}} | {{BRENT_DUBAI_COMMENT}} |

#### 3.3.2 跨能源比价（横向）
| 比价 | 当前值 | 历史均值 | 偏离度 | LNG替代吸引力 |
|------|--------|----------|--------|---------------|
| 原油/LNG | {{OIL_LNG_RATIO}} | {{OIL_LNG_HISTORICAL}} | {{OIL_LNG_DEVIATION}} | {{OIL_LNG_ATTRACTION}} |
| 煤炭/LNG | {{COAL_LNG_RATIO}} | {{COAL_LNG_HISTORICAL}} | {{COAL_LNG_DEVIATION}} | {{COAL_LNG_ATTRACTION}} |

### 3.4 驱动因素分析（五因子模型 + 纵向传导）

| 因子 | 指标 | 当前值 | 影响 | 评分 | 传导时滞 | 趋势 |
|------|------|--------|------|------|----------|------|
| **需求因子** | 全球GDP增速 | {{GLOBAL_GDP}} | {{DEMAND_IMPACT}} | {{DEMAND_SCORE}}/25 | 3-6月 | {{DEMAND_TREND}} |
| **供给因子** | OPEC+产量 | {{OPEC_PRODUCTION}} | {{SUPPLY_IMPACT}} | {{SUPPLY_SCORE}}/25 | 即时 | {{SUPPLY_TREND}} |
| **库存因子** | EIA商业库存 | {{EIA_INVENTORY}} | {{INVENTORY_IMPACT}} | {{INVENTORY_SCORE}}/25 | 1-2月 | {{INVENTORY_TREND}} |
| **美元因子** | 美元指数 | {{DXY}} | {{DOLLAR_IMPACT}} | {{DOLLAR_SCORE}}/25 | 即时 | {{DOLLAR_TREND}} |
| **风险因子** | VIX指数 | {{VIX}} | {{RISK_IMPACT}} | {{RISK_SCORE}}/25 | 即时 | {{RISK_TREND}} |

#### 3.4.1 纵向：五因子历史传导路径
```
当前传导路径:
GDP {{GLOBAL_GDP}}% → 需求 {{DEMAND_IMPACT}} → 库存 {{INVENTORY_CHANGE}} → 价格 ${{BRENT_PRICE}}

历史对比:
2022年: GDP 3.2% → 需求强劲 → 库存下降 → 价格 $95
2023年: GDP 2.8% → 需求平稳 → 库存回升 → 价格 $82
当前: GDP {{GLOBAL_GDP}}% → {{DEMAND_STATUS}} → {{INVENTORY_STATUS}} → 价格 ${{BRENT_PRICE}}
```

---

## 第四章：LNG价格分析（纵横深度）

### 4.1 国际LNG价格

| 市场 | 价格 | 单位 | 涨跌 | 置信度 | 来源 |
|------|------|------|------|--------|------|
| JKM | ${{JKM_PRICE}} | 美元/百万英热 | {{JKM_CHANGE}} | {{JKM_CONFIDENCE}} | {{JKM_SOURCE}} |
| TTF | €{{TTF_PRICE}} | 欧元/兆瓦时 | {{TTF_CHANGE}} | {{TTF_CONFIDENCE}} | {{TTF_SOURCE}} |
| Henry Hub | ${{HH_PRICE}} | 美元/百万英热 | {{HH_CHANGE}} | {{HH_CONFIDENCE}} | {{HH_SOURCE}} |

#### 4.1.1 横向：全球价差三角
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

套利机会: {{ARBITRAGE_OPPORTUNITY}}
```

#### 4.1.2 纵向：历史极端值对比
| 指标 | 当前 | 1年前 | 3年前 | 历史最高 | 历史最低 |
|------|------|-------|-------|----------|----------|
| JKM | ${{JKM_PRICE}} | ${{JKM_1Y}} | ${{JKM_3Y}} | ${{JKM_MAX}} | ${{JKM_MIN}} |
| TTF | €{{TTF_PRICE}} | €{{TTF_1Y}} | €{{TTF_3Y}} | €{{TTF_MAX}} | €{{TTF_MIN}} |
| HH | ${{HH_PRICE}} | ${{HH_1Y}} | ${{HH_3Y}} | ${{HH_MAX}} | ${{HH_MIN}} |

### 4.2 国内LNG价格

#### 4.2.1 液厂价格（横向：区域对比）
| 区域 | 均价 | 涨跌 | 与全国均价差 | 驱动因素 |
|------|------|------|--------------|----------|
| 西北 | {{NORTHWEST_PRICE}} | {{NORTHWEST_CHANGE}} | {{NORTHWEST_SPREAD}} | {{NORTHWEST_DRIVER}} |
| 华北 | {{NORTH_PRICE}} | {{NORTH_CHANGE}} | {{NORTH_SPREAD}} | {{NORTH_DRIVER}} |
| 华东 | {{EAST_PRICE}} | {{EAST_CHANGE}} | {{EAST_SPREAD}} | {{EAST_DRIVER}} |
| 华南 | {{SOUTH_PRICE}} | {{SOUTH_CHANGE}} | {{SOUTH_SPREAD}} | {{SOUTH_DRIVER}} |

#### 4.2.2 接收站价格（纵向：历史趋势）
| 接收站 | 当前 | 1月前 | 3月前 | 1年前 | 趋势 |
|--------|------|-------|-------|-------|------|
| 宁波中海油 | {{NINGBO_PRICE}} | {{NINGBO_1M}} | {{NINGBO_3M}} | {{NINGBO_1Y}} | {{NINGBO_TREND}} |
| 舟山新奥 | {{ZHOUSHAN_PRICE}} | {{ZHOUSHAN_1M}} | {{ZHOUSHAN_3M}} | {{ZHOUSHAN_1Y}} | {{ZHOUSHAN_TREND}} |
| 上海五号沟 | {{SHANGHAI_PRICE}} | {{SHANGHAI_1M}} | {{SHANGHAI_3M}} | {{SHANGHAI_1Y}} | {{SHANGHAI_TREND}} |
| 浙能温州 | {{WENZHOU_PRICE}} | {{WENZHOU_1M}} | {{WENZHOU_3M}} | {{WENZHOU_1Y}} | {{WENZHOU_TREND}} |

### 4.3 区域价差分析（横向）

| 价差 | 当前值 | 正常范围 | 解读 |
|------|--------|----------|------|
| JKM-TTF | ${{JKM_TTF_SPREAD}} | $0-2 | {{JKM_TTF_COMMENT}} |
| 液厂-接收站 | {{FACTORY_TERMINAL_SPREAD}}元/吨 | 800-1000 | {{FACTORY_TERMINAL_COMMENT}} |
| 华东-西北 | {{EAST_NORTHWEST_SPREAD}}元/吨 | 300-500 | {{EAST_NORTHWEST_COMMENT}} |

---

## 第五章：供给分析（纵横深度）

### 5.1 横向：全球产能分布
| 国家 | 产量 | 产能利用率 | 全球占比 | 同比变化 |
|------|------|------------|----------|----------|
| 美国 | {{US_PRODUCTION}} | {{US_UTILIZATION}} | {{US_SHARE}}% | {{US_YOY}} |
| 卡塔尔 | {{QA_PRODUCTION}} | {{QA_UTILIZATION}} | {{QA_SHARE}}% | {{QA_YOY}} |
| 澳大利亚 | {{AU_PRODUCTION}} | {{AU_UTILIZATION}} | {{AU_SHARE}}% | {{AU_YOY}} |
| 俄罗斯 | {{RU_PRODUCTION}} | {{RU_UTILIZATION}} | {{RU_SHARE}}% | {{RU_YOY}} |

### 5.2 纵向：产能建设周期
| 国家 | 当前产能 | 在建产能 | 预计投产 | 产能趋势 |
|------|----------|----------|----------|----------|
| 美国 | {{US_CURRENT}} | {{US_UNDER_CONSTRUCTION}} | {{US_COMING_ONLINE}} | {{US_TREND}} |
| 卡塔尔 | {{QA_CURRENT}} | {{QA_UNDER_CONSTRUCTION}} | {{QA_COMING_ONLINE}} | {{QA_TREND}} |

### 5.3 供应风险因素（纵横评估）
| 风险因素 | 影响程度 | 概率 | 时间维度 | 地域维度 |
|----------|----------|------|----------|----------|
| {{SUPPLY_RISK_1}} | {{RISK_1_IMPACT}} | {{RISK_1_PROB}} | {{RISK_1_TIME}} | {{RISK_1_REGION}} |
| {{SUPPLY_RISK_2}} | {{RISK_2_IMPACT}} | {{RISK_2_PROB}} | {{RISK_2_TIME}} | {{RISK_2_REGION}} |

---

## 第六章：需求分析（纵横深度）

### 6.1 横向：全球需求分布
| 区域 | 需求量 | 全球占比 | 同比变化 | 季节性 |
|------|--------|----------|----------|--------|
| 中国 | {{CN_DEMAND}} | {{CN_SHARE}}% | {{CN_YOY}} | {{CN_SEASONAL}} |
| 日本 | {{JP_DEMAND}} | {{JP_SHARE}}% | {{JP_YOY}} | {{JP_SEASONAL}} |
| 韩国 | {{KR_DEMAND}} | {{KR_SHARE}}% | {{KR_YOY}} | {{KR_SEASONAL}} |
| 欧洲 | {{EU_DEMAND}} | {{EU_SHARE}}% | {{EU_YOY}} | {{EU_SEASONAL}} |

### 6.2 纵向：中国进口历史演变
| 指标 | 当前 | 1年前 | 3年前 | 趋势 |
|------|------|-------|-------|------|
| 月度进口量 | {{CHINA_IMPORT_VOLUME}} | {{CHINA_IMPORT_1Y}} | {{CHINA_IMPORT_3Y}} | {{CHINA_IMPORT_TREND}} |
| 进口均价 | {{CHINA_IMPORT_PRICE}} | {{CHINA_PRICE_1Y}} | {{CHINA_PRICE_3Y}} | {{CHINA_PRICE_TREND}} |
| 澳大利亚占比 | {{AUSTRALIA_SHARE}}% | {{AUSTRALIA_SHARE_1Y}}% | {{AUSTRALIA_SHARE_3Y}}% | {{AUSTRALIA_TREND}} |

### 6.3 季节性因素（纵向规律）
| 季节 | 历史需求特征 | 当前偏离 | 预期 |
|------|--------------|----------|------|
| 春季(3-5月) | {{SPRING_HISTORICAL}} | {{SPRING_DEVIATION}} | {{SPRING_FORECAST}} |
| 夏季(6-8月) | {{SUMMER_HISTORICAL}} | {{SUMMER_DEVIATION}} | {{SUMMER_FORECAST}} |
| 秋季(9-11月) | {{AUTUMN_HISTORICAL}} | {{AUTUMN_DEVIATION}} | {{AUTUMN_FORECAST}} |
| 冬季(12-2月) | {{WINTER_HISTORICAL}} | {{WINTER_DEVIATION}} | {{WINTER_FORECAST}} |

---

## 第七章：库存与平衡（纵横深度）

### 7.1 横向：全球库存对比
| 区域 | 库存量 | 库存率 | 同比变化 | 状态 |
|------|--------|--------|----------|------|
| 美国 | {{US_INVENTORY}} | {{US_INVENTORY_RATE}} | {{US_INVENTORY_CHANGE}} | {{US_INVENTORY_STATUS}} |
| 欧洲 | {{EU_INVENTORY}} | {{EU_INVENTORY_RATE}} | {{EU_INVENTORY_CHANGE}} | {{EU_INVENTORY_STATUS}} |
| 中国 | {{CN_INVENTORY}} | {{CN_INVENTORY_RATE}} | {{CN_INVENTORY_CHANGE}} | {{CN_INVENTORY_STATUS}} |

### 7.2 纵向：库存历史周期
| 区域 | 当前 | 1年前 | 3年均值 | 5年均值 | 历史分位 |
|------|------|-------|---------|---------|----------|
| 美国 | {{US_INVENTORY}} | {{US_INV_1Y}} | {{US_INV_3Y_AVG}} | {{US_INV_5Y_AVG}} | {{US_INV_PERCENTILE}} |
| 欧洲 | {{EU_INVENTORY}} | {{EU_INV_1Y}} | {{EU_INV_3Y_AVG}} | {{EU_INV_5Y_AVG}} | {{EU_INV_PERCENTILE}} |
| 中国 | {{CN_INVENTORY}} | {{CN_INV_1Y}} | {{CN_INV_3Y_AVG}} | {{CN_INV_5Y_AVG}} | {{CN_INV_PERCENTILE}} |

### 7.3 供需平衡表（纵横交叉）
| 项目 | 2025年 | 2026年(Q1) | 2026年(预测) | 同比变化 | 趋势 |
|------|--------|------------|--------------|----------|------|
| **总供给** | {{TOTAL_SUPPLY_2025}} | {{TOTAL_SUPPLY_Q1}} | {{TOTAL_SUPPLY_2026}} | {{TOTAL_SUPPLY_CHANGE}} | {{SUPPLY_TREND}} |
| **总需求** | {{TOTAL_DEMAND_2025}} | {{TOTAL_DEMAND_Q1}} | {{TOTAL_DEMAND_2026}} | {{TOTAL_DEMAND_CHANGE}} | {{DEMAND_TREND}} |
| **供需缺口** | {{GAP_2025}} | {{GAP_Q1}} | {{GAP_2026}} | {{GAP_CHANGE}} | {{GAP_TREND}} |

---

## 第八章：风险与展望（纵横预测）

### 8.1 地缘政治风险（纵横评估）
| 风险因素 | 影响程度 | 概率 | 时间维度 | 地域维度 | 连锁反应 |
|----------|----------|------|----------|----------|----------|
| {{GEOPOLITICAL_RISK_1}} | {{RISK_1_IMPACT}} | {{RISK_1_PROB}} | {{RISK_1_TIME}} | {{RISK_1_REGION}} | {{RISK_1_CHAIN}} |
| {{GEOPOLITICAL_RISK_2}} | {{RISK_2_IMPACT}} | {{RISK_2_PROB}} | {{RISK_2_TIME}} | {{RISK_2_REGION}} | {{RISK_2_CHAIN}} |

### 8.2 价格预测区间（纵横推演）

| 品种 | 短期(1月) | 中期(3月) | 长期(6月) | 置信度 | 关键假设 |
|------|-----------|-----------|-----------|--------|----------|
| Brent | {{BRENT_SHORT}} | {{BRENT_MEDIUM}} | {{BRENT_LONG}} | {{BRENT_CONFIDENCE}} | {{BRENT_ASSUMPTION}} |
| JKM | {{JKM_SHORT}} | {{JKM_MEDIUM}} | {{JKM_LONG}} | {{JKM_CONFIDENCE}} | {{JKM_ASSUMPTION}} |
| 国内液厂 | {{FACTORY_SHORT}} | {{FACTORY_MEDIUM}} | {{FACTORY_LONG}} | {{FACTORY_CONFIDENCE}} | {{FACTORY_ASSUMPTION}} |

### 8.3 情景分析（纵横交叉）
| 情景 | 概率 | 价格预测 | 触发条件 | 纵横依据 |
|------|------|----------|----------|----------|
| 乐观 | {{BULL_PROB}}% | {{BULL_PRICE}} | {{BULL_TRIGGER}} | {{BULL_CROSS}} |
| 基准 | {{BASE_PROB}}% | {{BASE_PRICE}} | {{BASE_TRIGGER}} | {{BASE_CROSS}} |
| 悲观 | {{BEAR_PROB}}% | {{BEAR_PRICE}} | {{BEAR_TRIGGER}} | {{BEAR_CROSS}} |

---

## 第九章：纵横综合洞察

### 9.1 横向扫描总结
| 维度 | 核心发现 | 异常信号 | 行动建议 |
|------|----------|----------|----------|
| 跨市场 | {{CROSS_MARKET_SUMMARY}} | {{CROSS_MARKET_ALERT}} | {{CROSS_MARKET_ACTION}} |
| 跨地域 | {{CROSS_REGION_SUMMARY}} | {{CROSS_REGION_ALERT}} | {{CROSS_REGION_ACTION}} |
| 跨时间 | {{CROSS_TIME_SUMMARY}} | {{CROSS_TIME_ALERT}} | {{CROSS_TIME_ACTION}} |

### 9.2 纵向挖掘总结
| 维度 | 核心发现 | 趋势判断 | 行动建议 |
|------|----------|----------|----------|
| 历史周期 | {{HISTORICAL_SUMMARY}} | {{HISTORICAL_TREND}} | {{HISTORICAL_ACTION}} |
| 因果传导 | {{CAUSAL_SUMMARY}} | {{CAUSAL_TREND}} | {{CAUSAL_ACTION}} |
| 预测推演 | {{FORECAST_SUMMARY}} | {{FORECAST_TREND}} | {{FORECAST_ACTION}} |

### 9.3 纵横交叉核心洞察
> {{CORE_CROSS_INSIGHT}}

**关键矛盾点**:
1. {{KEY_CONTRADICTION_1}}
2. {{KEY_CONTRADICTION_2}}

**高确定性判断**:
- {{HIGH_CERTAINTY_1}}
- {{HIGH_CERTAINTY_2}}

**监测重点**:
1. {{MONITORING_1}}
2. {{MONITORING_2}}
3. {{MONITORING_3}}

---

## 第十章：数据附录

### 10.1 数据来源说明
| 助理 | 数据类型 | 主要来源 | 备用来源 | 验证来源 |
|------|----------|----------|----------|----------|
| 原油 | 原油价格 | {{CRUDE_PRIMARY_SOURCE}} | {{CRUDE_BACKUP_SOURCE}} | {{CRUDE_VERIFY_SOURCE}} |
| 海明 | 国际气价 | {{INTL_PRIMARY_SOURCE}} | {{INTL_BACKUP_SOURCE}} | {{INTL_VERIFY_SOURCE}} |
| 润仓 | 国内价格 | {{DOMESTIC_PRIMARY_SOURCE}} | {{DOMESTIC_BACKUP_SOURCE}} | {{DOMESTIC_VERIFY_SOURCE}} |
| 欧风 | 欧洲库存 | {{EU_PRIMARY_SOURCE}} | {{EU_BACKUP_SOURCE}} | {{EU_VERIFY_SOURCE}} |
| 洋基 | 美国数据 | {{US_PRIMARY_SOURCE}} | {{US_BACKUP_SOURCE}} | {{US_VERIFY_SOURCE}} |

### 10.2 置信度评级表
| 助理 | 数据类型 | 置信度 | 评分 | 主要依据 |
|------|----------|--------|------|----------|
| 原油 | 原油价格 | {{CRUDE_CONFIDENCE}} | {{CRUDE_SCORE}} | {{CRUDE_SCORE_REASON}} |
| 海明 | 国际气价 | {{INTL_CONFIDENCE}} | {{INTL_SCORE}} | {{INTL_SCORE_REASON}} |
| 润仓 | 国内价格 | {{DOMESTIC_CONFIDENCE}} | {{DOMESTIC_SCORE}} | {{DOMESTIC_SCORE_REASON}} |
| 欧风 | 欧洲库存 | {{EU_CONFIDENCE}} | {{EU_SCORE}} | {{EU_SCORE_REASON}} |
| 洋基 | 美国数据 | {{US_CONFIDENCE}} | {{US_SCORE}} | {{US_SCORE_REASON}} |

### 10.3 审核报告
**审核评分**: {{AUDIT_SCORE}}分  
**审核结论**: {{AUDIT_RESULT}}  
**审核时间**: {{AUDIT_TIME}}

#### 主要问题
{{AUDIT_ISSUES}}

#### 改进建议
{{AUDIT_RECOMMENDATIONS}}

### 10.4 术语表
| 术语 | 英文 | 解释 |
|------|------|------|
| JKM | Japan-Korea Marker | 日韩基准LNG价格 |
| TTF | Title Transfer Facility | 荷兰天然气交易中心 |
| Henry Hub | - | 美国天然气定价基准 |
| Backwardation | - | 现货溢价（近月>远月） |
| Contango | - | 期货溢价（远月>近月） |

---

*报告生成时间: {{GENERATION_TIME}}*  
*版本: v6.3.1-FULL | 架构: 主会话直采 + 纵横分析法（全融合）| 标准: IEA/EIA*  
*数据采集: 12助理并行 | 审核: 自动审核 + 纵横交叉验证*  
*生成模式: 每周日全融合深度版*
