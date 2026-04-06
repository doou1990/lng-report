# 优化计划执行文档 - 期货价格与库存数据

**执行时间**: 2026-04-05 18:26  
**执行目标**: 解决4项严重差距  
**状态**: 数据源已找到，开始实施

---

## ✅ 第一步完成: 数据源搜索

### 1. 期货价格数据源 ✅

#### Brent原油期货
| 数据源 | 类型 | 覆盖 | 状态 |
|--------|------|------|------|
| **Oil Price API** | ICE Brent Futures API | 96个月合约 | ⭐ 推荐 |
| **ICE官网** | 官方数据 | 全部合约 | ✅ 可用 |
| **Databento** | 综合期货数据 | 多交易所 | ✅ 可用 |

**API端点**:
```
Oil Price API: https://docs.oilpriceapi.com/api-reference/futures/ice-brent
ICE官网: https://www.ice.com/products/219/Brent-Crude-Futures
```

#### JKM LNG期货
| 数据源 | 类型 | 覆盖 | 状态 |
|--------|------|------|------|
| **ICE官网** | JKM LNG (Platts) Future | 全部合约 | ⭐ 推荐 |
| **TradingView** | JKM1! 连续合约 | 实时图表 | ✅ 可用 |
| **Barchart** | JKM期货价格 | 多合约 | ✅ 可用 |

**API端点**:
```
ICE官网: https://www.ice.com/products/6753280/JKM-LNG-PLATTS-Future
合约规格: https://www.ice.com/api/productguide/spec/6753280/pdf
```

#### TTF天然气期货
| 数据源 | 类型 | 覆盖 | 状态 |
|--------|------|------|------|
| **ICE官网** | Dutch TTF Gas Futures | 全部合约 | ⭐ 推荐 |
| **Barchart** | TTF期货价格 | 多合约 | ✅ 可用 |
| **Commodities-API** | TFMI月度价格 | API接口 | ✅ 可用 |

**API端点**:
```
ICE官网: https://www.ice.com/products/68361290/Dutch-TTF-Natural-Gas-1st-Line-Financial-Futures
Commodities-API: https://commodities-api.com/symbols/TFMI
```

---

### 2. 库存数据源 ✅

#### 欧洲LNG库存
| 数据源 | 类型 | 覆盖 | 状态 |
|--------|------|------|------|
| **GIE AGSI** | 欧洲储气库存 | 欧盟各国 | ⭐ 推荐 |
| **Energy Dashboard** | 瑞士能源仪表板 | 可视化 | ✅ 可用 |

**API端点**:
```
GIE AGSI: https://agsi.gie.eu/
透明度平台: https://www.gie.eu/agsi-and-alsi-transparency-platforms/
```

#### 美国天然气库存
| 数据源 | 类型 | 覆盖 | 状态 |
|--------|------|------|------|
| **EIA API** | 美国天然气库存 | 全美 | ⭐ 推荐 |

**API端点**:
```
EIA API: https://catalog.data.gov/dataset/natural-gas-data-storage-application-programming-interface-api
```

#### 中国LNG库存
| 数据源 | 类型 | 覆盖 | 状态 |
|--------|------|------|------|
| **卓创资讯** | 接收站供应量 | 全国 | ⚠️ 需订阅 |
| **JLC** | 中国商品数据 | 能源 | ⚠️ 需付费 |
| **隆众资讯** | 库存数据 | 部分 | ⚠️ 需订阅 |

**状态**: 中国库存数据需要付费订阅，暂时使用公开数据源估算

---

## 🎯 第二步: 实施计划

### 新增助理: 期货助理 (第11位)

**职责**: 采集期货价格数据

**采集内容**:
```yaml
Brent原油期货:
  - 现货价格 (Spot)
  - 1个月远期 (M1)
  - 3个月远期 (M3)
  - 6个月远期 (M6)
  数据源: ICE, Oil Price API

JKM LNG期货:
  - 现货价格 (Spot)
  - 1个月远期 (M1)
  - 3个月远期 (M3)
  数据源: ICE

TTF天然气期货:
  - 现货价格 (Spot)
  - 1个月远期 (M1)
  - 3个月远期 (M3)
  数据源: ICE

Henry Hub期货:
  - 现货价格 (Spot)
  - 1个月远期 (M1)
  数据源: CME, NGI
```

### 新增助理: 库存助理 (第12位)

**职责**: 采集库存数据

**采集内容**:
```yaml
欧洲库存:
  - 欧盟整体库存水平
  - 主要国家库存 (德国/法国/意大利)
  - 库存变化趋势
  数据源: GIE AGSI

美国库存:
  - EIA周度库存数据
  - 库存变化
  - 与5年均值对比
  数据源: EIA API

中国库存 (估算):
  - 主要接收站库存估算
  - 基于进口量和消费量推算
  数据源: 公开数据估算
```

---

## 📊 第三步: 价差分析模块

### 价差计算

```python
# 价差计算公式

# 1. JKM-TTF价差 (跨区套利)
jkm_ttf_spread = JKM_price - TTF_price
# 单位统一为 $/MMBtu

# 2. 原油-LNG热值比价
crude_lng_ratio = Brent_price / (JKM_price * 5.8)
# Brent: $/barrel
# JKM: $/MMBtu
# 1 barrel = 5.8 MMBtu

# 3. 期货-现货价差 (Contango/Backwardation)
contango = Futures_M1 - Spot
# >0: Contango (期货升水)
# <0: Backwardation (期货贴水)

# 4. 进口-国产价差
import_domestic_spread = Import_LNG_price - Domestic_LNG_price
```

### 价差展示

```yaml
价差仪表板:
  - JKM-TTF价差走势图
  - 原油-LNG比价走势图
  - 期限结构图 (Spot/M1/M3/M6)
  - 套利机会提示
```

---

## 🔧 第四步: 技术实施

### 期货数据采集代码框架

```python
# futures_collector.py
import requests
from datetime import datetime

class FuturesCollector:
    def __init__(self):
        self.ice_base_url = "https://www.ice.com"
        self.oilprice_api_key = "YOUR_API_KEY"
    
    def get_brent_futures(self):
        """获取Brent原油期货价格"""
        # 调用ICE API或Oil Price API
        pass
    
    def get_jkm_futures(self):
        """获取JKM LNG期货价格"""
        # 调用ICE API
        pass
    
    def get_ttf_futures(self):
        """获取TTF天然气期货价格"""
        # 调用ICE API
        pass
    
    def calculate_spreads(self):
        """计算价差"""
        # JKM-TTF价差
        # 原油-LNG比价
        # 期限结构
        pass
```

### 库存数据采集代码框架

```python
# inventory_collector.py
import requests

class InventoryCollector:
    def __init__(self):
        self.gie_agsi_url = "https://agsi.gie.eu/api"
        self.eia_api_key = "YOUR_API_KEY"
    
    def get_eu_inventory(self):
        """获取欧洲库存数据"""
        # 调用GIE AGSI API
        pass
    
    def get_us_inventory(self):
        """获取美国库存数据"""
        # 调用EIA API
        pass
    
    def calculate_inventory_trend(self):
        """计算库存趋势"""
        # 与历史同期对比
        # 与5年均值对比
        pass
```

---

## 📅 实施时间表

### 今晚 (2026-04-05)
- [x] 搜索期货数据源 ✅
- [x] 搜索库存数据源 ✅
- [ ] 设计期货助理协议
- [ ] 设计库存助理协议

### 明天 (2026-04-06)
- [ ] 实现期货数据采集代码
- [ ] 实现库存数据采集代码
- [ ] 测试数据源可用性

### 本周内 (2026-04-11前)
- [ ] 期货价格数据上线
- [ ] 库存数据上线
- [ ] 价差分析模块上线
- [ ] 更新报告模板

---

## 🎯 预期成果

### 数据完整度提升

| 数据类型 | 当前 | 优化后 | 提升 |
|----------|------|--------|------|
| 价格数据 | 现货 | 现货+期货 | +100% |
| 价差分析 | 无 | 4种价差 | 新增 |
| 库存数据 | 无 | 欧美中 | 新增 |
| **数据完整度** | **80%** | **90%** | **+10%** |

### 报告内容增强

新增模块:
1. ✅ 期货价格板块 (Brent/JKM/TTF/HH)
2. ✅ 价差分析板块 (JKM-TTF/原油-LNG/期限结构)
3. ✅ 库存监控板块 (欧美中库存水平)
4. ✅ 市场情绪指标 (基于价差和库存)

---

## 📚 参考资源

### API文档
- [Oil Price API - ICE Brent](https://docs.oilpriceapi.com/api-reference/futures/ice-brent)
- [ICE JKM LNG Futures](https://www.ice.com/products/6753280/JKM-LNG-PLATTS-Future)
- [ICE TTF Gas Futures](https://www.ice.com/products/68361290/Dutch-TTF-Natural-Gas-1st-Line-Financial-Futures)
- [GIE AGSI](https://agsi.gie.eu/)
- [EIA Natural Gas API](https://catalog.data.gov/dataset/natural-gas-data-storage-application-programming-interface-api)

---

*执行状态: 数据源已找到，开始实施*  
*下一步: 设计助理协议和实现代码*
