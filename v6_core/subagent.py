"""
子代理采集器
使用OpenClaw子代理执行Tier 1和Tier 2采集任务
"""
import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SubAgentTask:
    """子代理任务"""
    task_id: str
    field: str
    name: str
    category: str
    tier: int
    instructions: str
    timeout: int = 300  # 默认5分钟超时


class SubAgentCollector:
    """
    子代理采集器
    
    负责:
    1. 创建子代理会话执行采集任务
    2. 管理子代理超时和重试
    3. 聚合子代理返回结果
    4. 失败时触发降级策略
    """
    
    # 子代理超时配置
    TIMEOUTS = {
        "web_collection": 300,    # 网页采集: 5分钟
        "search_validation": 180,  # 搜索验证: 3分钟
        "data_processing": 60      # 数据处理: 1分钟
    }
    
    # 批处理大小
    BATCH_SIZE = 3
    
    def __init__(self):
        """初始化子代理采集器"""
        self.stats = {
            "total_tasks": 0,
            "success": 0,
            "failed": 0,
            "timeout": 0
        }
    
    async def collect_batch(self, tasks: List[SubAgentTask]) -> Dict[str, Any]:
        """
        批量执行采集任务
        
        采用分批并行策略，每批最多3个任务，避免同时启动过多子代理
        
        Args:
            tasks: 子代理任务列表
            
        Returns:
            采集结果字典
        """
        results = {}
        self.stats["total_tasks"] = len(tasks)
        
        # 分批处理
        for i in range(0, len(tasks), self.BATCH_SIZE):
            batch = tasks[i:i + self.BATCH_SIZE]
            print(f"\n🔄 Processing batch {i//self.BATCH_SIZE + 1}/{(len(tasks)-1)//self.BATCH_SIZE + 1}")
            print(f"   Tasks: {[t.name for t in batch]}")
            
            # 并行执行批次内的任务
            batch_results = await self._execute_batch(batch)
            results.update(batch_results)
            
            # 批次间短暂延迟，避免资源竞争
            if i + self.BATCH_SIZE < len(tasks):
                await asyncio.sleep(2)
        
        return results
    
    async def _execute_batch(self, tasks: List[SubAgentTask]) -> Dict[str, Any]:
        """执行一批子代理任务"""
        # 创建异步任务
        coroutines = [self._execute_single_task(task) for task in tasks]
        
        # 并行执行，等待所有完成
        batch_results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # 处理结果
        results = {}
        for task, result in zip(tasks, batch_results):
            if isinstance(result, Exception):
                print(f"   ✗ {task.name}: Failed - {str(result)}")
                self.stats["failed"] += 1
                results[task.field] = self._create_error_result(task, str(result))
            else:
                print(f"   ✓ {task.name}: Success")
                self.stats["success"] += 1
                results[task.field] = result
        
        return results
    
    async def _execute_single_task(self, task: SubAgentTask) -> Dict[str, Any]:
        """
        执行单个子代理任务
        
        这里使用OpenClaw的sessions_spawn功能创建子代理
        """
        # 构建子代理提示词
        prompt = self._build_agent_prompt(task)
        
        # 模拟子代理执行（实际实现将使用sessions_spawn）
        # 在真实环境中，这里应该调用:
        # result = await sessions_spawn(
        #     task=prompt,
        #     timeout=task.timeout,
        #     mode="run"
        # )
        
        # 模拟结果（用于测试）
        await asyncio.sleep(1)  # 模拟执行时间
        
        return {
            "field": task.field,
            "name": task.name,
            "value": None,  # 子代理应填充实际值
            "unit": "",
            "timestamp": datetime.now().isoformat(),
            "source": f"SubAgent-Tier{task.tier}",
            "confidence": "B" if task.tier == 1 else "C",
            "tier": task.tier,
            "notes": f"Collected by subagent: {task.task_id}"
        }
    
    def _build_agent_prompt(self, task: SubAgentTask) -> str:
        """构建子代理提示词"""
        base_prompt = f"""你是一名专业的能源数据采集助理，负责采集{task.name}数据。

任务信息:
- 数据字段: {task.field}
- 数据类别: {task.category}
- 采集层级: Tier {task.tier} ({"网页采集" if task.tier == 1 else "搜索验证"})

{task.instructions}

输出要求:
请以JSON格式返回采集结果:
{{
  "field": "{task.field}",
  "name": "{task.name}",
  "value": <数值>,
  "unit": "<单位>",
  "timestamp": "<ISO时间戳>",
  "source": "<数据来源>",
  "url": "<数据URL>",
  "confidence": "<A/B/C/D>",
  "notes": "<备注信息>"
}}

重要提示:
1. 如果无法获取数据，value设为null，confidence设为"D"
2. 必须提供数据来源URL
3. 优先使用当日数据，其次3日内数据
4. 如果多源数据差异>5%，标注差异并选择最权威的来源
"""
        return base_prompt
    
    def _create_error_result(self, task: SubAgentTask, error_msg: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "field": task.field,
            "name": task.name,
            "value": None,
            "unit": "",
            "timestamp": datetime.now().isoformat(),
            "source": "Error",
            "confidence": "D",
            "tier": task.tier,
            "notes": f"Collection failed: {error_msg}"
        }
    
    def create_web_collection_tasks(self, missing_fields: List[Dict]) -> List[SubAgentTask]:
        """
        创建网页采集任务
        
        Args:
            missing_fields: 缺失字段列表
            
        Returns:
            子代理任务列表
        """
        tasks = []
        
        # 按类别分组
        categories = {}
        for field in missing_fields:
            cat = field.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(field)
        
        # 为每个类别创建任务
        task_id = 0
        for category, fields in categories.items():
            for field in fields:
                task = SubAgentTask(
                    task_id=f"web_{task_id:03d}",
                    field=field.get("field", ""),
                    name=field.get("name", ""),
                    category=category,
                    tier=1,
                    instructions=self._get_web_instructions(category, field),
                    timeout=self.TIMEOUTS["web_collection"]
                )
                tasks.append(task)
                task_id += 1
        
        return tasks
    
    def create_search_validation_tasks(self, fields_to_validate: List[Dict]) -> List[SubAgentTask]:
        """
        创建搜索验证任务
        
        Args:
            fields_to_validate: 需要验证的字段列表
            
        Returns:
            子代理任务列表
        """
        tasks = []
        
        task_id = 0
        for field in fields_to_validate:
            task = SubAgentTask(
                task_id=f"search_{task_id:03d}",
                field=field.get("field", ""),
                name=field.get("name", ""),
                category=field.get("category", "other"),
                tier=2,
                instructions=self._get_search_instructions(field),
                timeout=self.TIMEOUTS["search_validation"]
            )
            tasks.append(task)
            task_id += 1
        
        return tasks
    
    def _get_web_instructions(self, category: str, field: Dict) -> str:
        """获取网页采集指令"""
        instructions_map = {
            "国际原油": """
采集步骤:
1. 访问OilPrice.com或TradingEconomics.com
2. 查找最新现货价格
3. 记录价格数值、单位和更新时间
4. 验证数据时效性(优先当日数据)
""",
            "国际LNG": """
采集步骤:
1. 访问OilPrice.com的LNG价格页面
2. 查找JKM、TTF、Henry Hub价格
3. 记录价格数值、单位和更新时间
4. 验证数据时效性
""",
            "国内LNG": """
采集步骤:
1. 访问Mysteel能源板块或隆众资讯
2. 查找LNG工厂出厂价和接收站挂牌价
3. 重点关注浙江地区价格(宁波、舟山)
4. 记录价格数值(元/吨)和更新时间
""",
            "库存数据": """
采集步骤:
1. 访问EIA官网的石油和天然气库存页面
2. 查找最新库存数据
3. 记录库存数值、单位和报告日期
4. 验证数据为官方发布
""",
            "default": """
采集步骤:
1. 使用web_fetch工具访问权威数据源
2. 提取最新价格/数据
3. 记录数值、单位和来源
4. 验证数据准确性
"""
        }
        
        return instructions_map.get(category, instructions_map["default"])
    
    def _get_search_instructions(self, field: Dict) -> str:
        """获取搜索验证指令"""
        field_name = field.get("name", "")
        
        return f"""
验证任务:
1. 使用Exa或Tavily搜索"{field_name} 最新"
2. 获取至少2个独立来源的数据
3. 比较数据差异:
   - 如果差异<5%: 确认数据可靠
   - 如果差异5-10%: 标注差异，选择权威来源
   - 如果差异>10%: 标注数据不确定性高
4. 返回验证结果和交叉验证信息
"""
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("📊 SubAgent Collection Statistics")
        print("=" * 60)
        print(f"Total Tasks: {self.stats['total_tasks']}")
        print(f"Success:     {self.stats['success']} ({self.stats['success']/max(self.stats['total_tasks'],1)*100:.1f}%)")
        print(f"Failed:      {self.stats['failed']} ({self.stats['failed']/max(self.stats['total_tasks'],1)*100:.1f}%)")
        print(f"Timeout:     {self.stats['timeout']}")


# 便捷函数
async def collect_via_subagents(tasks: List[SubAgentTask]) -> Dict[str, Any]:
    """
    通过子代理采集数据的便捷函数
    
    Args:
        tasks: 子代理任务列表
        
    Returns:
        采集结果字典
    """
    collector = SubAgentCollector()
    return await collector.collect_batch(tasks)


if __name__ == "__main__":
    # 测试子代理采集器
    test_tasks = [
        SubAgentTask(
            task_id="test_001",
            field="china_lng_factory",
            name="国内LNG工厂价",
            category="国内LNG",
            tier=1,
            instructions="Test instruction",
            timeout=60
        ),
        SubAgentTask(
            task_id="test_002",
            field="zhejiang_ningbo",
            name="浙江宁波接收站",
            category="国内LNG",
            tier=1,
            instructions="Test instruction",
            timeout=60
        )
    ]
    
    results = asyncio.run(collect_via_subagents(test_tasks))
    print(f"\nCollected {len(results)} results")
