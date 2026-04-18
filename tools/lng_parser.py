#!/usr/bin/env python3
"""
LNG数据采集工具 - 简化版
使用 web_fetch 获取的内容进行提取
"""

import json
import re
from datetime import datetime

# 直接使用已抓取的内容进行测试
SAMPLE_CONTENT = '''
## 【2026.3.31】LNG市场整体报价分析——成本端边际松动，LNG市场高位震荡！

 日期：2026-03-31 11:42:08
 浏览：497 来源：LNG168物联网
 编辑：赵小斐

 春季进入传统需求淡季，北方供暖结束后工业用气需求有所回落，城燃企业及下游工厂库存处于可控区间，进一步抑制了价格上行空间，预计近期国内LNG价格将以高位震荡为主。

2026年3月1日-3月31日
国内LNG液价均价走势图

LNG物联网市场点评

据LNG物联网数据统计：截止2026年3月31日133家国内LNG工厂，67家检修/停产/停报/内销，整体对外开工率50%，目前本网统计市场均价为4738元/吨。较高价报价5400元/吨，较低价报价4000元/吨。

19家国内LNG接收站均价为5901元/吨，较高价是中海油宁波（浙、沪）报价6210元/吨，较低价是河北曹妃甸报价5450元/吨。

以上价格信息仅供参考，实际价格以液厂或贸易商价格确认函为准（盖章）。
国内LNG价：
今日国内LNG价格集中上行，17家调涨，较高涨幅150元/吨。中石油直供全国液厂2026年4月上半月原料气竞拍落幕，交收期为3月31日8:00至4月15日8:00。本次起拍价2.8元/方，成交区间2.90-3.00元/方，均价2.95元/方，较3月下旬微降0.05元/方；成交量4200万方，无流拍，投放量环比增加但气源仍偏紧。成本端虽边际松动，但仍高于当前市场价，叠加部分液厂减产、停产，对液价形成有力支撑。市场观望情绪浓厚，贸易商多持观望态度，需求端按需采购，部分液价探涨，但整体价格波动幅度有限，形成 "成本托底、需求制约" 的双向平衡格局。具体来看，西北、内蒙古、河北、西南、湖北地区主流成交价走高。海气方面，上海五号沟LNG价格回落。
国际油价：
  截至2026年3月31日10：56时，NYMEX原油[CL00Y]价格指数102.12，同比上期下降0.76，降幅0.74%。
  春季进入传统需求淡季，北方供暖结束后工业用气需求有所回落，城燃企业及下游工厂库存处于可控区间，进一步抑制了价格上行空间，预计近期国内LNG价格将以高位震荡为主。
注：以上提供的数据和信息仅供参考，任何依据此数据和信息而进行的投资、买卖、运营等行为所造成的任何直接或间接损失及法律后果均应当自行承担，与LNG168物联网无关。
'''


class LNGDataParser:
    """LNG数据解析器"""
    
    def __init__(self):
        self.patterns = {
            'report_date': r'【(\d{4}\.\d{1,2}\.\d{1,2})】',
            'factory': {
                'total': r'(\d+)家国内LNG工厂',
                'maintenance': r'(\d+)家检修',
                'operating_rate': r'开工率(\d+)%',
                'avg_price': r'市场均价为(\d+)元/吨',
                'high_price': r'较高价报价(\d+)元/吨',
                'low_price': r'较低价报价(\d+)元/吨',
            },
            'station': {
                'total': r'(\d+)家国内LNG接收站',
                'avg_price': r'接收站均价为(\d+)元/吨',
                'high': r'较高价是(.*?)报价(\d+)元/吨',
                'low': r'较低价是(.*?)报价(\d+)元/吨',
            },
            'bidding': {
                'start_price': r'起拍价([\d.]+)元/方',
                'price_range': r'成交区间([\d.]+)-([\d.]+)元/方',
                'avg_price': r'均价([\d.]+)元/方',
                'volume': r'成交量(\d+)万方',
            },
            'oil': {
                'nymex': r'NYMEX原油.*?价格指数([\d.]+)',
            }
        }
    
    def parse(self, text: str) -> dict:
        """解析LNG文本内容"""
        
        result = {
            'source': 'LNG物联网',
            'timestamp': datetime.now().isoformat(),
            'report_date': None,
            'factory': {},
            'station': {},
            'bidding': {},
            'oil': {},
        }
        
        # 提取报告日期
        date_match = re.search(self.patterns['report_date'], text)
        if date_match:
            result['report_date'] = date_match.group(1)
        
        # 提取液厂数据
        for key, pattern in self.patterns['factory'].items():
            match = re.search(pattern, text)
            if match:
                result['factory'][key] = match.group(1)
        
        # 提取接收站数据
        for key, pattern in self.patterns['station'].items():
            if key in ['high', 'low']:
                match = re.search(pattern, text)
                if match:
                    result['station'][f'{key}_station'] = match.group(1).strip()
                    result['station'][f'{key}_price'] = match.group(2)
            else:
                match = re.search(pattern, text)
                if match:
                    result['station'][key] = match.group(1)
        
        # 提取原料气竞拍数据
        for key, pattern in self.patterns['bidding'].items():
            match = re.search(pattern, text)
            if match:
                if key == 'price_range':
                    result['bidding'][key] = f"{match.group(1)}-{match.group(2)}"
                else:
                    result['bidding'][key] = match.group(1)
        
        # 提取原油价格
        for key, pattern in self.patterns['oil'].items():
            match = re.search(pattern, text)
            if match:
                result['oil'][key] = match.group(1)
        
        return result
    
    def format_markdown(self, data: dict) -> str:
        """格式化为Markdown报告"""
        
        lines = []
        lines.append("# LNG市场数据报告")
        lines.append(f"**数据来源**: {data['source']}")
        lines.append(f"**报告日期**: {data.get('report_date', 'N/A')}")
        lines.append(f"**抓取时间**: {data['timestamp']}")
        lines.append("")
        
        # 液厂数据
        if data['factory']:
            lines.append("## 国内LNG液厂价格")
            factory = data['factory']
            lines.append(f"| 指标 | 数值 |")
            lines.append(f"|------|------|")
            lines.append(f"| 统计家数 | {factory.get('total', 'N/A')}家 |")
            lines.append(f"| 检修/停产 | {factory.get('maintenance', 'N/A')}家 |")
            lines.append(f"| 开工率 | {factory.get('operating_rate', 'N/A')}% |")
            lines.append(f"| 市场均价 | {factory.get('avg_price', 'N/A')}元/吨 |")
            lines.append(f"| 最高价 | {factory.get('high_price', 'N/A')}元/吨 |")
            lines.append(f"| 最低价 | {factory.get('low_price', 'N/A')}元/吨 |")
            lines.append("")
        
        # 接收站数据
        if data['station']:
            lines.append("## 国内LNG接收站价格")
            station = data['station']
            lines.append(f"| 指标 | 数值 |")
            lines.append(f"|------|------|")
            lines.append(f"| 统计家数 | {station.get('total', 'N/A')}家 |")
            lines.append(f"| 市场均价 | {station.get('avg_price', 'N/A')}元/吨 |")
            if 'high_station' in station:
                lines.append(f"| 最高价 | {station['high_station']} {station.get('high_price', 'N/A')}元/吨 |")
            if 'low_station' in station:
                lines.append(f"| 最低价 | {station['low_station']} {station.get('low_price', 'N/A')}元/吨 |")
            lines.append("")
        
        # 原料气竞拍
        if data['bidding']:
            lines.append("## 原料气竞拍")
            bidding = data['bidding']
            lines.append(f"| 指标 | 数值 |")
            lines.append(f"|------|------|")
            lines.append(f"| 起拍价 | {bidding.get('start_price', 'N/A')}元/方 |")
            lines.append(f"| 成交区间 | {bidding.get('price_range', 'N/A')}元/方 |")
            lines.append(f"| 成交均价 | {bidding.get('avg_price', 'N/A')}元/方 |")
            lines.append(f"| 成交量 | {bidding.get('volume', 'N/A')}万方 |")
            lines.append("")
        
        # 原油价格
        if data['oil']:
            lines.append("## 原油价格")
            oil = data['oil']
            lines.append(f"- NYMEX原油: {oil.get('nymex', 'N/A')}")
            lines.append("")
        
        return "\n".join(lines)


def main():
    """主函数"""
    print("=" * 60)
    print("LNG数据采集工具 - 基于Scrapling/web_fetch")
    print("=" * 60)
    print()
    
    parser = LNGDataParser()
    
    # 解析样本数据
    print("🕷️ 正在解析LNG物联网数据...")
    data = parser.parse(SAMPLE_CONTENT)
    
    # 输出JSON
    print("\n📊 提取的数据 (JSON):")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    # 输出Markdown报告
    print("\n" + "=" * 60)
    print("📄 Markdown报告:")
    print("=" * 60)
    report = parser.format_markdown(data)
    print(report)
    
    # 保存文件
    output_json = f"lng_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_md = f"lng_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n💾 文件已保存:")
    print(f"   - JSON: {output_json}")
    print(f"   - Markdown: {output_md}")


if __name__ == "__main__":
    main()
