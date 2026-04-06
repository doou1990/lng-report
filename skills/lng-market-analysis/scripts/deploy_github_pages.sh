#!/bin/bash
# GitHub Pages部署脚本
# 使用方法: 1. 在GitHub创建仓库 2. 修改下面的REPO_URL 3. 运行脚本

REPO_URL="https://github.com/YOUR_USERNAME/lng-report.git"
REPO_NAME="lng-report"

echo "=== LNG报告 GitHub Pages部署 ==="
echo ""

# 创建部署目录
mkdir -p /tmp/lng-report-deploy
cd /tmp/lng-report-deploy

# 复制网站文件
cp /var/www/lng-report/index.html .

# 创建GitHub Pages配置文件
cat > _config.yml << 'EOF'
title: LNG & 原油市场日报
description: 每日更新的LNG液化天然气与原油市场分析报告
EOF

# 初始化git仓库
git init
git add .
git commit -m "Initial commit: LNG report website"

echo ""
echo "=== 部署步骤 ==="
echo "1. 在GitHub创建新仓库: https://github.com/new"
echo "   仓库名: lng-report"
echo "   选择 Public"
echo ""
echo "2. 修改本脚本中的 REPO_URL 为你的仓库地址"
echo "   例如: https://github.com/你的用户名/lng-report.git"
echo ""
echo "3. 运行以下命令:"
echo "   cd /tmp/lng-report-deploy"
echo "   git remote add origin $REPO_URL"
echo "   git push -u origin main"
echo ""
echo "4. 在GitHub仓库设置中启用Pages:"
echo "   Settings → Pages → Source → Deploy from a branch"
echo "   选择 main branch → / (root) → Save"
echo ""
echo "5. 等待2-3分钟，访问:"
echo "   https://你的用户名.github.io/lng-report/"
echo ""
