# 数据采集技术深化学习总结

> 学习目标：提升网络爬虫、数据清洗、API集成三大核心能力，为LNG数据采集系统提供技术支撑

---

## 一、网络爬虫技术

### 1.1 Scrapy框架基础

#### 核心概念
| 组件 | 功能 | 说明 |
|------|------|------|
| **Spider** | 爬虫逻辑 | 定义如何抓取和解析页面 |
| **Item** | 数据容器 | 存储爬取的结构化数据 |
| **Pipeline** | 数据处理 | 清洗、验证、存储数据 |
| **Middleware** | 中间件 | 处理请求/响应，实现反爬、重试等 |
| **Scheduler** | 调度器 | 管理URL队列，控制爬取顺序 |

#### 基础使用模式
```python
import scrapy

class LNGSpider(scrapy.Spider):
    name = 'lng_spider'
    start_urls = ['https://example.com/lng-prices']
    
    def parse(self, response):
        # CSS选择器提取数据
        for item in response.css('.price-item'):
            yield {
                'date': item.css('.date::text').get(),
                'price': item.css('.price::text').get(),
                'region': item.css('.region::text').get()
            }
        
        # 翻页处理
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
```

#### 关键配置参数
```python
# settings.py
CONCURRENT_REQUESTS = 16          # 并发请求数
DOWNLOAD_DELAY = 1                # 下载延迟（秒）
RETRY_TIMES = 3                   # 重试次数
ROBOTSTXT_OBEY = True             # 遵守robots.txt
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0...'
}
```

### 1.2 反爬虫绕过技术

#### 常见反爬机制与应对

| 反爬机制 | 识别特征 | 应对策略 |
|----------|----------|----------|
| **User-Agent检测** | 返回403/拦截 | 使用真实浏览器UA轮换 |
| **IP频率限制** | 返回429/封禁 | 代理池轮换、降低频率 |
| **Cookie验证** | 需要特定Cookie | 模拟登录、Session保持 |
| **JavaScript挑战** | 页面需要JS执行 | 使用Selenium/Playwright |
| **验证码** | 出现CAPTCHA | 打码平台、机器学习识别 |
| **行为检测** | 鼠标轨迹、点击模式 | 模拟人类行为、随机延迟 |

#### Scrapling框架（推荐）

基于已有技能文档，Scrapling提供了现代化的反爬解决方案：

```python
from scrapling.fetchers import StealthyFetcher

# 自动绕过Cloudflare等反爬
StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    headless=True,
    solve_cloudflare=True
)
```

#### 代理池配置
```python
# 使用代理中间件
class ProxyMiddleware:
    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        request.meta['proxy'] = proxy
        
    def get_random_proxy(self):
        # 从代理池获取
        return random.choice(self.proxy_pool)
```

### 1.3 动态页面抓取

#### 技术选型对比

| 方案 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| **Selenium** | 复杂交互、旧项目 | 生态成熟 | 资源占用高、速度慢 |
| **Playwright** | 现代Web应用 | 速度快、支持多浏览器 | 学习成本 |
| **Scrapy-Splash** | Scrapy集成 | 轻量级 | 功能有限 |
| **Requests-HTML** | 简单JS渲染 | 易用 | 功能有限 |

#### Playwright动态抓取示例
```python
from playwright.sync_api import sync_playwright

def fetch_dynamic_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 拦截API请求（逆向工程）
        page.on('response', handle_response)
        
        page.goto(url, wait_until='networkidle')
        
        # 等待特定元素
        page.wait_for_selector('.data-loaded')
        
        content = page.content()
        browser.close()
        return content
```

#### API逆向工程（高级技巧）
```python
# 从浏览器Network面板发现隐藏API
import requests

headers = {
    'Authorization': 'Bearer token-from-devtools',
    'X-API-Key': 'key-from-js-analysis'
}

# 直接调用内部API，绕过前端渲染
response = requests.get(
    'https://api.example.com/internal/data',
    headers=headers
)
data = response.json()
```

---

## 二、数据清洗技术

### 2.1 Pandas数据处理

#### 核心数据结构
- **Series**: 一维带标签数组
- **DataFrame**: 二维表格数据结构

#### 常用清洗操作

```python
import pandas as pd
import numpy as np

# 1. 数据读取
df = pd.read_csv('lng_data.csv')
df = pd.read_excel('lng_prices.xlsx')
df = pd.read_json('api_response.json')

# 2. 缺失值处理
# 查看缺失值
print(df.isnull().sum())

# 删除缺失值过多的列
df = df.dropna(thresh=len(df)*0.5, axis=1)

# 填充缺失值
df['price'].fillna(df['price'].median(), inplace=True)
df['region'].fillna('Unknown', inplace=True)

# 3. 重复值处理
df.drop_duplicates(subset=['date', 'region'], keep='first', inplace=True)

# 4. 数据类型转换
df['date'] = pd.to_datetime(df['date'])
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['volume'] = df['volume'].astype('int64')

# 5. 字符串处理
df['region'] = df['region'].str.strip().str.upper()
df['price_str'] = df['price_str'].str.replace('$', '').str.replace(',', '')

# 6. 异常值标记
df['is_outlier'] = np.where(
    (df['price'] < df['price'].quantile(0.01)) |
    (df['price'] > df['price'].quantile(0.99)),
    1, 0
)
```

### 2.2 异常值检测算法

#### 统计方法

| 方法 | 原理 | 适用场景 |
|------|------|----------|
| **3σ原则** | 超出均值±3倍标准差为异常 | 正态分布数据 |
| **IQR法** | 超出Q1-1.5IQR或Q3+1.5IQR为异常 | 非正态分布 |
| **Z-Score** | 标准化后的绝对值>3为异常 | 有离群点的数据 |

```python
# IQR法实现
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers

# Z-Score法
from scipy import stats
df['z_score'] = np.abs(stats.zscore(df['price']))
df['is_outlier'] = df['z_score'] > 3
```

#### 机器学习方法

```python
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

# Isolation Forest（孤立森林）
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df['outlier_iso'] = iso_forest.fit_predict(df[['price', 'volume']])
# -1表示异常，1表示正常

# LOF（局部异常因子）
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
df['outlier_lof'] = lof.fit_predict(df[['price', 'volume']])
```

### 2.3 数据标准化方法

#### 标准化 vs 归一化

| 方法 | 公式 | 适用场景 | 特点 |
|------|------|----------|------|
| **Z-Score标准化** | (x-μ)/σ | 数据近似正态分布 | 均值为0，标准差为1 |
| **Min-Max归一化** | (x-min)/(max-min) | 需要固定范围[0,1] | 对异常值敏感 |
| **Robust标准化** | (x-Q1)/(Q3-Q1) | 含大量异常值 | 使用中位数和IQR |
| **对数变换** | log(x) | 右偏分布 | 压缩大值范围 |

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Z-Score标准化
scaler = StandardScaler()
df['price_scaled'] = scaler.fit_transform(df[['price']])

# Min-Max归一化
minmax = MinMaxScaler()
df['price_normalized'] = minmax.fit_transform(df[['price']])

# Robust标准化（抗异常值）
robust = RobustScaler()
df['price_robust'] = robust.fit_transform(df[['price']])

# 对数变换（处理右偏数据）
df['price_log'] = np.log1p(df['price'])  # log1p处理0值
```

---

## 三、API集成技术

### 3.1 RESTful API调用

#### HTTP方法语义

| 方法 | 操作 | 幂等性 | 用途 |
|------|------|--------|------|
| GET | 读取资源 | 是 | 获取数据 |
| POST | 创建资源 | 否 | 提交数据 |
| PUT | 更新资源（完整） | 是 | 替换数据 |
| PATCH | 更新资源（部分） | 否 | 修改部分字段 |
| DELETE | 删除资源 | 是 | 删除数据 |

#### Python调用示例

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 创建带重试机制的Session
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,  # 重试间隔：1s, 2s, 4s
    status_forcelist=[500, 502, 503, 504]
)
session.mount('https://', HTTPAdapter(max_retries=retries))

# GET请求
response = session.get(
    'https://api.example.com/lng/prices',
    params={'start_date': '2024-01-01', 'region': 'Asia'},
    timeout=(5, 30)  # (连接超时, 读取超时)
)
data = response.json()

# POST请求
response = session.post(
    'https://api.example.com/lng/submit',
    json={'price': 12.5, 'date': '2024-01-01'},
    headers={'Content-Type': 'application/json'}
)
```

### 3.2 API认证方式

#### 常见认证方式对比

| 方式 | 安全性 | 复杂度 | 适用场景 |
|------|--------|--------|----------|
| **API Key** | 低 | 简单 | 公开数据服务 |
| **Basic Auth** | 中 | 简单 | 内部系统 |
| **Bearer Token** | 中 | 中等 | 现代Web API |
| **OAuth 2.0** | 高 | 复杂 | 第三方应用授权 |
| **HMAC签名** | 高 | 复杂 | 金融/高安全场景 |

#### 实现示例

```python
# 1. API Key认证
headers = {'X-API-Key': 'your-api-key-here'}
response = requests.get(url, headers=headers)

# 2. Bearer Token认证
headers = {'Authorization': 'Bearer your-access-token'}
response = requests.get(url, headers=headers)

# 3. Basic Auth认证
from requests.auth import HTTPBasicAuth
response = requests.get(url, auth=HTTPBasicAuth('username', 'password'))

# 4. OAuth 2.0认证流程
from requests_oauthlib import OAuth2Session

oauth = OAuth2Session(client_id)
token = oauth.fetch_token(
    token_url='https://oauth.example.com/token',
    client_secret=client_secret,
    authorization_response=callback_url
)
response = oauth.get(protected_url)

# 5. HMAC签名（交易所常用）
import hmac
import hashlib
import time

def generate_signature(secret, params):
    message = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    return hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

timestamp = int(time.time() * 1000)
params = {'timestamp': timestamp, 'symbol': 'LNG'}
signature = generate_signature(api_secret, params)
headers = {'X-Signature': signature}
```

### 3.3 Rate Limit处理

#### 限流策略

| 策略 | 实现方式 | 适用场景 |
|------|----------|----------|
| **固定窗口** | 每N秒允许M次请求 | 简单限流 |
| **滑动窗口** | 基于时间窗口计数 | 更平滑的限流 |
| **令牌桶** | 匀速产生令牌 | 允许突发流量 |
| **漏桶** | 匀速处理请求 | 严格匀速输出 |

#### 实现代码

```python
import time
import threading
from collections import deque

class RateLimiter:
    """令牌桶限流器"""
    
    def __init__(self, rate=10, per=60):
        """
        rate: 每per秒允许的请求数
        per: 时间窗口（秒）
        """
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def acquire(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(self.rate, self.tokens + elapsed * (self.rate / self.per))
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
    
    def wait(self):
        while not self.acquire():
            time.sleep(0.1)

# 使用示例
limiter = RateLimiter(rate=10, per=60)  # 每分钟10次

def api_call_with_rate_limit(url):
    limiter.wait()  # 等待获取令牌
    return requests.get(url)

# 响应头限流处理
response = requests.get(api_url)
remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
reset_time = int(response.headers.get('X-RateLimit-Reset', 0))

if remaining < 5:
    sleep_time = max(0, reset_time - time.time())
    time.sleep(sleep_time)
```

#### 指数退避重试

```python
import random

def exponential_backoff_retry(func, max_retries=5):
    """指数退避重试策略"""
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            
            # 指数退避 + 随机抖动
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time:.2f}s...")
            time.sleep(wait_time)
```

---

## 四、LNG数据采集系统应用方案

### 4.1 可应用的技术点

#### 数据采集层

| 技术点 | 应用场景 | 优先级 |
|--------|----------|--------|
| Scrapy框架 | 多源LNG价格网站批量采集 | 高 |
| Scrapling反爬 | 绕过价格网站反爬机制 | 高 |
| Playwright动态抓取 | 获取JS渲染的价格图表数据 | 中 |
| API逆向工程 | 发现隐藏的数据API端点 | 中 |
| 代理池轮换 | 避免IP被封 | 高 |

#### 数据清洗层

| 技术点 | 应用场景 | 优先级 |
|--------|----------|--------|
| Pandas数据合并 | 多源数据整合对齐 | 高 |
| IQR异常值检测 | 识别异常价格波动 | 高 |
| 时间序列插值 | 填补缺失的价格数据 | 中 |
| Z-Score标准化 | 不同单位价格对比 | 低 |

#### API集成层

| 技术点 | 应用场景 | 优先级 |
|--------|----------|--------|
| RESTful API封装 | 统一数据接口输出 | 高 |
| Bearer Token认证 | 对接第三方数据服务 | 高 |
| 令牌桶限流 | 控制API调用频率 | 中 |
| 指数退避重试 | 提高API调用稳定性 | 中 |

### 4.2 系统架构建议

```
┌─────────────────────────────────────────────────────────────┐
│                    LNG数据采集系统                           │
├─────────────────────────────────────────────────────────────┤
│  采集层                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Scrapy爬虫   │  │ Playwright   │  │ API客户端    │      │
│  │ (静态页面)   │  │ (动态页面)   │  │ (直接对接)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  清洗层                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Pandas处理   │  │ 异常值检测   │  │ 数据标准化   │      │
│  │ (合并/去重)  │  │ (IQR/孤立森林)│  │ (Z-Score)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  存储层                                                      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ 时序数据库   │  │ 关系数据库   │                        │
│  │ (InfluxDB)   │  │ (PostgreSQL) │                        │
│  └──────────────┘  └──────────────┘                        │
├─────────────────────────────────────────────────────────────┤
│  API服务层                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ RESTful API  │  │ 认证中间件   │  │ 限流中间件   │      │
│  │ (FastAPI)    │  │ (JWT/OAuth)  │  │ (令牌桶)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 实施建议

#### 第一阶段：基础搭建（1-2周）
1. **搭建Scrapy项目框架**
   - 创建统一的Item定义
   - 配置Pipeline数据清洗流程
   - 实现基础反爬中间件

2. **开发首批数据源爬虫**
   - 选择2-3个主要LNG价格网站
   - 实现基础价格数据采集
   - 配置定时调度（Scrapyd/Cron）

#### 第二阶段：能力增强（2-3周）
1. **集成Scrapling反爬能力**
   - 替换部分Requests为StealthyFetcher
   - 配置代理池中间件
   - 实现动态页面抓取能力

2. **数据质量体系建设**
   - 实现异常值自动检测
   - 建立数据质量监控指标
   - 设计数据清洗规则引擎

#### 第三阶段：服务化（2周）
1. **API服务开发**
   - 基于FastAPI构建RESTful服务
   - 实现JWT认证机制
   - 集成限流和监控

2. **系统集成测试**
   - 端到端数据流测试
   - 性能压力测试
   - 异常场景演练

#### 关键技术决策

| 决策项 | 建议方案 | 理由 |
|--------|----------|------|
| 爬虫框架 | Scrapy + Scrapling | 成熟生态 + 现代反爬 |
| 动态渲染 | Playwright | 速度快、支持多浏览器 |
| 数据清洗 | Pandas + NumPy | 生态完善、性能优秀 |
| 异常检测 | IQR + 孤立森林 | 简单有效 + ML增强 |
| API框架 | FastAPI | 异步性能、自动文档 |
| 认证方式 | JWT Bearer | 现代标准、无状态 |
| 限流策略 | 令牌桶 | 允许突发、平滑限流 |

---

## 五、学习资源推荐

### 官方文档
- Scrapy: https://docs.scrapy.org/
- Scrapling: https://scrapling.readthedocs.io/
- Pandas: https://pandas.pydata.org/docs/
- FastAPI: https://fastapi.tiangolo.com/

### 实践项目
1. 搭建一个LNG价格监控爬虫
2. 实现数据清洗Pipeline
3. 构建RESTful API服务

---

*文档生成时间: 2026-04-05*
*适用项目: LNG数据采集系统*
