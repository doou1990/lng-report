#!/bin/bash
# v6.1 混合子代理模式 - 快速启动脚本

set -e

echo "🚀 LNG Market Analysis v6.1 - Hybrid SubAgent Mode"
echo "====================================================="
echo ""
echo "架构: 3 API子代理 + 1网页子代理 + 1审核子代理"
echo "预计耗时: < 6分钟"
echo ""

# 检查API密钥
if [ -z "$OILPRICE_API_KEY" ]; then
    echo "⚠️  Warning: OILPRICE_API_KEY not set"
    echo "   国际原油价格将无法采集 (Brent, WTI, JKM, TTF, HH)"
    echo "   获取密钥: https://oilpriceapi.com"
    echo ""
fi

if [ -z "$EIA_API_KEY" ]; then
    echo "⚠️  Warning: EIA_API_KEY not set"
    echo "   美国库存数据将无法采集"
    echo "   获取密钥: https://www.eia.gov/opendata (免费)"
    echo ""
fi

# 进入目录
cd /root/.openclaw/workspace/skills/lng-market-analysis/v6_core

# 运行采集
echo "📡 Starting Hybrid SubAgent Collection..."
echo ""

python3 -c "
import asyncio
import sys
sys.path.insert(0, '.')
from hybrid_subagent_mode import collect_with_hybrid_subagents

async def main():
    results = await collect_with_hybrid_subagents()
    print(f'\n✅ Total: {len(results)} fields collected')
    
    # 显示结果摘要
    print('\n📊 Results Summary:')
    for field, data in results.items():
        if data.value:
            print(f'  {data.name}: {data.value} {data.unit} [{data.confidence}级]')

asyncio.run(main())
"

echo ""
echo "====================================================="
echo "Done!"
