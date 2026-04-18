# GIE AGSI API 对接指南

## 概述

GIE (Gas Infrastructure Europe) AGSI (Aggregated Gas Storage Inventory) 是欧洲天然气基础设施协会提供的透明度平台，提供欧洲各国天然气库存数据。

## API 访问方式

### 1. 注册账户

访问 https://agsi.gie.eu/account 注册账户，获取个人 API 密钥。

**注册信息:**
- API 服务免费提供给公众使用
- 注册目的是为了评估和改进系统性能
- 可以选择订阅 API 邮件列表获取更新通知

### 2. API 密钥使用

**API 密钥**: `3e9a0844c1e529e1dd2119c1cca209e6`

**关联账户**: `285823779@qq.com` ✅

**当前状态**: ⚠️ 已关联账户，等待激活

**注意:** 
- 密钥已与邮箱账户关联
- 可能需要验证邮箱或等待 GIE 审核
- 激活通常需要几分钟到几小时

### 3. API 端点

```
基础URL: https://agsi.gie.eu/api

主要端点:
- /api/eu                    # 欧盟整体数据
- /api/{country_code}        # 特定国家数据 (如: /api/de, /api/fr)
- /api/data/{start}/{end}    # 历史数据范围
```

### 4. 请求示例

```bash
# 获取欧盟数据
curl "https://agsi.gie.eu/api/eu?api_key=YOUR_API_KEY"

# 获取德国数据
curl "https://agsi.gie.eu/api/de?api_key=YOUR_API_KEY"

# 获取历史数据
curl "https://agsi.gie.eu/api/data/2026-04-01/2026-04-07?api_key=YOUR_API_KEY&country=EU"
```

## 数据结构

### 响应字段说明

```json
{
  "name": "EU",                    // 国家/区域名称
  "code": "eu",                    // 国家代码
  "gasDayStart": "2026-04-05",     // 统计开始日期
  "gasDayEnd": "2026-04-06",       // 统计结束日期
  "gasInStorage": "321.4537",      // 库存量 (TWh)
  "consumption": "3519",           // 消费量 (GWh/d)
  "consumptionFull": "9.13",       // 可消费天数
  "injection": "2938.63",          // 注入量 (GWh/d)
  "withdrawal": "323.2",           // 提取量 (GWh/d)
  "netWithdrawal": "-2615.4",      // 净提取量 (GWh/d)
  "workingGasVolume": "1131.1772", // 工作气量 (TWh)
  "injectionCapacity": "12234.29", // 注入能力 (GWh/d)
  "withdrawalCapacity": "20050.69",// 提取能力 (GWh/d)
  "full": "28.42",                 // 填充率 (%)
  "trend": "0.23",                 // 日变化 (%)
  "status": "E"                    // 状态 (E=估算, C=确认)
}
```

## 国家代码映射

| 代码 | 国家 |
|------|------|
| eu | EU (欧盟整体) |
| at | Austria (奥地利) |
| be | Belgium (比利时) |
| bg | Bulgaria (保加利亚) |
| hr | Croatia (克罗地亚) |
| cz | Czech Republic (捷克) |
| dk | Denmark (丹麦) |
| fr | France (法国) |
| de | Germany (德国) |
| hu | Hungary (匈牙利) |
| it | Italy (意大利) |
| lv | Latvia (拉脱维亚) |
| nl | Netherlands (荷兰) |
| pl | Poland (波兰) |
| pt | Portugal (葡萄牙) |
| ro | Romania (罗马尼亚) |
| sk | Slovakia (斯洛伐克) |
| es | Spain (西班牙) |
| se | Sweden (瑞典) |
| uk | United Kingdom (英国) |

## 使用规范

### 数据引用要求

所有数据必须注明 GIE 为数据来源：

- 最低要求: 在数据下方注明 "GIE (Gas Infrastructure Europe)" 或 "GIE AGSI"
- 建议格式: "数据来源: GIE AGSI 透明度平台"
- 如果未注明来源，GIE 有权禁用 API 访问密钥

### 使用限制

- API 服务免费提供
- 仅提供平台上当前可用的数据（REMIT 提供的数据子集）
- 请合理使用，避免过度频繁的请求

## 集成到 LNG 报告

### Python 客户端

已创建 `tools/gie_storage_client.py` 客户端类：

```python
from tools.gie_storage_client import GIEStorageClient

# 初始化客户端
client = GIEStorageClient(api_key="your_api_key")

# 获取欧盟数据
eu_data = client.get_eu_inventory()

# 获取主要国家数据
countries = client.get_major_countries_inventory()

# 获取完整摘要
summary = client.get_inventory_summary()
```

### 数据采集脚本

使用 `scripts/fetch_inventory_data.py`：

```bash
# 获取 JSON 格式数据
python scripts/fetch_inventory_data.py

# 获取 Markdown 格式（用于报告）
python scripts/fetch_inventory_data.py --format markdown

# 保存到文件
python scripts/fetch_inventory_data.py --output inventory_2026-04-07.json
```

## 故障排除

### API 返回 "access denied"

**原因:** API 密钥未与注册账户关联

**解决方案:**
1. 访问 https://agsi.gie.eu/account 注册账户
2. 使用注册后的 API 密钥
3. 或联系 GIE 确认密钥状态

### 数据返回空

**原因:** 
- 日期范围无效
- 国家代码错误
- 该日期无数据

**解决方案:**
- 检查国家代码是否正确
- 使用最近日期查询
- 查看 GIE 网站确认数据可用性

### 请求超时

**解决方案:**
- 减少查询日期范围
- 使用分页参数
- 增加超时时间设置

## 相关链接

- GIE 官网: https://www.gie.eu
- AGSI 平台: https://agsi.gie.eu
- API 注册: https://agsi.gie.eu/account
- ALSI (LNG): https://alsi.gie.eu
- 数据使用规则: https://agsi.gie.eu/data-usage

## 更新日志

### 2026-04-07
- 完成 GIE API 客户端开发
- 创建库存助理配置
- 添加备用数据源支持
- 待解决: API 密钥需要注册账户关联
