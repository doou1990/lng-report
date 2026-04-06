#!/bin/bash
# LNG日报生成脚本 - 每日自动更新
# 使用方式: bash generate_daily_report.sh

REPORT_DATE=$(date +%Y-%m-%d)
REPORT_DIR="/root/.openclaw/workspace/memory/reports/LNG/daily_estimates/${REPORT_DATE}"
mkdir -p "$REPORT_DIR"

echo "=== LNG市场日报生成 ==="
echo "日期: $REPORT_DATE"
echo "========================"

# 阶段1: 9助理数据采集
echo ""
echo "【阶段1】9助理数据采集"
echo "------------------------"

# 1. 原油助理
echo "1. 原油助理采集原油价格..."
mcporter call 'exa.web_search_exa(query: "crude oil price Brent WTI today", numResults: 5, type: "auto")' > "$REPORT_DIR/1_oil_prices.txt" 2>&1

# 2. 海明 - 国际价格
echo "2. 海明采集LNG国际价格..."
mcporter call 'exa.web_search_exa(query: "LNG spot price JKM TTF Henry Hub today", numResults: 5, type: "auto")' > "$REPORT_DIR/2_lng_prices.txt" 2>&1

# 3. 陆远 - 中国市场
echo "3. 陆远采集中国数据..."
mcporter call 'exa.web_search_exa(query: "China LNG imports today", numResults: 5, type: "auto")' > "$REPORT_DIR/3_china.txt" 2>&1

# 4. 欧风 - 欧洲库存
echo "4. 欧风采集欧洲库存..."
mcporter call 'exa.web_search_exa(query: "Europe gas storage levels today", numResults: 5, type: "auto")' > "$REPORT_DIR/4_europe.txt" 2>&1

# 5. 洋基 - 美国产能
echo "5. 洋基采集美国产能..."
mcporter call 'exa.web_search_exa(query: "US LNG exports Cheniere today", numResults: 5, type: "auto")' > "$REPORT_DIR/5_usa.txt" 2>&1

echo ""
echo "数据采集完成！"
echo ""
echo "数据文件保存在: $REPORT_DIR/"
echo ""
echo "下一步: 人工整理数据并生成报告"
echo "报告模板: ~/.openclaw/workspace/skills/lng-market-analysis/templates/"
