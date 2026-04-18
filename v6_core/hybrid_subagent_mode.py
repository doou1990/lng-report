#!/usr/bin/env python3
"""
LNG市场分析助手 v6.1 - 混合子代理模式
核心特性: 
- API子代理 (3个): 采集国际数据，30秒超时
- 网页子代理 (1个): 采集国内数据，300秒超时
- 中孚审核子代理 (1个): 数据质量审核，60秒超时
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


@dataclass
class EvaluationReport:
    """评估报告"""
    timestamp: str
    total_score: float
    rating: str
    completeness: Dict
    quality: Dict
    anomalies: List[Dict]
    recommendations: List[str]


class HybridSubAgentCoordinator:
    """
    混合子代理协调器
    
    架构:
    Phase 1: 3个API子代理并行 (国际数据)
    Phase 2: 1个网页子代理 (国内数据)
    Phase 3: 1个中孚审核子代理 (质量评估)
    """
    
    def __init__(self):
        self.results: Dict[str, CollectionResult] = {}
        self.stats = {
            "api_success": 0,
            "api_failed": 0,
            "web_success": 0,
            "web_failed": 0,
            "start_time": None,
            "end_time": None
        }
    
    async def collect_all(self, date: Optional[str] = None) -> Dict[str, CollectionResult]:
        """
        执行混合子代理采集流程
        
        Args:
            date: 采集日期，默认今天
            
        Returns:
            采集结果字典
        """
        self.stats["start_time"] = datetime.now().isoformat()
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        
        print(f"🚀 LNG Market Analysis v6.1 - Hybrid SubAgent Mode")
        print(f"📅 Target Date: {target_date}")
        print("=" * 60)
        
        # Phase 1: API子代理并行采集 (国际数据)
        print("\n📡 Phase 1: API SubAgents (International Data)")
        print("-" * 60)
        await self._phase_1_api_collection()
        
        # Phase 2: 网页子代理采集 (国内数据)
        print("\n🌐 Phase 2: Web SubAgent (Domestic Data)")
        print("-" * 60)
        await self._phase_2_web_collection()
        
        # Phase 3: 中孚审核子代理
        print("\n📊 Phase 3: Evaluator SubAgent (Quality Audit)")
        print("-" * 60)
        eval_report = await self._phase_3_evaluation()
        
        # 计算派生字段
        self._calculate_derived_fields()
        
        self.stats["end_time"] = datetime.now().isoformat()
        self._print_stats(eval_report)
        
        return self.results
    
    # ==========================================
    # Phase 1: API子代理 (国际数据)
    # ==========================================
    
    async def _phase_1_api_collection(self):
        """Phase 1: 3个API子代理并行采集"""
        tasks = [
            self._spawn_crude_api_agent(),
            self._spawn_lng_api_agent(),
            self._spawn_inventory_api_agent(),
        ]
        
        print("Spawning 3 API SubAgents (30s timeout each)...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                print(f"   ✗ API Agent failed: {result}")
                self.stats["api_failed"] += 1
            elif isinstance(result, dict):
                for field, data in result.items():
                    if data:
                        self.results[field] = data
                        self.stats["api_success"] += 1
    
    async def _spawn_crude_api_agent(self) -> Dict[str, CollectionResult]:
        """子代理1: 原油域API采集"""
        prompt = """你是一名原油API数据采集助理。

【任务】通过OilPriceAPI采集Brent和WTI原油价格。

【API信息】
- Base URL: https://api.oilpriceapi.com/v1
- 商品代码: BRENT_USD, WTI_USD
- 从环境变量获取: OILPRICE_API_KEY

【执行步骤】
1. 读取环境变量 OILPRICE_API_KEY
2. 调用API: /prices/latest?by_code=BRENT_USD
3. 调用API: /prices/latest?by_code=WTI_USD
4. 解析JSON返回

【输出格式】
{
  "brent": {"field": "brent", "name": "Brent原油", "value": 73.21, "unit": "美元/桶", "timestamp": "2026-04-12T07:30:00Z", "source": "OilPriceAPI", "confidence": "A", "tier": 0, "notes": "Code: BRENT_USD"},
  "wti": {"field": "wti", "name": "WTI原油", "value": 69.85, "unit": "美元/桶", "timestamp": "2026-04-12T07:30:00Z", "source": "OilPriceAPI", "confidence": "A", "tier": 0, "notes": "Code: WTI_USD"}
}

【重要】只调用API，不搜索不爬网页。30秒内完成。"""
        
        return await self._execute_subagent("Crude API", prompt, 30)
    
    async def _spawn_lng_api_agent(self) -> Dict[str, CollectionResult]:
        """子代理2: 国际LNG域API采集"""
        prompt = """你是一名国际LNG API数据采集助理。

【任务】通过OilPriceAPI采集JKM、TTF、Henry Hub价格。

【API信息】
- Base URL: https://api.oilpriceapi.com/v1
- 商品代码: JKM_LNG_USD, TTF_GAS_USD, HH_GAS_USD
- 从环境变量获取: OILPRICE_API_KEY

【执行步骤】
1. 读取环境变量 OILPRICE_API_KEY
2. 调用API获取JKM、TTF、Henry Hub价格
3. 解析JSON返回

【输出格式】
{
  "jkm": {"field": "jkm", "name": "JKM LNG", "value": 11.25, "unit": "美元/MMBtu", "timestamp": "2026-04-12T07:30:00Z", "source": "OilPriceAPI", "confidence": "A", "tier": 0, "notes": "Code: JKM_LNG_USD"},
  "ttf": {"field": "ttf", "name": "TTF天然气", "value": 10.85, "unit": "美元/MMBtu", "timestamp": "2026-04-12T07:30:00Z", "source": "OilPriceAPI", "confidence": "A", "tier": 0, "notes": "Code: TTF_GAS_USD"},
  "henry_hub": {"field": "henry_hub", "name": "Henry Hub", "value": 3.05, "unit": "美元/MMBtu", "timestamp": "2026-04-12T07:30:00Z", "source": "OilPriceAPI", "confidence": "A", "tier": 0, "notes": "Code: HH_GAS_USD"}
}

【重要】只调用API，不搜索不爬网页。30秒内完成。"""
        
        return await self._execute_subagent("LNG API", prompt, 30)
    
    async def _spawn_inventory_api_agent(self) -> Dict[str, CollectionResult]:
        """子代理3: 库存域API采集"""
        prompt = """你是一名库存API数据采集助理。

【任务】通过EIA API采集美国原油库存和天然气库存。

【API信息】
- Base URL: https://api.eia.gov/v2
- 数据系列ID: PET.WCRSTUS1.W (原油), NG.NW2_EPG0_SWO_R48_BCF.W (天然气)
- 从环境变量获取: EIA_API_KEY

【执行步骤】
1. 读取环境变量 EIA_API_KEY
2. 调用API获取原油库存和天然气库存
3. 解析JSON返回，取最新记录

【输出格式】
{
  "us_crude_inventory": {"field": "us_crude_inventory", "name": "美国商业原油库存", "value": 450.2, "unit": "百万桶", "timestamp": "2026-04-11", "source": "EIA", "confidence": "A", "tier": 0, "notes": "Series: PET.WCRSTUS1.W"},
  "us_ng_inventory": {"field": "us_ng_inventory", "name": "美国天然气库存", "value": 1850, "unit": "十亿立方英尺", "timestamp": "2026-04-11", "source": "EIA", "confidence": "A", "tier": 0, "notes": "Series: NG.NW2_EPG0_SWO_R48_BCF.W"}
}

【重要】只调用API，不搜索不爬网页。30秒内完成。"""
        
        return await self._execute_subagent("Inventory API", prompt, 30)
    
    # ==========================================
    # Phase 2: 网页子代理 (国内数据)
    # ==========================================
    
    async def _phase_2_web_collection(self):
        """Phase 2: 网页子代理采集国内数据"""
        result = await self._spawn_domestic_web_agent()
        
        if isinstance(result, Exception):
            print(f"   ✗ Web Agent failed: {result}")
            self.stats["web_failed"] += 1
        elif isinstance(result, dict):
            for field, data in result.items():
                if data:
                    self.results[field] = data
                    self.stats["web_success"] += 1
    
    async def _spawn_domestic_web_agent(self) -> Dict[str, CollectionResult]:
        """子代理4: 国内数据网页采集"""
        prompt = """你是一名国内LNG数据网页采集助理。

【任务】采集中国LNG市场价格数据。

【必采数据】
1. 国内LNG工厂出厂均价
2. 浙江宁波接收站价格
3. 浙江舟山接收站价格
4. 上海五号沟接收站价格
5. 市场开工率

【数据源优先级】
1. Mysteel (mysteel.com) - 首选
2. 隆众资讯 - 备选
3. 百川盈孚 - 备选

【采集策略】
- 使用web_fetch工具访问网页
- 提取最新价格数据(元/吨)
- 记录数据来源和更新时间
- 优先当日数据，其次3日内

【输出格式】
{
  "china_lng_factory": {"field": "china_lng_factory", "name": "国内LNG工厂均价", "value": 4200, "unit": "元/吨", "timestamp": "2026-04-12", "source": "Mysteel", "confidence": "B", "tier": 1, "url": "https://...", "notes": "全国平均"},
  "zhejiang_ningbo": {"field": "zhejiang_ningbo", "name": "浙江宁波接收站", "value": 4500, "unit": "元/吨", "timestamp": "2026-04-12", "source": "Mysteel", "confidence": "B", "tier": 1, "url": "https://...", "notes": "中海油宁波"},
  "zhejiang_zhoushan": {"field": "zhejiang_zhoushan", "name": "浙江舟山接收站", "value": 4450, "unit": "元/吨", "timestamp": "2026-04-12", "source": "Mysteel", "confidence": "B", "tier": 1, "url": "https://...", "notes": "新奥舟山"},
  "shanghai_wuhaogou": {"field": "shanghai_wuhaogou", "name": "上海五号沟", "value": 4550, "unit": "元/吨", "timestamp": "2026-04-12", "source": "Mysteel", "confidence": "B", "tier": 1, "url": "https://...", "notes": "上海接收站"},
  "operating_rate": {"field": "operating_rate", "name": "开工率", "value": 58.5, "unit": "%", "timestamp": "2026-04-12", "source": "隆众资讯", "confidence": "B", "tier": 1, "url": "https://...", "notes": "全国平均"}
}

【重要】
- 必须使用web_fetch工具，不要直接搜索
- 如果某数据源失败，尝试备选源
- 如果无法获取，value设为null，confidence设为"D"
- 300秒内完成
"""
        
        return await self._execute_subagent("Domestic Web", prompt, 300)
    
    # ==========================================
    # Phase 3: 中孚审核子代理
    # ==========================================
    
    async def _phase_3_evaluation(self) -> EvaluationReport:
        """Phase 3: 中孚审核子代理评估数据质量"""
        return await self._spawn_evaluator_agent()
    
    async def _spawn_evaluator_agent(self) -> EvaluationReport:
        """子代理5: 中孚数据审核"""
        # 准备数据摘要
        data_summary = []
        for field, result in self.results.items():
            data_summary.append({
                "field": field,
                "name": result.name,
                "value": result.value,
                "source": result.source,
                "confidence": result.confidence
            })
        
        prompt = f"""你是一名数据质量审核助理(中孚)。

【任务】审核LNG市场数据的完整性和质量。

【采集数据】
{json.dumps(data_summary, ensure_ascii=False, indent=2)}

【必采数据清单】
1. brent - Brent原油价格
2. wti - WTI原油价格
3. jkm - JKM LNG价格
4. ttf - TTF天然气价格
5. henry_hub - Henry Hub价格
6. us_crude_inventory - 美国原油库存
7. us_ng_inventory - 美国天然气库存
8. china_lng_factory - 国内LNG工厂均价
9. zhejiang_ningbo - 浙江宁波接收站
10. zhejiang_zhoushan - 浙江舟山接收站
11. shanghai_wuhaogou - 上海五号沟
12. operating_rate - 开工率

【审核标准】
1. 完整性: 检查必采数据是否齐全
2. 数据来源: A级(官方API)>B级(网页)>C级(搜索)>D级(缺失)
3. 时效性: 优先当日数据
4. 异常检测: 价格倒挂、极端值、单位错误

【输出格式】
{{
  "timestamp": "2026-04-12T08:00:00Z",
  "total_score": 85.5,
  "rating": "B",
  "completeness": {{
    "coverage": 83.3,
    "missing_fields": ["zhejiang_zhoushan"],
    "collected_count": 10,
    "required_count": 12
  }},
  "quality": {{
    "a_level_count": 7,
    "b_level_count": 3,
    "c_level_count": 0,
    "d_level_count": 2
  }},
  "anomalies": [
    {{"type": "missing_data", "severity": "medium", "field": "zhejiang_zhoushan", "message": "数据缺失"}}
  ],
  "recommendations": [
    "建议补充浙江舟山接收站数据",
    "国内数据可考虑增加备用源"
  ]
}}

【重要】60秒内完成审核。"""
        
        try:
            result = await self._execute_subagent_raw("Evaluator", prompt, 60)
            
            # 解析评估报告
            eval_data = json.loads(result)
            return EvaluationReport(**eval_data)
            
        except Exception as e:
            print(f"   ✗ Evaluator failed: {e}")
            # 返回默认报告
            return EvaluationReport(
                timestamp=datetime.now().isoformat(),
                total_score=0,
                rating="D",
                completeness={"coverage": 0, "missing_fields": [], "collected_count": 0, "required_count": 12},
                quality={},
                anomalies=[{"type": "evaluation_failed", "severity": "high", "message": str(e)}],
                recommendations=["审核失败，请检查数据"]
            )
    
    # ==========================================
    # 工具函数
    # ==========================================
    
    async def _execute_subagent(self, name: str, prompt: str, timeout: int) -> Dict[str, CollectionResult]:
        """执行子代理并解析结果"""
        try:
            # 注意：这里使用 sessions_spawn 创建子代理
            # 实际环境中需要导入并使用正确的API
            # result = await sessions_spawn(task=prompt, timeout=timeout, mode="run")
            
            # 模拟子代理执行（实际实现时替换）
            print(f"   [SubAgent {name}] Starting...")
            await asyncio.sleep(1)  # 模拟执行
            
            # 模拟返回结果
            return {}
            
        except Exception as e:
            print(f"   ✗ SubAgent {name} failed: {e}")
            return {}
    
    async def _execute_subagent_raw(self, name: str, prompt: str, timeout: int) -> str:
        """执行子代理并返回原始结果"""
        try:
            print(f"   [SubAgent {name}] Starting...")
            await asyncio.sleep(1)  # 模拟执行
            return "{}"
        except Exception as e:
            raise e
    
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
    
    def _print_stats(self, eval_report: EvaluationReport):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("📈 Collection Statistics")
        print("=" * 60)
        print(f"API Success:    {self.stats['api_success']}")
        print(f"API Failed:     {self.stats['api_failed']}")
        print(f"Web Success:    {self.stats['web_success']}")
        print(f"Web Failed:     {self.stats['web_failed']}")
        print(f"Total Fields:   {len(self.results)}")
        
        # 审核报告
        print(f"\n📊 Quality Report")
        print(f"Total Score:    {eval_report.total_score}/100")
        print(f"Rating:         {eval_report.rating}")
        print(f"Completeness:   {eval_report.completeness.get('coverage', 0)}%")
        print(f"Anomalies:      {len(eval_report.anomalies)}")
        
        # 按置信度统计
        conf_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
        for result in self.results.values():
            if result.confidence in conf_counts:
                conf_counts[result.confidence] += 1
        
        print(f"\nConfidence Distribution:")
        for conf, count in conf_counts.items():
            print(f"  {conf}级: {count}")
        
        # 建议
        if eval_report.recommendations:
            print(f"\n💡 Recommendations:")
            for rec in eval_report.recommendations:
                print(f"  - {rec}")
    
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
async def collect_with_hybrid_subagents(date: Optional[str] = None) -> Dict[str, CollectionResult]:
    """
    使用混合子代理采集数据的便捷函数
    
    Args:
        date: 采集日期
        
    Returns:
        采集结果字典
    """
    coordinator = HybridSubAgentCoordinator()
    return await coordinator.collect_all(date)


if __name__ == "__main__":
    # 测试混合子代理采集
    results = asyncio.run(collect_with_hybrid_subagents())
    print(f"\n✅ Collected {len(results)} fields via Hybrid SubAgents")
