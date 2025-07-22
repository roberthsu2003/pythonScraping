# Crawl4AI 安裝與部署指南

本文件依據 [Crawl4AI 官方文件](https://docs.crawl4ai.com/core/installation/) 編寫，說明如何安裝、診斷、驗證、進階安裝與 Docker 部署。

---

## 1. 基本安裝

使用 pip 安裝 Crawl4AI 核心套件：
```bash
pip install crawl4ai
```
此步驟僅安裝核心功能，不包含進階特性（如 transformers 或 PyTorch）。

---

## 2. 初始設定與診斷

### 2.1 執行設定指令
安裝後請執行：
```bash
crawl4ai-setup
```
此指令會：
- 安裝或更新 Playwright 瀏覽器（Chromium、Firefox 等）
- 執行作業系統相依性檢查
- 確認環境已準備好進行爬蟲作業

### 2.2 診斷
可選擇執行診斷確認一切正常：
```bash
crawl4ai-doctor
```
此指令會：
- 檢查 Python 版本相容性
- 驗證 Playwright 安裝
- 檢查環境變數與函式庫衝突

如有錯誤，請依照建議修正後重新執行 `crawl4ai-setup`。

---

## 3. 驗證安裝：簡單爬蟲範例

以下為最簡單的 Python 爬蟲範例：
```python
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.example.com",
        )
        print(result.markdown[:300])  # 顯示前 300 字元

if __name__ == "__main__":
    asyncio.run(main())
```

預期結果：
- 會啟動 headless 瀏覽器載入 example.com
- 回傳約 300 字元的 markdown 內容

如遇錯誤，請再次執行 `crawl4ai-doctor` 或確認 Playwright 安裝。

---

## 4. 進階安裝（選用）

**僅在需要進階功能時安裝，否則會增加磁碟與記憶體用量。**

- 安裝 PyTorch 相關功能：
```bash
pip install crawl4ai[torch]
crawl4ai-setup
```
- 安裝 Transformers 相關功能：
```bash
pip install crawl4ai[transformer]
crawl4ai-setup
```
- 安裝所有進階功能：
```bash
pip install crawl4ai[all]
crawl4ai-setup
```

（可選）預先下載大型模型：
```bash
crawl4ai-download-models
```

---

## 5. Docker 部署（實驗性）

目前 Docker 僅供測試，**不建議用於生產環境**。未來將於 2025 Q1 推出穩定版。

拉取並啟動 Docker 容器：
```bash
docker pull unclecode/crawl4ai:basic
docker run -p 11235:11235 unclecode/crawl4ai:basic
```

啟動後可對 `http://localhost:11235/crawl` 發送 POST 請求進行爬蟲操作。

---

## 6. 本地伺服器模式（Legacy）

舊版文件提及的本地伺服器模式已部分被 Docker 方案取代，未來將有新架構釋出。建議等待官方正式說明。

---

## 小結
1. 以 pip 安裝並執行 `crawl4ai-setup`。
2. 有問題時執行 `crawl4ai-doctor`。
3. 用簡單範例驗證安裝。
4. 進階功能請依需求安裝。
5. Docker 僅供實驗，生產環境請等待穩定版。
6. 本地伺服器模式將有新方案。

更多細節請參考 [官方文件](https://docs.crawl4ai.com/core/installation/)。

