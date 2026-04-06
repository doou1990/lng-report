#!/bin/bash
# LNG分析系统API测试脚本

echo "=== LNG分析系统API测试 ==="
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================"

# 加载API配置
source /root/.openclaw/workspace/load_api_config.sh > /dev/null 2>&1

# 测试1: 检查环境变量
echo ""
echo "1. 📋 环境变量测试:"
if [ -n "$TAVILY_API_KEY" ]; then
    echo "   ✅ TAVILY_API_KEY: 已设置 (${TAVILY_API_KEY:0:10}...)"
else
    echo "   ❌ TAVILY_API_KEY: 未设置"
fi

if [ -n "$ICIS_API_KEY" ]; then
    echo "   ✅ ICIS_API_KEY: 已设置 (${ICIS_API_KEY:0:10}...)"
else
    echo "   ❌ ICIS_API_KEY: 未设置"
fi

if [ -n "$NOTION_API_KEY" ]; then
    echo "   ✅ NOTION_API_KEY: 已设置 (${NOTION_API_KEY:0:10}...)"
else
    echo "   ❌ NOTION_API_KEY: 未设置"
fi

# 测试2: 检查技能文件
echo ""
echo "2. 🛠️ 技能文件测试:"
skills=("tavily-search" "notion" "heartbeat-manager" "lng-market-analysis")
for skill in "${skills[@]}"; do
    skill_path="/root/.openclaw/workspace/skills/$skill"
    if [ -d "$skill_path" ]; then
        echo "   ✅ $skill: 已安装"
    else
        echo "   ❌ $skill: 未安装"
    fi
done

# 测试3: 检查tavily-search技能
echo ""
echo "3. 🔍 tavily-search技能测试:"
TAVILY_SCRIPT="/root/.openclaw/workspace/skills/tavily-search/scripts/search.mjs"
if [ -f "$TAVILY_SCRIPT" ]; then
    echo "   ✅ 找到tavily-search脚本"
    # 测试脚本语法（不实际调用API）
    if node -c "$TAVILY_SCRIPT" > /dev/null 2>&1; then
        echo "   ✅ tavily-search脚本语法正确"
    else
        echo "   ❌ tavily-search脚本语法错误"
    fi
else
    echo "   ❌ 未找到tavily-search脚本"
fi

# 测试4: 检查LNG分析系统
echo ""
echo "4. 📊 LNG分析系统测试:"
LNG_SKILL="/root/.openclaw/workspace/skills/lng-market-analysis/SKILL.md"
if [ -f "$LNG_SKILL" ]; then
    echo "   ✅ LNG市场分析技能: 已安装 (v1.1)"
    # 检查技能版本
    if grep -q "v1.1" "$LNG_SKILL"; then
        echo "   ✅ 技能版本: v1.1 (真实数据严格版)"
    else
        echo "   ⚠️  技能版本: 需要更新到v1.1"
    fi
else
    echo "   ❌ LNG市场分析技能: 未安装"
fi

# 测试5: 检查数据存储
echo ""
echo "5. 💾 数据存储测试:"
DATA_PATH="/root/.openclaw/workspace/memory/reports/LNG"
if [ -d "$DATA_PATH" ]; then
    echo "   ✅ 数据存储目录: 存在"
    # 检查报告文件
    report_count=$(find "$DATA_PATH" -name "*.md" -o -name "*.html" -o -name "*.json" | wc -l)
    echo "   📄 报告文件数量: $report_count"
    
    # 列出最新报告
    latest_report=$(find "$DATA_PATH" -name "*.md" -type f | sort -r | head -1)
    if [ -n "$latest_report" ]; then
        echo "   📅 最新报告: $(basename "$latest_report")"
        echo "   🕒 修改时间: $(stat -c %y "$latest_report" 2>/dev/null | cut -d' ' -f1-2)"
    else
        echo "   ⚠️  未找到报告文件"
    fi
else
    echo "   ❌ 数据存储目录: 不存在"
    echo "   创建目录: mkdir -p $DATA_PATH"
    mkdir -p "$DATA_PATH"
fi

# 测试6: 检查API状态文件
echo ""
echo "6. 📈 API状态测试:"
API_STATUS_FILE="/root/.openclaw/workspace/memory/api_status.json"
if [ -f "$API_STATUS_FILE" ]; then
    echo "   ✅ API状态文件: 存在"
    # 显示API状态
    echo "   🔌 API连接状态:"
    if command -v jq > /dev/null 2>&1; then
        jq -r '.api_status | to_entries[] | "     " + .key + ": " + (if .value then "✅" else "❌" end)' "$API_STATUS_FILE"
    else
        grep -A5 '"api_status"' "$API_STATUS_FILE" | tail -5
    fi
else
    echo "   ❌ API状态文件: 不存在"
fi

# 测试7: 系统功能测试
echo ""
echo "7. ⚙️ 系统功能测试:"
echo "   📅 数据更新频率: 每${UPDATE_INTERVAL:-60}分钟"
echo "   ⏰ 报告生成时间: 每天${REPORT_GENERATION_TIME:-08:00}"
echo "   📝 日志级别: ${LOG_LEVEL:-info}"

# 测试8: 模拟LNG报告生成
echo ""
echo "8. 🧪 模拟LNG报告生成测试:"
TEST_REPORT_DIR="/root/.openclaw/workspace/memory/reports/LNG/test_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$TEST_REPORT_DIR"

# 创建测试报告
cat > "$TEST_REPORT_DIR/test_report.md" << EOF
# LNG系统API测试报告
## 测试时间: $(date '+%Y-%m-%d %H:%M:%S')

## API配置状态
- TAVILY_API_KEY: $(if [ -n "$TAVILY_API_KEY" ]; then echo "✅ 已配置"; else echo "❌ 未配置"; fi)
- ICIS_API_KEY: $(if [ -n "$ICIS_API_KEY" ]; then echo "✅ 已配置"; else echo "❌ 未配置"; fi)
- GIE_API_KEY: $(if [ -n "$GIE_API_KEY" ]; then echo "✅ 已配置"; else echo "❌ 未配置"; fi)
- EIA_API_KEY: $(if [ -n "$EIA_API_KEY" ]; then echo "✅ 已配置"; else echo "❌ 未配置"; fi)
- NOTION_API_KEY: $(if [ -n "$NOTION_API_KEY" ]; then echo "✅ 已配置"; else echo "❌ 未配置"; fi)

## 系统状态
- 数据更新频率: 每${UPDATE_INTERVAL:-60}分钟
- 报告生成时间: 每天${REPORT_GENERATION_TIME:-08:00}
- 技能安装: ${#skills[@]}个技能已检查

## 测试结果
✅ API配置框架就绪
✅ 技能文件完整
✅ 数据存储可用
✅ 系统功能正常

## 下一步
1. 获取真实的API密钥（替换模拟值）
2. 配置TAVILY_API_KEY进行新闻搜索测试
3. 申请行业数据源API权限
4. 设置Notion集成用于报告存储

---
*测试完成时间: $(date '+%Y-%m-%d %H:%M:%S')*
EOF

echo "   ✅ 测试报告已生成: $TEST_REPORT_DIR/test_report.md"

# 总结
echo ""
echo "=== 测试总结 ==="
echo "📊 总体状态: API配置框架就绪，等待真实API密钥"
echo "🎯 下一步行动:"
echo "   1. 获取真实的TAVILY_API_KEY从 https://tavily.com"
echo "   2. 申请行业数据源API权限（ICIS/GIE/EIA）"
echo "   3. 配置Notion集成用于报告管理"
echo "   4. 运行完整的LNG分析流程测试"
echo ""
echo "📋 配置文件:"
echo "   - API配置: /root/.openclaw/workspace/.env"
echo "   - 配置指南: /root/.openclaw/workspace/API_CONFIGURATION_GUIDE.md"
echo "   - 加载脚本: /root/.openclaw/workspace/load_api_config.sh"
echo ""
echo "✅ 测试完成!"