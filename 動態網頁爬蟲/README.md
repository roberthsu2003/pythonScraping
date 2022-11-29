## 動態網頁爬蟲(Selenium)

###  Selenium 介紹
Selenium提供了一個簡單的API應用程式介面（英語：Application Programming Interface），使用者可以利用Selenium Webdriver 編寫功能及測試。

## 安裝套件
- 2個套件必需安裝
- selenium套件
- webdriver安裝

###  Selenium 安裝


在python裡執行以下程式碼，即可安裝Selenium套件。

```
pip install selenium
```


###  Webdriver 下載
#### 安裝有4種方法，可以選擇其中一種

[官網說明](https://pypi.org/project/selenium/)

要使用Selenium爬蟲前，Webdriver是必備的，而不同的瀏覽器會有不同的driver。以下提供四種常見的瀏覽器driver供大家參考及下載。

1. Chrome
2. Edge
3. Firefox
4. Safari

選定了瀏覽器，在下載前，請記得檢查目前電腦上的瀏覽器版本，再下載對應的Webdriver，之後也要適時更新版本以維護程式碼運行！

###  Chromedriver (手動下載)使用

```python
# 載入需要的套件
from selenium import webdriver

# 指定exe檔案路徑
driver = webdriver.Chrome("絕對路徑\chromedriver”)
```

###  使用webdriver-manager,自動下載(並且會自動更新,建議使用)

- webdriver-manager是third party開發,下載管理不同的brower有不同的語法。請參考以下網址
[webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)

```
pip install webdriver-manager
```

```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```


### 撰寫selenium的有8個流程
1. 建立一個session(開始一個工作)

```python
    driver = webdriver.Chrome()
```

2. 要求driver的browser瀏覽網頁

```python
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
```

3. 取得browser的資訊，或更改資料
	- browser size / position, cookies, alerts
	- [driver的資訊](./browser_infoomation.ipynb)

```python
    title = driver.title
```

4. 建立等待策略

- [等待策略細節說明](./wait_strategy.ipynb)

```python
    driver.implicitly_wait(0.5)
```

5. 取得網頁元素

```python
    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
```

6. 模擬網頁元素動作

```python
    text_box.send_keys("Selenium")
    submit_button.click()
```

7. 取得網頁元素資訊

```python
    value = message.text
```

8. 結束session工作

```python
    driver.quit()
```

9. 關閉browser

```python
	  driver.close()
```


### webdriver自動下載簡易範例
- [Browser interactions](https://www.selenium.dev/documentation/webdriver/interactions/)

```python
#使用webdriver-manager自動下載管理
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://www.selenium.dev/selenium/web/web-form.html") 
title = driver.title
assert title == "Web form"
driver.implicitly_wait(0.5)
text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
value = message.text

assert value == "Received!"
driver.quit()
#driver.close()
```



### 5. 整合BeautifulSoup

- driver.page_source取得所有的網頁內容

```python
from selenium import webdriver 
import time
driver = webdriver.Chrome('/Users/roberthsu2003/Downloads/chromedriver') 
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html') 
time.sleep(3)
print(driver.page_source)
driver.close()

===========輸出結果
<html><head>
<title>Some JavaScript-loaded content</title>
<script src="../js/jquery-2.1.1.min.js"></script>

</head>
<body>
<div id="content">Here is some important text you want to retrieve! <p></p><button id="loadedButton">A button to click!</button></div>

<script>
$.ajax({
    type: "GET",
    url: "loadedContent.php",
    success: function(response){

	setTimeout(function() {
	    $('#content').html(response);
	}, 2000);
    }
  });

function ajax_delay(str){
 setTimeout("str",2000);
}
</script>

</body></html>
```


## 實際案例
[台灣高鐵線上時刻表與票價查詢](./台灣高鐵.ipynb)
