# EIA API 对接模块
# 美国能源信息署数据获取
# API文档: https://www.eia.gov/opendata/

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class EIADataClient:
    """
    EIA (Energy Information Administration) API 客户端
    用于获取美国能源数据，包括原油、天然气、库存等
    """
    
    BASE_URL = "https://api.eia.gov/v2"
    API_KEY = "WIDdF25nyCOTDChYMdxX5KGVlctdyPDWQPlkxSYn"
    
    # 主要数据系列ID
    SERIES = {
        # 原油价格
        'brent_spot': 'PET.RBRTE.D',  # Brent原油现货价格
        'wti_spot': 'PET.RWTC.D',     # WTI原油现货价格
        
        # 天然气价格
        'henry_hub': 'NG.RNGWHHD.D',  # Henry Hub天然气价格
        
        # 库存数据
        'crude_stocks': 'PET.WCRSTUS1.W',  # 美国原油库存
        'gasoline_stocks': 'PET.WGASTUS1.W', # 美国汽油库存
        'ng_stocks': 'NG.NW2_EPG0_SWO_R48_BCF.W', # 天然气库存
        
        # 产量数据
        'crude_production': 'PET.MCRFPUS1.M', # 美国原油产量
        'ng_production': 'NG.N9070US2.M',     # 天然气产量
        
        # LNG出口
        'lng_exports': 'NG.NLNGEXUS.M',  # LNG出口量
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 EIA 客户端
        
        Args:
            api_key: EIA API密钥
        """
        self.api_key = api_key or self.API_KEY
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "LNG-Market-Analysis/4.4"
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        发送 API 请求
        
        Args:
            endpoint: API 端点
            params: 查询参数
            
        Returns:
            API 响应数据
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }
    
    def get_series_data(self, series_id: str, start_date: Optional[str] = None, 
                       end_date: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        获取特定数据系列
        
        Args:
            series_id: EIA数据系列ID
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            limit: 返回记录数
            
        Returns:
            数据系列
        """
        endpoint = f"seriesid/{series_id}"
        params = {
            'frequency': 'daily',
            'data[0]': 'value',
            'sort[0][column]': 'period',
            'sort[0][direction]': 'desc',
            'offset': 0,
            'length': limit
        }
        
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date
        
        return self._make_request(endpoint, params)
    
    def get_brent_price(self) -> Dict[str, Any]:
        """获取Brent原油现货价格"""
        return self.get_series_data(self.SERIES['brent_spot'], limit=5)
    
    def get_wti_price(self) -> Dict[str, Any]:
        """获取WTI原油现货价格"""
        return self.get_series_data(self.SERIES['wti_spot'], limit=5)
    
    def get_henry_hub_price(self) -> Dict[str, Any]:
        """获取Henry Hub天然气价格"""
        return self.get_series_data(self.SERIES['henry_hub'], limit=5)
    
    def get_crude_stocks(self) -> Dict[str, Any]:
        """获取美国原油库存"""
        return self.get_series_data(self.SERIES['crude_stocks'], limit=5)
    
    def get_ng_stocks(self) -> Dict[str, Any]:
        """获取美国天然气库存"""
        return self.get_series_data(self.SERIES['ng_stocks'], limit=5)
    
    def get_daily_summary(self) -> Dict[str, Any]:
        """
        获取每日数据摘要
        
        Returns:
            包含主要能源价格的摘要
        """
        summary = {
            'timestamp': datetime.now().isoformat(),
            'source': 'EIA API',
            'data': {}
        }
        
        # 获取Brent价格
        brent = self.get_brent_price()
        if 'response' in brent and 'data' in brent['response']:
            brent_data = brent['response']['data']
            if brent_data:
                summary['data']['brent'] = {
                    'price': brent_data[0].get('value'),
                    'date': brent_data[0].get('period'),
                    'unit': 'USD/barrel'
                }
        
        # 获取WTI价格
        wti = self.get_wti_price()
        if 'response' in wti and 'data' in wti['response']:
            wti_data = wti['response']['data']
            if wti_data:
                summary['data']['wti'] = {
                    'price': wti_data[0].get('value'),
                    'date': wti_data[0].get('period'),
                    'unit': 'USD/barrel'
                }
        
        # 获取Henry Hub价格
        hh = self.get_henry_hub_price()
        if 'response' in hh and 'data' in hh['response']:
            hh_data = hh['response']['data']
            if hh_data:
                summary['data']['henry_hub'] = {
                    'price': hh_data[0].get('value'),
                    'date': hh_data[0].get('period'),
                    'unit': 'USD/MMBtu'
                }
        
        # 获取原油库存
        crude = self.get_crude_stocks()
        if 'response' in crude and 'data' in crude['response']:
            crude_data = crude['response']['data']
            if crude_data:
                summary['data']['crude_stocks'] = {
                    'value': crude_data[0].get('value'),
                    'date': crude_data[0].get('period'),
                    'unit': 'thousand barrels'
                }
        
        # 获取天然气库存
        ng = self.get_ng_stocks()
        if 'response' in ng and 'data' in ng['response']:
            ng_data = ng['response']['data']
            if ng_data:
                summary['data']['ng_stocks'] = {
                    'value': ng_data[0].get('value'),
                    'date': ng_data[0].get('period'),
                    'unit': 'Bcf'
                }
        
        return summary


# 便捷函数
def get_eia_client(api_key: Optional[str] = None) -> EIADataClient:
    """获取 EIA 客户端实例"""
    return EIADataClient(api_key)


def fetch_eia_daily_summary() -> Dict[str, Any]:
    """
    获取EIA每日数据摘要（用于LNG报告）
    
    Returns:
        包含原油、天然气价格和库存的摘要
    """
    client = EIADataClient()
    return client.get_daily_summary()


if __name__ == "__main__":
    # 测试代码
    client = EIADataClient()
    
    print("=== EIA API 测试 ===")
    
    # 获取每日摘要
    summary = client.get_daily_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
