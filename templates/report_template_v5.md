# LNG原油市场日报 - 标准模板（v5.0）

**报告日期**: {{DATE}}  
**报告版本**: v5.0  
**审核评分**: {{AUDIT_SCORE}}分 ({{AUDIT_RESULT}})  
**数据完整度**: {{COMPLETENESS}}%  
**执行模式**: Planner-Generator-Evaluator

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

*报告生成时间: {{GENERATION_TIME}}*  
*版本: v5.0 | 架构: Planner-Generator-Evaluator | 标准: IEA/EIA*  
*数据采集: 12助理并行 | 审核: Evaluator*
