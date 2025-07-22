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

[**第1個爬蟲.ipynb**](./lesson1_第1個爬蟲.ipynb)

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

[**使用內容過濾器.ipynb**](./lesson3_使用內容過濾器.ipynb)

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig,CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

md_generator = DefaultMarkdownGenerator(
    content_filter = PruningContentFilter(threshold=0.4, threshold_type="fixed") #說明1
)

config = CrawlerRunConfig(
    cache_mode = CacheMode.BYPASS,
    markdown_generator = md_generator
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://news.ycombinator.com", config=config)
    print("raw Markdown length:",len(result.markdown.raw_markdown))
    print("Fit Markdown length:",len(result.markdown.fit_markdown))
```


### 5. 簡單資料擷取（基於CSS）

Crawl4AI 也可以使用 CSS 或 XPath 選擇器來擷取結構化資料 (JSON)。以下是一個基於 CSS 的簡單範例：

> 新功能！ Crawl4AI 現在提供了一個強大的實用程序，可以使用 LLM 自動產生提取模式。只需執行一次，即可獲得可重複使用的模式，實現快速：

**5.1 透過自訂的css_schema擷取網頁內容**

[**透過自訂的schema擷取網頁內容.ipynb**](./lesson4_透過css_schema取出內容.ipynb)

```python
import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():

    schema = {
        "name": "Example Items",
        "baseSelector": "div.item", #只有一筆,所以抓到1筆
        "fields": [
            {"name": "title", "selector": "h2", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

    raw_html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="raw://" + raw_html,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(schema)
            )
        )
        # The JSON output is stored in 'extracted_content'
        data = json.loads(result.extracted_content)
        print(result.extracted_content)
        print("========================")
        print(data)

if __name__ == "__main__":
    await main()

```

**5.2 透過手動方式產生css_schema**

[**‼️手動方式產生css_schema(內有多個實際案例)**](./手動方式產生css_schema)

**下方程式碼是透過手動schema建立的擷取範例**

```python
import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_crypto_prices():
    dummy_html = """
    <html>
      <body>
        <div class='crypto-row'>
          <h2 class='coin-name'>Bitcoin</h2>
          <span class='coin-price'>$28,000</span>
        </div>
        <div class='crypto-row'>
          <h2 class='coin-name'>Ethereum</h2>
          <span class='coin-price'>$1,800</span>
        </div>
      </body>
    </html>
    """
    #1. 定義一個簡單的extraction schema
    schema = {
        "name":"Crypto Prices",
        "baseSelector": "div.crypto-row", #有2筆,所以抓到2筆
        "fields":[
            {
                "name": "coin_name",
                "selector": "h2.coin-name",
                "type":"text"
            },
            {
                "name":"price",
                "selector":"span.coin-price",
                "type":"text"
            }
        ]
    }

    #2. 建立extraction strategy
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True) #Enables verbose logging for debugging purposes.

    #3. 設定爬蟲配置
    config = CrawlerRunConfig(
        cache_mode = CacheMode.BYPASS,
        extraction_strategy=extraction_strategy
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        #4. 執行爬蟲和提取任務
        raw_url = f"raw://{dummy_html}"
        result = await crawler.arun(
            url=raw_url,
            config=config
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return
        
        # 5. 解析被提取的json資料
        data = json.loads(result.extracted_content)
        print(f"Extracted {len(data)} coin entries")
        print(json.dumps(data[0], indent=2) if data else "No Data found")

await extract_crypto_prices()
```

**5.3 透過本地模型產生css_schema**

**5.4 透過gemini,openai,anthropic產生css_schema**

[**透過llama和Gemini模型實作的.ipynb**](./lesson4_css_base_使用llm建立schema.ipynb)

**下方是透過本地模型產生schema的程式碼**

```python
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai import LLMConfig, AsyncWebCrawler,CacheMode,CrawlerRunConfig
import json
from pprint import pprint

# Generate a schema (one-time cost)
#html = "<div class='product'><h2>Gaming Laptop</h2><span class='price'>$999.99</span></div>"
html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"

# Or using Ollama (open source, no token needed)
schema = JsonCssExtractionStrategy.generate_schema(
    html,
    llm_config = LLMConfig(provider="ollama/llama3.2", api_token=None)  # Not needed for Ollama
)

# Use the schema for fast, repeated extractions
strategy = JsonCssExtractionStrategy(schema)

#非常重要,一定要有CrawlerRunConfig的實體
#一定要有extraction_strategy的引數名稱
#不然使用result.extracted_content會是None

config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    extraction_strategy=strategy
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url = f"raw://{html}",
        config=config
    )

    print("=====lamma3.2產生的schema=========")
    pprint(schema)
    data = json.loads(result.extracted_content)
    print("==========擷取結果==========")
    pprint(data)

```


**下方是透過gemini的擷取的程式碼**

```python
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai import LLMConfig,CrawlerRunConfig
from pprint import pprint

# Generate a schema (one-time cost)
html = """
<html>
    <body>
        <div class='product'>
            <h2>Gaming Laptop</h2>
            <span class='price'>$999.99</span>
        </div>
    <body>
</html>
"""

# Using OpenAI (requires API token)

schema = JsonCssExtractionStrategy.generate_schema(
    html,
    llm_config = LLMConfig(        
        provider="gemini/gemini-2.5-flash",
        api_token="gemini api key")  # Required for OpenAI
)

# 手動產生的schema
# schema = {
#     'name': 'Product Details',
#     'baseSelector': '.product',
#     'fields': [
#         {'name': 'title', 
#          'selector': 'h2', 
#          'type': 'text'},
#         {'name': 'price',
#          'selector': '.price',
#          'type': 'text'}]
# }

# Use the schema for fast, repeated extractions
strategy = JsonCssExtractionStrategy(schema,verbose=True)

#3. 設定爬蟲配置
config = CrawlerRunConfig(
    cache_mode = CacheMode.BYPASS,
    extraction_strategy=strategy
)
async with AsyncWebCrawler() as crawler:
    raw_url = f"raw://{html}"
    result = await crawler.arun(
        url = raw_url,
        config=config
    )
    print("======Gmini 自動產生的schema======")
    print(schema)
    print("=======取出的結果===========")
    data = json.loads(result.extracted_content)
    print(data)
```







