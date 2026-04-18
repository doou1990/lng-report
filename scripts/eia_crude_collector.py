#!/usr/bin/env python3
"""
EIA原油价格数据采集模块
从EIA API获取WTI和Brent原油现货价格
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional, List

# API配置
EIA_API_KEY = "WIDdF25nyCOTDChYMdxX5KGVlctdyPDWQPlkxSYn"
EIA_BASE_URL = "https://api.eia.gov/v2"

# 产品代码
PRODUCT_WTI = "EPCWTI"      # WTI原油
PRODUCT_BRENT = "EPCBRENT"  # Brent原油

class EIACrudeOilCollector:
    """EIA原油价格数据采集器"""
    
    def __init__(self, api_key: str = EIA_API_KEY):
        self.api_key = api_key
        self.base_url = EIA_BASE_URL
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        params['api_key'] = self.api_key
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API请求失败: {e}")
            return None
    
    def get_crude_price(self, product_code: str, frequency: str = "daily", 
                        limit: int = 1) -> Optional[List[Dict]]:
        """
        获取原油价格
        
        Args:
            product_code: EPCWTI (WTI) 或 EPCBRENT (Brent)
            frequency: daily/weekly/monthly
            limit: 返回数据条数
        
        Returns:
            价格数据列表
        """
        params = {
            'data[]': 'value',
            'facets[product][]': product_code,
            'frequency': frequency,
            'sort[0][column]': 'period',
            'sort[0][direction]': 'desc',
            'length': limit
        }
        
        data = self._make_request('/petroleum/pri/spt/data', params)
        if data and 'response' in data and 'data' in data['response']:
            return data['response']['data']
        return None
    
    def get_wti_price(self, frequency: str = "daily", limit: int = 1) -> Optional[Dict]:
        """获取WTI原油价格"""
        data = self.get_crude_price(PRODUCT_WTI, frequency, limit)
        if data and len(data) > 0:
            return {
                'date': data[0]['period'],
                'price': float(data[0]['value']) if data[0]['value'] else None,
                'product': 'WTI',
                'unit': 'Dollars per Barrel'
            }
        return None
    
    def get_brent_price(self, frequency: str = "daily", limit: int = 1) -> Optional[Dict]:
        """获取Brent原油价格"""
        data = self.get_crude_price(PRODUCT_BRENT, frequency, limit)
        if data and len(data) > 0:
            return {
                'date': data[0]['period'],
                'price': float(data[0]['value']) if data[0]['value'] else None,
                'product': 'Brent',
                'unit': 'Dollars per Barrel'
            }
        return None
    
    def get_both_prices(self) -> Dict:
        """获取WTI和Brent最新价格"""
        return {
            'wti': self.get_wti_price(),
            'brent': self.get_brent_price(),
            'timestamp': datetime.now().isoformat()
        }


# 使用示例
if __name__ == "__main__":
    collector = EIACrudeOilCollector()
    
    # 获取WTI价格
    wti = collector.get_wti_price()
    print(f"WTI: {wti}")
    
    # 获取Brent价格
    brent = collector.get_brent_price()
    print(f"Brent: {brent}")
    
    # 获取两者
    both = collector.get_both_prices()
    print(f"\n原油数据:\n{json.dumps(both, indent=2, ensure_ascii=False)}")
