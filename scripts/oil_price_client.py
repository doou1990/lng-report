"""
Oil Price API 数据采集模块
备用数据源 - 当需要实时Brent/WTI期货价格时使用

文档: https://docs.oilpriceapi.com/
"""

import requests
from typing import Optional, Dict
from datetime import datetime


class OilPriceAPIClient:
    """
    Oil Price API 客户端
    
    免费试用: 7天, 10,000请求
    付费方案: $15/月起, 10,000请求/月
    
    特点:
    - 5分钟更新频率
    - 50+商品品种
    - 支持WTI/Brent/天然气等
    """
    
    BASE_URL = "https://api.oilpriceapi.com/v1"
    
    # 主要商品代码
    COMMODITIES = {
        'WTI_SPOT': 'WTI_USD',           # WTI现货
        'BRENT_SPOT': 'BRENT_CRUDE_USD', # Brent现货
        'NATURAL_GAS': 'NATURAL_GAS_USD', # Henry Hub天然气
        'DIESEL': 'DIESEL_USD',          # 柴油
        'HEATING_OIL': 'HEATING_OIL_USD', # 取暖油
        'GASOLINE': 'GASOLINE_USD',      # 汽油
    }
    
    def __init__(self, api_key: str):
        """
        初始化客户端
        
        Args:
            api_key: Oil Price API密钥
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {api_key}',
            'Content-Type': 'application/json'
        })
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        发送API请求
        
        Args:
            endpoint: API端点
            params: 请求参数
            
        Returns:
            API响应数据
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Oil Price API请求失败: {e}")
            return None
        except Exception as e:
            print(f"请求异常: {e}")
            return None
    
    def get_latest_price(self, commodity_code: str) -> Optional[Dict]:
        """
        获取最新价格
        
        Args:
            commodity_code: 商品代码 (如 'WTI_USD', 'BRENT_CRUDE_USD')
            
        Returns:
            价格数据
            {
                'price': 74.52,
                'formatted': '$74.52',
                'currency': 'USD',
                'code': 'WTI_USD',
                'created_at': '2025-12-29T15:30:00.000Z',
                'type': 'spot_price',
                'source': 'oilprice.business_insider'
            }
        """
        params = {'by_code': commodity_code}
        data = self._make_request('prices/latest', params)
        
        if data and data.get('status') == 'success':
            return data.get('data')
        return None
    
    def get_wti_price(self) -> Optional[Dict]:
        """获取WTI最新价格"""
        return self.get_latest_price(self.COMMODITIES['WTI_SPOT'])
    
    def get_brent_price(self) -> Optional[Dict]:
        """获取Brent最新价格"""
        return self.get_latest_price(self.COMMODITIES['BRENT_SPOT'])
    
    def get_natural_gas_price(self) -> Optional[Dict]:
        """获取Henry Hub天然气价格"""
        return self.get_latest_price(self.COMMODITIES['NATURAL_GAS'])
    
    def get_past_day(self, commodity_code: str) -> Optional[Dict]:
        """
        获取过去24小时价格数据
        
        Args:
            commodity_code: 商品代码
            
        Returns:
            24小时价格数据
        """
        params = {'by_code': commodity_code}
        return self._make_request('prices/past_day', params)
    
    def get_past_week(self, commodity_code: str) -> Optional[Dict]:
        """
        获取过去7天价格数据
        
        Args:
            commodity_code: 商品代码
            
        Returns:
            7天价格数据
        """
        params = {'by_code': commodity_code}
        return self._make_request('prices/past_week', params)
    
    def get_past_month(self, commodity_code: str) -> Optional[Dict]:
        """
        获取过去30天价格数据
        
        Args:
            commodity_code: 商品代码
            
        Returns:
            30天价格数据
        """
        params = {'by_code': commodity_code}
        return self._make_request('prices/past_month', params)
    
    def get_all_commodities(self) -> Optional[Dict]:
        """
        获取所有可用商品列表
        
        Returns:
            商品列表
        """
        return self._make_request('commodities')
    
    def format_price_report(self, commodity_code: str) -> str:
        """
        格式化价格报告
        
        Args:
            commodity_code: 商品代码
            
        Returns:
            Markdown格式的价格报告
        """
        data = self.get_latest_price(commodity_code)
        
        if not data:
            return f"❌ 无法获取 {commodity_code} 价格数据"
        
        return f"""
**{data.get('code', commodity_code)} 价格**
- 当前价格: {data.get('formatted', 'N/A')}
- 更新时间: {data.get('created_at', 'N/A')}
- 数据来源: {data.get('source', 'N/A')}
- 数据类型: {data.get('type', 'N/A')}
"""


# 便捷函数
def get_oil_price_summary(api_key: str) -> str:
    """
    获取油价摘要（用于报告）
    
    Args:
        api_key: Oil Price API密钥
        
    Returns:
        Markdown格式的油价摘要
    """
    client = OilPriceAPIClient(api_key)
    
    wti = client.get_wti_price()
    brent = client.get_brent_price()
    
    report = "## 🛢️ 原油价格 (Oil Price API)\n\n"
    
    if wti:
        report += f"**WTI**: {wti.get('formatted', 'N/A')} (更新: {wti.get('created_at', 'N/A')[:10]})\n\n"
    else:
        report += "**WTI**: 数据获取失败\n\n"
    
    if brent:
        report += f"**Brent**: {brent.get('formatted', 'N/A')} (更新: {brent.get('created_at', 'N/A')[:10]})\n\n"
    else:
        report += "**Brent**: 数据获取失败\n\n"
    
    report += "*数据来源: Oil Price API (5分钟更新)*"
    
    return report


# 使用示例
if __name__ == "__main__":
    # 注意: 需要真实的API Key才能运行
    # 获取方式: https://oilpriceapi.com/signup
    
    print("=" * 50)
    print("Oil Price API 客户端")
    print("=" * 50)
    print("\n使用说明:")
    print("1. 访问 https://oilpriceapi.com/signup 注册账户")
    print("2. 获取API Key")
    print("3. 使用客户端获取实时价格")
    print("\n示例代码:")
    print("""
    from oil_price_client import OilPriceAPIClient
    
    client = OilPriceAPIClient('YOUR_API_KEY')
    
    # 获取WTI价格
    wti = client.get_wti_price()
    print(f\"WTI: {wti['formatted']}\")
    
    # 获取Brent价格
    brent = client.get_brent_price()
    print(f\"Brent: {brent['formatted']}\")
    """)
    print("\n" + "=" * 50)
