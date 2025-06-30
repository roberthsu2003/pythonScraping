#使用Crawl4AI爬取台灣即時股票資訊
import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig,CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

#爬取https://www.wantgoo.com/stock/2330/technical-chart的資料
async def crawl_stock_info():
    print("\n=== 爬取台灣即時股票資訊 ===")
    url = "https://www.wantgoo.com/stock/2330/technical-chart"

    # 定義 CSS 提取 Schema
    # 根據網頁結構，我們需要找到包含股票資訊的區塊
    # 這裡假設股票名稱在 .stock-name 類別中，即時價格在 .stock-price 類別中
    # 實際應用中需要根據目標網站的 HTML 結構來調整這些選擇器
    stock_schema = {
        "name": "StockInfo",
        "baseSelector": "main.main",  # 從整個頁面開始選擇
        "fields": [
            {
                "name": "股票號碼",
                "selector": "span.astock-code[c-model='id']", # 假設股票代碼在這個選擇器下
                "type": "text"
            },
            {
                "name": "股票名稱",
                "selector": "h3.astock-name[c-model='name']",  # 假設股票名稱在這個選擇器下
                "type": "text"
            },
            {
                "name": "即時價格",
                "selector":"div.quotes-info div.deal",
                "type": "text"

            },
            {
                "name": "漲跌",
                "selector":"div.quotes-info span.chg[c-model='change']",
                "type": "text"
            },
            {
                "name": "漲跌百分比",
                "selector":"div.quotes-info span.chg-rate[c-model='changeRate']",
                "type": "text"
            },
            {
                "name": "開盤價",
                "selector":"div.quotes-info #quotesUl span[c-model-dazzle='text:open,class:openUpDn']",
                "type": "text"
            },
            {
                "name": "最高價",
                "selector":"div.quotes-info #quotesUl span[c-model-dazzle='text:high,class:highUpDn']",
                "type": "text"

            },
            {
                "name": "成交量(張)",
                "selector":"div.quotes-info #quotesUl span[c-model='volume']",
                "type": "text" 
            },
            {
                "name": "最低價",
                "selector":"div.quotes-info #quotesUl span[c-model-dazzle='text:low,class:lowUpDn']",
                "type": "text" 
            },
            {
                "name": "前一日收盤價",
                "selector":"div.quotes-info #quotesUl span[c-model='previousClose']",
                "type": "text" 
            }

        ]
    }

    # 將 BrowserConfig 直接傳遞給 AsyncWebCrawle
    browserConfig = BrowserConfig(
        headless=False,
        verbose=True,
        #use_persistent_context=True,
        browser_mode="dedicated",
        )
    js_command = [
        "document.querySelector('.my-drawer-toggle-btn')?.click();"
    ]

    extraction_strategy = JsonCssExtractionStrategy(schema=stock_schema)

    config = CrawlerRunConfig(
            extraction_strategy=extraction_strategy,
            cache_mode=CacheMode.BYPASS,
            scan_full_page=True,
            js_code=js_command,        
            verbose=True,            
        )
    
    async with AsyncWebCrawler(config=browserConfig) as crawler:           
        results = await crawler.arun(
            url,
            config=config,
            wait_for_selector=["h3.astock-name", "span.astock-code"],
            scroll_delay=10,
        )
        for result in results:
            if result.success:                
                data = json.loads(result.extracted_content)
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(f"Failed to crawl {result.url}: {result.error_message}")
        
        
        

async def main():
    await crawl_stock_info()

if __name__ == "__main__":
    asyncio.run(main())
