# Copilot 知識庫配置

## 專案文件
documents:
  - path: "README.md"
    type: "documentation"
    description: "專案使用說明和安裝指南"
    
  - path: "prd.md"
    type: "specification"
    description: "產品需求文件，包含完整功能規格"

## 程式碼模組
modules:
  - path: "index.py"
    type: "entry_point"
    description: "主程式入口，提供選單介面"
    key_functions:
      - "main()"
      - "選擇執行模式邏輯"
    
  - path: "wantgoo.py"
    type: "core_module"
    description: "爬蟲核心模組，負責股票資料獲取"
    key_functions:
      - "get_stock_data(urls)"
      - "get_stocks_with_twstock()"
    dependencies:
      - "crawl4ai"
      - "twstock"
      - "asyncio"
    
  - path: "stock_gui.py"
    type: "ui_module" 
    description: "GUI 介面模組，實作 tkinter 圖形介面"
    key_classes:
      - "StockCrawlerGUI"
    key_functions:
      - "setup_ui()"
      - "start_crawling()"
      - "display_results()"
    dependencies:
      - "tkinter"
      - "threading"

## API 參考
apis:
  crawl4ai:
    - "AsyncWebCrawler"
    - "BrowserConfig"
    - "CrawlerRunConfig"
    - "JsonCssExtractionStrategy"
    
  twstock:
    - "codes"
    - "stock info structure"
    
  tkinter:
    - "ttk components"
    - "Treeview"
    - "ScrolledText"

## 設計模式
patterns:
  - name: "模組化設計"
    description: "分離關注點，每個模組負責特定功能"
    files: ["index.py", "wantgoo.py", "stock_gui.py"]
    
  - name: "非同步處理"
    description: "使用 asyncio 和 threading 避免阻塞 UI"
    files: ["wantgoo.py", "stock_gui.py"]
    
  - name: "錯誤處理"
    description: "全面的異常捕獲和使用者友善的錯誤訊息"
    files: ["*.py"]

## 常見問題解決方案
troubleshooting:
  - issue: "爬蟲無法取得資料"
    solutions:
      - "檢查網路連線"
      - "驗證 CSS 選擇器"
      - "檢查 crawl4ai 配置"
    files: ["wantgoo.py"]
    
  - issue: "GUI 介面凍結"
    solutions:
      - "確保使用 threading 進行爬蟲"
      - "檢查 asyncio 事件循環"
      - "驗證進度更新機制"
    files: ["stock_gui.py"]
    
  - issue: "股票清單載入失敗"
    solutions:
      - "檢查 twstock 安裝"
      - "驗證網路連線"
      - "檢查過濾條件"
    files: ["wantgoo.py"]

## 最佳實踐
best_practices:
  code_style:
    - "遵循 PEP 8 命名規範"
    - "使用有意義的變數和函數名稱"
    - "適當的程式碼註解"
    
  error_handling:
    - "捕獲具體的異常類型"
    - "提供使用者友善的錯誤訊息"
    - "記錄詳細的錯誤資訊"
    
  performance:
    - "使用非同步處理避免阻塞"
    - "適當的速率限制"
    - "資源清理和記憶體管理"

## 擴展指南
extensions:
  data_export:
    description: "新增資料匯出功能 (CSV, Excel)"
    suggested_files: ["新增 export_module.py"]
    integration_points: ["stock_gui.py 新增匯出按鈕"]
    
  data_visualization:
    description: "新增股票資料視覺化圖表"
    suggested_dependencies: ["matplotlib", "pandas"]
    integration_points: ["stock_gui.py 新增圖表面板"]
    
  scheduling:
    description: "新增定時自動爬取功能"
    suggested_dependencies: ["schedule", "apscheduler"]
    integration_points: ["index.py 新增排程選項"]
