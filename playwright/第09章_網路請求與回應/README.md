# 第九章：網路請求與回應

學習如何攔截、監聽和修改網路請求。

## 9.1 監聽網路請求

### 攔截 API 請求
```python
# 監聽所有請求
page.on("request", lambda request: print(f"請求: {request.url}"))

# 監聽特定請求
page.on("request", lambda request: 
    print(f"API: {request.url}") if "/api/" in request.url else None
)
```

### 查看請求內容
```python
def print_request_details(request):
    print(f"URL: {request.url}")
    print(f"方法: {request.method}")
    print(f"標頭: {request.headers}")
    if request.post_data:
        print(f"POST 資料: {request.post_data}")

page.on("request", print_request_details)
page.goto("https://example.com")
```

---

## 9.2 模擬網路回應

### Mock API 回應
```python
# 攔截並修改回應
def handle_route(route):
    if "/api/users" in route.request.url:
        # 回傳假資料
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"users": [{"id": 1, "name": "測試用戶"}]}'
        )
    else:
        route.continue_()

page.route("**/*", handle_route)
page.goto("https://example.com")
```

### 修改回應內容
```python
# 攔截圖片請求
def block_images(route):
    if route.request.resource_type == "image":
        route.abort()  # 阻止圖片載入
    else:
        route.continue_()

page.route("**/*", block_images)
```

---

## 9.3 處理 AJAX 請求

### 等待特定 API 完成
```python
# 等待 API 回應
with page.expect_response("**/api/data") as response_info:
    page.click("button#load-data")

response = response_info.value
print(f"狀態碼: {response.status}")
print(f"回應: {response.text()}")
```

### 獲取 API 回應資料
```python
import json

def get_api_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 監聽 API 回應
        def handle_response(response):
            if "/api/products" in response.url:
                data = response.json()
                print(f"商品數量: {len(data)}")
                # 處理資料
                for product in data:
                    print(f"- {product['name']}: ${product['price']}")
        
        page.on("response", handle_response)
        
        # 觸發 API 請求
        page.goto("https://example-shop.com")
        page.wait_for_load_state("networkidle")
        
        browser.close()
```

---

## 9.4 實作：抓取動態載入的資料

### 範例：擷取 AJAX 載入的商品資料

```python
from playwright.sync_api import sync_playwright
import json

def scrape_ajax_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        products = []
        
        # 監聽 API 回應
        def capture_api_response(response):
            if "/api/products" in response.url and response.status == 200:
                try:
                    data = response.json()
                    products.extend(data)
                    print(f"擷取到 {len(data)} 個商品")
                except:
                    pass
        
        page.on("response", capture_api_response)
        
        # 訪問網站
        page.goto("https://example-shop.com")
        page.wait_for_load_state("networkidle")
        
        # 滾動載入更多
        for _ in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
        
        # 儲存資料
        with open("products_from_api.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        print(f"總共擷取 {len(products)} 個商品")
        
        browser.close()

if __name__ == "__main__":
    scrape_ajax_data()
```

---

## 完整範例：攔截和記錄所有 API 請求

```python
from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def monitor_api_calls():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        api_calls = []
        
        # 記錄所有請求
        def log_request(request):
            if "/api/" in request.url:
                api_calls.append({
                    "timestamp": datetime.now().isoformat(),
                    "method": request.method,
                    "url": request.url,
                    "headers": dict(request.headers),
                    "post_data": request.post_data
                })
        
        # 記錄所有回應
        def log_response(response):
            if "/api/" in response.url:
                for call in api_calls:
                    if call["url"] == response.url:
                        call["status"] = response.status
                        try:
                            call["response"] = response.json()
                        except:
                            call["response"] = response.text()
                        break
        
        page.on("request", log_request)
        page.on("response", log_response)
        
        # 執行操作
        page.goto("https://example.com")
        page.click("button#load-data")
        page.wait_for_load_state("networkidle")
        
        # 儲存 API 記錄
        with open("api_log.json", "w", encoding="utf-8") as f:
            json.dump(api_calls, f, ensure_ascii=False, indent=2)
        
        print(f"記錄了 {len(api_calls)} 個 API 呼叫")
        
        browser.close()

if __name__ == "__main__":
    monitor_api_calls()
```

---

## 實用技巧

### 阻擋特定資源以提升速度
```python
def block_resources(route):
    # 阻擋圖片、字體、樣式表
    resource_type = route.request.resource_type
    if resource_type in ["image", "font", "stylesheet"]:
        route.abort()
    else:
        route.continue_()

page.route("**/*", block_resources)
```

### 修改請求標頭
```python
def modify_headers(route):
    headers = route.request.headers
    headers["Custom-Header"] = "MyValue"
    route.continue_(headers=headers)

page.route("**/*", modify_headers)
```

---

## 練習題

1. 監聽並記錄一個網站的所有 API 請求
2. 攔截特定 API 並回傳假資料
3. 阻擋圖片載入以提升爬蟲速度
4. 擷取 AJAX 動態載入的資料

---

[← 上一章：截圖與錄影](../第08章_截圖與錄影/README.md) | [返回目錄](../README.md) | [下一章：登入與Cookie處理 →](../第10章_登入與Cookie處理/README.md)
