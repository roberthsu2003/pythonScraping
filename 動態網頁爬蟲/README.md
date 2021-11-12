## 動態網頁爬蟲(Selenium)

### 1. Selenium 介紹
Selenium提供了一個簡單的API應用程式介面（英語：Application Programming Interface），使用者可以利用Selenium Webdriver 編寫功能及測試(test)。

### 2. Selenium 安裝

在python裡執行以下程式碼，即可安裝Selenium套件。

```
pip install selenium
```


### 3. Webdriver 下載

[官網說明](https://pypi.org/project/selenium/)

要使用Selenium爬蟲前，Webdriver是必備的，而不同的瀏覽器會有不同的driver。以下提供四種常見的瀏覽器driver供大家參考及下載。

1. Chrome
2. Edge
3. Firefox
4. Safari

選定了瀏覽器，在下載前，請記得檢查目前電腦上的瀏覽器版本，再下載對應的Webdriver，之後也要適時更新版本以維護程式碼運行！

### 4. Chromedriver 使用

```python
# 載入需要的套件
from selenium import webdriver

# 指定exe檔案路徑
driver = webdriver.Chrome("絕對路徑\chromedriver”)
```

### 5.delay數秒後關閉視窗

```
time.sleep(3)
driver.close()
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
