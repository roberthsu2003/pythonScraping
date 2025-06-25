# Crawl4A快速入門
[官方的Quick Start](https://docs.crawl4ai.com/core/quickstart/)

- 使用最小的配置,運行爬蟲
- 產生Markdown的輸出（並了解他如何受到內容過濾器的影響)
- 嘗試一種基於CSS的簡單提取策略
- 了解基於LLM的擷取(包括開源和閉源模型)
- 抓取透過JavaScript載入內容的動態網頁

### 1. 介紹
- 非同步爬蟲,`AsyncWebClawer`
- 可透過`rowserConfig`和`CrawlerRunConfig`設定瀏覽器和運行設定。
- 透過預設 MarkdownGenerator 自動將 HTML 轉換為 Markdown（支援其它過濾器）。
- 多種擷取策略（基於 LLM 或「傳統」CSS/XPath）。

### 2. 第一個爬蟲

下面是一個最小的 Python 腳本，它會建立一個 AsyncWebCrawler，取得一個網頁，並列印其 Markdown 輸出的前 300 個字元：

[**第1個爬蟲.ipynb**](./lesson1_第1個爬串.ipynb)

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com")
        print(result.markdown[:300]) #

if __name__ == '__main__':
    #asyncio,run(main())
    await main()
```


### 3.基本配置(簡單介紹)

Crawl4AI 的爬蟲可以透過兩個主要類別進行高度客製化：

1. BrowserConfig：控制瀏覽器的行為（無頭模式或完整使用者介面、使用者代理、JavaScript 開關等）。
2. Crawler RunConfig：控制每個爬蟲如何運作（快取caching、提取extraction、逾時timeout、掛接hooking等）。

[**簡單配置.ipynb**](./lesson2_基本配置.ipynb)

```python
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_conf= BrowserConfig(headless=True)
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS #說明1
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url='https://example.com',
            config=run_conf
        )
        print(result.markdown)

if __name__ == "__main__":
	#asyncio,run(main())
    await main()
```

### 4. 產生MarkDown輸出
預設情況下，Crawl4AI 會自動從每個爬取的頁面產生 Markdown 檔案。不過，具體輸出結果取決於你指定了 Markdown 產生器還是內容過濾器。

- result.markdown:  
直接將 HTML 轉換為 Markdown。

- result.markdown.fit_markdown:  
套用任何已配置的內容過濾器（例如,PruningContentFilter)。


