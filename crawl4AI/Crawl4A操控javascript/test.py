import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def main():
    async with AsyncWebCrawler() as crawler:
        try:
            # Step 1: Load initial Hacker News page
            print("開始載入初始頁面...")
            config = CrawlerRunConfig(
                wait_for="css:.athing:nth-child(30)",  # Wait for 30 items
                session_id="hn_session",
                cache_mode=CacheMode.BYPASS,
                timeout=30  # 增加超時時間
            )
            
            result = await crawler.arun(
                url="https://news.ycombinator.com",
                config=config
            )
            
            if result.success:
                initial_items = result.cleaned_html.count("athing")
                print(f"Step 1 完成: 載入了 {initial_items} 個項目")
                
                # Step 2: Load more items
                print("開始載入更多項目...")
                load_more_js = [
                    "window.scrollTo(0, document.body.scrollHeight);",
                    "await new Promise(resolve => setTimeout(resolve, 2000));",  # 等待 2 秒
                    # 點擊 "More" 連結
                    """
                    const moreLink = document.querySelector('a.morelink');
                    if (moreLink) {
                        moreLink.click();
                        return true;
                    }
                    return false;
                    """
                ]
                
                next_page_conf = CrawlerRunConfig(
                    js_code=load_more_js,
                    wait_for="""js:() => {
                        const items = document.querySelectorAll('.athing');
                        console.log('Current items count:', items.length);
                        return items.length > 30;
                    }""",
                    js_only=True,
                    session_id="hn_session",            
                    cache_mode=CacheMode.BYPASS,
                    delay_before_return_html=3  # 等待更多內容載入
                )
                
                # 繼續使用相同的 session
                result2 = await crawler.arun(
                    url="https://news.ycombinator.com",
                    config=next_page_conf
                )
                
                if result2.success:
                    total_items = result2.cleaned_html.count("athing")
                    print(f"Step 2 完成: 總共載入了 {total_items} 個項目")
                    
                    # 可選：保存結果到文件
                    with open("hn_results.html", "w", encoding="utf-8") as f:
                        f.write(result2.cleaned_html)
                    print("結果已保存到 hn_results.html")
                else:
                    print(f"Step 2 失敗: {result2.error_message}")
                    
            else:
                print(f"Step 1 失敗: {result.error_message}")
                
        except Exception as e:
            print(f"發生錯誤: {e}")
            import traceback
            traceback.print_exc()

# 修正：使用正確的方式運行異步函數
if __name__ == "__main__":
    asyncio.run(main())