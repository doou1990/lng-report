# LNG搜索策略优化技能
# LNG Search Strategy Optimization Skill
# 版本: 1.0
# 创建时间: 2026-04-18

---
name: "LNG搜索策略优化"
version: "1.0"
created: "2026-04-18"
updated: "2026-04-18"
trigger: "搜索成功率 < 80% 或连续失败"
auto_approval: true  # 关键词优化自动批准
---

## 优化流程

### 触发条件
1. 单次搜索失败（无结果或结果不可用）
2. 连续 3 天同一数据项搜索成功率 < 80%
3. 用户反馈搜索结果不满意

### 优化策略

#### 策略 1: 关键词扩展
**原始关键词 → 扩展关键词**

| 数据项 | 原始关键词 | 扩展后关键词 | 原理 |
|--------|-----------|-------------|------|
| 浙江LNG | "浙江LNG价格" | "浙江LNG 宁波 舟山 接收站 今日价格" | 增加具体地点 |
| JKM | "JKM价格" | "JKM LNG price today $/MMBtu" | 英文+单位 |
| TTF期货 | "TTF期货" | "TTF gas futures ICE €/MWh" | 交易所+单位 |
| Henry Hub | "Henry Hub" | "Henry Hub Natural Gas Futures CME" | 完整名称+交易所 |

#### 策略 2: 同义词替换
建立 LNG 领域同义词库：

```yaml
同义词库:
  LNG:
    - 液化天然气
    - LNG
    - 液化天然气价格
  
  接收站:
    - LNG终端
    - 接收站
    - 码头
    - 气化站
  
  出厂价:
    - 工厂价
    - 液厂价
    - 出厂价格
    - 出厂报价
```

#### 策略 3: 时间限定优化
- 失败时自动添加时间限定："今日"、"最新"、"2026年"
- 优先使用 "today"、"latest" 英文关键词（国际数据）

#### 策略 4: 来源限定
- 失败时限定权威来源："site:oilchem.net"、"site:mysteel.com"
- 公众号搜索：限定 "LNG天然气平台"、"LNG行业信息"

## 关键词进化记录

### 成功案例

| 数据项 | 原始关键词 | 优化后关键词 | 成功率 | 优化日期 |
|--------|-----------|-------------|--------|----------|
| JKM现货 | "JKM价格" | "JKM LNG price today $/MMBtu" | 70%→92% | 2026-04-12 |
| TTF期货 | "TTF价格" | "TTF gas futures ICE €/MWh" | 65%→88% | 2026-04-12 |
| 宁波价格 | "宁波LNG" | "中海油宁波 LNG 接收站 价格" | 60%→85% | 2026-04-15 |
| Henry Hub | "Henry Hub" | "Henry Hub Natural Gas spot price" | 55%→82% | 2026-04-15 |

### 失败案例分析

| 数据项 | 尝试关键词 | 失败原因 | 改进方向 |
|--------|-----------|----------|----------|
| 温州LNG | "温州LNG价格" | 数据公开度低 | 转向浙能官网 |
| 中国库存 | "中国LNG库存" | 无权威公开源 | 使用估算模型 |

## 当前优化关键词库（v6.3）

| 数据项 | 优化关键词 | 成功率 | 最后更新 |
|--------|-----------|--------|----------|
| Brent现货 | "Brent crude oil price today USD barrel" | 95% | 2026-04-12 |
| WTI现货 | "WTI crude oil price today USD barrel" | 95% | 2026-04-12 |
| JKM现货 | "JKM LNG price today $/MMBtu" | 92% | 2026-04-12 |
| TTF现货 | "TTF natural gas price today €/MWh" | 88% | 2026-04-12 |
| Henry Hub现货 | "Henry Hub Natural Gas spot price $/MMBtu" | 82% | 2026-04-15 |
| 宁波接收站 | "中海油宁波 LNG 接收站 价格 元/吨" | 85% | 2026-04-15 |
| 舟山接收站 | "舟山 LNG 接收站 新奥 价格" | 80% | 2026-04-15 |
| 全国出厂均价 | "LNG出厂价格 全国均价 今日" | 75% | 2026-04-12 |

## 优化规则引擎

```python
# 伪代码：关键词优化决策
if search_success_rate < 0.8:
    if fail_reason == "no_results":
        # 扩展关键词
        new_keyword = expand_keywords(original_keyword)
    elif fail_reason == "outdated":
        # 添加时间限定
        new_keyword = add_time_limit(original_keyword)
    elif fail_reason == "irrelevant":
        # 添加来源限定
        new_keyword = add_source_limit(original_keyword)
    
    # 测试新关键词
    test_result = test_search(new_keyword)
    if test_result.success_rate > 0.8:
        update_keyword_library(data_item, new_keyword)
        log_optimization(data_item, original_keyword, new_keyword)
```

## 变更日志

### v1.0 (2026-04-18)
- 初始版本创建
- 建立 4 种优化策略
- 记录历史成功案例
