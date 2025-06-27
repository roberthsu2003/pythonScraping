import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

dummy_html = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>電子商務產品目錄範例</title>
    <style>
        .category { border: 1px solid #ddd; padding: 20px; margin-bottom: 30px; }
        .category-name { color: #333; border-bottom: 2px solid #2196F3; padding-bottom: 10px; }
        .product { border: 1px solid #eee; padding: 15px; margin: 15px 0; background: #f9f9f9; }
        .product-name { color: #e91e63; font-size: 1.2em; }
        .product-price { color: #4CAF50; font-weight: bold; }
        .product-details { background: #f0f7ff; padding: 10px; margin: 10px 0; }
        .product-features { list-style-type: none; padding: 0; }
        .product-features li { padding: 5px 0; }
        .review { border-top: 1px dashed #ccc; padding: 10px 0; }
        .related-products { background: #fff8e1; padding: 10px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="category" data-cat-id="cat-001">
        <h2 class="category-name">3C電子產品</h2>
        <div class="product">
            <h3 class="product-name">無線藍牙耳機 Pro</h3>
            <p class="product-price">NT$ 2,980</p>
            <div class="product-details">
                <span class="brand">品牌: SoundMax</span>
                <span class="model">型號: SM-BT500</span>
            </div>
            <ul class="product-features">
                <li>主動降噪功能</li>
                <li>續航力30小時</li>
                <li>IPX7防水等級</li>
            </ul>
            <div class="review">
                <span class="reviewer">張先生</span>
                <span class="rating">★★★★☆ (4.5)</span>
                <p class="review-text">降噪效果非常好，長時間佩戴也很舒適</p>
            </div>
            <div class="review">
                <span class="reviewer">王小姐</span>
                <span class="rating">★★★★★ (5.0)</span>
                <p class="review-text">音質超出預期，CP值很高</p>
            </div>
            <div class="related-products">
                <ul>
                    <li><span class="related-name">無線充電盒</span> <span class="related-price">NT$ 690</span></li>
                    <li><span class="related-name">耳機保護套</span> <span class="related-price">NT$ 350</span></li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""

async def extract_ecommerce_data():
    strategy = JsonCssExtractionStrategy(schema, verbose=False)  # verbose 設為 False
    config = CrawlerRunConfig()
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=f"raw://{dummy_html}", extraction_strategy=strategy, config=config)
        if result.success and result.extracted_content:
            print(json.dumps(json.loads(result.extracted_content), indent=2, ensure_ascii=False))
        else:
            print("Crawl failed or no data extracted:", result.error_message)

schema = {
    "name": "E-commerce Product Catalog",
    "baseSelector": "div.category",
    "fields": [
        {
            "name": "category_name",
            "selector": "h2.category-name",
            "type": "text"
        },
        {
            "name": "products",
            "selector": "div.product",
            "type": "nested_list",
            "fields": [
                {"name": "name", "selector": "h3.product-name", "type": "text"},
                {"name": "price", "selector": "p.product-price", "type": "text"},
                {
                    "name": "details",
                    "selector": "div.product-details",
                    "type": "nested",
                    "fields": [
                        {"name": "brand", "selector": "span.brand", "type": "text"},
                        {"name": "model", "selector": "span.model", "type": "text"}
                    ]
                },
                {
                    "name": "features",
                    "selector": "ul.product-features li",
                    "type": "list",
                    "fields": [{"name": "feature", "type": "text"}]
                },
                {
                    "name": "reviews",
                    "selector": "div.review",
                    "type": "nested_list",
                    "fields": [
                        {"name": "reviewer", "selector": "span.reviewer", "type": "text"},
                        {"name": "rating", "selector": "span.rating", "type": "text"},
                        {"name": "comment", "selector": "p.review-text", "type": "text"}
                    ]
                },
                {
                    "name": "related_products",
                    "selector": "ul.related-products li",
                    "type": "list",
                    "fields": [
                        {"name": "name", "selector": "span.related-name", "type": "text"},
                        {"name": "price", "selector": "span.related-price", "type": "text"}
                    ]
                }
            ]
        }
    ]
}

if __name__ == "__main__":
    asyncio.run(extract_ecommerce_data())