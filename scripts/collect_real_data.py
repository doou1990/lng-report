#!/usr/bin/env python3
"""
LNG报告数据采集脚本 - 使用真实API数据
整合 EIA API + 其他数据源
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 添加工具目录到路径
sys.path.insert(0, '/root/.openclaw/workspace/skills/lng-market-analysis/tools')

try:
    from eia_data_client import EIADataClient
    from gie_storage_client import GIEStorageClient
    from fallback_inventory import FallbackInventoryData
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def collect_real_data():
    """
    采集真实数据，禁止使用估算
    """
    result = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "data_quality": "real_only",
            "version": "4.4.2"
        },
        "data": {},
        "missing": [],
        "sources": {}
    }
    
    print("=== 开始采集真实数据 ===")
    
    # 1. EIA API 数据 (美国)
    print("\n[1/3] 采集EIA数据...")
    try:
        eia_client = EIADataClient()
        eia_summary = eia_client.get_daily_summary()
        
        if 'data' in eia_summary:
            result['data']['eia'] = eia_summary['data']
            result['sources']['eia'] = {
                'name': 'EIA (Energy Information Administration)',
                'url': 'https://api.eia.gov',
                'status': 'success',
                'confidence': 'A'
            }
            print(f"  ✅ Brent: ${eia_summary['data']['brent']['price']}/桶")
            print(f"  ✅ WTI: ${eia_summary['data']['wti']['price']}/桶")
            print(f"  ✅ Henry Hub: ${eia_summary['data']['henry_hub']['price']}/MMBtu")
            print(f"  ✅ 原油库存: {eia_summary['data']['crude_stocks']['value']}千桶")
            print(f"  ✅ 天然气库存: {eia_summary['data']['ng_stocks']['value']} Bcf")
    except Exception as e:
        result['missing'].append('eia_data')
        result['sources']['eia'] = {'status': 'failed', 'error': str(e)}
        print(f"  ❌ EIA数据获取失败: {e}")
    
    # 2. GIE API 数据 (欧洲)
    print("\n[2/3] 采集GIE数据...")
    try:
        gie_client = GIEStorageClient()
        eu_data = gie_client.get_eu_inventory()
        
        if 'error' not in eu_data and eu_data.get('inventory', {}).get('fill_percentage'):
            result['data']['gie'] = eu_data
            result['sources']['gie'] = {
                'name': 'GIE AGSI',
                'url': 'https://agsi.gie.eu',
                'status': 'success',
                'confidence': 'A'
            }
            print(f"  ✅ 欧盟库存: {eu_data['inventory']['fill_percentage']}%")
        else:
            # GIE API 失败，标记为缺失
            result['missing'].append('gie_eu_inventory')
            result['sources']['gie'] = {
                'status': 'failed',
                'error': 'API access denied or no data',
                'note': '需要联系GIE技术支持'
            }
            print(f"  ❌ GIE API 无法访问 (密钥未激活)")
    except Exception as e:
        result['missing'].append('gie_eu_inventory')
        result['sources']['gie'] = {'status': 'failed', 'error': str(e)}
        print(f"  ❌ GIE数据获取失败: {e}")
    
    # 3. 其他数据源 (待对接)
    print("\n[3/3] 其他数据源...")
    result['missing'].extend([
        'jkm_price',
        'ttf_price', 
        'china_lng_price',
        'zhejiang_terminal_price'
    ])
    print("  ⚠️ 以下数据待对接可靠API:")
    print("     - JKM LNG价格")
    print("     - TTF天然气价格")
    print("     - 中国LNG价格")
    print("     - 浙江接收站价格")
    
    # 数据质量评估
    total_expected = 8
    available = len(result['data'].get('eia', {})) + (1 if 'gie' in result['data'] else 0)
    
    result['metadata']['completeness'] = f"{available}/{total_expected}"
    result['metadata']['confidence'] = 'A' if available >= 6 else 'B' if available >= 4 else 'C'
    
    print(f"\n=== 数据采集完成 ===")
    print(f"数据完整度: {available}/{total_expected}")
    print(f"综合置信度: {result['metadata']['confidence']}")
    print(f"缺失数据: {len(result['missing'])}项")
    
    return result

def save_report(data, output_dir):
    """保存数据到文件"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # JSON格式
    json_file = output_path / f"market_data_{data['metadata']['date']}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 数据已保存: {json_file}")
    return str(json_file)

if __name__ == "__main__":
    # 采集数据
    data = collect_real_data()
    
    # 保存到文件
    output_dir = "/root/.openclaw/workspace/memory/reports/LNG/daily_estimates"
    save_report(data, output_dir)
    
    # 输出摘要
    print("\n" + "="*60)
    print("EIA API 数据摘要:")
    print("="*60)
    if 'eia' in data['data']:
        eia = data['data']['eia']
        print(f"Brent原油: ${eia['brent']['price']}/桶 ({eia['brent']['date']})")
        print(f"WTI原油: ${eia['wti']['price']}/桶 ({eia['wti']['date']})")
        print(f"Henry Hub: ${eia['henry_hub']['price']}/MMBtu ({eia['henry_hub']['date']})")
    print("="*60)
