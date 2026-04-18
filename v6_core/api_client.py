"""
OilPriceAPI.com 客户端
提供原油和LNG价格的API直连采集
"""
import requests
import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PriceData:
    """价格数据结构"""
    price: float
    currency: str
    unit: str
    timestamp: str
    source: str
    confidence: str
    code: str
    name: str


class OilPriceAPIClient:
    """
    OilPriceAPI.com 客户端
    
    支持的商品代码:
    - BRENT_USD: Brent原油 (美元/桶)
    - WTI_USD: WTI原油 (美元/桶)
    - JKM_LNG_USD: JKM LNG (美元/MMBtu)
    - TTF_GAS_USD: TTF天然气 (美元/MMBtu)
    - HH_GAS_USD: Henry Hub天然气 (美元/MMBtu)
    """
    
    BASE_URL = "https://api.oilpriceapi.com/v1"
    
    # 商品代码映射
    COMMODITY_CODES = {
        "brent": "BRENT_USD",
        "wti": "WTI_USD",
        "jkm": "JKM_LNG_USD",
        "ttf": "TTF_GAS_USD",
        "henry_hub": "HH_GAS_USD",
        "natural_gas": "NATURAL_GAS_USD"
    }
    
    # 中文名称映射
    COMMODITY_NAMES = {
        "BRENT_USD": "Brent原油",
        "WTI_USD": "WTI原油",
        "JKM_LNG_USD": "JKM LNG",
        "TTF_GAS_USD": "TTF天然气",
        "HH_GAS_USD": "Henry Hub",
        "NATURAL_GAS_USD": "天然气"
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_key: OilPriceAPI的API密钥。如果为None，将尝试从环境变量获取
        """
        self.api_key = api_key or self._get_api_key_from_env()
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _get_api_key_from_env(self) -> str:
        """从环境变量获取API密钥"""
        import os
        api_key = os.getenv("OILPRICE_API_KEY")
        if not api_key:
            raise ValueError(
                "OILPRICE_API_KEY not found. "
                "Please set it in environment variables or pass it to the constructor."
            )
        return api_key
    
    def get_price(self, code: str) -> Optional[PriceData]:
        """
        获取单个商品价格
        
        Args:
            code: 商品代码 (如 "BRENT_USD", "WTI_USD" 等)
            
        Returns:
            PriceData对象，如果失败则返回None
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/prices/latest",
                params={"by_code": code},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "success":
                return None
            
            price_info = data["data"]
            
            return PriceData(
                price=float(price_info["price"]),
                currency=price_info.get("currency", "USD"),
                unit=price_info.get("unit", "barrel"),
                timestamp=price_info.get("timestamp", datetime.now().isoformat()),
                source="OilPriceAPI",
                confidence="A",
                code=code,
                name=self.COMMODITY_NAMES.get(code, code)
            )
            
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.RequestException:
            return None
        except (KeyError, ValueError):
            return None
    
    def get_multiple(self, codes: List[str]) -> Dict[str, Optional[PriceData]]:
        """
        批量获取多个商品价格
        
        Args:
            codes: 商品代码列表
            
        Returns:
            字典，key为商品代码，value为PriceData或None
        """
        results = {}
        for code in codes:
            results[code] = self.get_price(code)
        return results
    
    def get_all_energy_prices(self) -> Dict[str, Optional[PriceData]]:
        """
        获取所有能源商品价格
        
        Returns:
            包含Brent、WTI、JKM、TTF、Henry Hub的字典
        """
        codes = [
            self.COMMODITY_CODES["brent"],
            self.COMMODITY_CODES["wti"],
            self.COMMODITY_CODES["jkm"],
            self.COMMODITY_CODES["ttf"],
            self.COMMODITY_CODES["henry_hub"]
        ]
        return self.get_multiple(codes)
    
    def get_historical(self, code: str, limit: int = 30) -> Optional[List[PriceData]]:
        """
        获取历史价格数据
        
        Args:
            code: 商品代码
            limit: 返回记录数，默认30条
            
        Returns:
            PriceData列表，如果失败则返回None
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/prices/historical",
                params={"by_code": code, "limit": limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "success":
                return None
            
            prices = []
            for item in data["data"]:
                prices.append(PriceData(
                    price=float(item["price"]),
                    currency=item.get("currency", "USD"),
                    unit=item.get("unit", "barrel"),
                    timestamp=item.get("timestamp", ""),
                    source="OilPriceAPI",
                    confidence="A",
                    code=code,
                    name=self.COMMODITY_NAMES.get(code, code)
                ))
            
            return prices
            
        except Exception:
            return None
    
    def check_health(self) -> bool:
        """
        检查API服务健康状态
        
        Returns:
            True如果服务正常，False否则
        """
        try:
            # 尝试获取Brent价格作为健康检查
            result = self.get_price("BRENT_USD")
            return result is not None
        except Exception:
            return False


class EIAAPIClient:
    """
    美国能源信息署(EIA) API客户端
    提供美国能源数据的官方API采集
    """
    
    BASE_URL = "https://api.eia.gov/v2"
    
    # 常用数据系列ID
    SERIES_IDS = {
        # 原油库存
        "crude_inventory": "PET.WCRSTUS1.W",  # 美国商业原油库存
        "crude_production": "PET.MCRFPUS1.M",  # 美国原油产量
        "crude_imports": "PET.WCRIMUS2.W",  # 美国原油进口
        
        # 天然气
        "ng_inventory": "NG.NW2_EPG0_SWO_R48_BCF.W",  # 天然气库存
        "ng_production": "NG.N9050US2.M",  # 天然气产量
        "lng_exports": "NG.NW2_EPG0_EEX_NUS-NUI_BCF.M",  # LNG出口
        
        # 价格
        "wti_price": "PET.RWTC.D",  # WTI现货价格
        "brent_price": "PET.RBRTE.D",  # Brent现货价格
        "henry_hub_price": "NG.RNGWHHD.D",  # Henry Hub价格
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化EIA API客户端
        
        Args:
            api_key: EIA API密钥。如果为None，将尝试从环境变量获取
        """
        self.api_key = api_key or self._get_api_key_from_env()
        self.session = requests.Session()
    
    def _get_api_key_from_env(self) -> str:
        """从环境变量获取API密钥"""
        import os
        api_key = os.getenv("EIA_API_KEY")
        if not api_key:
            raise ValueError(
                "EIA_API_KEY not found. "
                "Please set it in environment variables or pass it to the constructor."
            )
        return api_key
    
    def get_series(self, series_id: str, limit: int = 1) -> Optional[Dict]:
        """
        获取数据系列
        
        Args:
            series_id: EIA数据系列ID
            limit: 返回记录数
            
        Returns:
            包含数据的字典，如果失败则返回None
        """
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
                "source": "EIA",
                "confidence": "A"
            }
            
        except Exception:
            return None
    
    def get_crude_inventory(self) -> Optional[Dict]:
        """获取美国原油库存"""
        return self.get_series(self.SERIES_IDS["crude_inventory"])
    
    def get_ng_inventory(self) -> Optional[Dict]:
        """获取美国天然气库存"""
        return self.get_series(self.SERIES_IDS["ng_inventory"])
    
    def get_lng_exports(self) -> Optional[Dict]:
        """获取美国LNG出口"""
        return self.get_series(self.SERIES_IDS["lng_exports"])


# 便捷函数
def create_oilprice_client(api_key: Optional[str] = None) -> OilPriceAPIClient:
    """创建OilPriceAPI客户端的便捷函数"""
    return OilPriceAPIClient(api_key)


def create_eia_client(api_key: Optional[str] = None) -> EIAAPIClient:
    """创建EIA API客户端的便捷函数"""
    return EIAAPIClient(api_key)


# 测试代码
if __name__ == "__main__":
    # 测试OilPriceAPI
    print("Testing OilPriceAPI Client...")
    try:
        client = OilPriceAPIClient()
        
        # 测试单个价格获取
        brent = client.get_price("BRENT_USD")
        if brent:
            print(f"✓ Brent: ${brent.price} ({brent.timestamp})")
        else:
            print("✗ Failed to get Brent price")
        
        # 测试批量获取
        all_prices = client.get_all_energy_prices()
        print("\nAll Energy Prices:")
        for code, data in all_prices.items():
            if data:
                print(f"  ✓ {data.name}: ${data.price}")
            else:
                print(f"  ✗ {code}: Failed")
        
        # 健康检查
        healthy = client.check_health()
        print(f"\nAPI Health: {'✓ Healthy' if healthy else '✗ Unhealthy'}")
        
    except Exception as e:
        print(f"Error: {e}")
