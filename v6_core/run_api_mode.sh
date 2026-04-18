#!/bin/bash
# v6.1 API子代理模式 - 快速启动脚本

set -e

echo "🚀 LNG Market Analysis v6.1 - API SubAgent Mode"
echo "================================================"

# 检查API密钥
if [ -z "$OILPRICE_API_KEY" ]; then
    echo "⚠️  Warning: OILPRICE_API_KEY not set"
    echo "   Get your key at: https://oilpriceapi.com"
fi

if [ -z "$EIA_API_KEY" ]; then
    echo "⚠️  Warning: EIA_API_KEY not set"
    echo "   Get your key at: https://www.eia.gov/opendata"
fi

# 进入目录
cd /root/.openclaw/workspace/skills/lng-market-analysis/v6_core

# 运行采集
echo ""
echo "📡 Starting API SubAgent Collection..."
echo ""

python3 -c "
import asyncio
import sys
sys.path.insert(0, '.')
from api_subagent_mode import collect_with_api_subagents

results = asyncio.run(collect_with_api_subagents())
print(f'\n✅ Total: {len(results)} fields collected')
"

echo ""
echo "================================================"
echo "Done!"
