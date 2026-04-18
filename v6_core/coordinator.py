"""
统一采集协调器
实现分层采集策略: API > 网页 > 搜索
"""
import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import yaml

from .price_apis import OilPriceAPIClient, EIAAPIClient


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


@dataclass
class CollectionTask:
    """采集任务"""
    field: str
    name: str
    tiers: List[str]
    unit: str
    category: str


class TieredDataCollector:
    """
    分层数据采集器
    
    采集优先级:
    1. Tier 0: API直连 (OilPriceAPI, EIA API)
    2. Tier 1: 官方网页 (CME, ICE, Mysteel)
    3. Tier 2: 搜索验证 (Exa, Tavily)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化采集器
        
        Args:
            config_path: 配置文件路径，默认使用内置配置
        """
        self.config = self._load_config(config_path)
        self.results: Dict[str, CollectionResult] = {}
        
        # 初始化API客户端
        self.oilprice_client = None
        self.eia_client = None
        
        # 统计信息
        self.stats = {
            "api_success": 0,
            "api_failed": 0,
            "web_success": 0,
            "web_failed": 0,
            "search_success": 0,
            "search_failed": 0,
            "start_time": None,
            "end_time": None
        }
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        # 使用默认配置
        default_config_path = Path(__file__).parent.parent / "config" / "data_sources.yml"
        if default_config_path.exists():
            with open(default_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        return {}
    
    def _init_api_clients(self):
        """初始化API客户端"""
        try:
            self.oilprice_client = OilPriceAPIClient()
        except Exception as e:
            print(f"Warning: Failed to initialize OilPriceAPI client: {e}")
        
        try:
            self.eia_client = EIAAPIClient()
        except Exception as e:
            print(f"Warning: Failed to initialize EIA API client: {e}")
    
    def collect_all(self, date: Optional[str] = None) -> Dict[str, CollectionResult]:
        """
        执行完整采集流程
        
        Args:
            date: 采集日期，默认今天
            
        Returns:
            采集结果字典
        """
        self.stats["start_time"] = datetime.now().isoformat()
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        
        print(f"🚀 Starting LNG data collection for {target_date}")
        print("=" * 60)
        
        # 初始化API客户端
        self._init_api_clients()
        
        # 获取必采数据清单
        required_data = self.config.get("required_data", [])
        
        # Step 1: Tier 0 - API采集 (最高优先级)
        print("\n📡 Step 1: Tier 0 - API Collection")
        print("-" * 40)
        self._collect_tier_0(required_data)
        
        # Step 2: Tier 1 - 网页采集
        print("\n🌐 Step 2: Tier 1 - Web Collection")
        print("-" * 40)
        self._collect_tier_1(required_data)
        
        # Step 3: Tier 2 - 搜索验证
        print("\n🔍 Step 3: Tier 2 - Search Validation")
        print("-" * 40)
        self._collect_tier_2(required_data)
        
        # 计算派生字段
        self._calculate_derived_fields()
        
        self.stats["end_time"] = datetime.now().isoformat()
        
        # 打印统计
        self._print_stats()
        
        return self.results
    
    def _collect_tier_0(self, required_data: List[Dict]):
        """Tier 0: API采集"""
        api_config = self.config.get("data_sources", {}).get("tier_0_api", {})
        
        if not api_config.get("enabled", True):
            print("Tier 0 API collection disabled")
            return
        
        # OilPriceAPI采集
        if self.oilprice_client:
            oilprice_config = api_config.get("oilprice_api", {})
            endpoints = oilprice_config.get("endpoints", {})
            
            for key, endpoint in endpoints.items():
                field_name = endpoint.get("name", key)
                code = endpoint.get("code")
                
                print(f"  Fetching {field_name}...", end=" ")
                
                result = self.oilprice_client.get_price(code)
                if result:
                    self.results[key] = CollectionResult(
                        field=key,
                        name=field_name,
                        value=result.price,
                        unit=endpoint.get("unit", ""),
                        timestamp=result.timestamp,
                        source="OilPriceAPI",
                        confidence="A",
                        tier=0,
                        notes=f"Code: {code}"
                    )
                    self.stats["api_success"] += 1
                    print(f"✓ ${result.price}")
                else:
                    self.stats["api_failed"] += 1
                    print("✗ Failed")
        
        # EIA API采集
        if self.eia_client:
            eia_config = api_config.get("eia_api", {})
            endpoints = eia_config.get("endpoints", {})
            
            for key, endpoint in endpoints.items():
                field_name = endpoint.get("name", key)
                
                print(f"  Fetching {field_name}...", end=" ")
                
                result = self.eia_client.get_series(endpoint.get("series_id"))
                if result:
                    self.results[key] = CollectionResult(
                        field=key,
                        name=field_name,
                        value=result["value"],
                        unit=endpoint.get("unit", ""),
                        timestamp=result["period"],
                        source="EIA",
                        confidence="A",
                        tier=0,
                        notes=f"Series: {endpoint.get('series_id')}"
                    )
                    self.stats["api_success"] += 1
                    print(f"✓ {result['value']}")
                else:
                    self.stats["api_failed"] += 1
                    print("✗ Failed")
    
    def _collect_tier_1(self, required_data: List[Dict]):
        """Tier 1: 网页采集 - 使用子代理"""
        web_config = self.config.get("data_sources", {}).get("tier_1_web", {})
        
        if not web_config.get("enabled", True):
            print("Tier 1 web collection disabled")
            return
        
        # 找出Tier 0未采集到的字段
        missing_fields = []
        for item in required_data:
            field = item.get("field")
            if field not in self.results:
                missing_fields.append(item)
        
        if not missing_fields:
            print("  All fields collected from Tier 0, skipping Tier 1")
            return
        
        print(f"  {len(missing_fields)} fields need Tier 1 collection")
        
        # 这里将通过子代理执行网页采集
        # 实际实现将在subagent_collector.py中
        for item in missing_fields:
            field = item.get("field")
            print(f"  [SubAgent] Will collect {item.get('name')} via web scraping")
            # 标记为待子代理采集
            self.results[field] = CollectionResult(
                field=field,
                name=item.get("name", field),
                value=None,
                unit=item.get("unit", ""),
                timestamp=datetime.now().isoformat(),
                source="Pending-Web",
                confidence="B",
                tier=1,
                notes="To be collected by subagent"
            )
    
    def _collect_tier_2(self, required_data: List[Dict]):
        """Tier 2: 搜索验证"""
        search_config = self.config.get("data_sources", {}).get("tier_2_search", {})
        
        if not search_config.get("enabled", True):
            print("Tier 2 search collection disabled")
            return
        
        # 找出仍需验证的字段
        pending_fields = []
        for item in required_data:
            field = item.get("field")
            if field in self.results:
                result = self.results[field]
                # 如果已经是A级数据，不需要搜索验证
                if result.confidence != "A":
                    pending_fields.append(item)
        
        if not pending_fields:
            print("  No fields need Tier 2 validation")
            return
        
        print(f"  {len(pending_fields)} fields need Tier 2 validation")
        
        # 这里将通过子代理执行搜索验证
        for item in pending_fields:
            field = item.get("field")
            print(f"  [SubAgent] Will validate {item.get('name')} via search")
    
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
        print(f"API Success:    {self.stats['api_success']}")
        print(f"API Failed:     {self.stats['api_failed']}")
        print(f"Web Success:    {self.stats['web_success']}")
        print(f"Web Failed:     {self.stats['web_failed']}")
        print(f"Search Success: {self.stats['search_success']}")
        print(f"Search Failed:  {self.stats['search_failed']}")
        print(f"Total Collected: {len(self.results)}")
        
        # 按置信度统计
        confidence_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
        for result in self.results.values():
            if result.confidence in confidence_counts:
                confidence_counts[result.confidence] += 1
        
        print(f"\nConfidence Distribution:")
        for conf, count in confidence_counts.items():
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


class SubAgentCollector:
    """
    子代理采集器
    用于执行Tier 1和Tier 2的采集任务
    """
    
    def __init__(self, timeout: int = 300):
        """
        初始化子代理采集器
        
        Args:
            timeout: 子代理超时时间（秒），默认5分钟
        """
        self.timeout = timeout
    
    async def collect_via_subagent(self, task: CollectionTask) -> Optional[CollectionResult]:
        """
        通过子代理执行采集任务
        
        Args:
            task: 采集任务
            
        Returns:
            采集结果，如果失败则返回None
        """
        # 这里将实现子代理调用逻辑
        # 使用sessions_spawn创建子代理会话
        pass
    
    async def collect_batch(self, tasks: List[CollectionTask]) -> Dict[str, CollectionResult]:
        """
        批量执行采集任务
        
        Args:
            tasks: 采集任务列表
            
        Returns:
            采集结果字典
        """
        # 并行执行多个子代理任务
        pass


# 便捷函数
def collect_lng_data(date: Optional[str] = None, config_path: Optional[str] = None) -> Dict:
    """
    采集LNG数据的便捷函数
    
    Args:
        date: 采集日期
        config_path: 配置文件路径
        
    Returns:
        采集结果字典
    """
    collector = TieredDataCollector(config_path)
    return collector.collect_all(date)


if __name__ == "__main__":
    # 测试采集器
    results = collect_lng_data()
    print(f"\nCollected {len(results)} fields")
