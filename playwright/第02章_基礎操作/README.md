# 第二章：基礎操作

## 2.1 啟動瀏覽器

### 同步 vs 異步（sync/async）模式

**同步模式（適合初學者）**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    # 你的程式碼
    browser.close()
```

**異步模式（效能較好）**
```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # 你的程式碼
        await browser.close()

asyncio.run(main())
```

### 啟動 Chromium、Firefox、WebKit

```python
# 啟動 Chromium
browser = p.chromium.launch()

# 啟動 Firefox
browser = p.firefox.launch()

# 啟動 WebKit (Safari 核心)
browser = p.webkit.launch()
```

### 有頭模式 vs 無頭模式（headless）

```python
# 有頭模式（可以看到瀏覽器）
browser = p.chromium.launch(headless=False)

# 無頭模式（背景執行，預設）
browser = p.chromium.launch(headless=True)
```

---

## 2.2 頁面導航

### 開啟網頁：`page.goto()`

```python
# 基本用法
page.goto("https://www.example.com")

# 設定超時時間（毫秒）
page.goto("https://www.example.com", timeout=60000)

# 等待特定狀態
page.goto("https://www.example.com", wait_until="networkidle")
```

**wait_until 選項：**
- `load`：等待 load 事件（預設）
- `domcontentloaded`：等待 DOMContentLoaded 事件
- `networkidle`：等待網路閒置

### 等待頁面載入

```python
# 等待頁面完全載入
page.wait_for_load_state("load")

# 等待網路閒置
page.wait_for_load_state("networkidle")
```

### 頁面刷新與返回

```python
# 刷新頁面
page.reload()

# 返回上一頁
page.go_back()

# 前進下一頁
page.go_forward()
```

---

## 2.3 基本互動操作

### 點擊元素：`click()`

```python
# 點擊元素
page.click("button#submit")

# 雙擊
page.dblclick("div.item")

# 右鍵點擊
page.click("a.link", button="right")
```

### 輸入文字：`fill()` 和 `type()`

```python
# fill() - 快速填入（清除後輸入）
page.fill("input#username", "myusername")

# type() - 模擬鍵盤輸入（逐字輸入）
page.type("input#password", "mypassword", delay=100)
```

### 選擇下拉選單

```python
# 根據 value 選擇
page.select_option("select#country", "tw")

# 根據 label 選擇
page.select_option("select#country", label="Taiwan")

# 選擇多個選項
page.select_option("select#languages", ["python", "javascript"])
```

### 勾選核取方塊與單選按鈕

```python
# 勾選核取方塊
page.check("input#agree")

# 取消勾選
page.uncheck("input#agree")

# 切換狀態
if not page.is_checked("input#agree"):
    page.check("input#agree")
```

---

## 完整範例

```python
from playwright.sync_api import sync_playwright

def basic_operations():
    with sync_playwright() as p:
        # 啟動瀏覽器（有頭模式）
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        # 訪問網站
        page.goto("https://example.com/form")
        
        # 填寫表單
        page.fill("input#name", "張三")
        page.fill("input#email", "zhang@example.com")
        page.select_option("select#country", "Taiwan")
        page.check("input#subscribe")
        
        # 點擊提交按鈕
        page.click("button#submit")
        
        # 等待導航完成
        page.wait_for_load_state("networkidle")
        
        # 關閉瀏覽器
        browser.close()

if __name__ == "__main__":
    basic_operations()
```

---

## 練習題

1. 訪問一個網站並刷新頁面 3 次
2. 填寫一個登入表單（使用測試網站）
3. 練習使用 `fill()` 和 `type()` 的差異
4. 嘗試選擇不同的下拉選單選項

---

[← 上一章：Playwright 簡介](../第01章_Playwright簡介/README.md) | [返回目錄](../README.md) | [下一章：元素定位 →](../第03章_元素定位/README.md)
