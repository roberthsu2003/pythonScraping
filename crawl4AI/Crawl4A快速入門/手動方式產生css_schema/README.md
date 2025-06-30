# 手動方式產生css_schema

[**官網說明文件**](https://docs.crawl4ai.com/extraction/no-llm-strategies/)

提取JSON(無LLM)
Crawl4AI 最強大的功能之一是無需依賴大型語言模型即可從網站中提取結構化 JSON。 

## Crawl4AI 提供了幾種無需 LLM 的提取策略：

1. 透過 JsonCssExtractionStrategy 和 JsonXPathExtractionStrategy 使用 CSS 或 XPath 選擇器進行提取網頁資料
2. 使用 RegexExtract Strategy 的正規表示式提取器實現快速模式匹配

這些方法讓您可以立即提取資料（即使是從複雜或嵌套的 HTML 結構中提取資料），而無需 LLM 的成本、延遲或環境影響。

## 為什麼要避免使用 LLM 進行基本提取？

1. 更快、更便宜：無需 API 呼叫或 GPU 開銷。
2. 更低的碳足跡：LLM 推理可能耗能。基於模式的提取幾乎是零碳排放的。
3. 精準且可重複：CSS/XPath 選擇器和正規表示式模式會精確執行您的指定操作。 LLM 輸出可能會有所不同或產生幻覺。
4. 輕鬆擴展：對於數千頁，基於模式的提取可以快速並行運行。

下面，我們將探討如何建立這些模式，並將它們與 JsonCssExtractionStrategy（如果您喜歡 XPath，則可以使用 JsonXPathExtractionStrategy）結合使用。我們還將重點介紹嵌套元素和基本元素屬性等高級功能。

### 1. 基於模式的擷取

**schema的定義**

1. 一個`base selector`，用於標識頁面上的每個「容器」元素（例如，產品行、部落格文章卡片）。

2. ‘fields’描述要擷取的每個資料（文字、屬性、HTML 區塊等）要使用哪些 CSS/XPath 選擇器的欄位。

3. Nested 或 list 類型適用於重複或分層結構。

例如，如果您有一個產品列表，每個產品可能都有名稱、價格、評論和「相關產品」。對於一致、結構化的頁面來說，這種方法比 LLM 更快、更可靠。

---

### 2. 簡單範例：加密貨幣價格

[**台灣銀行牌告匯率**](./lesson1_台灣銀行牌告匯率.ipynb)

讓我們從使用 JsonCssExtractionStrategy 進行簡單的基於模式的提取開始。以下是從網站提取加密貨幣價格的程式碼片段（類似於舊版 Coinbase 範例）。注意，我們沒有調用任何 LLM：

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
        "baseSelector": "div.crypto-row",
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

#asyncio.run(extract_crypto_prices())
await extract_crypto_prices()

```

> [!Tip]
> - baseSelector:告知每一個「項目」（加密行）在哪裡。
> - fields:2個欄位(coin_name, price)使用簡單的css選取器
> - 每個欄位定義一個type(e.g., text, attribute, html, regex, etc.)

---

### 3. 高階Schema & 嵌套結構

實際網站通常會包含巢狀或重複的數據，例如包含產品的類別，而產品本身又包含評論或功能清單。為此，我們可以定義嵌套或列表（甚至是 nested_list）欄位。

**Sample E-Commerce HTML**

[**實作下方程式碼的實作ipynb**](./lesson2_高階schema和嵌套.ipynb)

**以下是HTML**

```
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
        
        <!-- 產品 1 -->
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
        
        <!-- 產品 2 -->
        <div class="product">
            <h3 class="product-name">智能運動手環</h3>
            <p class="product-price">NT$ 1,580</p>
            
            <div class="product-details">
                <span class="brand">品牌: FitLife</span>
                <span class="model">型號: FL-2023</span>
            </div>
            
            <ul class="product-features">
                <li>24小時心率監測</li>
                <li>睡眠品質分析</li>
                <li>50米防水</li>
            </ul>
            
            <div class="review">
                <span class="reviewer">李先生</span>
                <span class="rating">★★★★☆ (4.0)</span>
                <p class="review-text">電池續航力很強，一週充電一次即可</p>
            </div>
            
            <div class="related-products">
                <ul>
                    <li><span class="related-name">替換錶帶</span> <span class="related-price">NT$ 290</span></li>
                    <li><span class="related-name">專用充電座</span> <span class="related-price">NT$ 450</span></li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="category" data-cat-id="cat-002">
        <h2 class="category-name">家用電器</h2>
        
        <!-- 產品 3 -->
        <div class="product">
            <h3 class="product-name">智能空氣清淨機</h3>
            <p class="product-price">NT$ 8,990</p>
            
            <div class="product-details">
                <span class="brand">品牌: AirPure</span>
                <span class="model">型號: AP-3000</span>
            </div>
            
            <ul class="product-features">
                <li>PM2.5即時監測</li>
                <li>APP遠端控制</li>
                <li>靜音夜間模式</li>
            </ul>
            
            <div class="review">
                <span class="reviewer">陳太太</span>
                <span class="rating">★★★★★ (5.0)</span>
                <p class="review-text">過敏症狀明顯改善，非常值得購買</p>
            </div>
            
            <div>
                <ul class="related-products">
                    <li><span class="related-name">專用濾網組</span> <span class="related-price">NT$ 1,200</span></li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""
```

**以下是Schema**

```python
schema ={
    "name": "E-commerce 產品目錄",
    "baseSelector": "div.category",
    "baseFields":[
        {"name":"data_cat_id","type":"attribute","attribute":"data-cat-id"}
    ],
    "fields":[
        {
            "name":"目錄名稱",
            "selector":"h2.category-name",
            "type":"text"
        },
        {
            "name":"產品",
            "selector":"div.product",
            "type":"nested_list", #repeated, sub-objects
            "fields":[
                {
                    "name":"名稱",
                    "selector":"h3.product-name",
                    "type":"text"
                },
                {
                    "name":"價格",
                    "selector":"p.product-price",
                    "type":"text"
                },
                {
                    "name":"資訊",
                    "selector":"div.product-details",
                    "type":"nested",
                    "fields":[
                        {
                            "name":"品牌",
                            "selector":"span.brand",
                            "type":"text"
                        },
                        {
                            "name":"型號",
                            "selector":"span.model",
                            "type":"text"
                        }
                        
                    ]
                },
                {
                    "name":"功能",
                    "selector":"ul.product-features li",
                    "type":"list",
                    "fields":[
                        {
                            "name":"功能",
                            "type":"text"
                        }
                    ]
                },
                {
                    "name":"reviews",
                    "selector":"div.review",
                    "type":"nested_list",
                    "fields":[
                        {
                            "name":"reviewer",
                            "selector":"span.reviewer",
                            "type":"text"
                        },
                        {
                            "name":"rating",
                            "selector":"span.rating",
                            "type":"text"
                        },
                        {
                            "name":"comment",
                            "selector":"p.review-text",
                            "type":"text"
                        }
                    ]
                },
                {
                  "name":"相關產品",
                  "selector":".related-products li",
                  "type":"list",
                  "fields":[
                    {
                        "name":"名稱",
                        "selector":"span.related-name",
                        "type":"text"
                    },
                    {
                        "name":"價格",
                        "selector":"span.related-price",
                        "type":"text"
                    }
                  ]
                }
            ]
        }
    ]
}
```

**以下是程式碼**

```python
import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_ecommerce_data():
    strategy = JsonCssExtractionStrategy(schema, verbose=True)
    config = CrawlerRunConfig(
        extraction_strategy= strategy
    )
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=f"raw://{dummy_html}",
            config=config
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return
        
        print(result.extracted_content)
        #解析json output
        #data = json.loads(result.extracted_content)
        #print(json.dumps(data, indent=2, ensure_ascii=False) if data else "No data found.")

await extract_ecommerce_data()
```

### ‼️有關CSS schema內的Nested, list, nested_list
[**實際範例說明_nested,list,nested_list**](lesson3_nesting_types_example.ipynb)



