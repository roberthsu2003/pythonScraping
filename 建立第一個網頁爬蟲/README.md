## 建立第一個網頁爬蟲
### 網頁爬蟲的基本動作
1. 下載網頁
2. 取出所需的資料
3. 儲存資料
4. 移至下一頁面，重覆上面3個動作

### 下載整網頁內容
- 使用urllib package 內的 request module 內的 urlopen()這個function
- urlopen()可以透過internet來讀取資料(html檔案,影像檔或其他任何檔案)

```python
import requests
res = requests.get("http://pythonscraping.com/pages/page1.html")
print(res.text)


====================================
<html>
<head>
<title>A Useful Page</title>
</head>
<body>
<h1>An Interesting Title</h1>
<div>
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
</div>
</body>
</html>
```

## BeautifulSoup

這個package可以幫助我們利用python物件，有效的取得HTML架構內的資料。

### 安裝 BeautifulSoup

```
$ pip install beautifulsoup4
```

### 測試是否安裝成功,如果沒有發生錯誤,代表安裝成功

```python
from bs4 import BeautifulSoup
```

### 使用BeautifulSoup

取出page1.html內的第一個h1元素

```
import requests
from bs4 import BeautifulSoup

res = requests.get('http://pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(res.text, 'html.parser') #HTML content is then transformed into a BeautifulSoup object
print(bs.h1)
print(bs.html.body.h1)
print(bs.html.h1)
print(bs.body.h1)

結果:=======================================
<h1>An Interesting Title</h1>
<h1>An Interesting Title</h1>
<h1>An Interesting Title</h1>
<h1>An Interesting Title</h1>
```

### bs = BeautifulSoup(res.text, 'html.parser')
BeautifulSoup必需使用2個引數,第一個引數是html的內容,第二個引數是解析方式,這裏使用的是基本的**html.parser**,另外還有2種方式方式

1. 使用lxml

```
先安裝套件
>>> pip3 install lxml

bs = BeautifulSoup(html.read(), 'lxml'
```

2. 使用html5lib

```python
bs = BeautifulSoup(res.text, 'html5lib')
```

## 確保連線正常和處理意外錯誤

```python
res = requests.get('http://www.pythonscraping.com/pages/page1.html')
```

上面這行程式有可能遇到2個錯誤

1. 不存在page1.html
2. 主機伺服器沒有發現

### 解決網頁沒有發現
第1個錯誤會產生HTTP錯誤,有可能是"404 Page Not Found"或是"500 Internal Server Error",當發生這個錯誤時res.raise_for_status()會丟出一個exception HTTPError, 我們就必需手動處理這個錯誤

```python
import requests
from requests import ConnectionError,HTTPError,Timeout

try:
    res = requests.get('http://www.pythonscraping.com/pages/page1.html')
    res.raise_for_status()
except HTTPError as e:
    print(e)    
    #處理錯誤
else:
    print("沒有錯誤")
    #沒有發生錯誤
```

### 解決主機伺服器沒有發現

第2個錯誤是主機伺服器沒有發現，request.get()將會發出ConnectionError

```python
import requests
from requests import ConnectionError,HTTPError,Timeout

try:
    res = requests.get("https://pythonscrapingthisurldoesnotexist.com")    
    res.raise_for_status()    
except ConnectionError:
    print('找不到伺服器')
except HTTPError:
    print('網頁找不到')
except Timeout:
    print('超過時間沒有回應')
else:
    print('沒有發生問題')    
結果:==============================
找不到伺服器
```

就算上面沒有產生2個錯誤，也不能肯定你要找的元素標籤有存在，如果元素標籤不存在網頁內，BeautifulSoup會傳出一個None的物件，當操作None物件時，將會丟出AttributeError例外。

```python
import requests
from bs4 import BeautifulSoup

res = requests.get('http://pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(res.text, 'html.parser')
print(bs.header) #沒有header這個標籤
print(bs.header.h1) #None存取屬性會丟出AttributeError


結果=====================
None
AttributeError: 'NoneType' object has no attribute 'h1'
```

### 解決沒有發現標籤的解決方式如下程式

```python
import requests
from bs4 import BeautifulSoup

res = requests.get('http://pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(res.text, 'html.parser')

try:
    badContent = bs.header.h1
except AttributeError as e:
    print('標籤header沒有發現')
else:
    if badContent == None:
        print('標籤h1沒有發現')
    else:
        print('找到標籤')

結果:=========================
標籤header沒有發現
```

### 整合所有問題並簡化程式碼

```python
import requests
from requests import ConnectionError,HTTPError,Timeout
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
    except ConnectionError as e:
        return None
    except HTTPError as e:
        return None
    
    try:
        bs = BeautifulSoup(res.text, 'html.parser')
        title = bs.body.h1        
    except AttributeError as e:
        return None
    
    return title

title = getTitle('http://www.pythonscraping.com/pages/page1.html')

if title == None:
    print("沒有發現標籤")
else:
    print(title)    
結果:==================================
<h1>An Interesting Title</h1>
```

