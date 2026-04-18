#!/usr/bin/env python3
"""
LNG市场分析助手 v6.0 - 主运行脚本

执行完整的数据采集和报告生成流程
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core.coordinator import TieredDataCollector
from evaluator.quality_evaluator import DataQualityEvaluator


def run_collection(date: str = None, output_dir: str = "./output"):
    """
    执行完整采集流程
    
    Args:
        date: 采集日期 (YYYY-MM-DD)，默认今天
        output_dir: 输出目录
    """
    target_date = date or datetime.now().strftime("%Y-%m-%d")
    print(f"🚀 LNG Market Analysis v6.0")
    print(f"📅 Target Date: {target_date}")
    print("=" * 60)
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Step 1: 数据采集
    print("\n📡 Step 1: Data Collection")
    collector = TieredDataCollector()
    collection_results = collector.collect_all(target_date)
    
    # 导出原始数据
    raw_data_file = output_path / f"raw_data_{target_date}.json"
    collector.export_json(str(raw_data_file))
    
    # Step 2: 质量评估
    print("\n📊 Step 2: Quality Evaluation")
    
    # 转换为评估器需要的格式
    market_data = {}
    for field, result in collection_results.items():
        market_data[field] = {
            "value": result.value,
            "unit": result.unit,
            "timestamp": result.timestamp,
            "source": result.source,
            "confidence": result.confidence,
            "url": result.url,
            "notes": result.notes
        }
    
    evaluator = DataQualityEvaluator()
    eval_report = evaluator.evaluate(market_data)
    
    # 导出评估报告
    eval_file = output_path / f"evaluation_{target_date}.json"
    evaluator.export_report(eval_report, str(eval_file))
    
    # Step 3: 打印摘要
    print("\n" + "=" * 60)
    print("📋 Summary Report")
    print("=" * 60)
    print(f"Collection Date: {target_date}")
    print(f"Total Fields: {len(collection_results)}")
    print(f"Quality Score: {eval_report.total_score}/100")
    print(f"Rating: {eval_report.rating}")
    print(f"Completeness: {eval_report.completeness.get('coverage', 0)}%")
    print(f"Issues Found: {len(eval_report.anomalies)}")
    
    # 按置信度统计
    conf_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for result in collection_results.values():
        conf_counts[result.confidence] = conf_counts.get(result.confidence, 0) + 1
    
    print(f"\nConfidence Distribution:")
    for conf, count in conf_counts.items():
        print(f"  {conf}级: {count}")
    
    # 输出文件位置
    print(f"\n📁 Output Files:")
    print(f"  Raw Data: {raw_data_file}")
    print(f"  Evaluation: {eval_file}")
    
    return collection_results, eval_report


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="LNG Market Analysis v6.0")
    parser.add_argument(
        "--date",
        type=str,
        help="Target date (YYYY-MM-DD), default: today"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./output",
        help="Output directory, default: ./output"
    )
    parser.add_argument(
        "--test-api",
        action="store_true",
        help="Test API connections only"
    )
    
    args = parser.parse_args()
    
    if args.test_api:
        # 仅测试API连接
        print("🔧 Testing API Connections...")
        from api.price_apis import OilPriceAPIClient, EIAAPIClient
        
        try:
            oilprice = OilPriceAPIClient()
            healthy = oilprice.check_health()
            print(f"  OilPriceAPI: {'✓ Healthy' if healthy else '✗ Unhealthy'}")
        except Exception as e:
            print(f"  OilPriceAPI: ✗ Error - {e}")
        
        try:
            eia = EIAAPIClient()
            result = eia.get_crude_inventory()
            print(f"  EIA API: {'✓ Healthy' if result else '✗ Unhealthy'}")
        except Exception as e:
            print(f"  EIA API: ✗ Error - {e}")
        
        return
    
    # 执行完整流程
    run_collection(args.date, args.output)


if __name__ == "__main__":
    main()
