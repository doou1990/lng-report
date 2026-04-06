#!/bin/bash
# LNG分析系统API配置加载脚本

echo "=== LNG分析系统API配置加载 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================"

# 检查.env文件是否存在
ENV_FILE="/root/.openclaw/workspace/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ 未找到.env配置文件"
    echo "请复制.env.example为.env并填入实际的API密钥"
    echo "命令: cp /root/.openclaw/workspace/.env.example /root/.openclaw/workspace/.env"
    exit 1
fi

# 加载环境变量
echo "📋 加载环境变量..."
set -a
source "$ENV_FILE"
set +a

# 检查关键API密钥
echo ""
echo "🔍 检查API配置状态:"

# 检查TAVILY_API_KEY
if [ -n "$TAVILY_API_KEY" ] && [ "$TAVILY_API_KEY" != "tvly-your_actual_api_key_here" ]; then
    echo "✅ TAVILY_API_KEY: 已配置"
    export TAVILY_API_KEY="$TAVILY_API_KEY"
else
    echo "❌ TAVILY_API_KEY: 未配置或使用示例值"
    echo "   请从 https://tavily.com 获取API密钥"
fi

# 检查行业API密钥
industry_apis=("ICIS_API_KEY" "GIE_API_KEY" "EIA_API_KEY")
for api in "${industry_apis[@]}"; do
    if [ -n "${!api}" ] && [[ "${!api}" != *your_*api_key_here* ]]; then
        echo "✅ $api: 已配置"
    else
        echo "⚠️  $api: 未配置（LNG分析需要至少1个行业数据源）"
    fi
done

# 检查Notion API
if [ -f ~/.config/notion/api_key ]; then
    NOTION_KEY=$(cat ~/.config/notion/api_key 2>/dev/null)
    if [ -n "$NOTION_KEY" ]; then
        echo "✅ Notion API: 已配置（通过配置文件）"
        export NOTION_API_KEY="$NOTION_KEY"
    fi
elif [ -n "$NOTION_API_KEY" ] && [ "$NOTION_API_KEY" != "ntn_your_notion_api_key_here" ]; then
    echo "✅ Notion API: 已配置（通过环境变量）"
else
    echo "⚠️  Notion API: 未配置（可选，用于报告存储）"
fi

# 设置系统变量
echo ""
echo "⚙️ 设置系统配置:"

# 数据更新频率
if [ -n "$UPDATE_INTERVAL" ]; then
    echo "📅 数据更新频率: 每${UPDATE_INTERVAL}分钟"
else
    export UPDATE_INTERVAL=60
    echo "📅 数据更新频率: 使用默认值（60分钟）"
fi

# 报告生成时间
if [ -n "$REPORT_GENERATION_TIME" ]; then
    echo "⏰ 报告生成时间: 每天${REPORT_GENERATION_TIME}"
else
    export REPORT_GENERATION_TIME="08:00"
    echo "⏰ 报告生成时间: 使用默认值（08:00）"
fi

# 日志级别
if [ -n "$LOG_LEVEL" ]; then
    echo "📝 日志级别: ${LOG_LEVEL}"
else
    export LOG_LEVEL="info"
    echo "📝 日志级别: 使用默认值（info）"
fi

# 数据存储路径
if [ -n "$DATA_STORAGE_PATH" ]; then
    echo "💾 数据存储路径: ${DATA_STORAGE_PATH}"
    # 创建目录
    mkdir -p "$DATA_STORAGE_PATH"
else
    export DATA_STORAGE_PATH="/root/.openclaw/workspace/memory/reports/LNG"
    echo "💾 数据存储路径: 使用默认值（${DATA_STORAGE_PATH}）"
    mkdir -p "$DATA_STORAGE_PATH"
fi

# 创建API状态文件
API_STATUS_FILE="/root/.openclaw/workspace/memory/api_status.json"
cat > "$API_STATUS_FILE" << EOF
{
  "last_updated": "$(date -Iseconds)",
  "api_status": {
    "tavily": $(if [ -n "$TAVILY_API_KEY" ] && [ "$TAVILY_API_KEY" != "tvly-your_actual_api_key_here" ]; then echo "true"; else echo "false"; fi),
    "icis": $(if [ -n "$ICIS_API_KEY" ] && [[ "$ICIS_API_KEY" != *your_*api_key_here* ]]; then echo "true"; else echo "false"; fi),
    "gie": $(if [ -n "$GIE_API_KEY" ] && [[ "$GIE_API_KEY" != *your_*api_key_here* ]]; then echo "true"; else echo "false"; fi),
    "eia": $(if [ -n "$EIA_API_KEY" ] && [[ "$EIA_API_KEY" != *your_*api_key_here* ]]; then echo "true"; else echo "false"; fi),
    "notion": $(if [ -n "$NOTION_API_KEY" ] && [ "$NOTION_API_KEY" != "ntn_your_notion_api_key_here" ]; then echo "true"; else echo "false"; fi)
  },
  "system_config": {
    "update_interval_minutes": ${UPDATE_INTERVAL},
    "report_generation_time": "${REPORT_GENERATION_TIME}",
    "log_level": "${LOG_LEVEL}",
    "data_storage_path": "${DATA_STORAGE_PATH}"
  }
}
EOF

echo ""
echo "📊 API配置摘要:"
echo "   已加载 $(grep -c '=' "$ENV_FILE") 个环境变量"
echo "   API状态已保存到: $API_STATUS_FILE"

# 测试tavily-search技能（如果配置了API密钥）
if [ -n "$TAVILY_API_KEY" ] && [ "$TAVILY_API_KEY" != "tvly-your_actual_api_key_here" ]; then
    echo ""
    echo "🧪 测试tavily-search技能..."
    TEST_SCRIPT="/root/.openclaw/workspace/skills/tavily-search/scripts/search.mjs"
    if [ -f "$TEST_SCRIPT" ]; then
        echo "   测试命令: node $TEST_SCRIPT \"LNG market\" -n 1"
        # 实际测试（注释掉以避免频繁调用）
        # node "$TEST_SCRIPT" "LNG market" -n 1
        echo "   ✅ tavily-search技能就绪"
    else
        echo "   ❌ 未找到tavily-search技能脚本"
    fi
fi

echo ""
echo "✅ API配置加载完成"
echo "📋 详细配置指南: /root/.openclaw/workspace/API_CONFIGURATION_GUIDE.md"
echo "🔄 下次运行: source /root/.openclaw/workspace/load_api_config.sh"