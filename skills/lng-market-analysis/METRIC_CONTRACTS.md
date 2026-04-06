# Metric Contract定义 v4.0

## 什么是Metric Contract

Metric Contract是数据指标的正式定义，确保：
1. 所有人对指标的理解一致
2. 数据来源和计算方式透明
3. 历史对比有效
4. 异常检测准确

---

## 核心指标定义

### 1. Brent原油价格

```yaml
指标名称: Brent原油价格
英文名称: Brent Crude Oil Price
指标编码: OIL_BRENT_USD

定义:
  实体: 北海布伦特原油
  粒度: 日度现货价格
  单位: 美元/桶 (USD/barrel)
  
计算方式:
  分子: Brent现货交易价格
  分母: 1
  时间窗口: 交易日收盘价格
  时区: UTC
  
数据源:
  主要: EIA (美国能源信息署)
  备用: Reuters, Bloomberg, TradingEconomics
  
过滤条件:
  - 排除非交易日数据
  - 排除明显异常值(>3σ)
  
更新频率: 每日
延迟时间: T-1日

历史范围: 1987年至今

置信度评估:
  A级: EIA官方数据
  B级: Reuters/Bloomberg
  C级: 其他金融数据平台
```

### 2. WTI原油价格

```yaml
指标名称: WTI原油价格
英文名称: West Texas Intermediate Crude Oil Price
指标编码: OIL_WTI_USD

定义:
  实体: 西德克萨斯中质原油
  粒度: 日度现货价格
  单位: 美元/桶 (USD/barrel)
  
计算方式:
  分子: WTI现货交易价格
  分母: 1
  时间窗口: 交易日收盘价格
  时区: UTC-6 (美国中部时间)
  
数据源:
  主要: EIA
  备用: CME, Reuters, Bloomberg
  
过滤条件:
  - 排除非交易日数据
  - 排除明显异常值(>3σ)
  
更新频率: 每日
延迟时间: T-1日

历史范围: 1983年至今

置信度评估:
  A级: EIA官方数据
  B级: CME期货价格
  C级: 其他金融数据平台
```

### 3. 国内LNG市场均价

```yaml
指标名称: 国内LNG市场均价
英文名称: China LNG Market Average Price
指标编码: LNG_CN_AVG_CNY

定义:
  实体: 中国境内LNG工厂和接收站
  粒度: 日度市场均价
  单位: 元/吨 (CNY/ton)
  
计算方式:
  分子: 所有有效报价的总和
  分母: 有效报价数量
  时间窗口: 交易日
  时区: Asia/Shanghai
  
数据源:
  主要: LNG物联网 (lng168.com)
  备用: Mysteel, 隆众资讯, 生意社
  
覆盖范围:
  - 液厂: 全国133家LNG工厂
  - 接收站: 全国19家LNG接收站
  - 区域: 华北、华东、华南、华中、西南、西北、东北
  
过滤条件:
  - 排除检修/停产工厂
  - 排除明显异常值(>3σ)
  - 排除节假日无效报价
  
更新频率: 每日
延迟时间: T日或T-1日

历史范围: 2020年至今

置信度评估:
  A级: ≥3个来源一致，差异<3%
  B级: 2-3个来源，差异3-5%
  C级: 1-2个来源，差异5-10%
  D级: 无数据或差异>10%

注意事项:
  - 不同平台统计口径可能不同
  - 节假日市场休市，使用前一日数据
  - 浙江专区价格通常高于全国均价
```

### 4. 浙江专区LNG价格

```yaml
指标名称: 浙江专区LNG价格
英文名称: Zhejiang Region LNG Price
指标编码: LNG_ZJ_AVG_CNY

定义:
  实体: 浙江及周边地区LNG接收站
  粒度: 日度挂牌价格
  单位: 元/吨 (CNY/ton)
  
计算方式:
  分子: 各接收站挂牌价格
  分母: 接收站数量
  时间窗口: 交易日
  时区: Asia/Shanghai
  
覆盖接收站:
  1. 中海油宁波 (优先级★★★★★)
  2. 新奥舟山 (优先级★★★★★)
  3. 宁波北仑 (优先级★★★★☆)
  4. 嘉兴平湖 (优先级★★★★☆)
  5. 上海五号沟 (优先级★★★★☆)
  
数据源:
  主要: LNG物联网
  备用: 隆众资讯, Mysteel快讯
  
过滤条件:
  - 仅包含华东区域接收站
  - 排除长期停报站点
  - 区分省内/省外报价(如有)
  
更新频率: 每日
延迟时间: T-1日至T-3日

历史范围: 2020年至今

置信度评估:
  A级: 全部5个接收站有数据
  B级: 3-4个接收站有数据
  C级: 1-2个接收站有数据
  D级: 无数据

注意事项:
  - 中海油宁波通常为华东地区最高价
  - 部分接收站区分省内/省外报价
  - Mysteel详细数据需订阅
```

### 5. JKM LNG价格

```yaml
指标名称: JKM LNG价格
英文名称: Japan Korea Marker LNG Price
指标编码: LNG_JKM_USD

定义:
  实体: 东北亚LNG现货价格
  粒度: 日度评估价格
  单位: 美元/百万英热单位 (USD/MMBtu)
  
计算方式:
  分子: Platts评估的东北亚LNG现货价格
  分母: 1
  时间窗口: 每日评估
  时区: Singapore Time (SGT)
  
数据源:
  主要: Platts (需订阅)
  备用: LNGPriceIndex.com, Investing.com, CME期货
  
过滤条件:
  - 基于实际交易和报价评估
  - 排除异常交易(>2σ)
  
更新频率: 每日
延迟时间: T日

历史范围: 2009年至今

置信度评估:
  A级: Platts官方评估
  B级: LNGPriceIndex.com, CME期货
  C级: Investing.com, 其他平台
  D级: 无数据

注意事项:
  - Platts为行业基准，但需付费订阅
  - 免费替代源存在1-2天延迟
  - 期货价格与现货价格可能存在差异
```

### 6. TTF天然气价格

```yaml
指标名称: TTF天然气价格
英文名称: Title Transfer Facility Natural Gas Price
指标编码: GAS_TTF_EUR

定义:
  实体: 荷兰TTF天然气期货价格
  粒度: 日度期货结算价
  单位: 欧元/兆瓦时 (EUR/MWh)
  
计算方式:
  分子: TTF期货合约结算价格
  分母: 1
  时间窗口: 交易日收盘
  时区: CET/CEST (欧洲中部时间)
  
数据源:
  主要: ICE交易所
  备用: OilPriceAPI.com, TradingNews, TradingEconomics
  
过滤条件:
  - 排除非交易日数据
  - 排除合约切换期异常
  
更新频率: 每日
延迟时间: T-1日

历史范围: 2003年至今

置信度评估:
  A级: ICE官方数据
  B级: OilPriceAPI.com
  C级: TradingNews, TradingEconomics
  D级: 无数据

注意事项:
  - TTF为欧洲天然气基准价格
  - 受地缘政治和季节因素影响大
  - 价格波动可能剧烈
```

### 7. Henry Hub天然气价格

```yaml
指标名称: Henry Hub天然气价格
英文名称: Henry Hub Natural Gas Price
指标编码: GAS_HH_USD

定义:
  实体: 美国Henry Hub天然气现货价格
  粒度: 日度现货价格
  单位: 美元/百万英热单位 (USD/MMBtu)
  
计算方式:
  分子: Henry Hub现货交易价格
  分母: 1
  时间窗口: 交易日
  时区: UTC-6 (美国中部时间)
  
数据源:
  主要: EIA
  备用: CME, TradingNews, Natural Gas Intelligence
  
过滤条件:
  - 排除非交易日数据
  - 排除管道维护期异常
  
更新频率: 每日
延迟时间: T-1日

历史范围: 1997年至今

置信度评估:
  A级: EIA官方数据
  B级: CME期货价格
  C级: TradingNews, NGI
  D级: 无数据

注意事项:
  - Henry Hub为北美天然气基准
  - 受库存、天气、产量影响
  - 价格波动相对TTF较小
```

### 8. LNG开工率

```yaml
指标名称: LNG开工率
英文名称: LNG Plant Operating Rate
指标编码: LNG_OP_RATE_PCT

定义:
  实体: 中国LNG工厂开工情况
  粒度: 日度统计
  单位: 百分比 (%)
  
计算方式:
  分子: 实际开工工厂数量
  分母: 总工厂数量 - 长期停产工厂
  时间窗口: 每日统计
  时区: Asia/Shanghai
  
数据源:
  主要: LNG物联网
  备用: Mysteel, 隆众资讯
  
覆盖范围:
  - 全国133家LNG工厂
  - 排除检修/停产/内销工厂
  
更新频率: 每日
延迟时间: T日

历史范围: 2020年至今

置信度评估:
  A级: LNG物联网
  B级: Mysteel/隆众
  C级: 其他平台
  D级: 无数据

注意事项:
  - 开工率反映供应端情况
  - 检修季开工率通常下降
  - 与价格呈负相关关系
```

---

## 指标关系图

```
原油价格 (Brent/WTI)
    ↓ 影响
LNG生产成本
    ↓ 影响
国际LNG价格 (JKM)
    ↓ 影响
中国LNG进口成本
    ↓ 影响
国内LNG价格 (液厂+接收站)
    ↓ 分化
浙江专区价格 (华东高端市场)

Henry Hub (美国气价)
    ↓ 影响
美国LNG出口竞争力
    ↓ 影响
全球LNG供应格局

TTF (欧洲气价)
    ↓ 影响
欧亚LNG价差
    ↓ 影响
中国LNG进口来源选择

开工率
    ↓ 反映
国内供应情况
    ↓ 影响
国内价格波动
```

---

## 指标使用指南

### 报告中的指标呈现

```markdown
## 核心指标一览

| 指标 | 数值 | 单位 | 置信度 | 数据来源 |
|------|------|------|--------|----------|
| Brent原油 | $102.01 | USD/barrel | A | EIA |
| WTI原油 | $90.84 | USD/barrel | A | EIA |
| 国内LNG均价 | 4,813 | CNY/ton | B | LNG物联网 |
| 浙江专区均价 | 5,370 | CNY/ton | B | LNG物联网 |
| JKM | $18.75 | USD/MMBtu | B | LNGPriceIndex |
| TTF | €54.24 | EUR/MWh | B | OilPriceAPI |
| Henry Hub | $3.05 | USD/MMBtu | A | EIA |
| 开工率 | 47% | % | A | LNG物联网 |

**置信度说明**:
- A: 官方/权威数据源，高可信度
- B: 多源验证，中等可信度
- C: 单源或低时效，需谨慎使用
- D: 数据缺失，不可用
```

---

*Metric Contract v4.0 | 确保数据一致性和可比性*
