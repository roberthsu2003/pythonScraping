import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, JsonCssExtractionStrategy

async def main():
    url = 'https://www.wantgoo.com/stock/2317/technical-chart'
    #建立一個BrowserConfig,讓chromium的瀏覽器顯示
    #BrowserConfig實體

    browser_config = BrowserConfig(
        headless=True
    )
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

    # 建立一個AsyncWebCrawler的實體，並傳入BrowserConfig實體
    # 這樣可以讓爬蟲等待瀏覽器載入頁面，並且可以在瀏覽器中看到爬蟲的操作，方便除錯
    run_config = CrawlerRunConfig(
        wait_for_images=True,  # 等待圖片載入
        scan_full_page=True,  # 掃描整個頁面
        scroll_delay=0.5,     # 滾動步驟之間的延遲（秒)
        #想要在`class="my-drawer-toggle-btn"`的元素上點擊
        #js_code=["document.querySelector('.my-drawer-toggle-btn').click();"],
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(stock_schema),
        verbose=True
    )
    # 使用AsyncWebCrawler的實體來爬取網頁
    # 加入run_config參數
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url,config=run_config)
    
    print(result.extracted_content) 

if __name__ == '__main__':
    asyncio.run(main())
    