import asyncio
import json
import twstock

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    JsonCssExtractionStrategy,
    SemaphoreDispatcher,
    RateLimiter,
)

async def get_stock_data(urls: list[str]) -> list[dict]:
    """
    非同步地從 wantgoo.com 抓取股票資料。
    使用正則表達式從網頁內容中提取股票資訊。
    """
    import re
    
    browser_config = BrowserConfig(
        headless=True,  # 使用無頭瀏覽器提高效率
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )

    run_config = CrawlerRunConfig(
        wait_for_images=False,  # 不等待圖片載入
        scan_full_page=True,    # 需要掃描整個頁面以確保資料完整
        scroll_delay=1.0,       # 適中的延遲確保資料載入
        cache_mode=CacheMode.BYPASS,
        verbose=False           # 減少日誌輸出
    )

    dispatcher = SemaphoreDispatcher(
        semaphore_count=5,      # 適度增加並發數
        rate_limiter=RateLimiter(base_delay=(1.0, 2.0), max_delay=5.0)  # 大幅減少延遲
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=run_config,
            dispatcher=dispatcher,
        )
    
    all_results: list[dict] = []
    for result in results:
        try:
            # 從URL中提取股票代碼
            stock_code_match = re.search(r'/stock/(\d+)/', result.url)
            stock_code = stock_code_match.group(1) if stock_code_match else "未知"
            
            html_content = result.cleaned_html
            
            # 提取股票名稱 - 從title標籤中提取
            title_match = re.search(r'<title>([^<]+)</title>', html_content)
            if title_match:
                title_text = title_match.group(1)
                # 從標題中提取股票名稱，格式通常是 "股票名稱(代碼) - 其他文字"
                name_match = re.search(rf'([^(]+)\({stock_code}\)', title_text)
                stock_name = name_match.group(1).strip() if name_match else "未知"
            else:
                stock_name = "未知"
            
            # 提取股價資訊 - 尋找數字模式
            price_patterns = re.findall(r'\b\d+\.\d{2}\b', html_content)
            
            # 尋找成交量 - 通常是較大的整數，以千張或萬張為單位
            volume_patterns = re.findall(r'\b\d{4,}\b', html_content)  # 四位數以上的整數
            # 過濾掉股票代碼和年份等數字
            volume_candidates = [v for v in volume_patterns if v != stock_code and not v.startswith('20')]
            
            # 根據wantgoo網站的實際數字順序調整索引
            # index 6 通常是實際的即時價格
            current_price = float(price_patterns[6]) if len(price_patterns) > 6 else (float(price_patterns[0]) if len(price_patterns) > 0 else 0)
            # 尋找前日收盤價，通常在後面的位置
            prev_close = 0
            if len(price_patterns) > 7:
                # 嘗試找到合理的前日收盤價（應該接近當前價格）
                for i in range(7, min(len(price_patterns), 15)):
                    candidate = float(price_patterns[i])
                    # 前日收盤價應該與當前價格相差不會太遠（假設不超過20%）
                    if abs(candidate - current_price) / current_price < 0.2 and candidate > current_price * 0.5:
                        prev_close = candidate
                        break
            
            # 計算實際漲跌
            change_value = current_price - prev_close if prev_close > 0 else 0
            change_str = f"{change_value:+.2f}" if change_value != 0 else "0.00"
            
            stock_data = {
                "股票號碼": stock_code,
                "股票名稱": stock_name,
                "即時價格": f"{current_price:.2f}" if current_price > 0 else "N/A",
                "漲跌": change_str,
                "漲跌百分比": price_patterns[2] if len(price_patterns) > 2 else "N/A",
                "開盤價": price_patterns[3] if len(price_patterns) > 3 else "N/A",
                "最高價": price_patterns[4] if len(price_patterns) > 4 else "N/A",
                "最低價": price_patterns[5] if len(price_patterns) > 5 else "N/A",
                "成交量(張)": volume_candidates[0] if len(volume_candidates) > 0 else "N/A",  # 使用過濾後的成交量候選
                "前一日收盤價": f"{prev_close:.2f}" if prev_close > 0 else "N/A",
            }
            
            all_results.append(stock_data)
            
        except Exception as e:
            print(f"處理 {result.url} 時發生錯誤: {e}")
            # 添加錯誤資料以避免程式崩潰
            stock_code = re.search(r'/stock/(\d+)/', result.url).group(1) if re.search(r'/stock/(\d+)/', result.url) else "未知"
            all_results.append({
                "股票號碼": stock_code,
                "股票名稱": "資料獲取失敗",
                "即時價格": "N/A",
                "漲跌": "N/A",
                "漲跌百分比": "N/A",
                "開盤價": "N/A",
                "最高價": "N/A",
                "最低價": "N/A",
                "成交量(張)": "N/A",
                "前一日收盤價": "N/A",
            })

    return all_results

def get_stocks_with_twstock() -> list[dict]:
    """
    從 twstock 套件取得所有上市/上櫃公司清單。
    """
    stocks = twstock.codes
    stock_list = [
        {
            'code': code,
            'name': info.name,
            'market': info.market,
            'group': info.group
        }
        for code, info in stocks.items()
        if info.type == '股票' and len(code) == 4
    ]
    return stock_list