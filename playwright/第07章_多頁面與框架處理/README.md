# 第七章：多頁面與框架處理

處理多個分頁、彈出視窗和 iframe。

## 7.1 處理多個分頁

### 開啟新分頁
```python
# 方法1：在新分頁中開啟連結
with page.expect_popup() as popup_info:
    page.click("a[target='_blank']")
new_page = popup_info.value

# 方法2：手動建立新分頁
new_page = context.new_page()
new_page.goto("https://example.com")
```

### 切換分頁
```python
# 取得所有分頁
pages = context.pages

# 切換到特定分頁
pages[0].bring_to_front()
pages[1].bring_to_front()

# 在不同分頁操作
for page in pages:
    print(page.title())
```

### 關閉分頁
```python
# 關閉特定分頁
new_page.close()

# 關閉所有分頁（除了第一個）
for page in context.pages[1:]:
    page.close()
```

---

## 7.2 處理彈出視窗

### 監聽彈出視窗
```python
# 處理新視窗
with page.expect_popup() as popup_info:
    page.click("button#open-window")
popup = popup_info.value
popup.wait_for_load_state()
print(popup.title())
popup.close()
```

### 處理 alert、confirm、prompt
```python
# 處理 alert
page.on("dialog", lambda dialog: dialog.accept())
page.click("button#show-alert")

# 處理 confirm（確認/取消）
def handle_confirm(dialog):
    print(dialog.message)
    dialog.accept()  # 或 dialog.dismiss()

page.on("dialog", handle_confirm)
page.click("button#show-confirm")

# 處理 prompt（輸入文字）
def handle_prompt(dialog):
    dialog.accept("我的輸入")

page.on("dialog", handle_prompt)
page.click("button#show-prompt")
```

---

## 7.3 處理 iframe

### 切換到 iframe
```python
# 方法1：使用 frame_locator
frame = page.frame_locator("iframe#my-frame")
frame.locator("button").click()

# 方法2：取得 frame 物件
iframe = page.frame("frame-name")
iframe.click("button")

# 方法3：使用選擇器
iframe = page.frame_locator("css=iframe").first
iframe.locator("input").fill("text")
```

### 在 iframe 中操作元素
```python
# 定位 iframe 內的元素
page.frame_locator("iframe").locator("button#submit").click()

# 鏈式操作
page.frame_locator("iframe#outer") \
    .frame_locator("iframe#inner") \
    .locator("button").click()
```

---

## 7.4 實作：處理多視窗網站

```python
from playwright.sync_api import sync_playwright

def handle_multiple_windows():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://example.com")
        
        # 點擊會開啟新視窗的連結
        with page.expect_popup() as popup_info:
            page.click("a#open-new-window")
        
        # 取得新視窗
        new_window = popup_info.value
        new_window.wait_for_load_state()
        
        # 在新視窗操作
        print(f"新視窗標題: {new_window.title()}")
        new_window.click("button#action")
        
        # 切回原視窗
        page.bring_to_front()
        page.click("button#main-action")
        
        # 關閉新視窗
        new_window.close()
        
        context.close()
        browser.close()

if __name__ == "__main__":
    handle_multiple_windows()
```

---

## 完整範例：處理 iframe

```python
from playwright.sync_api import sync_playwright

def handle_iframe():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://example.com/page-with-iframe")
        
        # 在 iframe 中填寫表單
        iframe = page.frame_locator("iframe#form-iframe")
        iframe.locator("input#name").fill("張三")
        iframe.locator("input#email").fill("zhang@example.com")
        iframe.locator("button#submit").click()
        
        # 回到主頁面
        page.locator("button#main-page-button").click()
        
        browser.close()

if __name__ == "__main__":
    handle_iframe()
```

---

## 練習題

1. 開啟多個分頁並在不同分頁間切換
2. 處理會彈出新視窗的連結
3. 練習處理 alert、confirm、prompt
4. 在 iframe 中填寫表單並提交

---

[← 上一章：進階互動](../第06章_進階互動/README.md) | [返回目錄](../README.md) | [下一章：截圖與錄影 →](../第08章_截圖與錄影/README.md)
