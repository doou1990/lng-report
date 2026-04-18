#!/usr/bin/env python3
"""
LNG Market Report Generator - v6.2
报告生成器 - Markdown + HTML 双版本
"""

import json
from datetime import datetime
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, date: str = None):
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.report_date = datetime.now().strftime("%Y年%m月%d日")
        
    def generate_markdown(self, audited_data: Dict, audit_report: Dict) -> str:
        """生成 Markdown 格式报告"""
        
        md = f"""# LNG原油市场日报 ({self.report_date})

> **版本**: v6.2 全自动生成 | **数据质量**: {audit_report['overall_grade']}级 ({audit_report['average_score']}/100)

---

## 📊 数据质量总览

| 等级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| A级（官方API） | {audit_report['by_grade'].get('A', 0)}/19 | {audit_report['by_grade'].get('A', 0)*100//19}% | EIA官方数据 |
| B级（权威网站） | {audit_report['by_grade'].get('B', 0)}/19 | {audit_report['by_grade'].get('B', 0)*100//19}% | TradingView等 |
| C级（单一来源） | {audit_report['by_grade'].get('C', 0)}/19 | {audit_report['by_grade'].get('C', 0)*100//19}% | 未交叉验证 |
| D级（估算/可疑） | {audit_report['by_grade'].get('D', 0)}/19 | {audit_report['by_grade'].get('D', 0)*100//19}% | 估算或可疑 |

**整体评分**: {audit_report['average_score']}/100 | **审核时间**: {audit_report['timestamp'][:19]}

---

## 🛢️ 原油价格

| 指标 | 数值 | 置信度 | 来源 | 备注 |
|------|------|--------|------|------|
| Brent现货 | {self._format_value(audited_data.get('brent_spot'))} | {self._format_grade(audited_data.get('brent_spot'))} | {self._format_source(audited_data.get('brent_spot'))} | {self._format_note(audited_data.get('brent_spot'))} |
| WTI现货 | {self._format_value(audited_data.get('wti_spot'))} | {self._format_grade(audited_data.get('wti_spot'))} | {self._format_source(audited_data.get('wti_spot'))} | {self._format_note(audited_data.get('wti_spot'))} |
| Brent-WTI价差 | {self._calc_spread(audited_data.get('brent_spot'), audited_data.get('wti_spot'))} | - | 计算值 | - |

---

## 🔥 天然气价格

### 国际LNG价格

| 指标 | 数值 | 置信度 | 来源 | 备注 |
|------|------|--------|------|------|
| JKM现货 | {self._format_value(audited_data.get('jkm_spot'))} | {self._format_grade(audited_data.get('jkm_spot'))} | {self._format_source(audited_data.get('jkm_spot'))} | {self._format_note(audited_data.get('jkm_spot'))} |
| TTF现货 | {self._format_value(audited_data.get('ttf_spot'))} | {self._format_grade(audited_data.get('ttf_spot'))} | {self._format_source(audited_data.get('ttf_spot'))} | {self._format_note(audited_data.get('ttf_spot'))} |
| Henry Hub | {self._format_value(audited_data.get('henry_hub'))} | {self._format_grade(audited_data.get('henry_hub'))} | {self._format_source(audited_data.get('henry_hub'))} | {self._format_note(audited_data.get('henry_hub'))} |
| JKM-TTF价差 | {self._calc_spread(audited_data.get('jkm_spot'), audited_data.get('ttf_spot'))} | - | 计算值 | - |

### 期货价格（M1合约）

| 指标 | 数值 | 置信度 | 来源 | 备注 |
|------|------|--------|------|------|
| Brent期货M1 | {self._format_value(audited_data.get('brent_futures_m1'))} | {self._format_grade(audited_data.get('brent_futures_m1'))} | {self._format_source(audited_data.get('brent_futures_m1'))} | - |
| JKM期货M1 | {self._format_value(audited_data.get('jkm_futures_m1'))} | {self._format_grade(audited_data.get('jkm_futures_m1'))} | {self._format_source(audited_data.get('jkm_futures_m1'))} | - |
| TTF期货M1 | {self._format_value(audited_data.get('ttf_futures_m1'))} | {self._format_grade(audited_data.get('ttf_futures_m1'))} | {self._format_source(audited_data.get('ttf_futures_m1'))} | - |
| Henry Hub期货M1 | {self._format_value(audited_data.get('hh_futures_m1'))} | {self._format_grade(audited_data.get('hh_futures_m1'))} | {self._format_source(audited_data.get('hh_futures_m1'))} | - |

---

## 📦 库存数据

| 地区 | 库存水平 | 置信度 | 来源 | 备注 |
|------|----------|--------|------|------|
| 美国 | {self._format_value(audited_data.get('us_storage'))} | {self._format_grade(audited_data.get('us_storage'))} | {self._format_source(audited_data.get('us_storage'))} | {self._format_note(audited_data.get('us_storage'))} |
| 欧洲 | {self._format_value(audited_data.get('eu_storage'))} | {self._format_grade(audited_data.get('eu_storage'))} | {self._format_source(audited_data.get('eu_storage'))} | {self._format_note(audited_data.get('eu_storage'))} |
| 中国 | {self._format_value(audited_data.get('cn_storage'))} | {self._format_grade(audited_data.get('cn_storage'))} | {self._format_source(audited_data.get('cn_storage'))} | {self._format_note(audited_data.get('cn_storage'))} |

---

## 🇨🇳 国内市场

### 全国LNG价格

| 指标 | 数值 | 置信度 | 来源 | 备注 |
|------|------|--------|------|------|
| 全国出厂均价 | {self._format_value(audited_data.get('cn_lng_factory'))} | {self._format_grade(audited_data.get('cn_lng_factory'))} | {self._format_source(audited_data.get('cn_lng_factory'))} | {self._format_note(audited_data.get('cn_lng_factory'))} |

### 浙江专区

| 接收站 | 价格 | 置信度 | 来源 | 备注 |
|--------|------|--------|------|------|
| 宁波 | {self._format_value(audited_data.get('zhejiang_ningbo'))} | {self._format_grade(audited_data.get('zhejiang_ningbo'))} | {self._format_source(audited_data.get('zhejiang_ningbo'))} | {self._format_note(audited_data.get('zhejiang_ningbo'))} |
| 舟山 | {self._format_value(audited_data.get('zhejiang_zhoushan'))} | {self._format_grade(audited_data.get('zhejiang_zhoushan'))} | {self._format_source(audited_data.get('zhejiang_zhoushan'))} | {self._format_note(audited_data.get('zhejiang_zhoushan'))} |
| 温州 | {self._format_value(audited_data.get('zhejiang_wenzhou'))} | {self._format_grade(audited_data.get('zhejiang_wenzhou'))} | {self._format_source(audited_data.get('zhejiang_wenzhou'))} | {self._format_note(audited_data.get('zhejiang_wenzhou'))} |

---

## 📈 贸易数据

| 指标 | 数值 | 置信度 | 来源 | 备注 |
|------|------|--------|------|------|
| 美国LNG出口 | {self._format_value(audited_data.get('us_lng_export'))} | {self._format_grade(audited_data.get('us_lng_export'))} | {self._format_source(audited_data.get('us_lng_export'))} | {self._format_note(audited_data.get('us_lng_export'))} |
| 中国LNG进口 | {self._format_value(audited_data.get('cn_lng_import'))} | {self._format_grade(audited_data.get('cn_lng_import'))} | {self._format_source(audited_data.get('cn_lng_import'))} | {self._format_note(audited_data.get('cn_lng_import'))} |

---

## ⚠️ 数据警告

"""
        
        # 添加警告信息
        if audit_report.get('warnings'):
            for warning in audit_report['warnings']:
                md += f"- **{warning['severity'].upper()}**: {warning['message']}\n"
        else:
            md += "无异常警告\n"
        
        md += f"""

---

## 📝 数据来源说明

- **A级**: EIA API等官方数据源，高可信度
- **B级**: TradingView/Global LNG Hub等权威网站
- **C级**: 单一来源或行业网站，未交叉验证
- **D级**: 估算值或数据缺失，仅供参考

---

*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*  
*架构版本: v6.2 全自动主会话版*
"""
        
        return md
    
    def generate_html(self, audited_data: Dict, audit_report: Dict) -> str:
        """生成 HTML 格式报告"""
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LNG原油市场日报 - {self.report_date}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #0066cc; padding-bottom: 10px; }}
        h2 {{ color: #333; margin-top: 30px; border-left: 4px solid #0066cc; padding-left: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px; }}
        th {{ background: #0066cc; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9fa; }}
        .grade-A {{ color: #28a745; font-weight: bold; }}
        .grade-B {{ color: #17a2b8; font-weight: bold; }}
        .grade-C {{ color: #ffc107; font-weight: bold; }}
        .grade-D {{ color: #dc3545; font-weight: bold; }}
        .summary {{ background: #f8f9fa; padding: 15px; border-radius: 6px; margin: 20px 0; }}
        .warning {{ background: #fff3cd; border: 1px solid #ffc107; padding: 10px; border-radius: 4px; margin: 10px 0; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛢️ LNG原油市场日报</h1>
        <p style="color: #666;">{self.report_date} | 版本: v6.2 全自动生成</p>
        
        <div class="summary">
            <h3>📊 数据质量总览</h3>
            <p><strong>整体评分</strong>: <span class="grade-{audit_report['overall_grade']}">{audit_report['overall_grade']}级 ({audit_report['average_score']}/100)</span></p>
            <table>
                <tr>
                    <th>等级</th>
                    <th>数量</th>
                    <th>占比</th>
                    <th>说明</th>
                </tr>
                <tr><td><span class="grade-A">A级</span></td><td>{audit_report['by_grade'].get('A', 0)}/19</td><td>{audit_report['by_grade'].get('A', 0)*100//19}%</td><td>官方API数据</td></tr>
                <tr><td><span class="grade-B">B级</span></td><td>{audit_report['by_grade'].get('B', 0)}/19</td><td>{audit_report['by_grade'].get('B', 0)*100//19}%</td><td>权威网站数据</td></tr>
                <tr><td><span class="grade-C">C级</span></td><td>{audit_report['by_grade'].get('C', 0)}/19</td><td>{audit_report['by_grade'].get('C', 0)*100//19}%</td><td>单一来源</td></tr>
                <tr><td><span class="grade-D">D级</span></td><td>{audit_report['by_grade'].get('D', 0)}/19</td><td>{audit_report['by_grade'].get('D', 0)*100//19}%</td><td>估算/可疑</td></tr>
            </table>
        </div>

        <h2>🛢️ 原油价格</h2>
        <table>
            <tr><th>指标</th><th>数值</th><th>置信度</th><th>来源</th><th>备注</th></tr>
            <tr>
                <td>Brent现货</td>
                <td>{self._format_value(audited_data.get('brent_spot'))}</td>
                <td class="grade-{audited_data.get('brent_spot', {}).get('grade', 'D')}">{audited_data.get('brent_spot', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('brent_spot'))}</td>
                <td>{self._format_note(audited_data.get('brent_spot'))}</td>
            </tr>
            <tr>
                <td>WTI现货</td>
                <td>{self._format_value(audited_data.get('wti_spot'))}</td>
                <td class="grade-{audited_data.get('wti_spot', {}).get('grade', 'D')}">{audited_data.get('wti_spot', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('wti_spot'))}</td>
                <td>{self._format_note(audited_data.get('wti_spot'))}</td>
            </tr>
        </table>

        <h2>🔥 天然气价格</h2>
        <table>
            <tr><th>指标</th><th>数值</th><th>置信度</th><th>来源</th><th>备注</th></tr>
            <tr>
                <td>JKM现货</td>
                <td>{self._format_value(audited_data.get('jkm_spot'))}</td>
                <td class="grade-{audited_data.get('jkm_spot', {}).get('grade', 'D')}">{audited_data.get('jkm_spot', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('jkm_spot'))}</td>
                <td>{self._format_note(audited_data.get('jkm_spot'))}</td>
            </tr>
            <tr>
                <td>TTF现货</td>
                <td>{self._format_value(audited_data.get('ttf_spot'))}</td>
                <td class="grade-{audited_data.get('ttf_spot', {}).get('grade', 'D')}">{audited_data.get('ttf_spot', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('ttf_spot'))}</td>
                <td>{self._format_note(audited_data.get('ttf_spot'))}</td>
            </tr>
            <tr>
                <td>Henry Hub</td>
                <td>{self._format_value(audited_data.get('henry_hub'))}</td>
                <td class="grade-{audited_data.get('henry_hub', {}).get('grade', 'D')}">{audited_data.get('henry_hub', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('henry_hub'))}</td>
                <td>{self._format_note(audited_data.get('henry_hub'))}</td>
            </tr>
        </table>

        <h2>📦 库存数据</h2>
        <table>
            <tr><th>地区</th><th>库存水平</th><th>置信度</th><th>来源</th><th>备注</th></tr>
            <tr>
                <td>美国</td>
                <td>{self._format_value(audited_data.get('us_storage'))}</td>
                <td class="grade-{audited_data.get('us_storage', {}).get('grade', 'D')}">{audited_data.get('us_storage', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('us_storage'))}</td>
                <td>{self._format_note(audited_data.get('us_storage'))}</td>
            </tr>
            <tr>
                <td>欧洲</td>
                <td>{self._format_value(audited_data.get('eu_storage'))}</td>
                <td class="grade-{audited_data.get('eu_storage', {}).get('grade', 'D')}">{audited_data.get('eu_storage', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('eu_storage'))}</td>
                <td>{self._format_note(audited_data.get('eu_storage'))}</td>
            </tr>
        </table>

        <h2>🇨🇳 浙江专区</h2>
        <table>
            <tr><th>接收站</th><th>价格</th><th>置信度</th><th>来源</th><th>备注</th></tr>
            <tr>
                <td>宁波</td>
                <td>{self._format_value(audited_data.get('zhejiang_ningbo'))}</td>
                <td class="grade-{audited_data.get('zhejiang_ningbo', {}).get('grade', 'D')}">{audited_data.get('zhejiang_ningbo', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('zhejiang_ningbo'))}</td>
                <td>{self._format_note(audited_data.get('zhejiang_ningbo'))}</td>
            </tr>
            <tr>
                <td>舟山</td>
                <td>{self._format_value(audited_data.get('zhejiang_zhoushan'))}</td>
                <td class="grade-{audited_data.get('zhejiang_zhoushan', {}).get('grade', 'D')}">{audited_data.get('zhejiang_zhoushan', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('zhejiang_zhoushan'))}</td>
                <td>{self._format_note(audited_data.get('zhejiang_zhoushan'))}</td>
            </tr>
            <tr>
                <td>温州</td>
                <td>{self._format_value(audited_data.get('zhejiang_wenzhou'))}</td>
                <td class="grade-{audited_data.get('zhejiang_wenzhou', {}).get('grade', 'D')}">{audited_data.get('zhejiang_wenzhou', {}).get('grade', 'D')}</td>
                <td>{self._format_source(audited_data.get('zhejiang_wenzhou'))}</td>
                <td>{self._format_note(audited_data.get('zhejiang_wenzhou'))}</td>
            </tr>
        </table>

        <div class="footer">
            <p>报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>架构版本: v6.2 全自动主会话版</p>
            <p>数据等级说明: A级(官方API) > B级(权威网站) > C级(单一来源) > D级(估算/可疑)</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _format_value(self, data: Dict) -> str:
        """格式化数值"""
        if not data or data.get("value") is None:
            return "N/A"
        val = data.get("value")
        unit = data.get("unit", "")
        if isinstance(val, (int, float)):
            return f"{val:.2f} {unit}".strip()
        return str(val)
    
    def _format_grade(self, data: Dict) -> str:
        """格式化等级"""
        if not data:
            return "D"
        return data.get("grade", "D")
    
    def _format_source(self, data: Dict) -> str:
        """格式化来源"""
        if not data:
            return "-"
        return data.get("source", "-")
    
    def _format_note(self, data: Dict) -> str:
        """格式化备注"""
        if not data:
            return "-"
        note = data.get("note", "")
        issues = data.get("issues", [])
        if issues:
            note += "; " + "; ".join(issues)
        return note if note else "-"
    
    def _calc_spread(self, data1: Dict, data2: Dict) -> str:
        """计算价差"""
        if not data1 or not data2:
            return "N/A"
        val1 = data1.get("value")
        val2 = data2.get("value")
        if val1 is None or val2 is None:
            return "N/A"
        try:
            spread = float(val1) - float(val2)
            return f"{spread:.2f}"
        except:
            return "N/A"


if __name__ == "__main__":
    # 测试用例
    generator = ReportGenerator()
    
    test_data = {
        "brent_spot": {"value": 85.4, "grade": "A", "source": "EIA API", "unit": "$/barrel"},
        "wti_spot": {"value": 82.1, "grade": "A", "source": "EIA API", "unit": "$/barrel"},
        "jkm_spot": {"value": 12.5, "grade": "B", "source": "TradingView", "unit": "$/MMBtu"},
        "eu_storage": {"value": "58%", "grade": "D", "source": "估算", "note": "AGSI API失效"}
    }
    
    test_audit = {
        "overall_grade": "B",
        "average_score": 78.5,
        "by_grade": {"A": 8, "B": 6, "C": 3, "D": 2},
        "timestamp": "2026-04-12T12:00:00"
    }
    
    md = generator.generate_markdown(test_data, test_audit)
    html = generator.generate_html(test_data, test_audit)
    
    print("Markdown报告生成成功")
    print("HTML报告生成成功")
