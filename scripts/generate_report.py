#!/usr/bin/env python3
"""
LNG Market Report - v6.2 Main Entry
主执行脚本 - 全自动生成LNG市场报告
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict

# 添加脚本路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_collector import DataCollector
from auto_auditor import AutoAuditor
from report_generator import ReportGenerator

def main():
    """主执行函数"""
    print("=" * 60)
    print("LNG市场报告生成器 v6.2")
    print("全自动主会话版 | 零人工干预")
    print("=" * 60)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📅 报告日期: {date_str}")
    
    # 步骤1: 数据采集
    print("\n🔍 步骤1: 数据采集...")
    collector = DataCollector()
    raw_data = collector.collect_all()
    summary = collector.get_summary()
    print(f"   ✓ 采集完成: {summary['total']}项数据")
    print(f"   ✓ A级数据: {summary['by_grade'].get('A', 0)}项")
    print(f"   ✓ 待采集: {summary['by_grade'].get('pending', 0)}项")
    if summary['errors']:
        print(f"   ⚠ 错误: {summary['errors']}项")
    
    # 步骤2: 自动审核
    print("\n🔎 步骤2: 自动审核...")
    auditor = AutoAuditor()
    audited_data = auditor.audit_all(raw_data)
    audit_report = auditor.generate_audit_report(audited_data)
    print(f"   ✓ 审核完成")
    print(f"   ✓ 整体评分: {audit_report['average_score']}/100 ({audit_report['overall_grade']}级)")
    print(f"   ✓ A级: {audit_report['by_grade'].get('A', 0)}项")
    print(f"   ✓ B级: {audit_report['by_grade'].get('B', 0)}项")
    print(f"   ✓ C级: {audit_report['by_grade'].get('C', 0)}项")
    print(f"   ✓ D级: {audit_report['by_grade'].get('D', 0)}项")
    
    # 步骤3: 生成报告
    print("\n📝 步骤3: 生成报告...")
    generator = ReportGenerator(date_str)
    
    md_content = generator.generate_markdown(audited_data, audit_report)
    html_content = generator.generate_html(audited_data, audit_report)
    
    # 保存报告
    output_dir = f"/root/.openclaw/workspace/memory/reports/LNG/daily_estimates/{date_str}"
    os.makedirs(output_dir, exist_ok=True)
    
    md_path = f"{output_dir}/LNG_Market_Report_{date_str}.md"
    html_path = f"{output_dir}/LNG_Market_Report_{date_str}.html"
    json_path = f"{output_dir}/market_data.json"
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"   ✓ Markdown: {md_path}")
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   ✓ HTML: {html_path}")
    
    # 保存原始数据
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "date": date_str,
            "audit_report": audit_report,
            "data": audited_data
        }, f, ensure_ascii=False, indent=2)
    print(f"   ✓ JSON: {json_path}")
    
    print("\n" + "=" * 60)
    print("✅ 报告生成完成!")
    print(f"📊 数据质量: {audit_report['overall_grade']}级 ({audit_report['average_score']}/100)")
    print(f"📁 输出目录: {output_dir}")
    print("=" * 60)
    
    return {
        "md_path": md_path,
        "html_path": html_path,
        "json_path": json_path,
        "audit_report": audit_report
    }

if __name__ == "__main__":
    try:
        result = main()
        # 输出结果供调用方使用
        print("\n" + json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
