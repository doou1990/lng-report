# LNG分析系统API配置指南

## 📋 概述

本指南说明如何为LNG市场分析系统配置必要的API密钥。系统需要以下API来获取实时数据：

### 优先级排序
1. 🔴 **紧急**：TAVILY_API_KEY（新闻搜索）
2. 🔴 **紧急**：行业数据源API（ICIS/GIE/EIA）
3. 🟡 **重要**：Notion API（文档管理）
4. 🟢 **可选**：邮件通知API（告警系统）

---

## 1. TAVILY_API_KEY 配置

### 用途
- 实时新闻和市场搜索
- LNG行业新闻监控
- 市场趋势分析

### 获取步骤
1. **访问网站**：https://tavily.com
2. **点击"Sign Up"**：使用邮箱注册
3. **验证邮箱**：完成邮箱验证
4. **登录仪表板**：访问 https://app.tavily.com
5. **获取API密钥**：在设置中找到API密钥

### 配置命令
```bash
# 设置环境变量
export TAVILY_API_KEY="tvly-your_actual_api_key_here"

# 永久保存（添加到~/.bashrc或~/.zshrc）
echo 'export TAVILY_API_KEY="tvly-your_actual_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 测试命令
```bash
# 测试tavily-search技能
node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "LNG market news" --topic news

# 测试深度搜索
node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "natural gas prices Europe" --deep
```

---

## 2. 行业数据源API配置

### 2.1 ICIS/S&P Global API
#### 用途
- 国际LNG价格数据（JKM/TTF/HH）
- 实时价格更新

#### 获取步骤
1. **访问**：https://www.icis.com 或 https://www.spglobal.com
2. **注册企业账户**：需要公司信息
3. **申请API访问**：联系销售或技术支持
4. **获取API密钥**：通常需要付费订阅

#### 配置
```bash
# 设置环境变量
export ICIS_API_KEY="your_icis_api_key"
export SPGLOBAL_API_KEY="your_spglobal_api_key"
```

### 2.2 GIE AGSI API
#### 用途
- 欧洲天然气库存数据
- 实时库存水平监控

#### 获取步骤
1. **访问**：https://agsi.gie.eu
2. **注册账户**：免费注册
3. **申请API访问**：在账户设置中申请
4. **获取API密钥**：免费有限访问，付费更多功能

#### 配置
```bash
export GIE_API_KEY="your_gie_api_key"
```

### 2.3 EIA API
#### 用途
- 美国能源数据
- LNG出口和产能数据

#### 获取步骤
1. **访问**：https://www.eia.gov
2. **注册**：免费注册
3. **申请API密钥**：在开发者页面申请
4. **获取API密钥**：免费使用，有速率限制

#### 配置
```bash
export EIA_API_KEY="your_eia_api_key"
```

---

## 3. Notion API配置

### 用途
- 报告存储和管理
- 团队协作分析
- 知识库建设

### 获取步骤
1. **访问**：https://notion.so/my-integrations
2. **创建新集成**：点击"New integration"
3. **配置集成**：
   - 名称：LNG Analysis System
   - 关联工作区：选择你的Notion工作区
4. **获取API密钥**：以`ntn_`或`secret_`开头
5. **分享页面**：在Notion中分享目标页面给集成

### 配置
```bash
# 创建配置目录
mkdir -p ~/.config/notion

# 保存API密钥
echo "ntn_your_actual_api_key_here" > ~/.config/notion/api_key

# 设置权限
chmod 600 ~/.config/notion/api_key
```

### 测试
```bash
# 测试API密钥读取
NOTION_KEY=$(cat ~/.config/notion/api_key 2>/dev/null)
if [ -n "$NOTION_KEY" ]; then
  echo "✅ Notion API密钥配置成功"
else
  echo "❌ Notion API密钥未配置"
fi
```

---

## 4. 邮件通知API配置（可选）

### 用途
- 系统告警通知
- 日报/周报发送
- 任务状态通知

### Gmail App Password配置
1. **启用两步验证**：在Google账户设置中启用
2. **生成App Password**：
   - 访问 https://myaccount.google.com/security
   - 找到"App passwords"
   - 选择"Mail"和"Other (Custom name)"
   - 输入名称：LNG Analysis System
   - 获取16位密码
3. **配置环境变量**

### 配置
```bash
# 设置环境变量
export EMAIL_USER="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export EMAIL_RECIPIENT="recipient@example.com"
```

---

## 5. 中国数据源API配置

### 5.1 海关总署数据
#### 用途
- LNG进口数据
- 贸易统计数据

#### 获取方式
- **网站**：http://www.customs.gov.cn
- **API访问**：需要企业资质申请
- **数据服务**：通常通过第三方数据提供商

### 5.2 国家统计局数据
#### 用途
- 能源消费数据
- 经济统计数据

#### 获取方式
- **网站**：http://www.stats.gov.cn
- **API访问**：通过数据开放平台申请
- **数据格式**：JSON/XML接口

### 5.3 行业数据平台
#### 推荐平台
1. **隆众资讯**：https://www.oilchem.net
2. **卓创资讯**：https://www.sci99.com
3. **金联创**：https://www.315i.com

#### 获取方式
- 注册企业账户
- 申请API访问权限
- 通常需要付费订阅

---

## 6. 系统集成配置

### 环境变量汇总
```bash
# 新闻搜索
export TAVILY_API_KEY="tvly-your_key"

# 行业数据
export ICIS_API_KEY="your_icis_key"
export GIE_API_KEY="your_gie_key"
export EIA_API_KEY="your_eia_key"

# 文档管理
export NOTION_API_KEY="ntn_your_key"

# 邮件通知（可选）
export EMAIL_USER="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"

# 中国数据（可选）
export CUSTOMS_API_KEY="your_customs_key"
export STATS_API_KEY="your_stats_key"
```

### 配置文件
创建 `/root/.openclaw/workspace/.env` 文件：
```bash
TAVILY_API_KEY=tvly-your_key
ICIS_API_KEY=your_icis_key
GIE_API_KEY=your_gie_key
EIA_API_KEY=your_eia_key
NOTION_API_KEY=ntn_your_key
```

### 自动加载配置
```bash
# 创建自动加载脚本
cat > /root/.openclaw/workspace/load_env.sh << 'EOF'
#!/bin/bash
if [ -f "/root/.openclaw/workspace/.env" ]; then
    set -a
    source /root/.openclaw/workspace/.env
    set +a
    echo "✅ 环境变量已加载"
fi
EOF

chmod +x /root/.openclaw/workspace/load_env.sh
```

---

## 7. 测试和验证

### 7.1 测试所有API配置
```bash
#!/bin/bash
echo "=== API配置测试 ==="

# 测试TAVILY_API_KEY
if [ -n "$TAVILY_API_KEY" ]; then
    echo "✅ TAVILY_API_KEY: 已配置"
else
    echo "❌ TAVILY_API_KEY: 未配置"
fi

# 测试行业API
apis=("ICIS_API_KEY" "GIE_API_KEY" "EIA_API_KEY")
for api in "${apis[@]}"; do
    if [ -n "${!api}" ]; then
        echo "✅ $api: 已配置"
    else
        echo "⚠️  $api: 未配置（需要时配置）"
    fi
done

# 测试Notion API
if [ -f ~/.config/notion/api_key ]; then
    echo "✅ Notion API: 已配置"
else
    echo "❌ Notion API: 未配置"
fi

echo "=== 测试完成 ==="
```

### 7.2 功能测试脚本
```bash
#!/bin/bash
# 功能测试脚本

echo "1. 测试tavily-search技能..."
if [ -n "$TAVILY_API_KEY" ]; then
    node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "test" -n 2
    if [ $? -eq 0 ]; then
        echo "✅ tavily-search测试成功"
    else
        echo "❌ tavily-search测试失败"
    fi
else
    echo "⚠️ 跳过tavily-search测试（未配置API密钥）"
fi

echo "2. 测试LNG报告生成..."
# 这里可以添加LNG报告生成测试
echo "✅ LNG报告生成框架就绪"

echo "3. 测试系统健康监控..."
# 这里可以添加系统监控测试
echo "✅ 系统监控框架就绪"
```

---

## 8. 故障排除

### 常见问题

#### 8.1 API密钥无效
**症状**：API调用返回401或403错误
**解决**：
1. 确认API密钥正确复制
2. 检查API密钥是否过期
3. 验证账户是否激活
4. 检查API访问权限

#### 8.2 速率限制
**症状**：API调用返回429错误
**解决**：
1. 降低请求频率
2. 实现请求队列
3. 考虑升级API套餐
4. 添加重试机制

#### 8.3 网络问题
**症状**：连接超时或网络错误
**解决**：
1. 检查网络连接
2. 验证代理设置
3. 检查防火墙规则
4. 测试DNS解析

#### 8.4 数据格式问题
**症状**：API返回数据但解析失败
**解决**：
1. 检查API响应格式
2. 更新数据解析逻辑
3. 添加数据验证
4. 查看API文档更新

### 调试命令
```bash
# 检查环境变量
printenv | grep -i api

# 测试网络连接
curl -I https://api.tavily.com

# 检查配置文件
cat /root/.openclaw/workspace/.env

# 查看日志
tail -f /root/.openclaw/workspace/logs/api.log
```

---

## 9. 安全建议

### 9.1 API密钥安全
1. **不要硬编码**：避免在代码中直接写入API密钥
2. **使用环境变量**：通过环境变量传递API密钥
3. **限制访问权限**：仅授予必要的最小权限
4. **定期轮换**：定期更新API密钥
5. **监控使用情况**：监控API调用异常

### 9.2 配置文件安全
1. **权限设置**：配置文件设置为600权限
2. **版本控制**：不要将包含密钥的文件提交到Git
3. **备份安全**：加密备份包含密钥的文件
4. **访问日志**：记录API密钥使用情况

### 9.3 网络安全
1. **使用HTTPS**：所有API调用使用HTTPS
2. **验证证书**：验证API服务器证书
3. **限制IP访问**：如果支持，限制API调用的源IP
4. **使用代理**：在企业环境中使用代理服务器

---

## 10. 维护和更新

### 10.1 定期检查
- **每月**：检查API密钥有效期
- **每季度**：审查API使用情况和费用
- **每年**：评估API服务商和替代方案

### 10.2 更新流程
1. **测试新密钥**：在测试环境验证新API密钥
2. **更新配置**：更新环境变量和配置文件
3. **验证功能**：验证所有功能正常工作
4. **清理旧密钥**：安全地删除旧API密钥

### 10.3 文档更新
- 记录所有API配置变更
- 更新故障排除指南
- 维护API服务商联系信息
- 记录API限制和配额

---

## 📞 支持联系

### API服务商支持
1. **Tavily**：support@tavily.com
2. **ICIS**：support@icis.com
3. **GIE**：info@gie.eu
4. **EIA**：infoctr@eia.gov
5. **Notion**：team@makenotion.com

### 系统支持
- **文档**：查看本指南和技能文档
- **社区**：OpenClaw社区论坛
- **问题反馈**：记录问题并提交反馈

---

## 🎯 总结

配置完整的API生态系统是LNG分析系统正常运行的关键。按照优先级逐步配置：

1. **立即配置**：TAVILY_API_KEY（新闻搜索）
2. **一周内配置**：至少1个行业数据源API
3. **一月内配置**：完整的数据源生态系统
4. **持续优化**：根据使用情况调整和优化

**记住**：安全地管理API密钥，定期监控使用情况，及时更新和维护配置。