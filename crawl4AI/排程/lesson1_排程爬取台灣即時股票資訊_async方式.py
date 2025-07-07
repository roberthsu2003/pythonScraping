import asyncio
import json
import time
import schedule

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig,CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def crawl_single_url(crawler, url, config):
    results = await crawler.arun(
        url,
        config=config,
        wait_for_selector=["h3.astock-name", "span.astock-code"],
        scroll_delay=10
    )

    for result in results:
        if result.success:
            data = json.loads(result.extracted_content)
            print(json.dumps(data, indent=2, ensure_ascii=False))

async def crawl_stock_info():
    urls = [
        "https://www.wantgoo.com/stock/2330/technical-chart",
        "https://www.wantgoo.com/stock/2317/technical-chart"
    ]

    stock_schema = {
        "name": "StockInfo",
        "baseSelector": "main.main",  # 從整個頁面開始選擇
        "fields": [
            {
                "name":"日期時間",
                "selector":"time.last-time#lastQuoteTime",
                "type":"text"
            },
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
    browserConfig = BrowserConfig( # noqa
        headless=True,
        verbose=True,
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
        tasks = [crawl_single_url(crawler, url, config) for url in urls]
        await asyncio.gather(*tasks)
    

async def main():
    """主程式入口"""
    await crawl_stock_info()

if __name__ == "__main__":
    def crawl():
        asyncio.run(main())
    
    schedule.every(1).minutes.do(crawl)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    