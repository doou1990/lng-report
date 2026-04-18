#!/usr/bin/env python3
"""
OilPriceAPI 客户端 - 基于开源仓库 https://github.com/oilshit/oilprice-api

API端点: https://oilprice-api.com/api/v1
开源实现参考: oilprice-api 仓库
"""
import requests
import json
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OilPriceData:
    """油价数据结构"""
    symbol: str
    price: float
    currency: str
    unit: str
    timestamp: str
    change_24h: Optional[float] = None
    change_percent_24h: Optional[float] = None


class OilPriceAPIClient:
    """
    OilPriceAPI 客户端
    
    基于开源仓库 oilshit/oilprice-api 的API结构
    支持免费获取原油和天然气价格数据
    """
    
    # API基础URL (基于开源仓库文档)
    BASE_URL = "https://oilprice-api.herokuapp.com"
    
    # 支持的商品代码
    SYMBOLS = {
        "brent": "BRENT",
        "wti": "WTI",
        "jkm": "JKM",
        "ttf": "TTF",
        "henry_hub": "HH",
        "natural_gas": "NG"
    }
    
    def __init__(self):
        """初始化客户端 - 无需API密钥"""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        })
    
    def get_price(self, symbol: str) -> Optional[OilPriceData]:
        """
        获取单个商品价格
        
        Args:
            symbol: 商品代码 (brent, wti, jkm, ttf, henry_hub, natural_gas)
            
        Returns:
            OilPriceData对象，失败返回None
        """
        try:
            # 标准化symbol
            symbol_key = symbol.lower()
            if symbol_key not in self.SYMBOLS:
                print(f"   Unknown symbol: {symbol}")
                return None
            
            api_symbol = self.SYMBOLS[symbol_key]
            
            # 构建API URL
            url = f"{self.BASE_URL}/prices/{api_symbol}"
            
            print(f"   Fetching {symbol} from {url}...", end=" ")
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"✗ HTTP {response.status_code}")
                return None
            
            data = response.json()
            
            if not data or "price" not in data:
                print("✗ No price data")
                return None
            
            # 解析响应
            price_data = OilPriceData(
                symbol=symbol,
                price=float(data["price"]),
                currency=data.get("currency", "USD"),
                unit=data.get("unit", "barrel"),
                timestamp=data.get("timestamp", datetime.now().isoformat()),
                change_24h=data.get("change_24h"),
                change_percent_24h=data.get("change_percent_24h")
            )
            
            print(f"✓ ${price_data.price}")
            return price_data
            
        except requests.exceptions.Timeout:
            print("✗ Timeout")
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Request error: {e}")
            return None
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            print(f"✗ Parse error: {e}")
            return None
    
    def get_all_prices(self) -> Dict[str, Optional[OilPriceData]]:
        """
        获取所有能源商品价格
        
        Returns:
            包含所有商品价格的字典
        """
        results = {}
        
        print("\n📡 Fetching all energy prices from OilPriceAPI...")
        print("-" * 50)
        
        for symbol in self.SYMBOLS.keys():
            results[symbol] = self.get_price(symbol)
        
        return results
    
    def get_crude_prices(self) -> Dict[str, Optional[OilPriceData]]:
        """获取原油价格 (Brent + WTI)"""
        return {
            "brent": self.get_price("brent"),
            "wti": self.get_price("wti")
        }
    
    def get_gas_prices(self) -> Dict[str, Optional[OilPriceData]]:
        """获取天然气价格 (JKM + TTF + Henry Hub)"""
        return {
            "jkm": self.get_price("jkm"),
            "ttf": self.get_price("ttf"),
            "henry_hub": self.get_price("henry_hub")
        }


# 便捷函数
def get_oil_price(symbol: str) -> Optional[OilPriceData]:
    """获取单个油价的便捷函数"""
    client = OilPriceAPIClient()
    return client.get_price(symbol)


def get_all_energy_prices() -> Dict[str, Optional[OilPriceData]]:
    """获取所有能源价格的便捷函数"""
    client = OilPriceAPIClient()
    return client.get_all_prices()


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("OilPriceAPI Client Test")
    print("=" * 60)
    
    client = OilPriceAPIClient()
    
    # 测试单个价格获取
    print("\n1. Testing single price fetch:")
    brent = client.get_price("brent")
    if brent:
        print(f"   Brent: ${brent.price} {brent.currency}/{brent.unit}")
    
    # 测试批量获取
    print("\n2. Testing batch fetch:")
    all_prices = client.get_all_prices()
    
    success_count = sum(1 for p in all_prices.values() if p is not None)
    print(f"\n   Success: {success_count}/{len(all_prices)}")
    
    for symbol, data in all_prices.items():
        if data:
            print(f"   {symbol.upper()}: ${data.price}")
        else:
            print(f"   {symbol.upper()}: Failed")
    
    print("\n" + "=" * 60)
    print("Test completed")
