# Python `asyncio` 教學大綱與範例

## 教學目標

- 讓學生理解 `asyncio` 的核心概念：非同步程式設計與事件迴圈。
- 學會使用 `async def`、`await` 與事件迴圈來撰寫非同步程式。
- 透過簡單範例，快速上手 `asyncio` 的基本應用。

## 教學大綱

### 1. 什麼是 `asyncio`？

- **概念**：`asyncio` 是 Python 用於非同步程式設計的標準庫，適用於 I/O 密集型任務（例如網路請求、檔案讀寫）。
- **核心思想**：非同步程式允許程式在等待 I/O 操作和伺服器(MCP)時執行其他任務，提升效率。
- **關鍵詞**：
    - `async def`：定義非同步函數（coroutine）。
    - `await`：暫停非同步函數，等待某個任務完成。
    - 事件迴圈（Event Loop）：管理非同步任務的執行順序。

### 2. 為什麼需要 `asyncio`？

- **同步 vs 非同步**：
    - 同步程式：任務按順序執行，等待 I/O 會`阻塞程式`。
    - 非同步程式：任務可交錯執行，等待 I/O 時可切換到其他任務。
- **使用場景**：
    - 網路請求（爬蟲、API 呼叫）。
    - 檔案讀寫。
    - 即時應用（聊天室、伺服器）。

### 3. 基本語法

- **定義非同步函數**：

```python
async def my_function():
    # 非同步程式碼
    pass
```

- **等待任務**：

```python
await some_async_function()
```

- **執行非同步程式**：
> [!IMPORTANT]  
> `asyncio.run(main())`只可以在py檔執行  
> ipynb檔無法執行,原因是ipynb本身在執行時,已經有建立事件迴圈,所以必需使用`await main()`  

    使用 `asyncio.run(main())` 或事件迴圈來運行非同步函數。
    

### 4. 簡單範例

#### 範例 1：基本非同步函數
[**ipynb檔實作**](asyncio非同步編程.ipynb) 

模擬不同任務的等待時間，展示非同步執行的優勢。

```python
import asyncio

async def say_hello(name, delay):
    print(f"{name} 開始執行")
    await asyncio.sleep(delay)  # 模擬 I/O 等待
    print(f"{name} 完成，耗時 {delay} 秒")

async def main():
    # 同時執行多個任務
    await asyncio.gather(say_hello("任務1", 2), say_hello("任務2", 1))

# 執行非同步程式
asyncio.run(main()) # py檔
await main() # ipynb檔
```

**預期輸出**：

```other
任務1 開始執行
任務2 開始執行
任務2 完成，耗時 1 秒
任務1 完成，耗時 2 秒
```

**說明**：`asyncio.gather` 讓多個任務並行執行，總耗時取決於最長任務（2秒），而非串行執行（3秒）。

#### 範例 2：模擬非同步網路請求

模擬抓取多個網站資料，展示非同步在網路請求中的應用。

```python
import asyncio

async def fetch_data(url, delay):
    print(f"開始抓取 {url}")
    await asyncio.sleep(delay)  # 模擬網路延遲
    print(f"完成抓取 {url}")
    return f"資料來自 {url}"

async def main():
    urls = [("網站1", 2), ("網站2", 1), ("網站3", 3)]
    tasks = [fetch_data(url, delay) for url, delay in urls]
    results = await asyncio.gather(*tasks)
    print("所有資料：", results)

asyncio.run(main()) #py檔執行
await main() # ipynb檔執行
```

**預期輸出**：

```other
開始抓取 網站1
開始抓取 網站2
開始抓取 網站3
完成抓取 網站2
完成抓取 網站1
完成抓取 網站3
所有資料：['資料來自 網站1', '資料來自 網站2', '資料來自 網站3']
```

**說明**：每個「網路請求」並行執行，總耗時為最長任務的 3 秒。

### 5. 實作練習

- **練習 1**：撰寫一個非同步程式，模擬 5 個任務（每個任務隨機延遲 1-5 秒），並輸出每個任務的完成時間。
- **練習 2**：模擬一個非同步爬蟲，抓取 3 個網站資料，並將結果儲存到列表中。
- **進階練習**：使用 `asyncio.create_task` 建立任務，觀察與 `asyncio.gather` 的差異。

### 6. 常見問題與注意事項

- **不能在非 async 函數中使用 await**：`await` 只能用在 `async def` 函數內。
- **asyncio.run() 只能呼叫一次**：主程式入口應只呼叫一次 `asyncio.run()`。
- **使用 asyncio.sleep() 模擬 I/O**：不要用 `time.sleep()`，因為它會阻塞整個程式。
- **事件迴圈管理**：確保程式結束前關閉事件迴圈（`asyncio.run()` 會自動處理）。

## 教學建議

- **課堂演示**：運行範例程式，展示同步與非同步執行的時間差異。
- **實作引導**：讓學生修改範例程式，調整延遲時間或任務數量，觀察結果。
- **討論場景**：與學生討論 `asyncio` 在爬蟲、伺服器等實際應用中的好處。

---

如何和學生討論 asyncio 在爬蟲實際應用中的好處

要與學生討論 `asyncio` 在爬蟲實際應用中的好處，可以透過結構化的方式引導他們理解非同步程式設計如何提升爬蟲效率，並結合具體場景與範例，讓討論更生動且貼近實務。以下是一個討論框架，包含引導問題、核心好處、實際案例與互動建議，幫助學生快速抓住重點並參與討論。

### 討論框架：`asyncio` 在爬蟲中的好處

#### 1. 開場：引入爬蟲與非同步的關聯

- **問題引導**：
    - 「假設你要從 100 個網頁抓取資料，每個網頁需要 1 秒回應，如果用傳統同步方式，需要多久？如果能同時發送多個請求呢？」
    - 「什麼是爬蟲中最耗時的部分？（提示：網路請求、等待回應）」
- **目的**：讓學生意識到爬蟲中的 I/O 等待是瓶頸，非同步程式可以解決這個問題。
- **簡介**：說明 `asyncio` 讓爬蟲能並行處理多個網路請求，減少等待時間。

#### 2. 核心好處：逐一討論 `asyncio` 的優勢

以下是 `asyncio` 在爬蟲中的主要好處，建議逐一與學生探討，並搭配簡單範例或比喻。

- **好處 1：提升效率，減少總執行時間**
    - **說明**：同步爬蟲按順序等待每個網頁回應，總時間是所有請求時間的總和。`asyncio` 允許並行發送請求，總時間接近最慢的單一請求。
    - **比喻**：「同步爬蟲像一個人在 10 家店排隊買東西，每次都要等結帳完才能去下一家。非同步爬蟲像同時派 10 個機器人去買，總時間只取決於最慢的那家店。」
    - **問題引導**：「如果抓 100 個網頁，同步需要 100 秒，非同步可能只需要 5 秒，你覺得這對什麼場景特別有用？（如大規模資料收集）」
    - **範例程式**（可展示或讓學生修改）：

```python
import asyncio
import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"抓取 {url} 完成")
            return await response.text()

async def main():
    urls = ["https://example.com", "https://python.org", "https://github.com"]
    tasks = [fetch_url(url) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

        **說明**：使用 `aiohttp`（支援非同步的 HTTP 庫）抓取多個網頁，展示並行請求的效率。

- **好處 2：節省資源，輕量級並行**
    - **說明**：`asyncio` 使用單執行緒的事件迴圈管理多個任務，相比多執行緒或多進程爬蟲，記憶體和 CPU 使用量更低。
    - **比喻**：「多執行緒像開 100 輛車同時送貨，每輛車耗油又占路。`asyncio` 像一個高效的快遞員，快速切換路線，只用一輛車完成所有送貨。」
    - **問題引導**：「如果你的電腦只有 4 核 CPU，多執行緒爬蟲能開幾個執行緒？`asyncio` 為什麼能處理更多任務？」
    - **討論場景**：在伺服器上運行爬蟲時，`asyncio` 能支援數千個並行請求，適合高併發但低計算需求的任務。
- **好處 3：靈活控制任務與錯誤處理**
    - **說明**：`asyncio` 提供 `asyncio.gather`、`asyncio.create_task` 等工具，可輕鬆管理多個任務的執行順序，並處理請求失敗的情況。
    - **範例**：展示如何處理超時或失敗的請求：

```python
import asyncio
import aiohttp

async def fetch_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=2) as response:
                return await response.text()
    except Exception as e:
        print(f"抓取 {url} 失敗: {e}")
        return None

async def main():
    urls = ["https://example.com", "https://invalid-url", "https://python.org"]
    results = await asyncio.gather(*[fetch_url(url) for url in urls], return_exceptions=True)
    print([r[:50] if r else None for r in results])  # 顯示部分結果

asyncio.run(main())
```

        **問題引導**：「如果一個網頁超時或失敗，會影響其他請求嗎？如何改進程式來重試失敗的請求？」

- **好處 4：支援大規模爬蟲與即時應用**
    - **說明**：`asyncio` 適合抓取大量網頁（如新聞網站、電商價格）或即時應用（如監控網站更新）。
    - **案例**：假設要監控 1000 個商品價格，同步爬蟲可能需要數小時，`asyncio` 可在數分鐘內完成。
    - **問題引導**：「如果要每 10 分鐘檢查一次網站更新，`asyncio` 怎麼幫你節省時間和資源？」

#### 3. 實際案例：讓學生聯想應用場景

- **案例分享**：
    - **新聞爬蟲**：用 `asyncio` 同時抓取多個新聞網站的頭條，快速彙整最新資訊。
    - **電商價格監控**：並行檢查多個電商平台的商品價格，找出最優惠的選項。
    - **API 批量請求**：從天氣 API 抓取多個城市的即時資料，整合成報表。
- **問題引導**：
    - 「你們有沒有想抓取的網站或資料？用 `asyncio` 會怎麼設計爬蟲？」
    - 「如果網站有限制每秒請求次數，`asyncio` 怎麼幫你控制請求速率？（提示：使用 `asyncio.Semaphore`）」
- **互動**：讓學生提出一個爬蟲需求（如抓取社群媒體貼文），現場討論如何用 `asyncio` 實現。

#### 4. 對比其他方法：加深理解

- **與多執行緒爬蟲比較**：
    - 多執行緒適合 CPU 密集任務，但爬蟲是 I/O 密集，`asyncio` 更輕量且易於管理。
    - 問題：「為什麼不用 `threading` 模組來爬網頁？」
- **與同步爬蟲比較**：
    - 使用 `requests` 的同步爬蟲簡單但慢，`asyncio` + `aiohttp` 速度快但學習曲線稍高。
    - 問題：「什麼時候用同步爬蟲就夠了？什麼時候需要 `asyncio`？」

#### 5. 實作引導：動手體驗好處

- **簡單任務**：讓學生修改範例程式，增加 10 個網頁的抓取任務，觀察執行時間。
- **進階任務**：讓學生實現一個帶超時機制的爬蟲，抓取 5 個網頁並記錄失敗的請求。
- **觀察效果**：比較同步爬蟲（用 `requests`）與非同步爬蟲（用 `aiohttp`）的執行時間，讓學生直觀感受差異。

#### 6. 總結與開放討論

- **總結要點**：
    - `asyncio` 讓爬蟲並行處理網路請求，大幅縮短執行時間。
    - 它節省資源，適合大規模或即時爬蟲。
    - 靈活的任務管理和錯誤處理提升爬蟲的穩定性。
- **開放問題**：
    - 「你覺得 `asyncio` 在爬蟲以外還能用在什麼地方？（如聊天伺服器、資料庫查詢）」
    - 「如果網站有反爬機制，`asyncio` 會遇到什麼挑戰？（如 IP 封鎖、速率限制）」
- **鼓勵實作**：建議學生回家用 `asyncio` 寫一個小型爬蟲（如抓取天氣資料），並分享結果。

### 教學建議

- **使用視覺化輔助**：畫圖展示同步爬蟲（單一時間軸）與非同步爬蟲（多任務並行）的差異。
- **現場演示**：運行範例程式，抓取真實網頁（如 `example.com`），讓學生看到即時效果。
- **分組討論**：將學生分組，每組設計一個爬蟲場景（如抓取電影評分、股票價格），並說明如何用 `asyncio` 實現。
- **注意學生程度**：若學生是初學者，聚焦於效率與簡單範例；若學生有經驗，可深入討論 `asyncio.Semaphore` 或反爬機制。

透過這個框架，學生能清楚理解 `asyncio` 在爬蟲中的實際價值，並透過問題與實作加深印象。





---

## 第2篇文章

教學生 asyncio 時，可以從簡單且易懂的範例開始，讓學生理解非同步程式設計的核心概念：協程（coroutine）、事件循環（event loop）、以及 async/await 語法。以下是幾個適合入門的教學重點與範例：

## 1. 介紹 async/await 與協程

- 用 `async def` 定義協程函式，使用 `await` 等待非同步操作完成。
- 範例：簡單的非同步等待與輸出

```python
import asyncio

async def say_hello():
    await asyncio.sleep(1)  # 非同步等待1秒
    print("hello")

asyncio.run(say_hello())
```

這個範例讓學生看到非同步函式的基本結構，以及 `asyncio.sleep` 是非同步等待的示範。

## 2. 多個非同步任務同時執行

- 示範多個任務如何同時執行，節省總時間。
- 範例：兩個非同步任務並行執行

```python
import asyncio
import time

async def echo(msg, delay):
    await asyncio.sleep(delay)
    print(msg)

async def main():
    start_time = time.time()
    task1 = asyncio.create_task(echo('任務1完成', 1))
    task2 = asyncio.create_task(echo('任務2完成', 2))
    await task1
    await task2
    print(f"總共花費 {time.time() - start_time:.2f} 秒")

asyncio.run(main())
```

此範例展示如何用 `asyncio.create_task` 建立任務，讓兩個任務同時進行，總時間約為較長任務的時間（約2秒），而非兩者相加的3秒。

## 3. 使用 asyncio.gather 同步等待多個任務

- 示範如何同時啟動多個協程並等待全部完成。
- 範例：同時發出多個 HTTP 請求（模擬）

```python
import asyncio

async def fake_request(id):
    await asyncio.sleep(1)
    print(f"請求{id}完成")
    return id

async def main():
    tasks = [fake_request(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print("所有請求完成，結果:", results)

asyncio.run(main())
```

這個範例讓學生理解 `asyncio.gather` 可以同時等待多個協程完成，並收集結果。

## 4. 簡單的同步 vs 非同步比較

- 示範同步執行多個任務的耗時與非同步執行的差異，強調非同步的效能優勢。

```python
import time

def task(id, delay):
    print(f"開始任務{id}")
    time.sleep(delay)
    print(f"任務{id}完成")

start = time.time()
task(1, 1)
task(2, 2)
print(f"同步總耗時: {time.time() - start:.2f} 秒")
```

與非同步版本比較，幫助學生理解非同步的意義。

---



