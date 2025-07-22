# crawl4AI初體驗
- [github crawl4AI](https://github.com/unclecode/crawl4ai)
- [crawl4AI官方網站使用說明書](https://docs.crawl4ai.com/)

## Playwright 是什麼？為什麼用在 crawl4AI？

**Playwright** 是由微軟（Microsoft）開發的開源瀏覽器自動化工具，主要用於現代 Web 應用的自動化測試與爬蟲。它支援多種主流瀏覽器（Chromium、Firefox、WebKit），並且可以跨平台（Windows、Linux、macOS）運作，API 可用於 Python、JavaScript、TypeScript、.NET、Java 等多種語言

### 主要特點

- **跨瀏覽器與跨平台**：同一套 API 可同時控制多種瀏覽器與作業系統。
- **自動等待元素**：Playwright 在操作網頁元素前會自動等待元素可互動，減少因元素尚未載入導致的錯誤。
- **支援動態內容**：能夠正確處理 JavaScript 動態渲染的網頁，這是傳統爬蟲（如 requests、BeautifulSoup）難以做到的。
- **同步與非同步 API**：Python 版本同時支援同步（sync）與非同步（asyncio）操作，適合高效能需求。
- **高階互動**：可模擬點擊、填寫表單、拖曳、上傳檔案等複雜操作。

### 用於爬蟲的優勢

許多現代網站內容是透過 JavaScript 動態載入的，傳統的 Python 爬蟲工具（如 requests）只能取得靜態 HTML，無法抓取這些動態資料。Playwright 可以像真人一樣操作瀏覽器，等待網頁渲染完成再進行資料擷取，非常適合用於需要登入、互動或資料需等待載入的情境。

### 與 crawl4AI 的結合

crawl4AI 是一套利用 AI 輔助進行網頁資料擷取的工具，Playwright 則負責瀏覽器自動化與動態網頁的內容載入。以一個常見流程為例：

1. 先用 Playwright 自動登入網站，取得登入後的 cookie 或 session。
2. 利用 Playwright 控制瀏覽器載入目標頁面，確保所有動態內容都已渲染。
3. 將已登入的狀態與 cookie 傳給 crawl4AI，由 AI 進行資料擷取與結構化。

這種組合能解決「需要登入、資料動態載入」等複雜網頁的爬取問題，是目前主流的高階爬蟲解決方案之一。

### Python Playwright 基本用法範例

```python
from playwright.async_api import async_playwright
import asyncio

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://example.com')
        await page.wait_for_selector('p') #等待元素載入
        content = await page.inner_text('p')
        print(content)
        await browser.close()
    
await run()
```
這段程式碼展示了如何用 Playwright 控制瀏覽器、載入頁面、等待元素並擷取內容

### Crawl4AI官方的第一個範例

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    #建立一個AsyncWebCrawler的實體
    async with AsyncWebCrawler() as crawler:
        #Run the crawler on a URL
        result = await crawler.arun(url='https://crawl4ai.com')

        #列印取出的結果
        print(result.markdown)

#py檔執行
asyncio.run(main()))

#jupyter notebook執行
#await main()

```

[**Crawl4AI極簡教程(核心版)**](./Crawl4AI極簡教程(核心版).ipynb)

---

**總結**：Playwright 是現代網頁自動化與爬蟲的強大工具，特別適合處理需要互動、登入、JavaScript 動態渲染等情境。它與 crawl4AI 搭配，可以大幅提升資料擷取的成功率與效率，是 Python 開發者不可或缺的爬蟲利器。
