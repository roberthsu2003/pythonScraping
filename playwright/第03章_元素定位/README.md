# 第三章：元素定位

元素定位是網頁自動化的核心技能。本章將學習多種定位元素的方法。

## 3.1 CSS 選擇器

### 基本 CSS 選擇器語法

```python
# 標籤選擇器
page.click("button")

# ID 選擇器
page.click("#submit-btn")

# 類別選擇器
page.click(".primary-button")

# 屬性選擇器
page.click("[data-test='login-button']")

# 組合選擇器
page.click("form#login button.submit")
```

### 常用 CSS 選擇器

| 選擇器 | 說明 | 範例 |
|--------|------|------|
| `element` | 標籤名稱 | `button`, `input` |
| `#id` | ID 選擇器 | `#submit` |
| `.class` | 類別選擇器 | `.btn-primary` |
| `[attr]` | 屬性選擇器 | `[type='submit']` |
| `parent > child` | 直接子元素 | `form > button` |
| `ancestor descendant` | 後代元素 | `div button` |
| `element:nth-child(n)` | 第 n 個子元素 | `li:nth-child(2)` |

---

## 3.2 XPath 定位

### XPath 基礎語法

```python
# 絕對路徑（不建議）
page.click("xpath=/html/body/div/button")

# 相對路徑
page.click("xpath=//button[@id='submit']")

# 文字匹配
page.click("xpath=//button[text()='登入']")

# 包含文字
page.click("xpath=//button[contains(text(), '提交')]")
```

### 常用 XPath 表達式

```python
# 根據屬性
"xpath=//input[@name='username']"

# 根據文字
"xpath=//a[text()='首頁']"

# 包含文字
"xpath=//div[contains(text(), '歡迎')]"

# 父子關係
"xpath=//form[@id='login']//input[@type='password']"

# 同級元素
"xpath=//label[text()='姓名']/following-sibling::input"
```

---

## 3.3 Playwright 內建定位器

Playwright 提供了更語義化的定位器，**建議優先使用**。

### `get_by_text()` - 根據文字定位

```python
# 精確匹配
page.get_by_text("登入").click()

# 部分匹配
page.get_by_text("登入", exact=False).click()
```

### `get_by_role()` - 根據角色定位

```python
# 點擊按鈕
page.get_by_role("button", name="提交").click()

# 點擊連結
page.get_by_role("link", name="首頁").click()

# 填寫文字框
page.get_by_role("textbox", name="用戶名").fill("admin")
```

**常用角色：**
- `button` - 按鈕
- `link` - 連結
- `textbox` - 文字框
- `checkbox` - 核取方塊
- `radio` - 單選按鈕
- `heading` - 標題

### `get_by_label()` - 根據標籤定位

```python
# 根據 label 文字
page.get_by_label("用戶名").fill("admin")
page.get_by_label("密碼").fill("password123")
```

### `get_by_placeholder()` - 根據提示文字定位

```python
page.get_by_placeholder("請輸入Email").fill("user@example.com")
page.get_by_placeholder("搜尋...").fill("Playwright")
```

### `get_by_test_id()` - 根據測試 ID 定位

```python
# HTML: <button data-testid="submit-btn">提交</button>
page.get_by_test_id("submit-btn").click()
```

---

## 3.4 定位策略最佳實踐

### 優先順序建議（由高到低）

1. **`get_by_role()`** - 最具語義，最穩定
2. **`get_by_label()`** - 適合表單元素
3. **`get_by_placeholder()`** - 適合輸入框
4. **`get_by_text()`** - 適合文字內容
5. **`get_by_test_id()`** - 需要在 HTML 中添加
6. **CSS 選擇器** - 靈活但可能不穩定
7. **XPath** - 最後選擇

### 如何處理動態元素

```python
# 使用部分匹配
page.locator("text=/產品.*/").click()

# 使用包含屬性
page.locator("[class*='btn-']").click()

# 組合定位
page.locator("form").get_by_role("button", name="提交").click()

# 鏈式定位
page.locator("div.container").locator("button.submit").click()
```

---

## 完整範例

```python
from playwright.sync_api import sync_playwright

def element_location_demo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://example.com/login")
        
        # 方法1：使用 get_by_label()
        page.get_by_label("用戶名").fill("admin")
        page.get_by_label("密碼").fill("password")
        
        # 方法2：使用 get_by_role()
        page.get_by_role("button", name="登入").click()
        
        # 方法3：使用 CSS 選擇器
        # page.click("#login-button")
        
        # 方法4：使用 XPath
        # page.click("xpath=//button[text()='登入']")
        
        browser.close()

if __name__ == "__main__":
    element_location_demo()
```

---

## 練習題

1. 使用 3 種不同方法定位同一個按鈕
2. 嘗試所有內建定位器（get_by_*）
3. 練習組合定位器的使用
4. 使用開發者工具查看元素，練習寫 CSS 選擇器

---

[← 上一章：基礎操作](../第02章_基礎操作/README.md) | [返回目錄](../README.md) | [下一章：等待與同步 →](../第04章_等待與同步/README.md)
