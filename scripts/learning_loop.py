#!/usr/bin/env python3
"""
LNG SKILL v6.3 学习循环执行器
Learning Loop Executor for LNG Market Analysis
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 配置路径
SKILL_DIR = Path("/root/.openclaw/workspace/skills/lng-market-analysis")
CONFIG_FILE = SKILL_DIR / "config" / "learning_loop.toml"
DATA_DIR = SKILL_DIR / "data"
LOG_FILE = SKILL_DIR / "logs" / "learning_loop.log"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
(LOG_FILE.parent).mkdir(exist_ok=True)

class LearningLoop:
    """学习循环主类"""
    
    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.evaluation_results = {}
        
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(log_entry.strip())
    
    def step1_evaluation(self) -> dict:
        """
        Step 1: 结果评估
        检查今日报告的数据质量，识别问题
        """
        self.log("=== Step 1: 结果评估 ===")
        
        # 读取今日报告数据
        report_file = DATA_DIR / f"market_data_{self.today}.json"
        if not report_file.exists():
            self.log(f"⚠️ 今日报告数据不存在: {report_file}")
            return {"status": "no_data"}
        
        with open(report_file, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        
        # 统计置信度分布
        confidence_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
        d_level_items = []
        
        for item_id, item_data in report_data.get("data", {}).items():
            confidence = item_data.get("confidence", "D")
            confidence_counts[confidence] += 1
            
            if confidence == "D":
                d_level_items.append({
                    "item": item_id,
                    "reason": item_data.get("notes", "未知原因")
                })
        
        total = sum(confidence_counts.values())
        
        self.log(f"📊 今日数据质量分布:")
        self.log(f"   A级: {confidence_counts['A']} ({confidence_counts['A']/total*100:.1f}%)")
        self.log(f"   B级: {confidence_counts['B']} ({confidence_counts['B']/total*100:.1f}%)")
        self.log(f"   C级: {confidence_counts['C']} ({confidence_counts['C']/total*100:.1f}%)")
        self.log(f"   D级: {confidence_counts['D']} ({confidence_counts['D']/total*100:.1f}%)")
        
        if d_level_items:
            self.log(f"⚠️  D级数据项 ({len(d_level_items)}个):")
            for item in d_level_items:
                self.log(f"   - {item['item']}: {item['reason']}")
        
        self.evaluation_results = {
            "date": self.today,
            "confidence_distribution": confidence_counts,
            "d_level_items": d_level_items,
            "total_items": total
        }
        
        return self.evaluation_results
    
    def step2_extraction(self, evaluation: dict) -> list:
        """
        Step 2: 技能提取
        根据评估结果，确定需要更新的技能
        """
        self.log("\n=== Step 2: 技能提取 ===")
        
        skills_to_update = []
        
        # 检查 D 级数据项（数据源发现问题）
        d_items = evaluation.get("d_level_items", [])
        if d_items:
            # 检查是否连续 3 天 D 级
            for item in d_items:
                item_name = item["item"]
                if self._check_consecutive_d_level(item_name, days=3):
                    skills_to_update.append({
                        "skill": "data_source_discovery",
                        "action": "discover_new_source",
                        "target": item_name,
                        "reason": f"{item_name} 连续3天D级"
                    })
                    self.log(f"🔍 触发数据源发现: {item_name}")
        
        # 检查搜索成功率（搜索优化问题）
        search_log = self._load_search_log()
        failed_searches = [s for s in search_log if not s["success"]]
        if len(failed_searches) >= 3:
            skills_to_update.append({
                "skill": "search_optimization",
                "action": "optimize_keywords",
                "target": failed_searches[-1]["query"],
                "reason": f"最近3次搜索失败"
            })
            self.log(f"🔍 触发搜索优化: 最近3次搜索失败")
        
        self.log(f"📋 需要更新的技能: {len(skills_to_update)}个")
        for skill in skills_to_update:
            self.log(f"   - {skill['skill']}: {skill['action']} ({skill['reason']})")
        
        return skills_to_update
    
    def step3_improvement(self, skills_to_update: list) -> dict:
        """
        Step 3: 技能改进
        执行技能更新，根据策略决定自动或审批
        """
        self.log("\n=== Step 3: 技能改进 ===")
        
        results = {
            "auto_approved": [],
            "pending_approval": [],
            "failed": []
        }
        
        for skill_update in skills_to_update:
            skill_name = skill_update["skill"]
            action = skill_update["action"]
            
            # 判断变更类型
            change_type = self._classify_change(skill_name, action)
            
            if change_type == "minor":
                # 小变更：自动执行
                self.log(f"✅ 自动批准 [{skill_name}]: {action}")
                self._execute_skill_update(skill_update)
                results["auto_approved"].append(skill_update)
            else:
                # 大变更：需审批
                self.log(f"⏸️  待审批 [{skill_name}]: {action}")
                results["pending_approval"].append(skill_update)
        
        self.log(f"\n📊 改进结果:")
        self.log(f"   自动批准: {len(results['auto_approved'])}个")
        self.log(f"   待审批: {len(results['pending_approval'])}个")
        
        return results
    
    def _check_consecutive_d_level(self, item_name: str, days: int) -> bool:
        """检查某数据项是否连续 N 天为 D 级"""
        # 简化实现：检查最近 N 天的报告
        d_count = 0
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            report_file = DATA_DIR / f"market_data_{date}.json"
            if report_file.exists():
                with open(report_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                item_data = data.get("data", {}).get(item_name, {})
                if item_data.get("confidence") == "D":
                    d_count += 1
        return d_count >= days
    
    def _load_search_log(self) -> list:
        """加载搜索日志"""
        log_file = DATA_DIR / "search_log.json"
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _classify_change(self, skill_name: str, action: str) -> str:
        """分类变更类型（minor/major）"""
        # 根据配置判断
        minor_actions = ["optimize_keywords", "rule_tuning"]
        if action in minor_actions:
            return "minor"
        return "major"
    
    def _execute_skill_update(self, skill_update: dict):
        """执行技能更新"""
        skill_name = skill_update["skill"]
        action = skill_update["action"]
        target = skill_update["target"]
        
        # 记录到技能更新日志
        update_log = {
            "date": self.today,
            "skill": skill_name,
            "action": action,
            "target": target,
            "auto_approved": True
        }
        
        log_file = DATA_DIR / "skill_updates.json"
        updates = []
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                updates = json.load(f)
        
        updates.append(update_log)
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(updates, f, ensure_ascii=False, indent=2)
    
    def run(self):
        """执行完整学习循环"""
        self.log(f"\n{'='*50}")
        self.log(f"🚀 LNG SKILL v6.3 学习循环启动")
        self.log(f"📅 日期: {self.today}")
        self.log(f"{'='*50}\n")
        
        # Step 1: 结果评估
        evaluation = self.step1_evaluation()
        
        if evaluation.get("status") == "no_data":
            self.log("\n⚠️ 无数据，跳过学习循环")
            return
        
        # Step 2: 技能提取
        skills_to_update = self.step2_extraction(evaluation)
        
        if not skills_to_update:
            self.log("\n✅ 无需更新技能")
            return
        
        # Step 3: 技能改进
        results = self.step3_improvement(skills_to_update)
        
        # 保存学习循环结果
        loop_result = {
            "date": self.today,
            "evaluation": evaluation,
            "skills_to_update": skills_to_update,
            "improvement_results": results
        }
        
        result_file = DATA_DIR / f"learning_loop_{self.today}.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(loop_result, f, ensure_ascii=False, indent=2)
        
        self.log(f"\n✅ 学习循环完成")
        self.log(f"📁 结果已保存: {result_file}")


def main():
    """主函数"""
    loop = LearningLoop()
    loop.run()


if __name__ == "__main__":
    main()
