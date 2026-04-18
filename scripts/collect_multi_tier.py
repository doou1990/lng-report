#!/usr/bin/env python3
"""
LNG报告数据采集脚本 v2.0
多层级数据源策略，按用户要求实现
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 添加工具目录到路径
sys.path.insert(0, '/root/.openclaw/workspace/skills/lng-market-analysis/tools')

try:
    from eia_data_client import EIADataClient
except ImportError:
    print("Error: EIA client not found")
    sys.exit(1)

def collect_data_multi_tier():
    """
    多层级数据采集
    层级1: 官方API (A级)
    层级2: 权威网站 (B级)
    层级3: 其他网站 (C级)
    层级4: 估算 (D级) - 尽量避免
    """
    result = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "version": "4.4.2",
            "strategy": "multi_tier"
        },
        "data": {
            "tier1_api": {},      # A级 - 官方API
            "tier2_authority": {}, # B级 - 权威网站
            "tier3_other": {},     # C级 - 其他网站
            "tier4_estimate": {}   # D级 - 估算(尽量避免)
        },
        "sources": {},
        "missing": []
    }
    
    print("=== 多层级数据采集开始 ===")
    
    # ========== 层级1: 官方API (A级) ==========
    print("\n[层级1] 官方API数据采集 (A级)...")
    
    # 1.1 EIA API (美国数据)
    print("  → EIA API (美国能源信息署)...")
    try:
        eia_client = EIADataClient()
        eia_data = eia_client.get_daily_summary()
        
        if 'data' in eia_data:
            result['data']['tier1_api']['eia'] = eia_data['data']
            result['sources']['eia'] = {
                'name': 'EIA (Energy Information Administration)',
                'url': 'https://api.eia.gov',
                'tier': 'A',
                'status': 'success',
                'last_update': eia_data['data'].get('brent', {}).get('date', 'N/A')
            }
            print(f"    ✅ Brent: ${eia_data['data']['brent']['price']}/桶")
            print(f"    ✅ WTI: ${eia_data['data']['wti']['price']}/桶")
            print(f"    ✅ Henry Hub: ${eia_data['data']['henry_hub']['price']}/MMBtu")
            print(f"    ✅ 原油库存: {eia_data['data']['crude_stocks']['value']}千桶")
            print(f"    ✅ 天然气库存: {eia_data['data']['ng_stocks']['value']} Bcf")
    except Exception as e:
        result['sources']['eia'] = {'tier': 'A', 'status': 'failed', 'error': str(e)}
        print(f"    ❌ EIA API失败: {e}")
    
    # 1.2 GIE API (欧洲数据) - 待激活
    print("  → GIE API (欧洲天然气库存)...")
    result['sources']['gie'] = {
        'tier': 'A',
        'status': 'pending',
        'note': 'API密钥待激活，暂时使用其他层级数据'
    }
    print(f"    ⏳ GIE API待激活")
    
    # ========== 层级2: 权威网站 (B级) ==========
    print("\n[层级2] 权威网站数据采集 (B级)...")
    print("  → CNBC, Bloomberg, Reuters...")
    print("  → Platts, ICIS...")
    print("  → 上海石油天然气交易中心...")
    
    # 标记为待采集（实际采集由助理执行）
    result['data']['tier2_authority'] = {
        'status': 'pending_collection',
        'sources': ['CNBC', 'Bloomberg', 'Platts', 'SHPGX']
    }
    result['sources']['tier2'] = {
        'tier': 'B',
        'status': 'pending',
        'note': '由12助理通过web_search采集'
    }
    print(f"    ⏳ 待12助理采集")
    
    # ========== 层级3: 其他网站 (C级) ==========
    print("\n[层级3] 其他网站数据采集 (C级)...")
    print("  → Mysteel, 隆众资讯...")
    print("  → LNG168.com...")
    print("  → Trading Economics...")
    
    result['data']['tier3_other'] = {
        'status': 'pending_collection',
        'sources': ['Mysteel', '隆众资讯', 'LNG168', 'Trading Economics']
    }
    result['sources']['tier3'] = {
        'tier': 'C',
        'status': 'pending',
        'note': '当层级1-2缺失时使用'
    }
    print(f"    ⏳ 备用数据源就绪")
    
    # ========== 层级4: 估算 (D级) - 尽量避免 ==========
    print("\n[层级4] 估算数据 (D级) - 尽量避免...")
    result['data']['tier4_estimate'] = {
        'status': 'avoid',
        'note': '仅当1-3层都无法获取时使用，必须明确标注'
    }
    result['sources']['tier4'] = {
        'tier': 'D',
        'status': 'avoid',
        'note': '尽量避免使用估算数据'
    }
    print(f"    ⚠️ 尽量避免使用")
    
    # ========== 数据保留策略 ==========
    print("\n[数据保留策略]...")
    print("  → EIA数据延迟时: 保留EIA最新数据 + 其他来源最新数据")
    print("  → 数据矛盾时: 标注多个来源，说明差异")
    print("  → 数据缺失时: 明确标注'数据缺失'，不编造")
    
    result['metadata']['retention_policy'] = {
        'eia_delay': '保留EIA最新 + 其他来源最新',
        'conflict': '标注多个来源，说明差异',
        'missing': '明确标注缺失，不编造'
    }
    
    # 统计
    tier1_count = len([v for v in result['data']['tier1_api'].values() if v])
    print(f"\n=== 数据采集完成 ===")
    print(f"层级1 (A级): {tier1_count}项")
    print(f"层级2 (B级): 待采集")
    print(f"层级3 (C级): 备用")
    print(f"层级4 (D级): 避免使用")
    
    return result

def save_data(data, output_dir):
    """保存数据到文件"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    json_file = output_path / f"multi_tier_data_{data['metadata']['date']}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 数据已保存: {json_file}")
    return str(json_file)

if __name__ == "__main__":
    # 采集数据
    data = collect_data_multi_tier()
    
    # 保存到文件
    output_dir = "/root/.openclaw/workspace/memory/reports/LNG/daily_estimates"
    save_data(data, output_dir)
    
    # 输出摘要
    print("\n" + "="*60)
    print("A级数据摘要 (EIA API):")
    print("="*60)
    if 'eia' in data['data']['tier1_api']:
        eia = data['data']['tier1_api']['eia']
        print(f"Brent原油: ${eia['brent']['price']}/桶 ({eia['brent']['date']})")
        print(f"WTI原油: ${eia['wti']['price']}/桶 ({eia['wti']['date']})")
        print(f"Henry Hub: ${eia['henry_hub']['price']}/MMBtu ({eia['henry_hub']['date']})")
        print(f"原油库存: {eia['crude_stocks']['value']}千桶")
        print(f"天然气库存: {eia['ng_stocks']['value']} Bcf")
    print("="*60)
    print("\n下一步: 启动12助理采集层级2-3数据")
