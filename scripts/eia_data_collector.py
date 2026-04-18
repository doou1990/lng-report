"""
EIA API Data Collector for LNG Market Analysis
采集美国天然气库存和价格数据
"""

import requests
import json
from typing import Dict, Optional, List
from datetime import datetime, timedelta

# API Configuration
EIA_API_KEY = "WIDdF25nyCOTDChYMdxX5KGVlctdyPDWQPlkxSYn"
EIA_BASE_URL = "https://api.eia.gov/v2"


class EIADataCollector:
    """EIA数据采集器"""
    
    def __init__(self, api_key: str = EIA_API_KEY):
        self.api_key = api_key
        self.base_url = EIA_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """发送API请求"""
        url = f"{self.base_url}/{endpoint}"
        default_params = {"api_key": self.api_key}
        if params:
            default_params.update(params)
        
        try:
            response = self.session.get(url, params=default_params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"EIA API请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return None
    
    def get_natural_gas_storage(self, length: int = 1) -> Optional[Dict]:
        """
        获取美国天然气库存数据
        
        Args:
            length: 返回记录数 (1-5000)
        
        Returns:
            库存数据字典
        """
        endpoint = "natural-gas/stor/wkly/data"
        params = {"length": length}
        
        data = self._make_request(endpoint, params)
        if data and "response" in data:
            return {
                "total_records": data["response"].get("total"),
                "date_format": data["response"].get("dateFormat"),
                "frequency": data["response"].get("frequency"),
                "data": data["response"].get("data", [])
            }
        return None
    
    def get_henry_hub_price(self, length: int = 1) -> Optional[Dict]:
        """
        获取Henry Hub天然气期货价格
        
        Args:
            length: 返回记录数 (1-5000)
        
        Returns:
            价格数据字典
        """
        endpoint = "natural-gas/pri/fut/data"
        params = {"length": length}
        
        data = self._make_request(endpoint, params)
        if data and "response" in data:
            return {
                "total_records": data["response"].get("total"),
                "date_format": data["response"].get("dateFormat"),
                "frequency": data["response"].get("frequency"),
                "data": data["response"].get("data", [])
            }
        return None
    
    def get_latest_storage_summary(self) -> Optional[Dict]:
        """
        获取最新库存数据摘要
        
        Returns:
            格式化的库存数据
        """
        data = self.get_natural_gas_storage(length=1)
        if not data or not data.get("data"):
            return None
        
        latest = data["data"][0]
        return {
            "date": latest.get("period"),
            "area": latest.get("area-name"),
            "storage_type": latest.get("process-name"),
            "volume_bcf": latest.get("value"),
            "series": latest.get("series-description")
        }
    
    def get_latest_henry_hub_price(self) -> Optional[Dict]:
        """
        获取最新Henry Hub价格
        
        Returns:
            格式化的价格数据
        """
        data = self.get_henry_hub_price(length=1)
        if not data or not data.get("data"):
            return None
        
        latest = data["data"][0]
        return {
            "date": latest.get("period"),
            "area": latest.get("area-name"),
            "contract": latest.get("process-name"),
            "price": latest.get("value"),
            "unit": "Dollars per Million Btu",
            "series": latest.get("series-description")
        }
    
    def get_storage_by_region(self, region: str = "R33", length: int = 4) -> Optional[List[Dict]]:
        """
        按地区获取库存数据
        
        Args:
            region: 地区代码 (R33=全美, R1=东北, R2=中西部, R3=南部, R4=西部)
            length: 返回记录数
        
        Returns:
            库存数据列表
        """
        endpoint = "natural-gas/stor/wkly/data"
        params = {
            "length": length,
            "facets[duoarea][]": region
        }
        
        data = self._make_request(endpoint, params)
        if data and "response" in data:
            return data["response"].get("data", [])
        return None


# 便捷函数
def get_eia_storage_summary() -> str:
    """获取EIA库存摘要（用于报告）"""
    collector = EIADataCollector()
    storage = collector.get_latest_storage_summary()
    
    if not storage:
        return "EIA库存数据暂不可用"
    
    return f"""
🇺🇸 **美国天然气库存 (EIA)**
- 数据日期: {storage.get('date', 'N/A')}
- 库存类型: {storage.get('storage_type', 'N/A')}
- 库存量: {storage.get('volume_bcf', 'N/A')} Bcf
- 数据来源: EIA Weekly Natural Gas Storage Report
"""


def get_eia_price_summary() -> str:
    """获取EIA价格摘要（用于报告）"""
    collector = EIADataCollector()
    price = collector.get_latest_henry_hub_price()
    
    if not price:
        return "Henry Hub价格数据暂不可用"
    
    return f"""
🇺🇸 **Henry Hub天然气价格 (EIA)**
- 数据日期: {price.get('date', 'N/A')}
- 期货合约: {price.get('contract', 'N/A')}
- 价格: ${price.get('price', 'N/A')}/MMBtu
- 数据来源: EIA Natural Gas Futures Prices
"""


if __name__ == "__main__":
    # 测试代码
    print("=" * 50)
    print("EIA API数据采集测试")
    print("=" * 50)
    
    collector = EIADataCollector()
    
    # 测试库存数据
    print("\n1. 美国天然气库存数据:")
    storage = collector.get_natural_gas_storage(length=1)
    if storage:
        print(f"   总记录数: {storage['total_records']}")
        print(f"   数据频率: {storage['frequency']}")
        if storage['data']:
            latest = storage['data'][0]
            print(f"   最新数据: {latest}")
    else:
        print("   获取失败")
    
    # 测试价格数据
    print("\n2. Henry Hub价格数据:")
    price = collector.get_henry_hub_price(length=1)
    if price:
        print(f"   总记录数: {price['total_records']}")
        print(f"   数据频率: {price['frequency']}")
        if price['data']:
            latest = price['data'][0]
            print(f"   最新数据: {latest}")
    else:
        print("   获取失败")
    
    # 测试格式化输出
    print("\n3. 格式化输出:")
    print(get_eia_storage_summary())
    print(get_eia_price_summary())
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)
