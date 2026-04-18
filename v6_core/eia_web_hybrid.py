#!/usr/bin/env python3
"""
LNG市场分析助手 v6.1 - EIA+网页混合模式
使用 EIA API (您已提供密钥) + 网页采集原油价格
"""
import asyncio
import json
import os
import requests
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


class EIAAPIClient:
    """EIA API 客户端 - 使用您提供的密钥"""
    
    BASE_URL = "https://api.eia.gov/v2"
    
    # 数据系列ID
    SERIES_IDS = {
        "wti_price": "PET.RWTC.D",  # WTI现货价格
        "brent_price": "PET.RBRTE.D",  # Brent现货价格
        "henry_hub_price": "NG.RNGWHHD.D",  # Henry Hub价格
        "us_crude_inventory": "PET.WCRSTUS1.W",  # 美国商业原油库存
        "us_ng_inventory": "NG.NW2_EPG0_SWO_R48_BCF.W",  # 天然气库存
        "lng_exports": "NG.NW2_EPG0_EEX_NUS-NUI_BCF.M",  # LNG出口
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("EIA_API_KEY")
        if not self.api_key:
            raise ValueError("EIA_API_KEY not found. Please set it in environment variables.")
        self.session = requests.Session()
    
    def get_series(self, series_id: str, limit: int = 1) -> Optional[Dict]:
        """获取数据系列"""
        try:
            url = f"{self.BASE_URL}/seriesid/{series_id}/data"
            params = {
                "api_key": self.api_key,
                "frequency": "daily",
                "data[0]": "value",
                "sort[0][column]": "period",
                "sort[0][direction]": "desc",
                "offset": 0,
                "length": limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "response" not in data or "data" not in data["response"]:
                return None
            
            records = data["response"]["data"]
            if not records:
                return None
            
            latest = records[0]
            return {
                "series_id": series_id,
                "value": float(latest["value"]),
                "period": latest["period"],
                "unit": data["response"].get("units", ""),
            }
            
        except Exception as e:
            print(f"   EIA API Error: {e}")
            return None
    
    def get_wti_price(self) -> Optional[Dict]:
        """获取WTI价格"""
        return self.get_series(self.SERIES_IDS["wti_price"])
    
    def get_brent_price(self) -> Optional[Dict]:
        """获取Brent价格"""
        return self.get_series(self.SERIES_IDS["brent_price"])
    
    def get_henry_hub_price(self) -> Optional[Dict]:
        """获取Henry Hub价格"""
        return self.get_series(self.SERIES_IDS["henry_hub_price"])
    
    def get_crude_inventory(self) -> Optional[Dict]:
        """获取原油库存"""
        return self.get_series(self.SERIES_IDS["us_crude_inventory"])
    
    def get_ng_inventory(self) -> Optional[Dict]:
        """获取天然气库存"""
        return self.get_series(self.SERIES_IDS["us_ng_inventory"])


class HybridCollector:
    """
    混合采集器
    - EIA API: 美国能源数据 (A级)
    - 网页采集: 国际LNG价格、国内数据 (B级)
    """
    
    def __init__(self):
        self.results: Dict[str, CollectionResult] = {}
        self.stats = {
            "eia_success": 0,
            "eia_failed": 0,
            "web_success": 0,
            "web_failed": 0,
            "start_time": None,
            "end_time": None
        }
        
        # 初始化EIA客户端
        try:
            self.eia_client = EIAAPIClient()
            print("✓ EIA API Client initialized")
        except Exception as e:
            print(f"✗ EIA API Client failed: {e}")
            self.eia_client = None
    
    async def collect_all(self, date: Optional[str] = None) -> Dict[str, CollectionResult]:
        """执行完整采集流程"""
        self.stats["start_time"] = datetime.now().isoformat()
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        
        print(f"🚀 LNG Market Analysis v6.1 - EIA+Web Hybrid Mode")
        print(f"📅 Target Date: {target_date}")
        print("=" * 60)
        
        # Phase 1: EIA API采集 (主会话直接调用，非子代理)
        print("\n📡 Phase 1: EIA API Collection (Direct)")
        print("-" * 60)
        await self._collect_eia_data()
        
        # Phase 2: 网页子代理采集 (国际LNG + 国内数据)
        print("\n🌐 Phase 2: Web SubAgent Collection")
        print("-" * 60)
        await self._collect_web_data()
        
        # Phase 3: 计算派生字段
        self._calculate_derived_fields()
        
        self.stats["end_time"] = datetime.now().isoformat()
        self._print_stats()
        
        return self.results
    
    async def _collect_eia_data(self):
        """使用EIA API采集数据 - 主会话直接调用"""
        if not self.eia_client:
            print("   EIA API not available, skipping")
            return
        
        eia_fields = [
            ("wti", "WTI原油", self.eia_client.get_wti_price, "美元/桶"),
            ("brent", "Brent原油", self.eia_client.get_brent_price, "美元/桶"),
            ("henry_hub", "Henry Hub", self.eia_client.get_henry_hub_price, "美元/MMBtu"),
            ("us_crude_inventory", "美国原油库存", self.eia_client.get_crude_inventory, "百万桶"),
            ("us_ng_inventory", "美国天然气库存", self.eia_client.get_ng_inventory, "十亿立方英尺"),
        ]
        
        for field, name, fetch_func, unit in eia_fields:
            print(f"   Fetching {name}...", end=" ")
            try:
                data = fetch_func()
                if data:
                    self.results[field] = CollectionResult(
                        field=field,
                        name=name,
                        value=data["value"],
                        unit=unit,
                        timestamp=data["period"],
                        source="EIA API",
                        confidence="A",
                        tier=0,
                        notes=f"Series: {data.get('series_id', '')}"
                    )
                    self.stats["eia_success"] += 1
                    print(f"✓ {data['value']}")
                else:
                    self.stats["eia_failed"] += 1
                    print("✗ Failed")
            except Exception as e:
                self.stats["eia_failed"] += 1
                print(f"✗ Error: {e}")
    
    async def _collect_web_data(self):
        """使用子代理采集网页数据"""
        # 这里将调用子代理采集网页数据
        # 为简化，先使用模拟数据演示架构
        
        print("   [Web SubAgent] International LNG prices")
        print("   - JKM: pending...")
        print("   - TTF: pending...")
        
        print("   [Web SubAgent] Domestic LNG prices")
        print("   - China factory: pending...")
        print("   - Zhejiang Ningbo: pending...")
        print("   - Zhejiang Zhoushan: pending...")
        
        # 模拟网页采集结果
        # 实际实现时，这里会调用 sessions_spawn 创建子代理
        self.stats["web_success"] = 0
        self.stats["web_failed"] = 0
    
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
                    confidence="A",
                    tier=0,
                    notes=f"Derived: Brent(${brent.value}) - WTI(${wti.value})"
                )
                print(f"\n📊 Calculated Brent-WTI spread: ${round(spread, 2)}")
    
    def _print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("📈 Collection Statistics")
        print("=" * 60)
        print(f"EIA API Success:  {self.stats['eia_success']}")
        print(f"EIA API Failed:   {self.stats['eia_failed']}")
        print(f"Web Success:      {self.stats['web_success']}")
        print(f"Web Failed:       {self.stats['web_failed']}")
        print(f"Total Fields:     {len(self.results)}")
        
        # 按置信度统计
        conf_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
        for result in self.results.values():
            if result.confidence in conf_counts:
                conf_counts[result.confidence] += 1
        
        print(f"\nConfidence Distribution:")
        for conf, count in conf_counts.items():
            print(f"  {conf}级: {count}")
        
        # 显示采集结果
        print(f"\n📊 Collected Data:")
        for field, result in self.results.items():
            if result.value:
                print(f"  {result.name}: {result.value} {result.unit} [{result.confidence}级]")
    
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
async def collect_lng_data(date: Optional[str] = None) -> Dict[str, CollectionResult]:
    """采集LNG数据的便捷函数"""
    collector = HybridCollector()
    return await collector.collect_all(date)


if __name__ == "__main__":
    # 测试采集
    results = asyncio.run(collect_lng_data())
    print(f"\n✅ Total: {len(results)} fields collected")
