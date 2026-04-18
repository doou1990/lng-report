#!/usr/bin/env python3
"""
欧洲天然气库存数据 - 备用采集方案
当 GIE API 不可用时使用
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class FallbackInventoryData:
    """
    备用库存数据源
    当 GIE API 不可用时提供估算数据或缓存数据
    """
    
    # 基于历史数据的估算模板
    EU_INVENTORY_TEMPLATE = {
        "country": "EU",
        "country_code": "EU",
        "gas_day": None,
        "updated_at": None,
        "inventory": {
            "gas_in_storage_twh": None,
            "working_gas_volume_twh": 1131.18,
            "fill_percentage": None,
            "injection_gwh_d": None,
            "withdrawal_gwh_d": None,
            "net_withdrawal_gwh_d": None,
            "trend_percentage": None,
            "consumption_full_days": None,
            "status": "E"
        },
        "fallback": True,
        "note": "GIE API 暂时不可用，使用估算数据"
    }
    
    # 主要国家基准数据 (TWh)
    COUNTRY_BASELINE = {
        "DE": {"name": "Germany", "working_volume": 247.10, "typical_fill": 25},
        "FR": {"name": "France", "working_volume": 123.88, "typical_fill": 23},
        "IT": {"name": "Italy", "working_volume": 180.0, "typical_fill": 35},
        "NL": {"name": "Netherlands", "working_volume": 120.0, "typical_fill": 28},
        "AT": {"name": "Austria", "working_volume": 100.28, "typical_fill": 35},
        "ES": {"name": "Spain", "working_volume": 35.0, "typical_fill": 65},
        "UK": {"name": "United Kingdom", "working_volume": 45.0, "typical_fill": 40}
    }
    
    @classmethod
    def get_estimate(cls, country_code: str = "eu") -> Dict[str, Any]:
        """
        获取估算库存数据
        
        Args:
            country_code: 国家代码
            
        Returns:
            估算的库存数据
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        if country_code.lower() == "eu":
            return cls._get_eu_estimate(today)
        else:
            return cls._get_country_estimate(country_code.upper(), today)
    
    @classmethod
    def _get_eu_estimate(cls, today: str) -> Dict[str, Any]:
        """获取欧盟整体估算数据"""
        data = cls.EU_INVENTORY_TEMPLATE.copy()
        data["gas_day"] = today
        data["updated_at"] = datetime.now().isoformat()
        
        # 基于季节的简单估算 (4月初)
        # 欧洲冬季结束，库存处于较低水平，开始注入
        month = datetime.now().month
        
        if month in [4, 5]:  # 春季
            estimated_fill = 28.0
            trend = 0.3
        elif month in [6, 7, 8]:  # 夏季
            estimated_fill = 55.0
            trend = 0.4
        elif month in [9, 10]:  # 秋季
            estimated_fill = 85.0
            trend = 0.2
        else:  # 冬季
            estimated_fill = 60.0
            trend = -0.5
        
        data["inventory"]["fill_percentage"] = estimated_fill
        data["inventory"]["gas_in_storage_twh"] = round(
            data["inventory"]["working_gas_volume_twh"] * estimated_fill / 100, 2
        )
        data["inventory"]["trend_percentage"] = trend
        data["inventory"]["consumption_full_days"] = round(estimated_fill / 3, 1)
        
        return data
    
    @classmethod
    def _get_country_estimate(cls, country_code: str, today: str) -> Dict[str, Any]:
        """获取特定国家估算数据"""
        baseline = cls.COUNTRY_BASELINE.get(country_code)
        
        if not baseline:
            return {
                "error": True,
                "message": f"No baseline data for {country_code}"
            }
        
        month = datetime.now().month
        
        # 根据季节调整填充率
        if month in [4, 5]:
            fill_factor = 0.9  # 春季较低
        elif month in [6, 7, 8]:
            fill_factor = 1.1  # 夏季填充
        elif month in [9, 10]:
            fill_factor = 1.2  # 秋季高填充
        else:
            fill_factor = 0.8  # 冬季消耗
        
        estimated_fill = round(baseline["typical_fill"] * fill_factor, 2)
        
        return {
            "country": baseline["name"],
            "country_code": country_code,
            "gas_day": today,
            "inventory": {
                "gas_in_storage_twh": round(
                    baseline["working_volume"] * estimated_fill / 100, 2
                ),
                "working_gas_volume_twh": baseline["working_volume"],
                "fill_percentage": estimated_fill,
                "status": "E"
            },
            "fallback": True,
            "note": "基于历史数据的估算值"
        }
    
    @classmethod
    def get_all_countries_estimate(cls) -> List[Dict[str, Any]]:
        """获取所有主要国家估算数据"""
        today = datetime.now().strftime("%Y-%m-%d")
        results = []
        
        for code in cls.COUNTRY_BASELINE.keys():
            data = cls._get_country_estimate(code, today)
            if "error" not in data:
                results.append(data)
        
        return results
    
    @classmethod
    def get_summary(cls) -> Dict[str, Any]:
        """获取库存摘要"""
        eu_data = cls.get_estimate("eu")
        countries = cls.get_all_countries_estimate()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "source": "FALLBACK_ESTIMATE",
            "note": "GIE API 不可用，使用基于历史数据的估算值",
            "eu": eu_data.get("inventory", {}),
            "major_countries": countries,
            "analysis": {
                "eu_fill_level": eu_data.get("inventory", {}).get("fill_percentage"),
                "eu_status": cls._get_status(
                    eu_data.get("inventory", {}).get("fill_percentage", 0)
                ),
                "trend": eu_data.get("inventory", {}).get("trend_percentage"),
                "days_of_consumption": eu_data.get("inventory", {}).get("consumption_full_days"),
                "confidence": "D",
                "data_quality": "估算值，仅供参考"
            }
        }
    
    @staticmethod
    def _get_status(fill_percentage: float) -> str:
        """根据填充率判断状态"""
        if fill_percentage >= 80:
            return "充足"
        elif fill_percentage >= 50:
            return "正常"
        elif fill_percentage >= 30:
            return "偏低"
        else:
            return "紧张"


if __name__ == "__main__":
    # 测试
    print("=== EU Estimate ===")
    eu = FallbackInventoryData.get_estimate("eu")
    print(json.dumps(eu, indent=2, ensure_ascii=False))
    
    print("\n=== Summary ===")
    summary = FallbackInventoryData.get_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
