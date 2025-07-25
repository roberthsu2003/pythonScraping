## 多網址爬蟲的「調度器」(Dispatcher)

### 什麼是 Dispatcher（調度器）？

當你要同時爬很多網址時，Dispatcher 就像一個「指揮家」，負責安排每個爬蟲任務什麼時候開始、要不要暫停、要不要慢一點，確保電腦不會過載，也不會被網站封鎖。

### 為什麼需要 Dispatcher？

- **同時處理多個網址**：不用一個一個慢慢爬，可以同時進行，速度更快。
- **自動調整速度**：如果網站回應太慢，或出現錯誤（像 429/503），會自動放慢速度或暫停。
- **保護電腦資源**：不會讓電腦記憶體爆掉，會根據電腦狀況自動調整。
- **即時監控**：可以看到目前爬了多少、還剩多少、電腦用多少資源。

### 常見的 Dispatcher 類型

| 類型                     | 說明                                   |
|--------------------------|----------------------------------------|
| MemoryAdaptiveDispatcher | 依照電腦記憶體自動調整同時爬的數量      |
| SemaphoreDispatcher      | 固定同時最多只能幾個任務一起執行        |

### 怎麼用？

- **arun_many()** 這個函式就是幫你自動用 Dispatcher 管理多個網址的爬取。
- 你只要把網址清單丟進去，它會自動安排、分批、調整速度，還會自動重試失敗的網址。

### 什麼時候用得到？

- **大量資料蒐集**：像要爬很多商品、新聞、股票資訊時。
- **API 有速率限制**：像有些網站規定一秒只能爬幾次，Dispatcher 會自動幫你控制。
- **想要即時知道進度**：可以看到目前爬到哪裡，有沒有出錯。

### 小結

Dispatcher 就像爬蟲的「智慧指揮家」，讓你不用擔心速度太快被封鎖，也不用怕電腦當機。只要用 arun_many()，就能輕鬆又安全地爬很多網址！

---

> **注意**：Crawl4AI 內建的 arun_many() 已經自動幫你用好 Dispatcher，不用自己寫複雜的程式。

## 實際範例

- **基本方法**（較慢）：用 for 迴圈一個一個爬
  - [範例程式1](./lesson1_爬取台灣即時股票資訊_loop方式.py)
- **進階方法**（推薦）：一次處理多個網址
  - [範例程式2](./lesson2_爬取台灣即時股票資訊_不同的schema.py)
- **進階方法**（推薦）：用 arun_many() 一次處理多個網址
  - [範例程式3](./lesson3_爬取台灣即時股票資訊_arun_many.py)

---

### 兩種方法的優缺點比較

| 方法         | 優點                                   | 缺點                                      |
|--------------|----------------------------------------|-------------------------------------------|
| 基本方法     | 觀念簡單、容易理解，適合初學者入門      | 速度慢、無法同時處理大量網址，效率較低      |
| 進階方法     | 可以同時爬很多網址，速度快，自動管理資源 | 程式碼稍複雜，但 arun_many() 已幫你包好    |

### 建議
- 如果你只是要爬幾個網址、想先練習基本觀念，可以用『基本方法』。
- 如果你要爬很多網址、追求效率，建議直接用『進階方法』（arun_many()），省時又安全。
			

