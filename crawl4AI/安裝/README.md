# crawl4AI安裝

## 步驟1:安裝
1. 安裝crawl4ai
2. 安裝nest_asyncio

```bash
> pip install -U crawl4ai
> pip install nest_asyncio  #請看說明1
```

## 步驟2:檢查版本

```python
import crawl4ai
print(crawl4ai.__version__.__version__)
```

## 步驟3:設定

```bash
> crawl4ai-setup
```

## 步驟4:測試

```bash
> crawl4ai-doctor
```


## 說明1:
使用 crawl4ai（或其他使用 asyncio 的套件）時會遇到的問題，以下是完整且清楚的說明：

⸻

🧠 為何安裝 crawl4ai 後，還要安裝 nest_asyncio？

✅ 1. crawl4ai 是什麼？
	•	crawl4ai 是一個基於 Playwright 的非同步爬蟲工具，內部使用 asyncio 執行非同步任務（例如瀏覽器自動控制、網頁渲染與資料擷取等）。
	•	所以它的程式設計方式是「非同步的」，也就是會用到 async def / await / asyncio.run() 等語法。

⸻

✅ 2. 問題在哪裡？

在某些執行環境（如 Jupyter Notebook、IPython）中，asyncio.run() 會出錯！

這是因為：
	•	asyncio.run() 的工作是建立一個新的事件迴圈（event loop）。
	•	但在 Jupyter Notebook 這種互動環境中，Python 已經偷偷建立了一個事件迴圈。
	•	所以你在 Jupyter 中執行 crawl4ai，它內部如果用 asyncio.run()，就會出現錯誤：

RuntimeError: asyncio.run() cannot be called from a running event loop



⸻

✅ 3. nest_asyncio 的作用

nest_asyncio 讓你可以在已經有事件迴圈的環境中，重複使用它。

簡單說，它會幫你「打開 Jupyter Notebook 的鎖」，允許你在已存在的 event loop 裡面再跑非同步任務。

⸻

✅ 4. 解決方式（使用方式）

通常你會這樣搭配使用：

import nest_asyncio
nest_asyncio.apply()  # 開啟多層事件迴圈的支援

這樣 crawl4ai（或其他 async 程式）就可以在 Notebook、Colab、REPL 順利執行。

⸻

✅ 總結重點

套件	功能說明
crawl4ai	基於 async 的網頁爬蟲框架，需要事件迴圈（event loop）運作
nest_asyncio	解決「Jupyter 等環境已有事件迴圈」的衝突，允許重複使用 asyncio 事件迴圈

---

## 在jupyter notebook執行的方式

```python
# 安裝 nest_asyncio（第一次執行時才需要）
!pip install nest_asyncio

# 套用 nest_asyncio，讓 asyncio.run 在 Notebook 內可以正常執行
import nest_asyncio
nest_asyncio.apply()

# 範例 4.2：模擬非同步網路請求
import asyncio
import time

async def task(id, delay):
    print(f"開始任務 {id}")
    await asyncio.sleep(delay)
    print(f"任務 {id} 完成")

async def main():
    start = time.time()

    # 非同步執行兩個任務（並行）
    tasks = [task(1, 1), task(2, 2)]
    await asyncio.gather(*tasks)

    print(f"總耗時: {time.time() - start:.2f} 秒")

# 使用 asyncio.run 執行 main（已修補事件迴圈）
asyncio.run(main())
```



