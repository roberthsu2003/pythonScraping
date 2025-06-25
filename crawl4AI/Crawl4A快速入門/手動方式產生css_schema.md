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



