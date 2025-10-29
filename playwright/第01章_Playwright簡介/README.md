# 第一章：Playwright 簡介

## 1.1 什麼是 Playwright？

### Web 自動化測試工具
Playwright 是由 Microsoft 開發的現代化網頁自動化測試框架，支援多種程式語言包括 Python、JavaScript、Java 和 .NET。

### 與 Selenium 的比較
| 特性 | Playwright | Selenium |
|------|-----------|----------|
| 速度 | 更快 | 較慢 |
| API 設計 | 現代化、簡潔 | 較為傳統 |
| 自動等待 | 內建智慧等待 | 需手動設定 |
| 多瀏覽器支援 | Chromium、Firefox、WebKit | Chrome、Firefox、Safari、Edge |
| 網路攔截 | 原生支援 | 需額外工具 |

### Playwright 的優勢
1. **速度快**：使用 CDP (Chrome DevTools Protocol) 直接通訊
2. **支援多瀏覽器**：一套程式碼可在不同瀏覽器執行
3. **更穩定**：內建自動等待機制，減少 flaky tests
4. **功能強大**：支援網路攔截、模擬、截圖、錄影等

---

## 1.2 Playwright 的應用場景

### 網頁爬蟲（抓取動態網站資料）
- 處理 JavaScript 渲染的網頁
- 抓取需要登入的網站資料
- 處理無限滾動頁面

### 自動化測試
- E2E (End-to-End) 測試
- 功能測試
- 回歸測試

### 網頁截圖與 PDF 生成
- 自動生成網頁截圖
- 將網頁轉換為 PDF
- 視覺回歸測試

### 表單自動填寫
- 自動化資料輸入
- 批量處理表單
- 重複性操作自動化

---

## 1.3 環境安裝與設定

### Python 環境檢查
```bash
# 檢查 Python 版本（需要 3.8 或以上）
python --version
# 或
python3 --version
```

### 安裝 Playwright
```bash
# 使用 pip 安裝
pip install playwright

# 或使用 pip3
pip3 install playwright
```

### 下載瀏覽器驅動
```bash
# 安裝所有瀏覽器
playwright install

# 只安裝特定瀏覽器
playwright install chromium
playwright install firefox
playwright install webkit
```

### 第一個測試程式
```python
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=False)
        
        # 開啟新分頁
        page = browser.new_page()
        
        # 訪問網站
        page.goto("https://www.google.com")
        
        # 取得標題
        print(page.title())
        
        # 關閉瀏覽器
        browser.close()

if __name__ == "__main__":
    run()
```

### 執行程式
```bash
python your_script.py
```

---

## 練習題

1. 安裝 Playwright 並驗證安裝成功
2. 執行第一個測試程式，訪問你喜歡的網站
3. 修改程式，讓瀏覽器訪問 3 個不同的網站
4. 嘗試使用不同的瀏覽器（Chromium、Firefox、WebKit）

---

## 補充資源

- [Playwright 官方文件](https://playwright.dev/python/)
- [Playwright GitHub](https://github.com/microsoft/playwright-python)
- [Playwright API 參考](https://playwright.dev/python/docs/api/class-playwright)

[← 返回主目錄](../README.md) | [下一章：基礎操作 →](../第02章_基礎操作/README.md)
