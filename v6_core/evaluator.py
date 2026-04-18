"""
数据质量评估器 (Evaluator)
系统化实现中孚审核流程
"""
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ConfidenceLevel(Enum):
    """置信度等级"""
    A = "A"  # 官方统计，经审计
    B = "B"  # 官方统计，估算成分
    C = "C"  # 行业调查/模型估算
    D = "D"  # 单一来源，未验证


class RatingLevel(Enum):
    """评级等级"""
    EXCELLENT = "A"  # >= 90分
    GOOD = "B"       # >= 75分
    FAIR = "C"       # >= 60分
    POOR = "D"       # < 60分


@dataclass
class Issue:
    """问题记录"""
    type: str
    severity: str  # high, medium, low
    field: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class DimensionScore:
    """维度评分"""
    name: str
    weight: float
    score: float
    max_score: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationReport:
    """评估报告"""
    timestamp: str
    total_score: float
    rating: str
    completeness: Dict[str, Any]
    quality: Dict[str, Any]
    anomalies: List[Issue]
    dimension_scores: List[DimensionScore]
    recommendations: List[str]


class DataQualityEvaluator:
    """
    数据质量评估器
    
    实现四级数据质量评级体系:
    - A级 (>=90分): 官方统计，经审计
    - B级 (>=75分): 官方统计，估算成分
    - C级 (>=60分): 行业调查/模型估算
    - D级 (<60分): 单一来源，未验证
    """
    
    # 评分权重配置
    WEIGHTS = {
        "data_source": 0.25,      # 数据来源
        "timeliness": 0.20,       # 时效性
        "multi_source": 0.25,     # 多源验证
        "completeness": 0.20,     # 数据完整性
        "traceability": 0.10      # 可追溯性
    }
    
    # 置信度分数映射
    CONFIDENCE_SCORES = {
        "A": 25,
        "B": 20,
        "C": 15,
        "D": 10
    }
    
    # 必采字段清单
    REQUIRED_FIELDS = [
        "brent_spot",
        "wti_spot",
        "jkm_price",
        "ttf_price",
        "henry_hub_price",
        "china_lng_factory",
        "china_receiving_station",
        "zhejiang_ningbo",
        "zhejiang_zhoushan",
        "shanghai_wuhaogou",
        "us_crude_inventory",
        "us_ng_inventory"
    ]
    
    # 异常检测规则
    ANOMALY_RULES = {
        "price_inversion": {
            "description": "WTI价格高于Brent",
            "check": lambda data: (
                data.get("wti_spot", {}).get("value", 0) > 
                data.get("brent_spot", {}).get("value", 0)
            ),
            "severity": "high",
            "message": "检测到价格倒挂: WTI > Brent"
        },
        "extreme_brent": {
            "description": "Brent价格异常",
            "check": lambda data: not (
                20 <= data.get("brent_spot", {}).get("value", 0) <= 200
            ),
            "severity": "high",
            "message": "Brent价格超出正常范围(20-200美元/桶)"
        },
        "extreme_wti": {
            "description": "WTI价格异常",
            "check": lambda data: not (
                20 <= data.get("wti_spot", {}).get("value", 0) <= 200
            ),
            "severity": "high",
            "message": "WTI价格超出正常范围(20-200美元/桶)"
        },
        "missing_zhejiang": {
            "description": "浙江专区数据缺失",
            "check": lambda data: not all(
                f in data and data[f].get("value") is not None
                for f in ["zhejiang_ningbo", "zhejiang_zhoushan"]
            ),
            "severity": "medium",
            "message": "浙江专区数据不完整"
        },
        "stale_data": {
            "description": "数据过时",
            "check": lambda data: any(
                self._is_stale(d.get("timestamp", ""))
                for d in data.values() if isinstance(d, dict)
            ),
            "severity": "low",
            "message": "部分数据超过7天"
        }
    }
    
    def __init__(self):
        """初始化评估器"""
        self.issues: List[Issue] = []
        self.dimension_scores: List[DimensionScore] = []
    
    def evaluate(self, market_data: Dict[str, Any]) -> EvaluationReport:
        """
        执行完整的数据质量评估
        
        Args:
            market_data: 市场数据字典
            
        Returns:
            评估报告
        """
        self.issues = []
        self.dimension_scores = []
        
        # 1. 完整性检查
        completeness = self._check_completeness(market_data)
        
        # 2. 质量评估 (各维度评分)
        quality = self._assess_quality(market_data)
        
        # 3. 异常检测
        anomalies = self._detect_anomalies(market_data)
        
        # 4. 计算总分
        total_score = self._calculate_total_score()
        
        # 5. 确定评级
        rating = self._determine_rating(total_score)
        
        # 6. 生成建议
        recommendations = self._generate_recommendations()
        
        return EvaluationReport(
            timestamp=datetime.now().isoformat(),
            total_score=total_score,
            rating=rating,
            completeness=completeness,
            quality=quality,
            anomalies=anomalies,
            dimension_scores=self.dimension_scores,
            recommendations=recommendations
        )
    
    def _check_completeness(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """检查数据完整性"""
        present = []
        missing = []
        
        for field in self.REQUIRED_FIELDS:
            if field in data and data[field].get("value") is not None:
                present.append(field)
            else:
                missing.append(field)
        
        coverage = len(present) / len(self.REQUIRED_FIELDS) if self.REQUIRED_FIELDS else 0
        
        # 浙江专区专项检查
        zhejiang_fields = ["zhejiang_ningbo", "zhejiang_zhoushan", "shanghai_wuhaogou"]
        zhejiang_present = [f for f in zhejiang_fields if f in present]
        zhejiang_coverage = len(zhejiang_present) / len(zhejiang_fields)
        
        result = {
            "total_required": len(self.REQUIRED_FIELDS),
            "present": len(present),
            "missing": missing,
            "coverage": round(coverage * 100, 2),
            "zhejiang_coverage": round(zhejiang_coverage * 100, 2),
            "zhejiang_present": zhejiang_present
        }
        
        # 记录完整性评分
        completeness_score = coverage * 100
        self.dimension_scores.append(DimensionScore(
            name="completeness",
            weight=self.WEIGHTS["completeness"],
            score=completeness_score * self.WEIGHTS["completeness"],
            max_score=100 * self.WEIGHTS["completeness"],
            details=result
        ))
        
        return result
    
    def _assess_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """评估数据质量"""
        quality_result = {}
        
        # 1. 数据来源评估
        source_score = self._assess_data_source(data)
        quality_result["data_source"] = source_score
        
        # 2. 时效性评估
        timeliness_score = self._assess_timeliness(data)
        quality_result["timeliness"] = timeliness_score
        
        # 3. 多源验证评估
        multi_source_score = self._assess_multi_source(data)
        quality_result["multi_source"] = multi_source_score
        
        # 4. 可追溯性评估
        traceability_score = self._assess_traceability(data)
        quality_result["traceability"] = traceability_score
        
        return quality_result
    
    def _assess_data_source(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """评估数据来源质量"""
        scores = []
        sources = {"A": 0, "B": 0, "C": 0, "D": 0}
        
        for field, value in data.items():
            if isinstance(value, dict):
                confidence = value.get("confidence", "D")
                score = self.CONFIDENCE_SCORES.get(confidence, 10)
                scores.append(score)
                sources[confidence] = sources.get(confidence, 0) + 1
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        result = {
            "average_score": round(avg_score, 2),
            "source_distribution": sources,
            "max_possible": 25
        }
        
        self.dimension_scores.append(DimensionScore(
            name="data_source",
            weight=self.WEIGHTS["data_source"],
            score=avg_score * self.WEIGHTS["data_source"],
            max_score=25 * self.WEIGHTS["data_source"],
            details=result
        ))
        
        return result
    
    def _assess_timeliness(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """评估数据时效性"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        scores = []
        
        for field, value in data.items():
            if isinstance(value, dict):
                timestamp = value.get("timestamp", "")
                try:
                    # 解析时间戳
                    if isinstance(timestamp, str):
                        data_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    else:
                        data_time = timestamp
                    
                    age_days = (now - data_time).days
                    
                    # 评分: 当日20分, 3日内15分, 周内10分, 过时5分
                    if age_days == 0:
                        score = 20
                    elif age_days <= 3:
                        score = 15
                    elif age_days <= 7:
                        score = 10
                    else:
                        score = 5
                    
                    scores.append(score)
                except:
                    scores.append(0)
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        result = {
            "average_score": round(avg_score, 2),
            "max_possible": 20
        }
        
        self.dimension_scores.append(DimensionScore(
            name="timeliness",
            weight=self.WEIGHTS["timeliness"],
            score=avg_score * self.WEIGHTS["timeliness"],
            max_score=20 * self.WEIGHTS["timeliness"],
            details=result
        ))
        
        return result
    
    def _assess_multi_source(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """评估多源验证情况"""
        # 简化实现：检查是否有多个不同来源的数据
        sources_per_field = {}
        
        for field, value in data.items():
            if isinstance(value, dict):
                source = value.get("source", "unknown")
                sources_per_field[field] = [source]
        
        # 统计多源验证情况
        multi_source_count = sum(1 for s in sources_per_field.values() if len(s) >= 2)
        total_fields = len(sources_per_field)
        
        if total_fields > 0:
            ratio = multi_source_count / total_fields
            # 评分: >=3源25分, 2源20分, 1源10分
            if ratio >= 0.5:
                score = 25
            elif ratio >= 0.3:
                score = 20
            else:
                score = 10
        else:
            score = 0
        
        result = {
            "multi_source_fields": multi_source_count,
            "total_fields": total_fields,
            "ratio": round(ratio * 100, 2) if total_fields > 0 else 0,
            "score": score,
            "max_possible": 25
        }
        
        self.dimension_scores.append(DimensionScore(
            name="multi_source",
            weight=self.WEIGHTS["multi_source"],
            score=score * self.WEIGHTS["multi_source"],
            max_score=25 * self.WEIGHTS["multi_source"],
            details=result
        ))
        
        return result
    
    def _assess_traceability(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """评估数据可追溯性"""
        traceable_count = 0
        total_count = 0
        
        for field, value in data.items():
            if isinstance(value, dict):
                total_count += 1
                # 检查是否有URL或详细来源信息
                if value.get("url") or value.get("notes") or value.get("source"):
                    traceable_count += 1
        
        if total_count > 0:
            ratio = traceable_count / total_count
            score = 10 if ratio >= 0.8 else (5 if ratio >= 0.5 else 0)
        else:
            score = 0
        
        result = {
            "traceable_fields": traceable_count,
            "total_fields": total_count,
            "ratio": round(ratio * 100, 2) if total_count > 0 else 0,
            "score": score,
            "max_possible": 10
        }
        
        self.dimension_scores.append(DimensionScore(
            name="traceability",
            weight=self.WEIGHTS["traceability"],
            score=score * self.WEIGHTS["traceability"],
            max_score=10 * self.WEIGHTS["traceability"],
            details=result
        ))
        
        return result
    
    def _detect_anomalies(self, data: Dict[str, Any]) -> List[Issue]:
        """检测数据异常"""
        issues = []
        
        for rule_name, rule in self.ANOMALY_RULES.items():
            try:
                if rule["check"](data):
                    issue = Issue(
                        type=rule_name,
                        severity=rule["severity"],
                        field="multiple",
                        message=rule["message"],
                        suggestion=self._get_suggestion(rule_name)
                    )
                    issues.append(issue)
                    self.issues.append(issue)
            except Exception:
                pass
        
        return issues
    
    def _get_suggestion(self, rule_name: str) -> str:
        """获取改进建议"""
        suggestions = {
            "price_inversion": "核实WTI和Brent价格数据源，检查是否为短期异常",
            "extreme_brent": "核实Brent价格数据，检查单位是否正确",
            "extreme_wti": "核实WTI价格数据，检查单位是否正确",
            "missing_zhejiang": "优先采集浙江专区数据，使用Mysteel或隆众资讯",
            "stale_data": "更新数据源，优先使用当日或3日内数据"
        }
        return suggestions.get(rule_name, "请核实数据准确性")
    
    def _calculate_total_score(self) -> float:
        """计算总分"""
        total = sum(ds.score for ds in self.dimension_scores)
        
        # 异常扣分
        for issue in self.issues:
            if issue.severity == "high":
                total -= 5
            elif issue.severity == "medium":
                total -= 3
            elif issue.severity == "low":
                total -= 1
        
        return max(0, round(total, 2))
    
    def _determine_rating(self, score: float) -> str:
        """根据分数确定评级"""
        if score >= 90:
            return RatingLevel.EXCELLENT.value
        elif score >= 75:
            return RatingLevel.GOOD.value
        elif score >= 60:
            return RatingLevel.FAIR.value
        else:
            return RatingLevel.POOR.value
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于问题生成建议
        for issue in self.issues:
            if issue.suggestion:
                recommendations.append(f"[{issue.severity.upper()}] {issue.suggestion}")
        
        # 基于评分生成建议
        for ds in self.dimension_scores:
            if ds.score < ds.max_score * 0.6:
                recommendations.append(
                    f"[IMPROVE] {ds.name}维度得分较低({ds.score:.1f}/{ds.max_score:.1f})，建议优化"
                )
        
        return list(set(recommendations))  # 去重
    
    @staticmethod
    def _is_stale(timestamp: str) -> bool:
        """检查数据是否过时(超过7天)"""
        try:
            from datetime import datetime
            data_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return (datetime.now() - data_time).days > 7
        except:
            return True
    
    def export_report(self, report: EvaluationReport, filepath: str):
        """导出评估报告"""
        data = {
            "timestamp": report.timestamp,
            "total_score": report.total_score,
            "rating": report.rating,
            "completeness": report.completeness,
            "quality": report.quality,
            "anomalies": [
                {
                    "type": i.type,
                    "severity": i.severity,
                    "field": i.field,
                    "message": i.message,
                    "suggestion": i.suggestion
                }
                for i in report.anomalies
            ],
            "dimension_scores": [
                {
                    "name": ds.name,
                    "weight": ds.weight,
                    "score": ds.score,
                    "max_score": ds.max_score
                }
                for ds in report.dimension_scores
            ],
            "recommendations": report.recommendations
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Evaluation report exported to: {filepath}")


# 便捷函数
def evaluate_market_data(data: Dict[str, Any]) -> EvaluationReport:
    """
    评估市场数据的便捷函数
    
    Args:
        data: 市场数据字典
        
    Returns:
        评估报告
    """
    evaluator = DataQualityEvaluator()
    return evaluator.evaluate(data)


if __name__ == "__main__":
    # 测试评估器
    test_data = {
        "brent_spot": {"value": 73.21, "confidence": "A", "source": "OilPriceAPI", "timestamp": "2026-04-11T10:00:00Z"},
        "wti_spot": {"value": 69.85, "confidence": "A", "source": "OilPriceAPI", "timestamp": "2026-04-11T10:00:00Z"},
        "jkm_price": {"value": 18.75, "confidence": "A", "source": "OilPriceAPI", "timestamp": "2026-04-11T10:00:00Z"},
        "ttf_price": {"value": 16.50, "confidence": "A", "source": "OilPriceAPI", "timestamp": "2026-04-11T10:00:00Z"},
        "henry_hub_price": {"value": 3.05, "confidence": "A", "source": "OilPriceAPI", "timestamp": "2026-04-11T10:00:00Z"},
    }
    
    report = evaluate_market_data(test_data)
    print(f"\nEvaluation Result:")
    print(f"  Score: {report.total_score}")
    print(f"  Rating: {report.rating}")
    print(f"  Completeness: {report.completeness.get('coverage', 0)}%")
    print(f"  Issues: {len(report.anomalies)}")
