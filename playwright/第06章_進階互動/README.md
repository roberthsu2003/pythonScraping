# 第六章：進階互動

學習更複雜的使用者互動操作。

## 6.1 滑鼠操作

### 懸停（hover）
```python
# 滑鼠懸停
page.hover("button#menu")
page.hover("div.dropdown-trigger")

# 懸停後點擊子選單
page.hover("li.menu-item")
page.click("a.submenu-link")
```

### 拖曳（drag and drop）
```python
# 方法1：使用 drag_and_drop
page.drag_and_drop("#source", "#target")

# 方法2：手動控制
page.hover("#draggable")
page.mouse.down()
page.hover("#droppable")
page.mouse.up()
```

### 雙擊與右鍵點擊
```python
# 雙擊
page.dblclick("div.item")

# 右鍵點擊
page.click("a.link", button="right")

# 中鍵點擊
page.click("a.link", button="middle")
```

---

## 6.2 鍵盤操作

### 按鍵輸入
```python
# 按下單個按鍵
page.keyboard.press("Enter")
page.keyboard.press("Tab")
page.keyboard.press("Escape")

# 輸入文字
page.keyboard.type("Hello World", delay=100)

# 按下並釋放
page.keyboard.down("Shift")
page.keyboard.press("A")
page.keyboard.up("Shift")
```

### 組合鍵
```python
# Ctrl+A（全選）
page.keyboard.press("Control+A")

# Ctrl+C（複製）
page.keyboard.press("Control+C")

# Ctrl+V（貼上）
page.keyboard.press("Control+V")

# Mac 使用 Meta（Command）
page.keyboard.press("Meta+A")
```

### 特殊按鍵
```python
# 方向鍵
page.keyboard.press("ArrowDown")
page.keyboard.press("ArrowUp")

# 功能鍵
page.keyboard.press("F5")  # 重新整理

# Page Down/Up
page.keyboard.press("PageDown")
page.keyboard.press("PageUp")
```

---

## 6.3 滾動操作

### 滾動到元素位置
```python
# 滾動到元素
page.locator("#footer").scroll_into_view_if_needed()

# 滾動到特定元素並點擊
element = page.locator("#bottom-button")
element.scroll_into_view_if_needed()
element.click()
```

### 滾動到頁面底部
```python
# 方法1：使用 JavaScript
page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

# 方法2：使用鍵盤
page.keyboard.press("End")

# 滾動到頂部
page.evaluate("window.scrollTo(0, 0)")
page.keyboard.press("Home")
```

### 處理無限滾動頁面
```python
def scroll_to_load_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/infinite-scroll")
        
        previous_height = 0
        while True:
            # 滾動到底部
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)  # 等待載入
            
            # 檢查是否還有新內容
            current_height = page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                break
            previous_height = current_height
        
        print("已載入所有內容")
        browser.close()
```

---

## 6.4 檔案上傳與下載

### 上傳檔案
```python
# 單檔案上傳
page.set_input_files("input[type='file']", "path/to/file.pdf")

# 多檔案上傳
page.set_input_files("input[type='file']", [
    "file1.jpg",
    "file2.jpg"
])

# 清除已選擇的檔案
page.set_input_files("input[type='file']", [])
```

### 下載檔案並儲存
```python
# 監聽下載事件
with page.expect_download() as download_info:
    page.click("a#download-link")

download = download_info.value

# 儲存檔案
download.save_as("downloaded_file.pdf")

# 取得檔案名稱
print(download.suggested_filename)
```

---

## 完整範例

```python
from playwright.sync_api import sync_playwright

def advanced_interactions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        page.goto("https://example.com")
        
        # 滑鼠懸停
        page.hover("#menu")
        page.wait_for_timeout(1000)
        
        # 鍵盤操作
        page.click("input#search")
        page.keyboard.type("Playwright", delay=100)
        page.keyboard.press("Enter")
        
        # 滾動操作
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        
        # 檔案上傳
        page.set_input_files("input[type='file']", "example.pdf")
        
        browser.close()

if __name__ == "__main__":
    advanced_interactions()
```

---

## 練習題

1. 練習懸停並點擊下拉選單
2. 使用鍵盤快捷鍵操作網頁
3. 實作無限滾動頁面的資料爬取
4. 練習檔案上傳和下載

---

[← 上一章：資料擷取](../第05章_資料擷取/README.md) | [返回目錄](../README.md) | [下一章：多頁面與框架處理 →](../第07章_多頁面與框架處理/README.md)
