# 第十一章：反爬蟲對策

了解常見的反爬蟲機制並學習應對策略。

## 11.1 常見的反爬蟲機制

### User-Agent 檢測
網站會檢查請求的 User-Agent，阻擋明顯的爬蟲工具。

### IP 限制
- 頻率限制（Rate Limiting）
- IP 封鎖
- 地理位置限制

### JavaScript 挑戰
- 需要執行 JavaScript 才能顯示內容
- CAPTCHA 驗證碼
- 指紋識別（Fingerprinting）

---

## 11.2 應對策略

### 設定 User-Agent
```python
from playwright.sync_api import sync_playwright

def set_user_agent():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 設定自訂 User-Agent
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        page = context.new_page()
        page.goto("https://example.com")
        
        context.close()
        browser.close()
```

### 使用代理伺服器
```python
def use_proxy():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 設定代理
        context = browser.new_context(
            proxy={
                "server": "http://proxy-server:8080",
                "username": "user",
                "password": "pass"
            }
        )
        
        page = context.new_page()
        page.goto("https://example.com")
        
        context.close()
        browser.close()
```

### 控制請求速度
```python
import random
import time

def crawl_with_delay():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3"
        ]
        
        for url in urls:
            page.goto(url)
            
            # 擷取資料
            print(page.title())
            
            # 隨機延遲 2-5 秒
            delay = random.uniform(2, 5)
            print(f"等待 {delay:.2f} 秒...")
            time.sleep(delay)
        
        browser.close()
```

---

## 11.3 模擬真實使用者行為

### 隨機延遲
```python
import random

def random_delay():
    # 隨機等待時間
    delay = random.uniform(1, 3)
    page.wait_for_timeout(int(delay * 1000))
```

### 滑鼠軌跡模擬
```python
def simulate_human_behavior(page):
    # 隨機滾動
    scroll_height = random.randint(300, 800)
    page.evaluate(f"window.scrollBy(0, {scroll_height})")
    page.wait_for_timeout(random.randint(500, 1500))
    
    # 隨機移動滑鼠
    page.mouse.move(
        random.randint(100, 500),
        random.randint(100, 500)
    )
    page.wait_for_timeout(random.randint(200, 800))
    
    # 模擬閱讀時間
    page.wait_for_timeout(random.randint(3000, 8000))
```

### 視窗大小設定
```python
def set_realistic_viewport():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 設定常見的螢幕解析度
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        page.goto("https://example.com")
        
        context.close()
        browser.close()
```

---

## 完整範例：綜合反爬蟲策略

```python
from playwright.sync_api import sync_playwright
import random
import time

def stealth_scraper():
    with sync_playwright() as p:
        # 使用真實的瀏覽器設定
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        context = browser.new_context(
            # 真實的 User-Agent
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            
            # 常見的視窗大小
            viewport={'width': 1920, 'height': 1080},
            
            # 語言和時區
            locale='zh-TW',
            timezone_id='Asia/Taipei',
            
            # 允許地理位置
            geolocation={'longitude': 121.5654, 'latitude': 25.0330},
            permissions=['geolocation']
        )
        
        page = context.new_page()
        
        # 隱藏 WebDriver 特徵
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        # 訪問網站
        page.goto("https://example.com")
        
        # 模擬人類行為
        # 1. 隨機滾動
        for _ in range(random.randint(2, 4)):
            scroll = random.randint(300, 800)
            page.evaluate(f"window.scrollBy(0, {scroll})")
            time.sleep(random.uniform(0.5, 1.5))
        
        # 2. 移動滑鼠
        page.mouse.move(random.randint(100, 500), random.randint(100, 500))
        time.sleep(random.uniform(0.3, 0.8))
        
        # 3. 模擬閱讀時間
        time.sleep(random.uniform(3, 6))
        
        # 擷取資料
        data = page.locator("#content").inner_text()
        print(data)
        
        context.close()
        browser.close()

if __name__ == "__main__":
    stealth_scraper()
```

---

## 進階技巧

### 隨機化請求參數
```python
def randomize_requests():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) Firefox/120.0'
    ]
    
    viewports = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1440, 'height': 900}
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        context = browser.new_context(
            user_agent=random.choice(user_agents),
            viewport=random.choice(viewports)
        )
        
        page = context.new_page()
        page.goto("https://example.com")
        
        context.close()
        browser.close()
```

### 處理 CAPTCHA
```python
def handle_captcha():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://example.com")
        
        # 檢查是否有 CAPTCHA
        if page.locator("#captcha").is_visible():
            print("偵測到 CAPTCHA，請手動完成驗證")
            
            # 等待用戶完成 CAPTCHA
            page.wait_for_selector("#captcha", state="hidden", timeout=120000)
            print("CAPTCHA 已完成")
        
        # 繼續操作
        page.click("button#submit")
        
        browser.close()
```

---

## 倫理與法律

### 重要提醒

1. **遵守 robots.txt** - 尊重網站的爬蟲政策
2. **控制請求頻率** - 不要對伺服器造成負擔
3. **尊重版權** - 不要盜用內容
4. **遵守使用條款** - 閱讀並遵守網站的服務條款
5. **合理使用** - 僅用於合法目的

### 檢查 robots.txt
```python
def check_robots_txt():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 檢查 robots.txt
        page.goto("https://example.com/robots.txt")
        robots_txt = page.content()
        print(robots_txt)
        
        browser.close()
```

---

## 練習題

1. 設定多個 User-Agent 並隨機使用
2. 實作隨機延遲的爬蟲
3. 模擬真實使用者的瀏覽行為
4. 研究一個網站的 robots.txt

---

[← 上一章：登入與Cookie處理](../第10章_登入與Cookie處理/README.md) | [返回目錄](../README.md) | [下一章：效能優化 →](../第12章_效能優化/README.md)
