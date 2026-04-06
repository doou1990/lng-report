# LNG报告系统 v4.2 架构设计文档

**设计时间**: 2026-04-05 20:48  
**设计目标**: 整合claw-code和oh-my-openagent最佳实践  
**版本**: v4.2 (意图驱动 + 动态委派 + 多层验证 + Boulder会话)

---

## 🏗️ v4.2 整体架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LNG报告系统 v4.2 架构                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Layer 1: 意图解析层 (Intent Parser)                                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • 关键词识别                                                   │   │
│  │ • 上下文理解                                                   │   │
│  │ • 需求澄清                                                     │   │
│  │ • 任务清单生成                                                 │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Layer 2: 动态委派层 (Dynamic Delegation)                             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • 根据意图选择相关助理                                         │   │
│  │ • 动态组装Agent团队                                            │   │
│  │ • 并行任务分配                                                 │   │
│  │ • 资源优化调度                                                 │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Layer 3: 数据采集层 (12助理并行)                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 原油 │ 海明 │ 润仓 │ 陆远 │ 衡尺 │ 欧风 │ 金算 │ 盾甲 │        │   │
│  │ 镜史 │ 洋基 │ 期货 │ 库存 │                                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Layer 4: 多层验证层 (Multi-Layer Verification)                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ L1: 自动规则检查 → L2: 交叉验证 → L3: 异常检测 → L4: 人工审核  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Layer 5: 报告生成层 (Report Generation)                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • Markdown完整版                                               │   │
│  │ • HTML网页版 (ECharts交互)                                     │   │
│  │ • PDF导出版                                                    │   │
│  │ • API JSON版                                                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Layer 6: 会话管理层 (Boulder Session)                                │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • 状态跟踪 (boulder.json)                                      │   │
│  │ • 断点续传                                                     │   │
│  │ • 历史恢复                                                     │   │
│  │ • 进度保存                                                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Layer 1: 意图解析层

### 意图识别矩阵

| 用户输入 | 识别意图 | 任务清单 |
|----------|----------|----------|
| "LNG报告" | 标准日报 | 全部12助理 |
| "LNG报告 期货" | 期货增强 | 全部+期货重点 |
| "LNG报告 库存" | 库存增强 | 全部+库存重点 |
| "LNG价格" | 仅价格 | 原油+海明+润仓 |
| "浙江LNG价格" | 区域价格 | 润仓(浙江专区) |
| "国际LNG价格" | 国际价格 | 海明+欧风+洋基 |
| "原油报告" | 原油专题 | 原油+衡尺+镜史 |

### 意图解析代码

```python
# intent_parser.py

class IntentParser:
    """意图解析器 - 理解用户真正需求"""
    
    def __init__(self):
        self.intent_patterns = {
            'standard_report': {
                'keywords': ['LNG报告', '生成报告', 'LNG分析'],
                'required_agents': ['原油', '海明', '润仓', '陆远', '衡尺', '欧风', '金算', '盾甲', '镜史', '洋基'],
                'optional_agents': ['期货', '库存'],
                'output_format': ['markdown', 'html']
            },
            'futures_enhanced': {
                'keywords': ['期货', 'futures', '远期价格'],
                'required_agents': ['原油', '海明', '期货'],
                'focus': 'futures_data',
                'output_format': ['markdown', 'html']
            },
            'inventory_enhanced': {
                'keywords': ['库存', 'inventory', 'storage'],
                'required_agents': ['欧风', '库存'],
                'focus': 'inventory_data',
                'output_format': ['markdown', 'html']
            },
            'price_only': {
                'keywords': ['价格', 'price', '多少钱'],
                'required_agents': ['原油', '海明', '润仓'],
                'output_format': ['html']
            },
            'zhejiang_focus': {
                'keywords': ['浙江', '宁波', '舟山'],
                'required_agents': ['润仓'],
                'focus': 'zhejiang_section',
                'output_format': ['html']
            }
        }
    
    def parse(self, user_input: str, context: dict = None) -> dict:
        """
        解析用户输入，返回任务清单
        
        Args:
            user_input: 用户输入文本
            context: 上下文信息（历史对话等）
        
        Returns:
            任务清单字典
        """
        user_input_lower = user_input.lower()
        
        # 1. 匹配意图模式
        matched_intent = None
        for intent_name, config in self.intent_patterns.items():
            if any(kw in user_input_lower for kw in config['keywords']):
                matched_intent = intent_name
                break
        
        # 2. 默认意图
        if not matched_intent:
            matched_intent = 'standard_report'
        
        # 3. 构建任务清单
        intent_config = self.intent_patterns[matched_intent]
        task_list = {
            'intent': matched_intent,
            'user_request': user_input,
            'required_agents': intent_config['required_agents'],
            'optional_agents': intent_config.get('optional_agents', []),
            'focus_areas': intent_config.get('focus', 'full'),
            'output_formats': intent_config['output_format'],
            'estimated_time': self._estimate_time(intent_config),
            'priority': self._calculate_priority(user_input, context)
        }
        
        return task_list
    
    def _estimate_time(self, config: dict) -> int:
        """估算执行时间（秒）"""
        base_time = 60  # 基础时间
        agent_time = len(config['required_agents']) * 30  # 每个助理30秒
        return base_time + agent_time
    
    def _calculate_priority(self, user_input: str, context: dict) -> str:
        """计算任务优先级"""
        if '紧急' in user_input or 'urgent' in user_input.lower():
            return 'P0'
        elif '今天' in user_input or '立即' in user_input:
            return 'P1'
        else:
            return 'P2'

# 使用示例
if __name__ == '__main__':
    parser = IntentParser()
    
    # 测试用例
    test_inputs = [
        "LNG报告",
        "LNG报告 期货",
        "浙江LNG价格",
        "国际原油和LNG价格"
    ]
    
    for input_text in test_inputs:
        result = parser.parse(input_text)
        print(f"\n输入: {input_text}")
        print(f"意图: {result['intent']}")
        print(f"必需助理: {result['required_agents']}")
        print(f"可选助理: {result['optional_agents']}")
```

---

## 🎯 Layer 2: 动态委派层

### 动态Agent选择算法

```python
# dynamic_delegation.py

class DynamicDelegator:
    """动态Agent委派器 - 根据意图组装Agent团队"""
    
    def __init__(self):
        self.agent_registry = {
            '原油': {'cost': 1.0, 'speed': 'fast', 'reliability': 0.95},
            '海明': {'cost': 1.0, 'speed': 'fast', 'reliability': 0.90},
            '润仓': {'cost': 1.2, 'speed': 'medium', 'reliability': 0.85},
            '陆远': {'cost': 0.8, 'speed': 'fast', 'reliability': 0.88},
            '衡尺': {'cost': 0.8, 'speed': 'fast', 'reliability': 0.85},
            '欧风': {'cost': 1.0, 'speed': 'medium', 'reliability': 0.87},
            '金算': {'cost': 0.8, 'speed': 'fast', 'reliability': 0.82},
            '盾甲': {'cost': 0.8, 'speed': 'fast', 'reliability': 0.80},
            '镜史': {'cost': 0.6, 'speed': 'fast', 'reliability': 0.75},
            '洋基': {'cost': 0.8, 'speed': 'fast', 'reliability': 0.78},
            '期货': {'cost': 1.5, 'speed': 'slow', 'reliability': 0.85},
            '库存': {'cost': 1.2, 'speed': 'medium', 'reliability': 0.80}
        }
    
    def delegate(self, task_list: dict, budget: float = None) -> dict:
        """
        根据任务清单动态委派Agent
        
        Args:
            task_list: 意图解析后的任务清单
            budget: 成本预算（可选）
        
        Returns:
            委派计划
        """
        required = task_list['required_agents']
        optional = task_list['optional_agents']
        
        # 1. 必需Agent必须包含
        selected_agents = required.copy()
        
        # 2. 根据意图选择可选Agent
        if task_list['intent'] == 'futures_enhanced':
            if '期货' in optional:
                selected_agents.append('期货')
        
        elif task_list['intent'] == 'inventory_enhanced':
            if '库存' in optional:
                selected_agents.append('库存')
        
        elif task_list['intent'] == 'standard_report':
            # 标准报告：根据预算决定是否包含期货和库存
            if budget and budget > 20:  # 预算充足
                selected_agents.extend(['期货', '库存'])
        
        # 3. 优化执行顺序（依赖关系）
        execution_order = self._optimize_order(selected_agents)
        
        # 4. 计算总成本和时间
        total_cost = sum(self.agent_registry[agent]['cost'] for agent in selected_agents)
        estimated_time = max(self.agent_registry[agent]['speed'] for agent in selected_agents)
        
        return {
            'selected_agents': selected_agents,
            'execution_order': execution_order,
            'parallel_groups': self._create_parallel_groups(execution_order),
            'total_cost': total_cost,
            'estimated_time': estimated_time,
            'fallback_plan': self._create_fallback(selected_agents)
        }
    
    def _optimize_order(self, agents: list) -> list:
        """优化执行顺序（考虑依赖关系）"""
        # 基础数据先采集
        priority = {
            '原油': 1, '海明': 1,  # 基础价格
            '润仓': 2, '陆远': 2,  # 国内数据
            '期货': 3, '库存': 3,  # 增强数据
            '衡尺': 4, '欧风': 4,  # 分析数据
            '金算': 5, '盾甲': 5, '镜史': 5, '洋基': 5  # 其他
        }
        return sorted(agents, key=lambda x: priority.get(x, 99))
    
    def _create_parallel_groups(self, ordered_agents: list) -> list:
        """创建并行执行组"""
        # 每组最多5个Agent（系统限制）
        groups = []
        for i in range(0, len(ordered_agents), 5):
            groups.append(ordered_agents[i:i+5])
        return groups
    
    def _create_fallback(self, selected_agents: list) -> dict:
        """创建备用计划"""
        fallback = {}
        for agent in selected_agents:
            if agent == '期货':
                fallback[agent] = ['原油', '海明']  # 用现货价格替代
            elif agent == '库存':
                fallback[agent] = ['欧风']  # 用欧洲数据替代
            else:
                fallback[agent] = ['主代理']  # 主代理补采
        return fallback

# 使用示例
if __name__ == '__main__':
    delegator = DynamicDelegator()
    
    task = {
        'intent': 'futures_enhanced',
        'required_agents': ['原油', '海明', '润仓'],
        'optional_agents': ['期货', '库存']
    }
    
    plan = delegator.delegate(task, budget=25)
    print(f"选定助理: {plan['selected_agents']}")
    print(f"并行组: {plan['parallel_groups']}")
    print(f"总成本: {plan['total_cost']}")
    print(f"备用计划: {plan['fallback_plan']}")
```

---

## ✅ Layer 4: 多层验证层

### 4层验证架构

```python
# multi_layer_verification.py

class MultiLayerVerification:
    """多层验证系统 - 信任但验证"""
    
    def __init__(self):
        self.validation_rules = {
            'price_range': {
                'brent': (50, 150),  # $/barrel
                'wti': (50, 150),
                'jkm': (10, 30),     # $/MMBtu
                'ttf': (20, 100),    # €/MWh
                'domestic_lng': (3000, 8000)  # 元/吨
            },
            'max_daily_change': 0.20,  # 20%
            'max_source_discrepancy': 0.05  # 5%
        }
    
    def verify(self, data: dict) -> dict:
        """
        执行4层验证
        
        Args:
            data: 采集的原始数据
        
        Returns:
            验证报告
        """
        report = {
            'data': data,
            'l1_auto_check': self._l1_auto_check(data),
            'l2_cross_validation': self._l2_cross_validation(data),
            'l3_anomaly_detection': self._l3_anomaly_detection(data),
            'l4_manual_audit': None,  # 由中孚执行
            'final_confidence': None,
            'issues': []
        }
        
        # 计算最终置信度
        report['final_confidence'] = self._calculate_confidence(report)
        
        return report
    
    def _l1_auto_check(self, data: dict) -> dict:
        """L1: 自动规则检查"""
        results = {'passed': True, 'checks': []}
        
        for indicator, value in data.items():
            # 检查数值范围
            if indicator in self.validation_rules['price_range']:
                min_val, max_val = self.validation_rules['price_range'][indicator]
                if not (min_val <= value <= max_val):
                    results['passed'] = False
                    results['checks'].append({
                        'indicator': indicator,
                        'check': 'range',
                        'status': 'failed',
                        'value': value,
                        'expected': f'{min_val}-{max_val}'
                    })
                else:
                    results['checks'].append({
                        'indicator': indicator,
                        'check': 'range',
                        'status': 'passed'
                    })
            
            # 检查非空
            if value is None or value == '':
                results['passed'] = False
                results['checks'].append({
                    'indicator': indicator,
                    'check': 'not_null',
                    'status': 'failed'
                })
        
        return results
    
    def _l2_cross_validation(self, data: dict) -> dict:
        """L2: 多源交叉验证"""
        results = {'passed': True, 'validations': []}
        
        # 假设data包含多个来源
        for indicator, sources in data.items():
            if isinstance(sources, list) and len(sources) > 1:
                values = [s['value'] for s in sources]
                avg = sum(values) / len(values)
                max_diff = max(abs(v - avg) / avg for v in values)
                
                if max_diff > self.validation_rules['max_source_discrepancy']:
                    results['passed'] = False
                    results['validations'].append({
                        'indicator': indicator,
                        'status': 'discrepancy',
                        'max_diff': max_diff,
                        'sources': sources
                    })
                else:
                    results['validations'].append({
                        'indicator': indicator,
                        'status': 'consistent',
                        'max_diff': max_diff
                    })
        
        return results
    
    def _l3_anomaly_detection(self, data: dict) -> dict:
        """L3: 统计异常检测"""
        results = {'passed': True, 'anomalies': []}
        
        # 加载历史数据（简化示例）
        historical_avg = {
            'brent': 85,
            'jkm': 15,
            'domestic_lng': 4500
        }
        
        for indicator, value in data.items():
            if indicator in historical_avg:
                avg = historical_avg[indicator]
                deviation = abs(value - avg) / avg
                
                # 3σ原则（简化）
                if deviation > 0.30:  # 30%偏差
                    results['passed'] = False
                    results['anomalies'].append({
                        'indicator': indicator,
                        'value': value,
                        'historical_avg': avg,
                        'deviation': deviation,
                        'severity': 'high' if deviation > 0.50 else 'medium'
                    })
                else:
                    results['anomalies'].append({
                        'indicator': indicator,
                        'status': 'normal',
                        'deviation': deviation
                    })
        
        return results
    
    def _calculate_confidence(self, report: dict) -> str:
        """计算最终置信度"""
        score = 100
        
        # L1扣分
        if not report['l1_auto_check']['passed']:
            score -= 20
        
        # L2扣分
        if not report['l2_cross_validation']['passed']:
            score -= 15
        
        # L3扣分
        if not report['l3_anomaly_detection']['passed']:
            score -= 10
        
        # 转换为等级
        if score >= 90:
            return 'A'
        elif score >= 75:
            return 'B'
        elif score >= 60:
            return 'C'
        else:
            return 'D'

# 使用示例
if __name__ == '__main__':
    verifier = MultiLayerVerification()
    
    test_data = {
        'brent': 109.24,
        'jkm': 18.75,
        'domestic_lng': 4813
    }
    
    report = verifier.verify(test_data)
    print(f"L1自动检查: {report['l1_auto_check']['passed']}")
    print(f"L2交叉验证: {report['l2_cross_validation']['passed']}")
    print(f"L3异常检测: {report['l3_anomaly_detection']['passed']}")
    print(f"最终置信度: {report['final_confidence']}")
```

---

## 💾 Layer 6: Boulder会话管理层

### Boulder状态跟踪系统

```python
# boulder_session.py
import json
import os
from datetime import datetime
from typing import Dict, Any

class BoulderSession:
    """Boulder会话管理 - 断点续传支持"""
    
    def __init__(self, session_id: str = None):
        self.session_file = '/root/.openclaw/workspace/boulder.json'
        self.session_id = session_id or self._generate_session_id()
        self.state = self._load_state()
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return datetime.now().strftime('%Y%m%d-%H%M%S')
    
    def _load_state(self) -> dict:
        """加载会话状态"""
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return self._create_initial_state()
    
    def _create_initial_state(self) -> dict:
        """创建初始状态"""
        return {
            'session_id': self.session_id,
            'status': 'initialized',
            'created_at': datetime.now().isoformat(),
            'last_update': datetime.now().isoformat(),
            'completed_tasks': [],
            'in_progress_tasks': [],
            'pending_tasks': [],
            'checkpoints': [],
            'metadata': {}
        }
    
    def save(self):
        """保存会话状态"""
        self.state['last_update'] = datetime.now().isoformat()
        with open(self.session_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def start_task(self, task_name: str, metadata: dict = None):
        """开始任务"""
        task = {
            'name': task_name,
            'started_at': datetime.now().isoformat(),
            'status': 'in_progress',
            'metadata': metadata or {}
        }
        self.state['in_progress_tasks'].append(task)
        self.save()
    
    def complete_task(self, task_name: str, result: dict = None):
        """完成任务"""
        # 从in_progress移除
        self.state['in_progress_tasks'] = [
            t for t in self.state['in_progress_tasks'] 
            if t['name'] != task_name
        ]
        
        # 添加到completed
        task = {
            'name': task_name,
            'completed_at': datetime.now().isoformat(),
            'result': result or {}
        }
        self.state['completed_tasks'].append(task)
        self.save()
    
    def create_checkpoint(self, name: str, data: dict):
        """创建检查点"""
        checkpoint = {
            'name': name,
            'created_at': datetime.now().isoformat(),
            'data': data
        }
        self.state['checkpoints'].append(checkpoint)
        self.save()
    
    def recover(self) -> dict:
        """恢复会话"""
        if self.state['in_progress_tasks']:
            # 有进行中的任务，需要恢复
            return {
                'status': 'recovery_needed',
                'in_progress': self.state['in_progress_tasks'],
                'completed': self.state['completed_tasks'],
                'last_checkpoint': self.state['checkpoints'][-1] if self.state['checkpoints'] else None
            }
        else:
            return {
                'status': 'clean',
                'completed': self.state['completed_tasks']
            }
    
    def get_progress(self) -> dict:
        """获取进度"""
        total = len(self.state['completed_tasks']) + len(self.state['in_progress_tasks']) + len(self.state['pending_tasks'])
        completed = len(self.state['completed_tasks'])
        
        return {
            'total_tasks': total,
            'completed': completed,
            'in_progress': len(self.state['in_progress_tasks']),
            'pending': len(self.state['pending_tasks']),
            'percentage': (completed / total * 100) if total > 0 else 0
        }

# 使用示例
if __name__ == '__main__':
    # 创建会话
    boulder = BoulderSession()
    
    # 开始任务
    boulder.start_task('期货数据采集', {'agents': ['期货']})
    boulder.start_task('库存数据采集', {'agents': ['库存']})
    
    # 创建检查点
    boulder.create_checkpoint('数据采集完成', {'data': 'raw_data'})
    
    # 完成任务
    boulder.complete_task('期货数据采集', {'records': 10})
    
    # 查看进度
    progress = boulder.get_progress()
    print(f"进度: {progress['percentage']}%")
    
    # 恢复检查
    recovery = boulder.recover()
    print(f"恢复状态: {recovery['status']}")
```

---

## 🚀 整合：v4.2 完整工作流

```python
# v4_2_workflow.py

class LNGReportSystemV42:
    """LNG报告系统 v4.2 - 完整工作流"""
    
    def __init__(self):
        self.intent_parser = IntentParser()
        self.delegator = DynamicDelegator()
        self.verifier = MultiLayerVerification()
        self.boulder = BoulderSession()
    
    def generate_report(self, user_input: str) -> dict:
        """
        v4.2 完整报告生成流程
        """
        try:
            # 1. 意图解析
            print("🔍 Phase 1: 意图解析...")
            task_list = self.intent_parser.parse(user_input)
            
            # 2. 动态委派
            print("🎯 Phase 2: 动态委派...")
            delegation_plan = self.delegator.delegate(task_list)
            
            # 3. 数据采集 (并行)
            print("📊 Phase 3: 数据采集...")
            raw_data = self._collect_data(delegation_plan)
            
            # 4. 多层验证
            print("✅ Phase 4: 多层验证...")
            verification_report = self.verifier.verify(raw_data)
            
            # 5. 报告生成
            print("📝 Phase 5: 报告生成...")
            report = self._generate_output(verification_report, task_list)
            
            # 6. 保存状态
            self.boulder.complete_task('report_generation', {'status': 'success'})
            
            return {
                'status': 'success',
                'report': report,
                'verification': verification_report,
                'boulder_state': self.boulder.get_progress()
            }
            
        except Exception as e:
            # 错误处理：保存状态以便恢复
            self.boulder.create_checkpoint('error', {'error': str(e)})
            raise
    
    def _collect_data(self, plan: dict) -> dict:
        """并行数据采集"""
        # 实现并行采集逻辑
        pass
    
    def _generate_output(self, verified_data: dict, task_list: dict) -> dict:
        """生成报告输出"""
        # 实现报告生成逻辑
        pass

# 主入口
if __name__ == '__main__':
    system = LNGReportSystemV42()
    
    # 测试
    result = system.generate_report("LNG报告 期货")
    print(f"报告生成: {result['status']}")
```

---

## 📊 v4.2 vs v4.1 对比

| 特性 | v4.1 | v4.2 | 提升 |
|------|------|------|------|
| 意图解析 | 关键词匹配 | 智能意图理解 | ⬆️ |
| Agent委派 | 固定12助理 | 动态选择 | ⬆️ |
| 验证机制 | 单层审核 | 4层验证 | ⬆️ |
| 会话管理 | 日志记录 | Boulder断点续传 | ⬆️ |
| 成本优化 | 无 | 智能预算控制 | ⬆️ |
| 恢复能力 | 无 | 断点续传 | ⬆️ |

---

*设计完成: 2026-04-05 21:00*  
*版本: v4.2 架构设计*  
*状态: 准备实施*
