#!/usr/bin/env python3
"""
库存数据采集脚本 - 库存助理专用
用于LNG市场分析报告中的全球库存数据获取

使用方法:
    python fetch_inventory_data.py [--output OUTPUT_FILE]

输出:
    JSON格式的库存数据，包含欧盟、主要国家、美国、中国库存
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 添加工具目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

try:
    from gie_storage_client import GIEStorageClient
except ImportError:
    print("Error: gie_storage_client.py not found", file=sys.stderr)
    sys.exit(1)


def fetch_all_inventory_data() -> dict:
    """
    采集所有库存数据
    
    Returns:
        完整的库存数据字典
    """
    client = GIEStorageClient()
    
    result = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "GIE AGSI API",
            "version": "4.4"
        },
        "eu_inventory": {},
        "major_countries": [],
        "us_inventory": {},  # 待EIA API对接
        "china_inventory": {},  # 待数据源对接
        "analysis": {}
    }
    
    # 1. 获取欧盟整体数据
    print("Fetching EU inventory data...", file=sys.stderr)
    eu_data = client.get_eu_inventory()
    
    if "error" not in eu_data:
        result["eu_inventory"] = {
            "country": eu_data.get("country"),
            "gas_day": eu_data.get("gas_day"),
            "updated_at": eu_data.get("updated_at"),
            **eu_data.get("inventory", {})
        }
        
        # 计算分析指标
        inv = eu_data.get("inventory", {})
        result["analysis"] = {
            "eu_fill_level": inv.get("fill_percentage"),
            "eu_status": _get_status(inv.get("fill_percentage", 0)),
            "trend": inv.get("trend_percentage"),
            "days_of_consumption": inv.get("consumption_full_days"),
            "confidence": _calculate_confidence(eu_data)
        }
    else:
        print(f"Warning: Failed to fetch EU data: {eu_data.get('message')}", file=sys.stderr)
        result["eu_inventory"] = {"error": eu_data.get("message")}
    
    # 2. 获取主要国家数据
    print("Fetching major countries data...", file=sys.stderr)
    major_countries = ["de", "fr", "it", "nl", "at", "es", "uk"]
    
    for country_code in major_countries:
        country_data = client.get_current_inventory(country_code)
        
        if "error" not in country_data:
            result["major_countries"].append({
                "country_code": country_code.upper(),
                "country": country_data.get("country"),
                "gas_day": country_data.get("gas_day"),
                **country_data.get("inventory", {})
            })
        else:
            print(f"Warning: Failed to fetch {country_code}: {country_data.get('message')}", 
                  file=sys.stderr)
    
    # 3. 生成汇总统计
    if result["major_countries"]:
        fill_levels = [c.get("fill_percentage", 0) for c in result["major_countries"] 
                       if c.get("fill_percentage")]
        if fill_levels:
            result["analysis"]["avg_major_countries_fill"] = round(sum(fill_levels) / len(fill_levels), 2)
            result["analysis"]["highest_fill_country"] = max(
                result["major_countries"], 
                key=lambda x: x.get("fill_percentage", 0)
            ).get("country")
            result["analysis"]["lowest_fill_country"] = min(
                result["major_countries"], 
                key=lambda x: x.get("fill_percentage", 0) if x.get("fill_percentage") else 100
            ).get("country")
    
    return result


def _get_status(fill_percentage: float) -> str:
    """根据填充率返回状态描述"""
    if fill_percentage >= 80:
        return "充足"
    elif fill_percentage >= 50:
        return "正常"
    elif fill_percentage >= 30:
        return "偏低"
    else:
        return "紧张"


def _calculate_confidence(data: dict) -> str:
    """计算数据置信度等级"""
    if "error" in data:
        return "D"
    
    inventory = data.get("inventory", {})
    
    # 检查关键字段完整性
    required_fields = ["gas_in_storage_twh", "fill_percentage", "working_gas_volume_twh"]
    missing = [f for f in required_fields if inventory.get(f) is None]
    
    if missing:
        return "C"
    
    # 检查数据时效性
    updated_at = data.get("updated_at", "")
    if updated_at:
        try:
            update_time = datetime.fromisoformat(updated_at.replace(" ", "T"))
            hours_ago = (datetime.now() - update_time).total_seconds() / 3600
            if hours_ago < 24:
                return "A"
            elif hours_ago < 48:
                return "B"
            else:
                return "C"
        except:
            return "B"
    
    return "B"


def format_for_report(data: dict) -> str:
    """
    格式化为报告文本
    
    Args:
        data: 库存数据字典
        
    Returns:
        Markdown格式的报告文本
    """
    lines = []
    
    # 标题
    lines.append("## 全球LNG库存数据")
    lines.append("")
    
    # 欧盟数据
    eu = data.get("eu_inventory", {})
    analysis = data.get("analysis", {})
    
    lines.append("### 欧盟天然气库存")
    lines.append("")
    lines.append(f"- **统计日期**: {eu.get('gas_day', 'N/A')}")
    lines.append(f"- **库存量**: {eu.get('gas_in_storage_twh', 'N/A')} TWh")
    lines.append(f"- **填充率**: {eu.get('fill_percentage', 'N/A')}% ({analysis.get('eu_status', 'N/A')})")
    lines.append(f"- **工作气量**: {eu.get('working_gas_volume_twh', 'N/A')} TWh")
    lines.append(f"- **日变化**: {eu.get('trend_percentage', 'N/A')}%")
    lines.append(f"- **可消费天数**: {eu.get('consumption_full_days', 'N/A')} 天")
    lines.append(f"- **数据置信度**: {analysis.get('confidence', 'N/A')} 级")
    lines.append("")
    
    # 主要国家
    countries = data.get("major_countries", [])
    if countries:
        lines.append("### 主要欧洲国家库存")
        lines.append("")
        lines.append("| 国家 | 填充率 | 库存量(TWh) | 日变化 |")
        lines.append("|------|--------|-------------|--------|")
        
        for c in sorted(countries, key=lambda x: x.get("fill_percentage", 0), reverse=True):
            lines.append(
                f"| {c.get('country', 'N/A')} | "
                f"{c.get('fill_percentage', 'N/A')}% | "
                f"{c.get('gas_in_storage_twh', 'N/A')} | "
                f"{c.get('trend_percentage', 'N/A')}% |"
            )
        lines.append("")
    
    # 分析总结
    lines.append("### 库存分析")
    lines.append("")
    
    if analysis.get("avg_major_countries_fill"):
        lines.append(f"- **主要国家平均填充率**: {analysis['avg_major_countries_fill']}%")
    if analysis.get("highest_fill_country"):
        lines.append(f"- **库存最高**: {analysis['highest_fill_country']}")
    if analysis.get("lowest_fill_country"):
        lines.append(f"- **库存最低**: {analysis['lowest_fill_country']}")
    
    lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch LNG inventory data")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--format", "-f", choices=["json", "markdown"], 
                       default="json", help="Output format")
    args = parser.parse_args()
    
    # 采集数据
    data = fetch_all_inventory_data()
    
    # 输出
    if args.format == "markdown":
        output = format_for_report(data)
        print(output)
    else:
        output = json.dumps(data, indent=2, ensure_ascii=False)
        print(output)
    
    # 保存到文件
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nData saved to: {args.output}", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
