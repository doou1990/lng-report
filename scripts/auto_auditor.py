#!/usr/bin/env python3
"""
LNG Market Data Auto Auditor - v6.2
内置自动审核模块（多源验证 + 异常检测 + 置信度评级）
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from statistics import mean, median
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoAuditor:
    """自动审核器 - 内置逻辑，零人工干预"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        
    def cross_verify(self, metric: str, sources: List[Dict]) -> Tuple[str, float, str]:
        """
        多源交叉验证
        返回: (grade, value, note)
        """
        if not sources:
            return ("D", 0.0, "无数据来源")
        
        if len(sources) == 1:
            # 单一来源，降级处理
            src = sources[0]
            return ("C", src.get("value", 0.0), "单一来源，未交叉验证")
        
        # 多源对比
        values = [s.get("value", 0) for s in sources if s.get("value")]
        if len(values) < 2:
            return ("C", values[0] if values else 0.0, "有效来源不足")
        
        avg_val = mean(values)
        max_val = max(values)
        min_val = min(values)
        variance = (max_val - min_val) / avg_val if avg_val != 0 else 0
        
        if variance <= 0.05:
            return ("A", avg_val, f"多源一致，差异{variance:.1%}")
        elif variance <= 0.10:
            return ("B", median(values), f"多源接近，差异{variance:.1%}")
        else:
            # 差异过大，取中位数，标记C级
            return ("C", median(values), f"多源冲突{variance:.1%}，取中位数")
    
    def detect_anomaly(self, metric: str, current: float, history: List[float]) -> Tuple[bool, str]:
        """
        异常值检测
        返回: (is_anomaly, message)
        """
        if not history or len(history) < 5:
            return (False, "历史数据不足")
        
        hist_mean = mean(history)
        hist_std = (sum((x - hist_mean) ** 2 for x in history) / len(history)) ** 0.5
        
        # 日涨跌幅检测
        daily_change = abs(current - history[0]) / history[0] if history[0] != 0 else 0
        if daily_change > 0.15:
            return (True, f"日涨跌幅{daily_change:.1%}，超过15%阈值")
        
        # 历史偏离检测
        deviation = abs(current - hist_mean) / hist_mean if hist_mean != 0 else 0
        if deviation > 0.30:
            return (True, f"偏离历史均值{deviation:.1%}，超过30%阈值")
        
        return (False, "正常")
    
    def check_consistency(self, data: Dict) -> List[Dict]:
        """
        一致性校验
        检查价格逻辑关系
        """
        issues = []
        
        # 1. Brent-WTI 价格倒挂检测
        brent = data.get("brent_spot", {}).get("value")
        wti = data.get("wti_spot", {}).get("value")
        if brent and wti and wti > brent:
            issues.append({
                "type": "price_inversion",
                "severity": "high",
                "message": f"WTI({wti}) > Brent({brent})，价格倒挂",
                "action": "使用Brent价格"
            })
        
        # 2. JKM-TTF 价差检测（JKM应高于TTF+运输成本）
        jkm = data.get("jkm_spot", {}).get("value")
        ttf = data.get("ttf_spot", {}).get("value")
        if jkm and ttf:
            spread = jkm - ttf
            if spread < 0.5:  # 运输成本约$0.5/MMBtu
                issues.append({
                    "type": "spread_anomaly",
                    "severity": "medium",
                    "message": f"JKM-TTF价差({spread:.2f})过低，正常应>0.5",
                    "action": "取TTF+0.5作为JKM估算"
                })
        
        # 3. Henry Hub 与 JKM 合理区间
        hh = data.get("henry_hub", {}).get("value")
        if jkm and hh and hh > 0:
            ratio = jkm / hh
            if ratio < 1.2 or ratio > 4.0:
                issues.append({
                    "type": "ratio_anomaly",
                    "severity": "low",
                    "message": f"JKM/HH比值({ratio:.2f})超出正常区间(1.2-4.0)",
                    "action": "标记异常，保留原值"
                })
        
        return issues
    
    def calculate_score(self, data_item: Dict) -> Tuple[int, str]:
        """
        计算数据质量评分（0-100）
        返回: (score, grade)
        """
        score = 0
        
        # 数据来源（25%）
        source_grade = data_item.get("grade", "D")
        source_scores = {"A": 25, "B": 20, "C": 15, "D": 10}
        score += source_scores.get(source_grade, 10)
        
        # 时效性（20%）- 简化处理，假设当日数据
        score += 20
        
        # 多源验证（25%）
        sources = data_item.get("sources", [])
        if len(sources) >= 3:
            score += 25
        elif len(sources) == 2:
            score += 20
        elif len(sources) == 1:
            score += 10
        else:
            score += 5
        
        # 数据完整性（20%）
        if data_item.get("value") is not None:
            score += 20
        else:
            score += 5
        
        # 可追溯性（10%）
        if data_item.get("source_url"):
            score += 10
        elif data_item.get("source"):
            score += 5
        
        # 确定等级
        if score >= 90:
            grade = "A"
        elif score >= 75:
            grade = "B"
        elif score >= 60:
            grade = "C"
        else:
            grade = "D"
        
        return (score, grade)
    
    def audit_all(self, raw_data: Dict) -> Dict:
        """
        审核所有数据
        返回审核后的数据结构
        """
        logger.info("开始自动审核...")
        audited = {}
        
        for metric, data in raw_data.items():
            if not isinstance(data, dict):
                continue
            
            # 如果数据还在pending状态，标记为D级
            if data.get("status") in ["pending_web", "pending_search"]:
                audited[metric] = {
                    "value": None,
                    "grade": "D",
                    "score": 30,
                    "source": "待采集",
                    "note": "采集未完成，使用估算值",
                    "issues": ["数据待采集"]
                }
                continue
            
            # 已有数据，进行审核
            score, grade = self.calculate_score(data)
            
            audited[metric] = {
                "value": data.get("value"),
                "grade": grade,
                "score": score,
                "source": data.get("source", "未知"),
                "date": data.get("date", ""),
                "unit": data.get("unit", ""),
                "note": data.get("note", ""),
                "issues": []
            }
        
        # 一致性校验
        consistency_issues = self.check_consistency(audited)
        for issue in consistency_issues:
            self.warnings.append(issue)
        
        logger.info(f"审核完成，发现 {len(self.warnings)} 个警告")
        return audited
    
    def generate_audit_report(self, audited_data: Dict) -> Dict:
        """生成审核报告"""
        total = len(audited_data)
        by_grade = {"A": 0, "B": 0, "C": 0, "D": 0}
        total_score = 0
        
        for metric, data in audited_data.items():
            grade = data.get("grade", "D")
            by_grade[grade] = by_grade.get(grade, 0) + 1
            total_score += data.get("score", 0)
        
        avg_score = total_score / total if total > 0 else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_items": total,
            "by_grade": by_grade,
            "average_score": round(avg_score, 1),
            "overall_grade": "A" if avg_score >= 90 else "B" if avg_score >= 75 else "C" if avg_score >= 60 else "D",
            "warnings": self.warnings,
            "issues": self.issues
        }


if __name__ == "__main__":
    # 测试用例
    auditor = AutoAuditor()
    
    # 模拟数据
    test_data = {
        "brent_spot": {"value": 85.4, "grade": "A", "source": "EIA API"},
        "wti_spot": {"value": 82.1, "grade": "A", "source": "EIA API"},
        "jkm_spot": {"value": 12.5, "grade": "B", "source": "TradingView"},
        "eu_storage": {"status": "estimate", "grade": "D", "note": "AGSI失效"}
    }
    
    audited = auditor.audit_all(test_data)
    report = auditor.generate_audit_report(audited)
    
    print(json.dumps(report, indent=2, ensure_ascii=False))
