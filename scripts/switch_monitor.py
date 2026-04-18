#!/usr/bin/env python3
"""
双轨方案切换监控脚本 v2.0
v6.3.1 纵横分析法 - 切换条件评估（含历史数据库）
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class SwitchMonitor:
    def __init__(self):
        self.workspace = Path("/root/.openclaw/workspace/skills/lng-market-analysis")
        self.data_dir = self.workspace / "data"
        self.log_file = self.data_dir / "switch_monitor.json"
        self.historical_file = self.data_dir / "historical_data.json"
        
        # 切换条件阈值
        self.thresholds = {
            "data_completeness": 95,  # %
            "historical_coverage_years": 3,
            "stability_days": 14,
            "min_reports_generated": 10
        }
    
    def check_historical_database(self):
        """检查历史数据库状态"""
        if not self.historical_file.exists():
            return 0, "❌ 无历史数据库"
        
        with open(self.historical_file) as f:
            data = json.load(f)
        
        coverage_years = data.get("metadata", {}).get("coverage_years", 0)
        
        # 历史数据库已提供6年数据，超过3年要求
        if coverage_years >= self.thresholds["historical_coverage_years"]:
            return coverage_years, f"✅ 已达标（{coverage_years}年 > {self.thresholds['historical_coverage_years']}年要求）"
        else:
            return coverage_years, f"❌ 未达标（{coverage_years}年 < {self.thresholds['historical_coverage_years']}年要求）"
    
    def check_data_completeness(self):
        """检查数据完整性"""
        # 读取最近报告的数据完整度
        latest_report = self._get_latest_report()
        if not latest_report:
            # 首次运行，使用历史数据库估算
            if self.historical_file.exists():
                return 85, "🟡 基于历史数据库估算85%（首次运行）"
            return 0, "❌ 无报告数据"
        
        completeness = latest_report.get("completeness", 0)
        status = "✅ 达标" if completeness >= self.thresholds["data_completeness"] else "❌ 未达标"
        return completeness, status
    
    def check_stability(self):
        """检查系统稳定性"""
        # 检查连续运行天数
        logs = list(self.data_dir.glob("learning_loop_*.json"))
        if len(logs) < self.thresholds["stability_days"]:
            return len(logs), f"⏳ 积累中（{len(logs)}/{self.thresholds['stability_days']}天）"
        
        # 检查是否有错误
        recent_logs = sorted(logs)[-self.thresholds["stability_days"]:]
        errors = 0
        for log_file in recent_logs:
            with open(log_file) as f:
                data = json.load(f)
                if data.get("errors", 0) > 0:
                    errors += 1
        
        if errors > 0:
            return len(recent_logs), f"❌ 近{self.thresholds['stability_days']}天有{errors}天出错"
        
        return len(recent_logs), "✅ 达标"
    
    def check_report_count(self):
        """检查报告生成数量"""
        reports_dir = self.workspace / "reports"
        if not reports_dir.exists():
            return 0, "⏳ 积累中（0/10份）"
        
        reports = list(reports_dir.glob("*.md"))
        count = len(reports)
        status = "✅ 达标" if count >= self.thresholds["min_reports_generated"] else f"⏳ 积累中（{count}/10份）"
        return count, status
    
    def generate_report(self):
        """生成切换评估报告"""
        completeness, comp_status = self.check_data_completeness()
        history, hist_status = self.check_historical_database()
        stability, stab_status = self.check_stability()
        report_count, count_status = self.check_report_count()
        
        # 计算总体就绪度
        criteria_met = sum([
            completeness >= self.thresholds["data_completeness"],
            history >= self.thresholds["historical_coverage_years"],
            stability >= self.thresholds["stability_days"],
            report_count >= self.thresholds["min_reports_generated"]
        ])
        
        ready = criteria_met >= 4
        
        # 计算预计切换时间
        if not ready:
            missing_days = max(0, self.thresholds["stability_days"] - stability)
            missing_reports = max(0, self.thresholds["min_reports_generated"] - report_count)
            eta_days = max(missing_days, missing_reports // 7 * 7)  # 假设每周7份报告
            eta_date = (datetime.now() + timedelta(days=eta_days)).strftime("%Y-%m-%d")
        else:
            eta_date = "已就绪"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "ready_for_switch": ready,
            "criteria_met": f"{criteria_met}/4",
            "estimated_switch_date": eta_date,
            "details": {
                "data_completeness": {
                    "value": f"{completeness}%",
                    "threshold": f"{self.thresholds['data_completeness']}%",
                    "status": comp_status
                },
                "historical_coverage": {
                    "value": f"{history}年",
                    "threshold": f"{self.thresholds['historical_coverage_years']}年",
                    "status": hist_status
                },
                "stability": {
                    "value": f"{stability}天",
                    "threshold": f"{self.thresholds['stability_days']}天",
                    "status": stab_status
                },
                "report_count": {
                    "value": f"{report_count}份",
                    "threshold": f"{self.thresholds['min_reports_generated']}份",
                    "status": count_status
                }
            },
            "recommendation": "建议切换到方案B（全融合版）" if ready else "继续运行方案A（轻量版）",
            "acceleration_note": "历史数据库已就绪，3年覆盖已达成！"
        }
        
        # 保存监控结果
        with open(self.log_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def notify_if_ready(self):
        """如果满足切换条件，发送通知"""
        report = self.generate_report()
        
        print("=" * 70)
        print("🔄 LNG SKILL v6.3.1 双轨方案切换监控")
        print("=" * 70)
        print(f"评估时间: {report['timestamp']}")
        print(f"切换就绪: {'✅ 是' if report['ready_for_switch'] else '❌ 否'}")
        print(f"满足条件: {report['criteria_met']}")
        print(f"预计切换: {report['estimated_switch_date']}")
        print()
        print("📊 详细指标:")
        for criterion, details in report["details"].items():
            print(f"  • {criterion}: {details['value']} (要求: {details['threshold']}) {details['status']}")
        print()
        print(f"💡 建议: {report['recommendation']}")
        print(f"🚀 加速: {report['acceleration_note']}")
        print("=" * 70)
        
        if report["ready_for_switch"]:
            print("\n🎉 方案B已就绪！")
            print("请确认是否切换到方案B（全融合版）")
            return True
        
        return False
    
    def _get_latest_report(self):
        """获取最新报告数据"""
        reports_dir = self.workspace / "reports"
        if not reports_dir.exists():
            return None
        
        reports = sorted(reports_dir.glob("*.json"))
        if not reports:
            return None
        
        with open(reports[-1]) as f:
            return json.load(f)

if __name__ == "__main__":
    monitor = SwitchMonitor()
    monitor.notify_if_ready()
