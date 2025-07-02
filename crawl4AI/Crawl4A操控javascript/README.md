# 網頁互動(Page Interaction)

[官網Page Interaction說明](https://docs.crawl4ai.com/core/page-interaction/)

Crawl4AI 提供了強大的功能，可與動態網頁互動、處理 JavaScript 執行、等待條件和管理多步驟流程。您可以:透過組合 js_code、wait_for 和某些爬蟲來執行設定參數:

1. 點擊“更多”按鈕(Click “Load More” buttons)
2. 填寫表格並提交(Fill forms and submit them)
3. 等待元素或資料出現(Wait for elements or data to appear)
4. 跨多個步驟重複使用session(Reuse sessions across multiple steps)

## 1. JavaScript 執行

### 基本執行

Crawler RunConfig 中的 js 程式碼接受單一 JS 字串或 JS 片段清單。

範例：我們將捲動到頁面底部，然後選擇性地點擊「載入更多」按鈕。

```python
```

## 實際案例
- [**Crawl4AI爬取台灣即時股票資訊**](./lesson1_爬取台灣即時股票資訊.py)