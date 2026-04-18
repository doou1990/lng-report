#!/bin/bash
# v6.0 快速切换脚本

SKILL_DIR="/root/.openclaw/workspace/skills/lng-market-analysis"

case "$1" in
    v6|6)
        echo "🚀 Switching to v6.0..."
        cd "$SKILL_DIR/v6_core"
        python3 run.py "${@:2}"
        ;;
    v5|5)
        echo "📋 Using v5.0 (legacy)..."
        echo "v5.0 execution via original skill..."
        ;;
    test)
        echo "🧪 Testing v6.0 API connections..."
        cd "$SKILL_DIR/v6_core"
        python3 run.py --test-api
        ;;
    *)
        echo "Usage: $0 [v6|v5|test]"
        echo "  v6   - Use v6.0 (recommended)"
        echo "  v5   - Use v5.0 (legacy)"
        echo "  test - Test v6.0 API connections"
        ;;
esac
