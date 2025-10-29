# 第十二章：效能優化

學習如何提升爬蟲的執行效率。

## 12.1 提升爬蟲速度

### 禁用圖片載入
```python
def block_images():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 攔截並阻擋圖片
        def route_handler(route):
            if route.request.resource_type == "image":
                route.abort()
            else:
                route.continue_()
        
        context = browser.new_context()
        page = context.new_page()
        page.route("**/*", route_handler)
        
        page.goto("https://example.com")
        
        context.close()
        browser.close()
```

### 禁用 CSS 和字體載入
```python
def block_resources():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        
        # 阻擋多種資源
        def block_handler(route):
            resource_type = route.request.resource_type
            if resource_type in ["image", "stylesheet", "font"]:
                route.abort()
            else:
                route.continue_()
        
        page.route("**/*", block_handler)
        page.goto("https://example.com")
        
        context.close()
        browser.close()
```

### 完整的資源優化
```python
def optimize_loading():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        context = browser.new_context(
            # 禁用 JavaScript（如果不需要）
            java_script_enabled=True
        )
        
        page = context.new_page()
        
        # 阻擋不必要的資源
        page.route("**/*", lambda route: (
            route.abort() if route.request.resource_type in 
            ["image", "media", "font", "stylesheet"] 
            else route.continue_()
        ))
        
        # 快速載入
        page.goto("https://example.com", wait_until="domcontentloaded")
        
        # 擷取資料
        data = page.inner_text("#content")
        
        context.close()
        browser.close()
```

---

## 12.2 平行處理

### 多個瀏覽器上下文
```python
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor

def scrape_url(url, browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    title = page.title()
    context.close()
    return title

def parallel_scraping():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3"
        ]
        
        # 使用執行緒池
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = executor.map(
                lambda url: scrape_url(url, browser),
                urls
            )
        
        for url, title in zip(urls, results):
            print(f"{url}: {title}")
        
        browser.close()
```

### 多執行緒爬取
```python
from concurrent.futures import ThreadPoolExecutor
import threading

thread_local = threading.local()

def get_browser():
    if not hasattr(thread_local, "browser"):
        from playwright.sync_api import sync_playwright
        thread_local.playwright = sync_playwright().start()
        thread_local.browser = thread_local.playwright.chromium.launch()
    return thread_local.browser

def scrape_page(url):
    browser = get_browser()
    context = browser.new_context()
    page = context.new_page()
    
    page.goto(url)
    title = page.title()
    
    context.close()
    return {"url": url, "title": title}

def multi_threaded_scraping():
    urls = [f"https://example.com/page{i}" for i in range(1, 11)]
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(scrape_page, urls))
    
    for result in results:
        print(f"{result['url']}: {result['title']}")
```

### 批次處理
```python
def batch_processing(urls, batch_size=5):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            
            print(f"處理批次 {i//batch_size + 1}")
            
            for url in batch:
                page = browser.new_page()
                page.goto(url)
                # 處理頁面
                print(page.title())
                page.close()
        
        browser.close()
```

---

## 12.3 資源管理

### 正確關閉瀏覽器
```python
def proper_cleanup():
    playwright = None
    browser = None
    context = None
    page = None
    
    try:
        from playwright.sync_api import sync_playwright
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://example.com")
        # 處理資料
        
    except Exception as e:
        print(f"發生錯誤: {e}")
    
    finally:
        # 依序關閉資源
        if page:
            page.close()
        if context:
            context.close()
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
```

### 記憶體管理
```python
def memory_efficient_scraping(urls):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for url in urls:
            # 每個 URL 使用新的 context
            context = browser.new_context()
            page = context.new_page()
            
            page.goto(url)
            # 處理資料
            data = page.inner_text("#content")
            
            # 立即關閉以釋放記憶體
            page.close()
            context.close()
            
            print(f"已處理: {url}")
        
        browser.close()
```

### 錯誤處理與重試機制
```python
import time

def scrape_with_retry(url, max_retries=3):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        for attempt in range(max_retries):
            try:
                page.goto(url, timeout=30000)
                data = page.inner_text("#content")
                browser.close()
                return data
            
            except Exception as e:
                print(f"嘗試 {attempt + 1} 失敗: {e}")
                
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 指數退避
                    print(f"等待 {wait_time} 秒後重試...")
                    time.sleep(wait_time)
                else:
                    print(f"達到最大重試次數，放棄 {url}")
                    browser.close()
                    return None
```

---

## 完整範例：高效能爬蟲

```python
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
import time

class EfficientScraper:
    def __init__(self, headless=True):
        self.playwright = None
        self.browser = None
        self.headless = headless
    
    def start(self):
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless
        )
    
    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def scrape_page(self, url):
        context = self.browser.new_context()
        page = context.new_page()
        
        # 阻擋不必要的資源
        page.route("**/*", lambda route: (
            route.abort() if route.request.resource_type in 
            ["image", "media", "font"] 
            else route.continue_()
        ))
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # 擷取資料
            title = page.title()
            content = page.inner_text("body")
            
            return {
                "url": url,
                "title": title,
                "content_length": len(content)
            }
        
        except Exception as e:
            print(f"錯誤 ({url}): {e}")
            return None
        
        finally:
            page.close()
            context.close()
    
    def scrape_urls(self, urls, max_workers=5):
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.scrape_page, url) for url in urls]
            
            for future in futures:
                result = future.result()
                if result:
                    results.append(result)
        
        return results

def main():
    urls = [f"https://example.com/page{i}" for i in range(1, 21)]
    
    scraper = EfficientScraper(headless=True)
    scraper.start()
    
    start_time = time.time()
    results = scraper.scrape_urls(urls, max_workers=5)
    end_time = time.time()
    
    print(f"爬取 {len(results)} 個頁面")
    print(f"耗時: {end_time - start_time:.2f} 秒")
    
    scraper.stop()

if __name__ == "__main__":
    main()
```

---

## 效能優化檢查清單

- [ ] 使用無頭模式（headless=True）
- [ ] 阻擋不必要的資源（圖片、CSS、字體）
- [ ] 使用 domcontentloaded 而非完全載入
- [ ] 實作平行處理
- [ ] 正確管理記憶體（及時關閉 page 和 context）
- [ ] 加入錯誤處理和重試機制
- [ ] 控制並發數量
- [ ] 使用批次處理
- [ ] 監控效能指標

---

## 練習題

1. 實作一個阻擋所有圖片的爬蟲
2. 使用多執行緒同時爬取 10 個網頁
3. 比較有/無資源優化的速度差異
4. 實作帶有重試機制的穩定爬蟲

---

[← 上一章：反爬蟲對策](../第11章_反爬蟲對策/README.md) | [返回目錄](../README.md) | [下一章：實戰專案 →](../第13章_實戰專案/README.md)
