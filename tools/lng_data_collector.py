#!/usr/bin/env python3
"""
LNG数据采集工具 - 基于Scrapling
用于抓取LNG物联网、隆众资讯等数据源
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional

# 尝试导入scrapling
try:
    from scrapling.fetchers import Fetcher, StealthyFetcher
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    print("⚠️ Scrapling未安装，使用备用方案")


class LNGDataCollector:
    """LNG数据采集器"""
    
    def __init__(self):
        self.data_sources = {
            'lng168': {
                'name': 'LNG物联网',
                'base_url': 'https://www.lng168.com',
                'reliability': 'A'
            },
            'oilchem': {
                'name': '隆众资讯',
                'base_url': 'https://www.oilchem.net',
                'reliability': 'A'
            },
            'mysteel': {
                'name': 'Mysteel',
                'base_url': 'https://nenghua.m.mysteel.com',
                'reliability': 'B'
            }
        }
    
    def fetch_lng168_news(self, news_id: str = "10906") -> Optional[Dict]:
        """
        抓取LNG物联网价格文章
        
        Args:
            news_id: 文章ID，默认10906（最新价格分析）
            
        Returns:
            提取的价格数据字典
        """
        url = f"https://www.lng168.com/gateWay/newsDetail?id={news_id}"
        
        try:
            if SCRAPLING_AVAILABLE:
                page = Fetcher.get(url, timeout=15)
                text = page.text
            else:
                # 备用方案：使用requests
                import requests
                response = requests.get(url, timeout=15, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                text = response.text
            
            return self._parse_lng168_content(text)
            
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            return None
    
    def _parse_lng168_content(self, text: str) -> Dict:
        """解析LNG物联网文章内容"""
        
        data = {
            'source': 'LNG物联网',
            'timestamp': datetime.now().isoformat(),
            'raw_text': text,
            'extracted_data': {}
        }
        
        # 提取日期
        date_match = re.search(r'【(\d{4}\.\d{1,2}\.\d{1,2})】', text)
        if date_match:
            data['report_date'] = date_match.group(1)
        
        # 提取液厂数据
        factory_pattern = r'(\d+)家国内LNG工厂.*?(\d+)家检修.*?开工率(\d+)%.*?市场均价为(\d+)元/吨'
        factory_match = re.search(factory_pattern, text, re.DOTALL)
        if factory_match:
            data['extracted_data']['液厂'] = {
                '统计家数': int(factory_match.group(1)),
                '检修家数': int(factory_match.group(2)),
                '开工率': f"{factory_match.group(3)}%",
                '市场均价': f"{factory_match.group(4)}元/吨"
            }
        
        # 提取接收站数据
        station_pattern = r'(\d+)家国内LNG接收站均价为(\d+)元/吨.*?较高价是(.*?)报价(\d+)元/吨.*?较低价是(.*?)报价(\d+)元/吨'
        station_match = re.search(station_pattern, text, re.DOTALL)
        if station_match:
            data['extracted_data']['接收站'] = {
                '统计家数': int(station_match.group(1)),
                '市场均价': f"{station_match.group(2)}元/吨",
                '最高价': {
                    '接收站': station_match.group(3).strip(),
                    '价格': f"{station_match.group(4)}元/吨"
                },
                '最低价': {
                    '接收站': station_match.group(5).strip(),
                    '价格': f"{station_match.group(6)}元/吨"
                }
            }
        
        # 提取原料气竞拍数据
        bidding_pattern = r'起拍价([\d.]+)元/方.*?成交区间([\d.]+)-([\d.]+)元/方.*?均价([\d.]+)元/方'
        bidding_match = re.search(bidding_pattern, text, re.DOTALL)
        if bidding_match:
            data['extracted_data']['原料气竞拍'] = {
                '起拍价': f"{bidding_match.group(1)}元/方",
                '成交区间': f"{bidding_match.group(2)}-{bidding_match.group(3)}元/方",
                '成交均价': f"{bidding_match.group(4)}元/方"
            }
        
        # 提取原油价格
        oil_pattern = r'NYMEX原油.*?价格指数([\d.]+)'
        oil_match = re.search(oil_pattern, text)
        if oil_match:
            data['extracted_data']['原油价格'] = {
                'NYMEX': f"{oil_match.group(1)}"
            }
        
        return data
    
    def fetch_latest_prices(self) -> Dict:
        """抓取最新价格数据（综合多个源）"""
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }
        
        # 1. LNG物联网
        print("🕷️ 正在抓取LNG物联网...")
        lng168_data = self.fetch_lng168_news()
        if lng168_data:
            results['sources']['lng168'] = lng168_data
            print("✅ LNG物联网抓取成功")
        else:
            print("❌ LNG物联网抓取失败")
        
        return results
    
    def format_report(self, data: Dict) -> str:
        """格式化数据为报告文本"""
        
        lines = []
        lines.append("# LNG市场数据抓取报告")
        lines.append(f"**抓取时间**: {data['timestamp']}")
        lines.append("")
        
        for source_name, source_data in data.get('sources', {}).items():
            lines.append(f"## {source_data.get('source', source_name)}")
            lines.append(f"**报告日期**: {source_data.get('report_date', 'N/A')}")
            lines.append("")
            
            extracted = source_data.get('extracted_data', {})
            
            # 液厂数据
            if '液厂' in extracted:
                factory = extracted['液厂']
                lines.append("### 液厂数据")
                lines.append(f"- 统计家数: {factory.get('统计家数', 'N/A')}")
                lines.append(f"- 检修家数: {factory.get('检修家数', 'N/A')}")
                lines.append(f"- 开工率: {factory.get('开工率', 'N/A')}")
                lines.append(f"- 市场均价: {factory.get('市场均价', 'N/A')}")
                lines.append("")
            
            # 接收站数据
            if '接收站' in extracted:
                station = extracted['接收站']
                lines.append("### 接收站数据")
                lines.append(f"- 统计家数: {station.get('统计家数', 'N/A')}")
                lines.append(f"- 市场均价: {station.get('市场均价', 'N/A')}")
                if '最高价' in station:
                    lines.append(f"- 最高价: {station['最高价']['接收站']} {station['最高价']['价格']}")
                if '最低价' in station:
                    lines.append(f"- 最低价: {station['最低价']['接收站']} {station['最低价']['价格']}")
                lines.append("")
            
            # 原料气竞拍
            if '原料气竞拍' in extracted:
                bidding = extracted['原料气竞拍']
                lines.append("### 原料气竞拍")
                lines.append(f"- 起拍价: {bidding.get('起拍价', 'N/A')}")
                lines.append(f"- 成交区间: {bidding.get('成交区间', 'N/A')}")
                lines.append(f"- 成交均价: {bidding.get('成交均价', 'N/A')}")
                lines.append("")
            
            # 原油价格
            if '原油价格' in extracted:
                oil = extracted['原油价格']
                lines.append("### 原油价格")
                lines.append(f"- NYMEX: {oil.get('NYMEX', 'N/A')}")
                lines.append("")
        
        return "\n".join(lines)


def main():
    """主函数"""
    print("=" * 50)
    print("LNG数据采集工具 - 基于Scrapling")
    print("=" * 50)
    print()
    
    collector = LNGDataCollector()
    
    # 抓取最新数据
    data = collector.fetch_latest_prices()
    
    # 格式化输出
    report = collector.format_report(data)
    print(report)
    
    # 保存到文件
    output_file = f"lng_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 数据已保存到: {output_file}")


if __name__ == "__main__":
    main()
