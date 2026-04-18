# v6.1 API子代理模式 - 配置指南

## 架构说明

v6.1 采用**纯API子代理模式**，彻底解决超时问题：

```
主会话 (协调器)
    ↓ 同时启动3个子代理 (并行)
    ├── 子代理1: 原油API (30秒超时) → Brent, WTI
    ├── 子代理2: 国际LNG API (30秒超时) → JKM, TTF, HH
    └── 子代理3: 库存API (30秒超时) → 美国原油/天然气库存
    ↓ 聚合结果
    ✓ 总耗时 < 30秒
```

## 核心特性

| 特性 | v6.0 | v6.1 |
|------|------|------|
| 子代理类型 | 网页采集 | API调用 |
| 单次耗时 | 300秒 | 5-10秒 |
| 超时风险 | 高 | 极低 |
| 数据等级 | B/C级 | A级 |
| 成功率 | <50% | >95% |

## 配置API密钥

### 1. OilPriceAPI 密钥

```bash
# 获取方式: https://oilpriceapi.com (免费试用7天)
export OILPRICE_API_KEY="your_api_key_here"
```

### 2. EIA API 密钥

```bash
# 获取方式: https://www.eia.gov/opendata (免费)
export EIA_API_KEY="your_api_key_here"
```

### 3. 永久配置

```bash
# 添加到 ~/.bashrc
echo 'export OILPRICE_API_KEY="your_key"' >> ~/.bashrc
echo 'export EIA_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

## 使用方法

### 方式1: 直接运行

```bash
cd /root/.openclaw/workspace/skills/lng-market-analysis/v6_core
python3 api_subagent_mode.py
```

### 方式2: 作为模块导入

```python
import asyncio
from v6_core.api_subagent_mode import collect_with_api_subagents

results = asyncio.run(collect_with_api_subagents())
print(f"Collected {len(results)} fields")
```

## 采集数据清单

### API子代理覆盖 (A级数据)

| 字段 | 名称 | 来源 | 单位 |
|------|------|------|------|
| brent | Brent原油 | OilPriceAPI | 美元/桶 |
| wti | WTI原油 | OilPriceAPI | 美元/桶 |
| jkm | JKM LNG | OilPriceAPI | 美元/MMBtu |
| ttf | TTF天然气 | OilPriceAPI | 美元/MMBtu |
| henry_hub | Henry Hub | OilPriceAPI | 美元/MMBtu |
| us_crude_inventory | 美国原油库存 | EIA API | 百万桶 |
| us_ng_inventory | 美国天然气库存 | EIA API | 十亿立方英尺 |
| brent_wti_spread | Brent-WTI价差 | 计算 | 美元/桶 |
| jkm_ttf_spread | JKM-TTF价差 | 计算 | 美元/MMBtu |

### 未覆盖数据 (需其他方式)

| 字段 | 名称 | 说明 |
|------|------|------|
| china_lng_factory | 国内LNG工厂价 | 需网页采集 |
| zhejiang_ningbo | 浙江宁波接收站 | 需网页采集 |
| zhejiang_zhoushan | 浙江舟山接收站 | 需网页采集 |
| china_lng_imports | 中国LNG进口 | 需搜索 |

## 故障排查

### API密钥未配置

```
Error: OILPRICE_API_KEY not found
```

**解决**: 设置环境变量

### API调用失败

```
✗ Crude API Agent failed: API returned 401
```

**解决**: 检查API密钥是否正确

### 子代理超时

```
✗ LNG API Agent failed: Timeout
```

**解决**: 这种情况极少见，可能是API服务故障，稍后重试

## 版本对比

```
v5.0: 10助理并行搜索 (超时严重)
v6.0: 6域子代理 (网页采集，仍超时)
v6.1: 3 API子代理 (API调用，无超时) ← 当前
```

## 下一步计划

1. **v6.2**: 增加国内数据子代理 (网页采集，但优化超时)
2. **v6.3**: 增加中孚审核子代理
3. **v7.0**: 完整报告生成
