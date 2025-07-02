# 網頁互動(Page Interaction)

[官網Page Interaction說明](https://docs.crawl4ai.com/core/page-interaction/)

Crawl4AI 提供了強大的功能，可與動態網頁互動、處理 JavaScript 執行、等待條件和管理多步驟流程。您可以:透過組合 js_code、wait_for 和某些爬蟲來執行設定參數:

1. 點擊“更多”按鈕(Click “Load More” buttons)
2. 填寫表格並提交(Fill forms and submit them)
3. 等待元素或資料出現(Wait for elements or data to appear)
4. 跨多個步驟重複使用session(Reuse sessions across multiple steps)

## 1. JavaScript 執行

### 基本執行

Crawler RunConfig 中的 js 程式碼接受單一 JS 字串或 JS 片段清單。

範例：我們將捲動到頁面底部，然後選擇性地點擊「載入更多」按鈕。

[**基本執行實作.ipynb**](./lesson1_向下捲動和按按鈕.ipynb)

```python
import asyncio
from crawl4ai import AsyncWebCrawler,CrawlerRunConfig

async def main():
    #single JS command
    config = CrawlerRunConfig(
        js_code="window.scrollTo(0, document.body.scrollHeight);"
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url='https://news.ycombinator.com',
            config = config
        )
        print(result.cleaned_html)
        print("Crawled length:", len(result.cleaned_html))

    #Multiple commands
    js_commands =[
        "window.scrollTo(0, document.body.scrollHeight);",
        "document.querySelector('a.morelink')?.click();"
    ]
    config = CrawlerRunConfig(js_code=js_commands, wait_for="css:.athing:nth-child(31)")

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url = 'https://news.ycombinator.com',
            config = config
        )
        print("After scroll+click, length:", len(result.cleaned_html))

if __name__ == "__main__":
    await main()

```

### 等待

有時，你只想等待特定元素出現。例如：

[**等待的實作範例.ipynb**](./lesson2_等待的操作.ipynb)

```python
#基於css

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig,BrowserConfig

async def main():
    base_browser = BrowserConfig(
        browser_type="chromium",
        headless=False
    )
    config = CrawlerRunConfig(
        #Wait for at least 30 items on Hacker News
        wait_for="css:.athing:nth-child(30)"
    )

    async with AsyncWebCrawler(config=base_browser) as crawler:
        result = await crawler.arun(
            url = 'https://news.ycombinator.com',
            config=config
        )
        print("We have at least 30 items loader!")
        print("Total items in HTML:",result.cleaned_html)

if __name__ == "__main__":
    await main()
```


```python
#基於javascript

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig,BrowserConfig

async def main():
    base_browser = BrowserConfig(
        browser_type="chromium",
        headless=False
    )

    wait_condition = """()=>{
        const items = document.querySelectorAll('.athing')
        return items.length > 50;
    }
    
    """

    config = CrawlerRunConfig(
        #Wait for at least 30 items on Hacker News
        wait_for=f"js:{wait_condition}"
    )

    async with AsyncWebCrawler(config=base_browser) as crawler:
        result = await crawler.arun(
            url = 'https://news.ycombinator.com',
            config=config
        )
        print("We have at least 30 items loader!")
        print("Total items in HTML:",result.cleaned_html)

if __name__ == "__main__":
    await main()
```

### ‼️處理動態內容流程

許多現代網站需要多個步驟：滾動、點擊「加載更多」或透過 JavaScript 更新。以下是一些典型的模式。

```python

```



## 實際案例
- [**Crawl4AI爬取台灣即時股票資訊**](./lesson1_爬取台灣即時股票資訊.py)