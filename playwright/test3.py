from playwright.sync_api import sync_playwright
from crawl4ai import CrawlerRunConfig, AsyncWebCrawler, CacheMode, JsonCssExtractionStrategy
import json
import asyncio

# 接下來將 html 傳入 Crawl4AI 的提取工具進行 schema 提取
async def main(raw_html, schema):
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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    html = page.content()  # 抓取完整 DOM
    print(html)
    browser.close()

schema = {
        "name": "Example Items",
        "baseSelector": "body > div",
        "fields": [
            {"name": "title", "selector": "h1", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

asyncio.run(main(html, schema))


