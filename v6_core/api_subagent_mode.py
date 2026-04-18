#!/usr/bin/env python3
"""
LNG市场分析助手 v6.1 - API子代理模式
核心特性: 子代理只调用API，不搜索不爬网页，彻底解决超时问题
"""
import asyncio
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class CollectionResult:
    """采集结果"""
    field: str
    name: str
    value: Any
    unit: str
    timestamp: str
    source: str
    confidence: str
    tier: int
    url: Optional[str] = None
    notes: Optional[str] = None


class APISubAgentCoordinator:
    """
    API子代理协调器
    
    架构:
    - 3个API子代理并行执行 (每个30秒超时)
    - 子代理只调用API，不搜索不爬网页
    - 主会话聚合结果
    """
    
    def __init__(self):
        self.results: Dict[str, CollectionResult] = {}
        self.stats = {
            "api_success": 0,
            "api_failed": 0,
            "start_time": None,
            "end_time": None
        }
    
    async def collect_all(self, date: Optional[str] = None) -> Dict[str, CollectionResult]:
        """
        执行API子代理采集流程
        
        Args:
            date: 采集日期，默认今天
            
        Returns:
            采集结果字典
        """
        self.stats["start_time"] = datetime.now().isoformat()
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        
        print(f"🚀 LNG Market Analysis v6.1 - API SubAgent Mode")
        print(f"📅 Target Date: {target_date}")
        print("=" * 60)
        
        # 创建3个API子代理任务
        tasks = [
            self._spawn_crude_api_agent(),      # 原油API
            self._spawn_lng_api_agent(),        # 国际LNG API
            self._spawn_inventory_api_agent(),  # 库存API
        ]
        
        # 并行执行所有子代理
        print("\n📡 Spawning 3 API SubAgents...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 聚合结果
        for result in results:
            if isinstance(result, Exception):
                print(f"   ✗ SubAgent failed: {result}")
                self.stats["api_failed"] += 1
            elif isinstance(result, dict):
                for field, data in result.items():
                    if data:
                        self.results[field] = data
                        self.stats["api_success"] += 1
        
        # 计算派生字段
        self._calculate_derived_fields()
        
        self.stats["end_time"] = datetime.now().isoformat()
        self._print_stats()
        
        return self.results
    
    async def _spawn_crude_api_agent(self) -> Dict[str, CollectionResult]:
        """
        子代理1: 原油域API采集
        采集: Brent, WTI
        """
        from sessions import sessions_spawn
        
        prompt = """你是一名原油API数据采集助理。

【任务】
通过OilPriceAPI采集Brent和WTI原油价格。

【API信息】
- Base URL: https://api.oilpriceapi.com/v1
- 商品代码: BRENT_USD, WTI_USD
- 从环境变量获取API密钥: OILPRICE_API_KEY

【执行步骤】
1. 读取环境变量 OILPRICE_API_KEY
2. 调用API获取Brent价格: /prices/latest?by_code=BRENT_USD
3. 调用API获取WTI价格: /prices/latest?by_code=WTI_USD
4. 解析返回的JSON数据

【输出格式】
返回JSON格式结果:
{
  "brent": {
    "field": "brent",
    "name": "Brent原油",
    "value": 73.21,
    "unit": "美元/桶",
    "timestamp": "2026-04-12T07:30:00Z",
    "source": "OilPriceAPI",
    "confidence": "A",
    "tier": 0,
    "notes": "Code: BRENT_USD"
  },
  "wti": {
    "field": "wti",
    "name": "WTI原油",
    "value": 69.85,
    "unit": "美元/桶",
    "timestamp": "2026-04-12T07:30:00Z",
    "source": "OilPriceAPI",
    "confidence": "A",
    "tier": 0,
    "notes": "Code: WTI_USD"
  }
}

【重要】
- 只调用API，不进行任何网页搜索或抓取
- 如果API调用失败，返回null值，confidence设为"D"
- 必须在30秒内完成
"""
        
        try:
            result = await sessions_spawn(
                task=prompt,
                timeout=30,
                mode="run"
            )
            
            # 解析子代理返回的JSON
            data = json.loads(result)
            results = {}
            
            for field, item in data.items():
                if item and item.get("value"):
                    results[field] = CollectionResult(**item)
            
            print(f"   ✓ Crude API Agent: {len(results)} fields")
            return results
            
        except Exception as e:
            print(f"   ✗ Crude API Agent failed: {e}")
            return {}
    
    async def _spawn_lng_api_agent(self) -> Dict[str, CollectionResult]:
        """
        子代理2: 国际LNG域API采集
        采集: JKM, TTF, Henry Hub
        """
        from sessions import sessions_spawn
        
        prompt = """你是一名国际LNG API数据采集助理。

【任务】
通过OilPriceAPI采集JKM、TTF、Henry Hub天然气价格。

【API信息】
- Base URL: https://api.oilpriceapi.com/v1
- 商品代码: JKM_LNG_USD, TTF_GAS_USD, HH_GAS_USD
- 从环境变量获取API密钥: OILPRICE_API_KEY

【执行步骤】
1. 读取环境变量 OILPRICE_API_KEY
2. 调用API获取JKM价格: /prices/latest?by_code=JKM_LNG_USD
3. 调用API获取TTF价格: /prices/latest?by_code=TTF_GAS_USD
4. 调用API获取Henry Hub价格: /prices/latest?by_code=HH_GAS_USD
5. 解析返回的JSON数据

【输出格式】
返回JSON格式结果:
{
  "jkm": {
    "field": "jkm",
    "name": "JKM LNG",
    "value": 11.25,
    "unit": "美元/MMBtu",
    "timestamp": "2026-04-12T07:30:00Z",
    "source": "OilPriceAPI",
    "confidence": "A",
    "tier": 0,
    "notes": "Code: JKM_LNG_USD"
  },
  "ttf": {
    "field": "ttf",
    "name": "TTF天然气",
    "value": 10.85,
    "unit": "美元/MMBtu",
    "timestamp": "2026-04-12T07:30:00Z",
    "source": "OilPriceAPI",
    "confidence": "A",
    "tier": 0,
    "notes": "Code: TTF_GAS_USD"
  },
  "henry_hub": {
    "field": "henry_hub",
    "name": "Henry Hub",
    "value": 3.05,
    "unit": "美元/MMBtu",
    "timestamp": "2026-04-12T07:30:00Z",
    "source": "OilPriceAPI",
    "confidence": "A",
    "tier": 0,
    "notes": "Code: HH_GAS_USD"
  }
}

【重要】
- 只调用API，不进行任何网页搜索或抓取
- 如果API调用失败，返回null值，confidence设为"D"
- 必须在30秒内完成
"""
        
        try:
            result = await sessions_spawn(
                task=prompt,
                timeout=30,
                mode="run"
            )
            
            data = json.loads(result)
            results = {}
            
            for field, item in data.items():
                if item and item.get("value"):
                    results[field] = CollectionResult(**item)
            
            print(f"   ✓ LNG API Agent: {len(results)} fields")
            return results
            
        except Exception as e:
            print(f"   ✗ LNG API Agent failed: {e}")
            return {}
    
    async def _spawn_inventory_api_agent(self) -> Dict[str, CollectionResult]:
        """
        子代理3: 库存域API采集
        采集: 美国原油库存、天然气库存
        """
        from sessions import sessions_spawn
        
        prompt = """你是一名库存API数据采集助理。

【任务】
通过EIA API采集美国原油库存和天然气库存数据。

【API信息】
- Base URL: https://api.eia.gov/v2
- 数据系列ID:
  - 原油库存: PET.WCRSTUS1.W
  - 天然气库存: NG.NW2_EPG0_SWO_R48_BCF.W
- 从环境变量获取API密钥: EIA_API_KEY

【执行步骤】
1. 读取环境变量 EIA_API_KEY
2. 调用API获取原油库存:
   GET /seriesid/PET.WCRSTUS1.W/data?api_key={EIA_API_KEY}
3. 调用API获取天然气库存:
   GET /seriesid/NG.NW2_EPG0_SWO_R48_BCF.W/data?api_key={EIA_API_KEY}
4. 解析返回的JSON数据，取最新一条记录

【输出格式】
返回JSON格式结果:
{
  "us_crude_inventory": {
    "field": "us_crude_inventory",
    "name": "美国商业原油库存",
    "value": 450.2,
    "unit": "百万桶",
    "timestamp": "2026-04-11",
    "source": "EIA",
    "confidence": "A",
    "tier": 0,
    "notes": "Series: PET.WCRSTUS1.W"
  },
  "us_ng_inventory": {
    "field": "us_ng_inventory",
    "name": "美国天然气库存",
    "value": 1850,
    "unit": "十亿立方英尺",
    "timestamp": "2026-04-11",
    "source": "EIA",
    "confidence": "A",
    "tier": 0,
    "notes": "Series: NG.NW2_EPG0_SWO_R48_BCF.W"
  }
}

【重要】
- 只调用API，不进行任何网页搜索或抓取
- 如果API调用失败，返回null值，confidence设为"D"
- 必须在30秒内完成
"""
        
        try:
            result = await sessions_spawn(
                task=prompt,
                timeout=30,
                mode="run"
            )
            
            data = json.loads(result)
            results = {}
            
            for field, item in data.items():
                if item and item.get("value"):
                    results[field] = CollectionResult(**item)
            
            print(f"   ✓ Inventory API Agent: {len(results)} fields")
            return results
            
        except Exception as e:
            print(f"   ✗ Inventory API Agent failed: {e}")
            return {}
    
    def _calculate_derived_fields(self):
        """计算派生字段"""
        # Brent-WTI价差
        if "brent" in self.results and "wti" in self.results:
            brent = self.results["brent"]
            wti = self.results["wti"]
            if brent.value and wti.value:
                spread = brent.value - wti.value
                self.results["brent_wti_spread"] = CollectionResult(
                    field="brent_wti_spread",
                    name="Brent-WTI价差",
                    value=round(spread, 2),
                    unit="美元/桶",
                    timestamp=brent.timestamp,
                    source="Calculated",
                    confidence=min(brent.confidence, wti.confidence),
                    tier=0,
                    notes=f"Derived: Brent(${brent.value}) - WTI(${wti.value})"
                )
                print(f"\n📊 Calculated Brent-WTI spread: ${round(spread, 2)}")
        
        # JKM-TTF价差
        if "jkm" in self.results and "ttf" in self.results:
            jkm = self.results["jkm"]
            ttf = self.results["ttf"]
            if jkm.value and ttf.value:
                spread = jkm.value - ttf.value
                self.results["jkm_ttf_spread"] = CollectionResult(
                    field="jkm_ttf_spread",
                    name="JKM-TTF价差",
                    value=round(spread, 2),
                    unit="美元/MMBtu",
                    timestamp=jkm.timestamp,
                    source="Calculated",
                    confidence=min(jkm.confidence, ttf.confidence),
                    tier=0,
                    notes=f"Derived: JKM(${jkm.value}) - TTF(${ttf.value})"
                )
                print(f"📊 Calculated JKM-TTF spread: ${round(spread, 2)}")
    
    def _print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("📈 Collection Statistics")
        print("=" * 60)
        print(f"API Success: {self.stats['api_success']}")
        print(f"API Failed:  {self.stats['api_failed']}")
        print(f"Total Fields: {len(self.results)}")
        
        # 按置信度统计
        conf_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
        for result in self.results.values():
            if result.confidence in conf_counts:
                conf_counts[result.confidence] += 1
        
        print(f"\nConfidence Distribution:")
        for conf, count in conf_counts.items():
            print(f"  {conf}级: {count}")
    
    def export_json(self, filepath: str):
        """导出结果为JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "data": {k: asdict(v) for k, v in self.results.items()}
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Results exported to: {filepath}")


# 便捷函数
async def collect_with_api_subagents(date: Optional[str] = None) -> Dict[str, CollectionResult]:
    """
    使用API子代理采集数据的便捷函数
    
    Args:
        date: 采集日期
        
    Returns:
        采集结果字典
    """
    coordinator = APISubAgentCoordinator()
    return await coordinator.collect_all(date)


if __name__ == "__main__":
    # 测试API子代理采集
    results = asyncio.run(collect_with_api_subagents())
    print(f"\n✅ Collected {len(results)} fields via API SubAgents")
