#!/usr/bin/env python3
"""
GIE API 状态检查工具
用于诊断 API 密钥状态和连接问题
"""

import requests
import sys
from datetime import datetime

API_KEY = "3e9a0844c1e529e1dd2119c1cca209e6"
ACCOUNT_EMAIL = "285823779@qq.com"
BASE_URL = "https://agsi.gie.eu/api"

def check_api_status():
    """检查 API 状态"""
    print("=" * 60)
    print("GIE AGSI API 状态检查")
    print("=" * 60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API 密钥: {API_KEY[:8]}...{API_KEY[-8:]}")
    print(f"关联账户: {ACCOUNT_EMAIL}")
    print()
    
    # 测试 1: 检查欧盟数据
    print("[测试 1] 获取欧盟库存数据...")
    try:
        url = f"{BASE_URL}/eu?api_key={API_KEY}"
        response = requests.get(url, timeout=30)
        data = response.json()
        
        if data.get("error"):
            print(f"  ❌ 失败: {data.get('message', 'Unknown error')}")
            print(f"  状态码: {response.status_code}")
        else:
            print(f"  ✅ 成功!")
            print(f"  数据日期: {data.get('gas_day', 'N/A')}")
            if data.get('data'):
                eu_data = data['data'][0]
                print(f"  填充率: {eu_data.get('full', 'N/A')}%")
                print(f"  库存量: {eu_data.get('gasInStorage', 'N/A')} TWh")
    except Exception as e:
        print(f"  ❌ 异常: {str(e)}")
    
    print()
    
    # 测试 2: 检查德国数据
    print("[测试 2] 获取德国库存数据...")
    try:
        url = f"{BASE_URL}/de?api_key={API_KEY}"
        response = requests.get(url, timeout=30)
        data = response.json()
        
        if data.get("error"):
            print(f"  ❌ 失败: {data.get('message', 'Unknown error')}")
        else:
            print(f"  ✅ 成功!")
    except Exception as e:
        print(f"  ❌ 异常: {str(e)}")
    
    print()
    
    # 测试 3: 检查网站可访问性
    print("[测试 3] 检查 GIE 网站可访问性...")
    try:
        response = requests.get("https://agsi.gie.eu", timeout=30)
        if response.status_code == 200:
            print(f"  ✅ 网站可访问 (状态码: {response.status_code})")
        else:
            print(f"  ⚠️ 网站返回异常状态码: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 无法访问网站: {str(e)}")
    
    print()
    print("=" * 60)
    print("诊断建议:")
    print("=" * 60)
    print("1. 检查邮箱 (285823779@qq.com) 是否收到验证邮件")
    print("2. 登录 https://agsi.gie.eu/account 查看账户状态")
    print("3. 确认 API 密钥已正确关联到账户")
    print("4. 如果刚注册，可能需要等待几分钟到几小时激活")
    print("5. 联系 GIE 支持: https://agsi.gie.eu/contact")
    print("=" * 60)

if __name__ == "__main__":
    check_api_status()
