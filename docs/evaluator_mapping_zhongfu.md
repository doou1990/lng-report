# 中孚经验 → Evaluator评估层映射文档

**版本**: v5.0  
**创建时间**: 2026-04-09  
**目标**: 将中孚的审核经验系统化映射到Evaluator评估层

---

## 一、中孚核心能力分析

### 1.1 中孚的历史审核经验

根据历史审核记录，中孚的核心能力包括：

| 能力 | 描述 | 频率 |
|------|------|------|
| **数据完整性检查** | 检查必采数据是否齐全 | 每次 |
| **多源交叉验证** | 对比多个来源的数据一致性 | 每次 |
| **异常值检测** | 识别价格异常、逻辑矛盾 | 每次 |
| **置信度评级** | A/B/C/D四级评级 | 每次 |
| **时效性检查** | 确认数据更新时间 | 每次 |
| **来源可追溯性** | 验证数据来源URL | 每次 |
| **问题清单生成** | 列出所有数据问题 | 每次 |
| **改进建议** | 提供具体改进方案 | 每次 |

### 1.2 中孚的审核流程（历史）

```
中孚审核流程 (v4.9.2)
│
├── 1. 数据完整性检查
│   ├── 检查10位助理数据是否全部返回
│   ├── 检查必采项是否齐全
│   └── 标记缺失数据
│
├── 2. 数据质量评估
│   ├── 多源对比（同一指标≥2来源）
│   ├── 异常值检测（差异>5%标注）
│   ├── 时效性检查（优先3日内数据）
│   └── 来源验证（URL可访问性）
│
├── 3. 置信度评级
│   ├── A级：官方数据，高可信度
│   ├── B级：市场报价，中等可信度
│   ├── C级：估算数据，需谨慎参考
│   └── D级：备用数据源，标注来源
│
├── 4. 评分计算
│   ├── 数据完整度 (0-100分)
│   ├── 数据质量分 (0-100分)
│   └── 综合评分 = 加权平均
│
├── 5. 审核结论
│   ├── 通过 (≥75分)
│   ├── 有条件通过 (60-74分)
│   └── 不通过 (<60分)
│
└── 6. 输出审核报告
    ├── 问题清单
    ├── 改进建议
    └── 置信度评级表
```

---

## 二、映射到Evaluator评估层

### 2.1 架构对比

| 层级 | v4.9.2 (中孚) | v5.0 (Evaluator) | 映射关系 |
|------|---------------|------------------|----------|
| **定位** | 独立审核助理 | 评估层核心组件 | 1:1映射 |
| **输入** | 10助理数据 | Generator输出 | 相同 |
| **输出** | 审核报告 | 评估报告+反馈 | 增强 |
| **评级** | A/B/C/D | A/B/C/D + 0-100分 | 细化 |
| **反馈** | 单向报告 | 双向反馈循环 | 升级 |

### 2.2 能力映射表

| 中孚能力 | Evaluator实现 | 技术方案 | 优先级 |
|----------|---------------|----------|--------|
| 数据完整性检查 | `check_completeness()` | 必采项清单比对 | P0 |
| 多源交叉验证 | `cross_validation()` | 差异度计算算法 | P0 |
| 异常值检测 | `detect_anomalies()` | 统计异常检测 | P0 |
| 置信度评级 | `rate_confidence()` | 四级评级+评分细则 | P0 |
| 时效性检查 | `check_freshness()` | 时间戳对比 | P1 |
| 来源可追溯 | `verify_sources()` | URL可达性检测 | P1 |
| 问题清单生成 | `generate_issues()` | 结构化问题输出 | P0 |
| 改进建议 | `suggest_improvements()` | 基于规则的推荐 | P1 |

---

## 三、Evaluator评估层设计

### 3.1 评估维度 (基于中孚经验扩展)

```python
class Evaluator:
    """
    Evaluator评估层 - 基于中孚经验系统化
    """
    
    # 评估维度权重 (基于历史审核经验优化)
    DIMENSION_WEIGHTS = {
        'data_source': 0.25,      # 数据来源 (中孚: 官方>市场>估算)
        'freshness': 0.20,        # 时效性 (中孚: 优先3日内)
        'multi_source': 0.25,     # 多源验证 (中孚: ≥2来源)
        'completeness': 0.20,     # 完整性 (中孚: 必采项检查)
        'traceability': 0.10      # 可追溯性 (中孚: URL验证)
    }
    
    # 置信度评级标准 (中孚标准细化)
    CONFIDENCE_LEVELS = {
        'A': {'min_score': 90, 'description': '官方统计，经审计'},
        'B': {'min_score': 75, 'description': '官方估算/权威行业'},
        'C': {'min_score': 60, 'description': '行业调查/模型估算'},
        'D': {'min_score': 0,  'description': '单一来源/未验证'}
    }
```

### 3.2 评估流程 (系统化中孚流程)

```
Evaluator评估流程 (v5.0)
│
├── 1. 输入接收
│   └── 接收Generator输出的market_data_v5.json
│
├── 2. 预检查 (Pre-check)
│   ├── 检查JSON格式有效性
│   ├── 检查必填字段存在性
│   └── 检查数据类型正确性
│
├── 3. 完整性评估 (Completeness)
│   ├── 加载必采项清单 (必采数据+浙江专区)
│   ├── 逐项检查存在性
│   ├── 计算完整度百分比
│   └── 标记缺失项
│
├── 4. 质量评估 (Quality)
│   ├── 4.1 数据来源评估
│   │   ├── A级来源: +25分 (EIA/IEA/海关)
│   │   ├── B级来源: +20分 (Platts/ICIS)
│   │   ├── C级来源: +15分 (行业估算)
│   │   └── D级来源: +10分 (单一媒体)
│   │
│   ├── 4.2 时效性评估
│   │   ├── 当日数据: +20分
│   │   ├── 3日内数据: +15分
│   │   ├── 周内数据: +10分
│   │   └── 过时数据: +5分
│   │
│   ├── 4.3 多源验证评估
│   │   ├── ≥3个来源: +25分
│   │   ├── 2个来源: +20分
│   │   ├── 1个来源: +10分
│   │   └── 无验证: +5分
│   │
│   ├── 4.4 可追溯性评估
│   │   ├── URL+时间戳: +10分
│   │   ├── 有来源说明: +5分
│   │   └── 无来源: +0分
│   │
│   └── 4.5 异常检测
│       ├── 价格倒挂检测 (WTI>Brent)
│       ├── 极端值检测 (>3σ)
│       ├── 逻辑矛盾检测
│       └── 单位一致性检查
│
├── 5. 评分计算 (Scoring)
│   ├── 各维度得分 × 权重
│   ├── 异常扣分
│   └── 总分 = Σ(维度得分) - 异常扣分
│
├── 6. 评级确定 (Rating)
│   ├── 总分≥90: A级
│   ├── 总分≥75: B级
│   ├── 总分≥60: C级
│   └── 总分<60: D级
│
├── 7. 问题生成 (Issue Generation)
│   ├── 完整性问题
│   ├── 质量问题
│   ├── 异常问题
│   └── 改进建议
│
├── 8. 反馈输出 (Feedback)
│   ├── 审核评分报告
│   ├── 问题清单
│   ├── 改进建议
│   └── 反馈给Planner (如果需要重采)
│
└── 9. 记忆存储 (Memory)
    ├── 存储审核结果到MemPalace
    └── 记录常见问题模式
```

---

## 四、中孚经验规则库

### 4.1 异常检测规则 (基于历史审核)

```python
ANOMALY_RULES = {
    # 价格倒挂检测 (中孚发现的问题)
    'price_inversion': {
        'description': 'WTI价格高于Brent',
        'condition': 'WTI > Brent',
        'severity': 'high',
        'action': '标注异常，调查原因'
    },
    
    # 极端价格检测
    'extreme_price': {
        'description': '价格偏离历史均值3σ',
        'condition': '|price - mean| > 3 * std',
        'severity': 'medium',
        'action': '标注异常，确认数据源'
    },
    
    # 单位不一致检测
    'unit_mismatch': {
        'description': 'JKM单位不明确',
        'condition': 'unit not in [$/MMBtu, $/mmbtu]',
        'severity': 'medium',
        'action': '要求明确单位'
    },
    
    # 多源差异检测 (中孚标准)
    'source_discrepancy': {
        'description': '多来源差异>5%',
        'condition': 'max_diff > 5%',
        'severity': 'medium',
        'action': '标注差异，降低置信度'
    },
    
    # 时效性问题
    'stale_data': {
        'description': '数据超过7天',
        'condition': 'age > 7 days',
        'severity': 'low',
        'action': '标注时效性，建议更新'
    }
}
```

### 4.2 必采项清单 (中孚标准固化)

```python
REQUIRED_DATA = {
    'crude_oil': {
        'brent_price': {'required': True, 'sources': 2},
        'wti_price': {'required': True, 'sources': 2},
        'brent_wti_spread': {'required': False, 'sources': 1}
    },
    'lng_international': {
        'jkm_price': {'required': True, 'sources': 2},
        'ttf_price': {'required': True, 'sources': 2},
        'henry_hub_price': {'required': True, 'sources': 2}
    },
    'lng_domestic': {
        'factory_avg_price': {'required': True, 'sources': 2},
        'terminal_avg_price': {'required': True, 'sources': 2},
        'operating_rate': {'required': True, 'sources': 1}
    },
    'zhejiang_zone': {
        'ningbo_price': {'required': True, 'sources': 1},
        'zhoushan_price': {'required': True, 'sources': 1},
        'shanghai_price': {'required': True, 'sources': 1},
        'wenzhou_price': {'required': False, 'sources': 1}
    },
    'inventory': {
        'us_inventory': {'required': False, 'sources': 1},
        'eu_inventory': {'required': False, 'sources': 1},
        'cn_inventory': {'required': False, 'sources': 1}
    }
}
```

---

## 五、Evaluator输出格式

### 5.1 审核报告模板

```json
{
  "audit_report": {
    "version": "5.0",
    "audit_time": "2026-04-09T21:15:00+08:00",
    "evaluator": "Evaluator-v5.0",
    
    "overall": {
      "score": 84,
      "level": "B",
      "result": "有条件通过",
      "completeness": "90%"
    },
    
    "dimensions": {
      "data_source": {
        "score": 20,
        "max": 25,
        "weight": 0.25,
        "details": "A级数据30%, B级数据50%"
      },
      "freshness": {
        "score": 18,
        "max": 20,
        "weight": 0.20,
        "details": "80%数据为3日内"
      },
      "multi_source": {
        "score": 15,
        "max": 25,
        "weight": 0.25,
        "details": "仅60%数据有多源验证"
      },
      "completeness": {
        "score": 18,
        "max": 20,
        "weight": 0.20,
        "details": "缺少中国库存数据"
      },
      "traceability": {
        "score": 10,
        "max": 10,
        "weight": 0.10,
        "details": "所有数据有来源标注"
      }
    },
    
    "issues": [
      {
        "id": "ISS-001",
        "type": "anomaly",
        "severity": "high",
        "title": "WTI>Brent价格倒挂",
        "description": "WTI($99.00) > Brent($98.30)，异常倒挂",
        "affected_data": ["crude.wti", "crude.brent"],
        "suggestion": "调查美国内陆供应紧张或物流瓶颈原因"
      },
      {
        "id": "ISS-002",
        "type": "quality",
        "severity": "medium",
        "title": "JKM单位不明确",
        "description": "JKM价格单位未明确标注",
        "affected_data": ["lng.jkm"],
        "suggestion": "明确标注为$/MMBtu或其他单位"
      },
      {
        "id": "ISS-003",
        "type": "completeness",
        "severity": "medium",
        "title": "缺少中国LNG库存数据",
        "description": "必采项中库存数据缺失",
        "affected_data": ["inventory.cn"],
        "suggestion": "补充中国LNG库存数据源"
      }
    ],
    
    "recommendations": [
      "建立价格异常预警机制",
      "强化多源验证流程",
      "补充中国库存数据源",
      "统一单位标注规范"
    ],
    
    "confidence_ratings": {
      "crude": {"level": "B", "score": 82},
      "lng_intl": {"level": "C", "score": 65},
      "lng_domestic": {"level": "B", "score": 78},
      "inventory": {"level": "B", "score": 75}
    },
    
    "feedback_to_planner": {
      "need_recollect": false,
      "priority_issues": ["ISS-001"],
      "notes": "数据整体可用，建议标注异常后生成报告"
    }
  }
}
```

---

## 六、与Planner的反馈循环

### 6.1 反馈机制

```
Evaluator → Planner 反馈循环
│
├── 情况1: 审核通过 (≥75分)
│   └── 反馈: {"action": "proceed", "notes": "数据质量良好"}
│
├── 情况2: 有条件通过 (60-74分)
│   └── 反馈: {"action": "proceed_with_warning", 
│              "issues": [...], 
│              "notes": "标注问题后生成报告"}
│
└── 情况3: 审核不通过 (<60分)
    └── 反馈: {"action": "recollect", 
               "priority_issues": [...],
               "notes": "关键数据缺失，需要重新采集"}
```

### 6.2 记忆学习

```python
# Evaluator学习机制
def learn_from_audit(audit_result):
    """
    从审核结果中学习，优化未来评估
    """
    # 存储常见问题模式
    mempalace.store({
        "issue_type": audit_result.issue_type,
        "pattern": audit_result.pattern,
        "solution": audit_result.solution
    }, category="audit_patterns")
    
    # 更新数据源可靠性评分
    for source in audit_result.sources:
        update_source_reliability(source.name, source.accuracy)
```

---

## 七、实施计划

### 7.1 开发优先级

| 阶段 | 功能 | 优先级 | 预计时间 |
|------|------|--------|----------|
| P0 | 完整性检查 | 高 | 1天 |
| P0 | 多源验证 | 高 | 1天 |
| P0 | 评分计算 | 高 | 1天 |
| P1 | 异常检测 | 中 | 2天 |
| P1 | 反馈循环 | 中 | 1天 |
| P2 | 记忆学习 | 低 | 2天 |

### 7.2 测试验证

```python
# 测试用例 (基于历史审核记录)
TEST_CASES = [
    {
        "name": "2026-04-09正常数据",
        "expected_score": 84,
        "expected_level": "B",
        "expected_issues": ["WTI>Brent", "JKM单位不明"]
    },
    {
        "name": "数据缺失场景",
        "expected_score": 55,
        "expected_level": "D",
        "expected_action": "recollect"
    }
]
```

---

## 八、总结

### 中孚经验 → Evaluator映射完成

| 中孚经验 | Evaluator实现 | 状态 |
|----------|---------------|------|
| 四级置信度评级 | `rate_confidence()` + 0-100分细则 | ✅ 映射完成 |
| 必采项检查 | `check_completeness()` | ✅ 映射完成 |
| 多源交叉验证 | `cross_validation()` | ✅ 映射完成 |
| 异常值检测 | `detect_anomalies()` | ✅ 映射完成 |
| 问题清单生成 | `generate_issues()` | ✅ 映射完成 |
| 改进建议 | `suggest_improvements()` | ✅ 映射完成 |
| 审核报告 | 结构化JSON输出 | ✅ 映射完成 |
| 反馈循环 | 与Planner双向通信 | ✅ 映射完成 |

**核心升级**: 从中孚的"人工审核" → Evaluator的"系统化评估"

---

*文档版本: v1.0*  
*映射完成时间: 2026-04-09*  
*下一步: 开发Evaluator代码实现*
