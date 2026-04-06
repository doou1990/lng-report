#!/bin/bash
# GitHub Pages 部署脚本

echo "🚀 LNG Report GitHub Pages 部署脚本"
echo "=================================="

# 检查Git配置
if [ -z "$(git config --global user.name)" ]; then
    echo "⚠️  Git用户名未配置"
    read -p "请输入Git用户名: " git_name
    git config --global user.name "$git_name"
fi

if [ -z "$(git config --global user.email)" ]; then
    echo "⚠️  Git邮箱未配置"
    read -p "请输入Git邮箱: " git_email
    git config --global user.email "$git_email"
fi

# 检查远程仓库
if ! git remote -v > /dev/null 2>&1; then
    echo "🔗 添加GitHub远程仓库..."
    git remote add origin https://github.com/doou1990/lng-report.git
fi

# 创建gh-pages分支（如果不存在）
if ! git branch -a | grep -q "gh-pages"; then
    echo "🌿 创建gh-pages分支..."
    git checkout --orphan gh-pages
    git rm -rf .
    
    # 创建基础HTML
    cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=memory/reports/LNG/daily_estimates/2026-04-06/index_v4.4.html">
    <title>LNG Report</title>
</head>
<body>
    <p>Redirecting to <a href="memory/reports/LNG/daily_estimates/2026-04-06/index_v4.4.html">latest report</a>...</p>
</body>
</html>
EOF
    
    git add index.html
    git commit -m "Initial gh-pages commit"
fi

# 推送代码
echo "📤 推送到GitHub..."
git push -u origin gh-pages

echo ""
echo "✅ 部署完成！"
echo "🌐 访问地址: https://doou1990.github.io/lng-report/"
echo ""
echo "⚠️  如果这是首次部署，请确保在GitHub仓库设置中启用GitHub Pages:"
echo "   1. 访问 https://github.com/doou1990/lng-report/settings/pages"
echo "   2. Source选择 'Deploy from a branch'"
echo "   3. Branch选择 'gh-pages'"
echo "   4. 点击Save"
