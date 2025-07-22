#使用台灣銀行牌告匯率
#網址:https://rate.bot.com.tw/xrt?Lang=zh-TW

import json
import asyncio
import os
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_crypto_prices():
#1. 定義一個簡單的extraction schema

    schema = {
        "name":"台幣匯率",
        "baseSelector":"table[title='牌告匯率'] tr",
        "fields":[
            {
                "name":"幣名",
                "selector":"td[data-table='幣別'] div.visible-phone.print_hide",
                "type":"text"
            },
            {
                "name":"現金匯率_本行買入",
                "selector":'[data-table="本行現金買入"]',
                "type":"text"
            },
            {
                "name":"現金匯率_本行賣出",
                "selector":'[data-table="本行現金賣出"]',
                "type":"text"
            },
            {
                "name":"即期匯率_本行買入",
                "selector":'[data-table="本行即期買入"]',
                "type":"text"
            },
            {
                "name":"即期匯率_本行賣出",
                "selector":'[data-table="本行即期賣出"]',
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
        raw_url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
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
        
        # 6. 儲存資料為JSON格式，建立適當的檔案名稱
        if data:
            # 建立基於時間的檔案名稱
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"台幣匯率_{timestamp}.json"
            
            # 確保資料夾存在
            os.makedirs("data", exist_ok=True)
            filepath = os.path.join("data", filename)
            
            # 儲存JSON檔案
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"資料已儲存至: {filepath}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("No Data found")

async def main():
    """主程式：每隔10分鐘自動執行一次爬蟲"""
    print("台幣匯率爬蟲程式啟動...")
    print("每10分鐘自動執行一次")
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n=== 開始執行爬蟲 ({current_time}) ===")
            
            await extract_crypto_prices()
            
            print("=== 爬蟲執行完成 ===")
            print("等待10分鐘後再次執行...")
            
            # 等待10分鐘 (600秒)
            await asyncio.sleep(600)
            
        except KeyboardInterrupt:
            print("\n程式被使用者中斷")
            break
        except Exception as e:
            print(f"執行過程中發生錯誤: {e}")
            print("等待10分鐘後重試...")
            await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())