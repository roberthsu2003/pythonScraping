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
    
---

### 4. 簡單範例

#### 範例 4.1 簡單的同步 vs 非同步比較
- 示範同步執行多個任務的耗時與非同步執行的差異，強調非同步的效能優勢。

**同步**

```python
#同步
import time

def task(id, delay):
    print(f"開始任務{id}")
    time.sleep(delay)
    print(f"任務{id}完成")

start = time.time()
task(1, 1)
task(2, 2)
print(f"同步總耗時: {time.time() - start:.2f} 秒")

#=====output=====
#結果一樣是3秒
```



#### 範例 4.2：模擬非同步網路請求

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

## 5. ‼️重要觀念
asyncio 非常核心且重要的觀念。

### 1. 呼叫 async def 函數得到的是「協程物件」，而不是結果
在傳統的同步 (synchronous) Python 程式中，當你呼叫一個函數時，程式會立即進入該函數執行，直到函數 return 結果為止。

然而，在非同步 (asynchronous) 程式中，當你呼叫一個用 async def 定義的函數時，它並不會馬上執行裡面的程式碼。相反地，它會立即回傳一個 協程物件 (coroutine object)。

你可以把這個協程物件想像成一個「任務的執行計畫」或「食譜」。

fetch_data(url, delay)：這就像是準備好一張寫著「去某個 url 拿資料，中間要等 delay 秒」的食譜。你只是拿到了這張食譜，但還沒有開始動手做菜。
tasks = [...]：這行程式碼就是把多張這樣的「食譜」（多個協程物件）搜集成一個列表 tasks。

所以，當 tasks = [fetch_data(url, delay) for url, delay in urls] 這行執行完畢時，你得到的 tasks 是一個像下面這樣的列表，裡面裝滿了待執行的「計畫」，但沒有任何一個計畫被真正啟動。

```
[<coroutine object fetch_data at 0x...>, <coroutine object fetch_data at 0x...>, ...]
```

### 2. 如何「執行」這些計畫？

這些「計畫」（協程物件）需要被提交給事件迴圈 (Event Loop) 來執行。事件迴圈就像一個總指揮官，它會負責調度所有任務。

範例程式碼中，執行這些任務的指令是這一行：

```python
results = await asyncio.gather(*tasks)

===說明===

asyncio.gather(*tasks)：這個函數的功能就是告訴事件迴圈：「嘿，我這裡有一堆任務 (tasks 列表)，請你『同時』去執行它們。」

await：這個關鍵字則是告訴 main 函數：「請在這裡暫停，直到 asyncio.gather 把所有任務都完成後，再繼續往下走。」

```

### 3. 流程總結

#### 1. 定義一個「協程函數」，這是一個任務的藍圖。
```
async def fetch_data(url, delay):
    print(f"開始抓取 {url}") # 這行在 gather 執行後才會印出
    await asyncio.sleep(delay)
    print(f"完成抓取 {url}")
    return f"資料來自 {url}"
```


#### 2. 呼叫 fetch_data，但只會得到「協程物件」(執行的計畫)。

這裡只是在建立計畫列表，尚未執行任何 print 或 sleep。

tasks = [fetch_data(url, delay) for url, delay in urls]

print(f"已建立 {len(tasks)} 個任務計畫，準備交給事件迴圈執行。")

#### 3. 使用 asyncio.gather 將所有任務計畫提交給事件迴圈。
事件迴圈開始執行後，才會真正進入 fetch_data 函數，並印出 "開始抓取..."。 

當遇到 await asyncio.sleep() 時，事件迴圈會聰明地切換到其他未完成的任務。

results = await asyncio.gather(*tasks)

print("所有資料：", results)

#### 4. 啟動整個非同步程式，運行 main 協程。

```
asyncio.run(main())
```

簡單來說：

fetch_data(url, delay) 創造了一個「待辦事項」。 tasks = [...] 則是把所有「待辦事項」整理成一個清單。 await asyncio.gather(*tasks) 才是真正把這份清單交給經理（事件迴圈）去執行。

這個「延遲執行」的特性正是 asyncio 強大的地方，它允許我們先把所有 I/O 密集型的任務都規劃好，然後一次性地交給事件迴圈去並行處理，從而大大提升程式效率。

---


#### ‼️重要觀念



它觸及了 asyncio 中「等待」與「並行」的核心差異。

#### `await` 的作用：立即執行並等待

**非同步** 

```python
import asyncio
async def task(id, delay):
    print(f'開始任務{id}')
    await asyncio.sleep(delay)
    print(f'任務{id}完成')

start = time.time()
async def main():
    await task(1,1)
    await task(2,2)
    
await main()
print(f'同步總耗時:{time.time() - start:.2f}秒')

#=====output=====
#結果一樣是3秒
``` 


當你在一個協程物件 (coroutine object) 前面加上 `await` 關鍵字時，它的意思是：

> **「立即將這個任務交給事件迴圈去執行，並且在這裡暫停，直到這個任務完成為止，然後再繼續執行下一行程式碼。」**

讓我們分解 `await task(1, 1)` 的步驟：

1. **`task(1, 1)`**：這部分和之前一樣，它會呼叫 `async def task(...)` 函數，並立即回傳一個「協程物件」（一個待辦事項的計畫）。
2. **`await`**：這是關鍵。`await` 關鍵字接收到這個協程物件後，會立刻把它提交給事件迴圈執行。`main` 函數的執行緒會在這裡「卡住」（但不會阻塞整個程式，事件迴圈仍然可以去跑別的任務），專心等待 `task(1, 1)` 這個協程執行完畢。

3. 循序執行 (Sequential Execution)

```python
# 執行並等待任務1完成
await task(1, 1) 

# 任務1完成後，才開始執行並等待任務2完成
await task(2, 2)

print(f"總共花費 {time.time() - start_time:.2f} 秒")
```

`任務 1 開始執行... 任務 1 完成，耗時 1 秒 任務 2 開始執行... 任務 2 完成，耗時 2 秒 總共花費 3.00 秒`

**說明**：`await task(2, 2)` 必須等到 `await task(1, 1)` 完全結束後才能開始。總時間是所有任務時間的總和 (1 + 2 = 3 秒)。

**使用asyncio.gather 同步等待多個任務, 並行執行 (Concurrent Execution)**  

```python
#非同步
import asyncio
async def task(id, delay):
    print(f'開始任務{id}')
    await asyncio.sleep(delay)
    print(f'任務{id}完成')

start = time.time()
async def main():
    tasks = [task(1,1), task(2,2)]
    await asyncio.gather(*tasks)
await main()
print(f'同步總耗時:{time.time() - start:.2f}秒')
```

`任務 1 開始執行... 任務 2 開始執行... 任務 1 完成，耗時 1 秒 任務 2 完成，耗時 2 秒 總共花費 2.00 秒`

**說明**：`asyncio.gather` 會同時啟動所有任務。事件迴圈會在任務之間巧妙切換。總時間取決於耗時最長的那個任務（2 秒）。

| **語法**                      | **執行方式**            | **意義**              | **使用時機**                     |
| --------------------------- | ------------------- | ------------------- | ---------------------------- |
| `await coro()`              | **循序 (Sequential)** | 「執行這個，等它做完，再做下一個。」  | 當後續的程式碼需要依賴前一個非同步任務的結果時。     |
| `await asyncio.gather(...)` | **並行 (Concurrent)** | 「把這些任務全部開始，等它們都做完。」 | 當你有一批獨立的非同步任務，希望它們同時執行以節省時間。 |

**使用asyncio.create_task(task(1,1))的並行 (Concurrent)**

```python
import asyncio
async def task(id, delay):
    print(f'開始任務{id}')
    await asyncio.sleep(delay)
    print(f'任務{id}完成')

start = time.time()
async def main():
    task1 = asyncio.create_task(task(1,1))
    task2 = asyncio.create_task(task(2,2))
    await task1
    await task2
   
    
await main()
print(f'同步總耗時:{time.time() - start:.2f}秒')
```

 `asyncio` 中實現**並行 (Concurrency)** 的一個非常關鍵的語法。

`task1 = asyncio.create_task(task(1, 1))`

讓我們一步步拆解它，並解釋它為什麼如此重要。

#### 1. `task(1, 1)`：建立一個「協程物件」

首先，`task(1, 1)` 這部分並不會立即執行 `task` 函數內的程式碼。因為 `task` 是用 `async def` 定義的，呼叫它只會回傳一個**協程物件 (coroutine object)**。

你可以把它想像成一個「待辦事項的計畫書」，裡面寫著要執行的步驟，但還沒有人開始動手。

### 2. `asyncio.create_task(...)`：將「計畫」變成「正在執行的任務」

這是最關鍵的一步。`asyncio.create_task()` 函數的作用是：

> **接收一個協程物件（計畫書），並將它提交給事件迴圈 (Event Loop)，告訴事件迴圈：「請立刻開始執行這個任務，不要等我！」**

它會將協程物件包裝成一個 `Task` 物件。這個 `Task` 物件會被事件迴圈排入行程，並在下一個可用的時間點開始執行。

最重要的是，`asyncio.create_task()` **不會**讓當前的程式（例如 `main` 函數）停下來等待。它提交任務後，程式會立刻繼續往下執行下一行。這就是實現並行的核心。

### 3. `task1 = ...`：取得任務的「控制權」

`asyncio.create_task()` 會立即回傳一個 `Task` 物件，我們將它存到 `task1` 變數中。

這個 `task1` 物件非常有用，它就像是那個正在背景執行的任務的「遙控器」或「控制權」。你可以透過它：

- **`await task1`**: 在未來的某個時間點，等待這個任務完成並取得其結果。
- **`task1.cancel()`**: 取消這個任務。
- **`task1.done()`**: 檢查任務是否已經完成。

### 範例：`create_task` vs `await`

讓我們用一個具體的例子來比較 `create_task` 和直接 `await` 的差別。

```
import asyncio
import time

async def task(id, delay):
    print(f"任務 {id}：開始執行，將等待 {delay} 秒...")
    await asyncio.sleep(delay)
    print(f"✅ 任務 {id}：完成！")
    return f"結果來自任務 {id}"

async def main():
    start_time = time.time()
    
    # --- 使用 asyncio.create_task ---
    # 立即安排任務1和任務2去執行，但主程式不等待，繼續往下走
    print("主程式：正在建立任務...")
    task1 = asyncio.create_task(task(1, 2))  # 任務1需要2秒
    task2 = asyncio.create_task(task(2, 1))  # 任務2需要1秒
    print("主程式：任務已建立並在背景執行，我現在可以做點別的事...")
    
    # 在這裡，task1 和 task2 已經在並行執行了
    
    # 現在，我們決定等待這兩個任務完成
    print("主程式：等待所有任務完成...")
    result1 = await task1
    result2 = await task2
    
    print(f"\n所有任務完成！總耗時: {time.time() - start_time:.2f} 秒")
    print(f"結果: {result1}, {result2}")

asyncio.run(main())

```

```plaintext
主程式：正在建立任務...
主程式：任務已建立並在背景執行，我現在可以做點別的事...
主程式：等待所有任務完成...
任務 1：開始執行，將等待 2 秒...
任務 2：開始執行，將等待 1 秒...
✅ 任務 2：完成！
✅ 任務 1：完成！

所有任務完成！總耗時: 2.00 秒
結果: 結果來自任務 1, 結果來自任務 2

```

1. `create_task` 讓 `任務1` 和 `任務2` 幾乎同時開始執行。
2. 主程式不需要等待，可以繼續執行 `print` 語句。
3. 總耗時取決於最長的任務（`任務1` 的 2 秒），而不是所有任務時間的總和 (2 + 1 = 3 秒)。這證明了它們是**並行**執行的。

如果我們改成直接 `await`，就會變成**循序 (Sequential)** 執行，總耗時會是 3 秒。

### 總結

| **語法**                               | **作用**                          | **執行方式**            |
| ------------------------------------ | ------------------------------- | ------------------- |
| `await task(...)`                    | 執行並**等待**單一任務完成，才會繼續。           | **循序 (Sequential)** |
| `t = asyncio.create_task(task(...))` | **立即安排**任務在背景執行，不等待，可透過 `t` 控制。 | **並行 (Concurrent)** |
| `await asyncio.gather(...)`          | 一次性**安排並等待**多個任務完成。             | **並行 (Concurrent)** |



簡單來說，`asyncio.create_task()` 是 `asyncio` 中啟動背景任務、實現真正並行的基礎工具。而 `asyncio.gather` 則是一個更方便的高階 API，它在內部也是幫你對每個協程使用了類似 `create_task` 的機制，然後一次性等待它們全部完成。
---



### 討論框架：`asyncio` 在爬蟲中的好處

#### 1. 爬蟲與非同步的關聯

- **問題**：
    - 「假設你要從 100 個網頁抓取資料，每個網頁需要 1 秒回應，如果用傳統同步方式，需要多久？如果能同時發送多個請求呢？」
    - 「什麼是爬蟲中最耗時的部分？（提示：網路請求、等待回應）」
- **目的**：爬蟲中的 I/O 等待是瓶頸，非同步程式可以解決這個問題。
- **簡介**：說明 `asyncio` 讓爬蟲能並行處理多個網路請求，減少等待時間。

#### 2. 核心好處： `asyncio` 的優勢

以下是 `asyncio` 在爬蟲中的主要好處，建議逐一與學生探討，並搭配簡單範例或比喻。

- **好處 1：提升效率，減少總執行時間**
    - **說明**：同步爬蟲按順序等待每個網頁回應，總時間是所有請求時間的總和。`asyncio` 允許並行發送請求，總時間接近最慢的單一請求。
    - **比喻**：「同步爬蟲像一個人在 10 家店排隊買東西，每次都要等結帳完才能去下一家。非同步爬蟲像同時派 10 個機器人去買，總時間只取決於最慢的那家店。」
    - **問題**：「如果抓 100 個網頁，同步需要 100 秒，非同步可能只需要 5 秒，你覺得這對什麼場景特別有用？（如大規模資料收集）」
    - **範例程式**：

```python
import asyncio
import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"抓取{url}完成")
            return await response.text()

async def main():
    urls = ["https://example.com", "https://python.org", "https://github.com"]
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for url, content in zip(urls, results):
        print(f"{url} 的內容：\n{content[:200]}...\n")  # 只顯示前200字，避免太長

await main()
```

**說明**：使用 `aiohttp`（支援非同步的 HTTP 庫）抓取多個網頁，展示並行請求的效率。

- **好處 2：節省資源，輕量級並行**
    - **說明**：`asyncio` 使用單執行緒的事件迴圈管理多個任務，相比多執行緒或多進程爬蟲，記憶體和 CPU 使用量更低。
    - **比喻**：「多執行緒像開 100 輛車同時送貨，每輛車耗油又占路。`asyncio` 像一個高效的快遞員，快速切換路線，只用一輛車完成所有送貨。」
    - **問題**：「如果你的電腦只有 4 核 CPU，多執行緒爬蟲能開幾個執行緒？`asyncio` 為什麼能處理更多任務？」
    - **討論**：在伺服器上運行爬蟲時，`asyncio` 能支援數千個並行請求，適合高併發但低計算需求的任務。
    - 
- **好處 3：靈活控制任務與錯誤處理**
    - **說明**：`asyncio` 提供 `asyncio.gather`、`asyncio.create_task` 等工具，可輕鬆管理多個任務的執行順序，並處理請求失敗的情況。
    - **範例**：展示如何處理超時或失敗的請求：

```python
import asyncio
import aiohttp

async def fetch_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,timeout=2) as response:
                return await response.text()
    except Exception as e:
        print(f'抓取{url}失數:{e}')
        return None

async def main():
    urls =  ["https://example.com", "https://invalid-url", "https://python.org"]
    results = await asyncio.gather(*[fetch_url(url) for url in urls], return_exceptions=True)
    for url, content in zip(urls, results):
        if content is None:
            print(f"{url} 發生錯誤\n")
        else:
            print(f"{url} 的內容：\n{content[:200]}...\n")  # 只顯示前200字，避免太長

await main()
```

**問題**：「如果一個網頁超時或失敗，會影響其他請求嗎？如何改進程式來重試失敗的請求？」

- **好處 4：支援大規模爬蟲與即時應用**
    - **說明**：`asyncio` 適合抓取大量網頁（如新聞網站、電商價格）或即時應用（如監控網站更新）。
    - **案例**：假設要監控 1000 個商品價格，同步爬蟲可能需要數小時，`asyncio` 可在數分鐘內完成。
    - **問題**：「如果要每 10 分鐘檢查一次網站更新，`asyncio` 怎麼幫你節省時間和資源？」

#### 3. 實際案例：聯想應用場景

- **案例分享**：
    - **新聞爬蟲**：用 `asyncio` 同時抓取多個新聞網站的頭條，快速彙整最新資訊。
    - **電商價格監控**：並行檢查多個電商平台的商品價格，找出最優惠的選項。
    - **API 批量請求**：從天氣 API 抓取多個城市的即時資料，整合成報表。
- **問題**：
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





