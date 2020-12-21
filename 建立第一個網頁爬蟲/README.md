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
from urllib.request import urlopen

html = urlopen('http://pythonscraping.com/pages/page1.html')
print(html.read())


====================================
b'<html>\n<head>\n<title>A Useful Page</title>\n</head>\n<body>\n<h1>An Interesting Title</h1>\n<div>\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n</div>\n</body>\n</html>\n'
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
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(html.read(), 'html.parser') #HTML content is then transformed into a BeautifulSoup object
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

### bs = BeautifulSoup(html.read(), 'html.parser')
BeautifulSoup必需使用2個引數,第一個引數是html的內容,第二個引數是解析方式,這裏使用的是基本的**html.parser**,另外還有2種方式方式

1. 使用lxml

```
先安裝套件
>>> pip3 install lxml

bs = BeautifulSoup(html.read(), 'lxml'
```

2. 使用html5lib

```python
bs = BeautifulSoup(html.read(), 'html5lib')
```

## 確保連線正常和處理意外錯誤

```python
html = urlopen('http://www.pythonscraping.com/pages/page1.html')
```

上面這行程式有可能遇到2個錯誤

1. 不存在page1.html
2. 主機伺服器沒有發現

### 解決網頁沒有發現
第1個錯誤會產生HTTP錯誤,有可能是"404 Page Not Found"或是"500 Internal Server Error",當發生這個錯誤時urlopen()會丟出一個exception HTTPError, 我們就必需手動處理這個錯誤

```python
from urllib.request import urlopen
from urllib.error import HTTPError

try:
    html = urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)    
    #處理錯誤
else:
    print("沒有錯誤")
    #沒有發生錯誤
```

### 解決主機伺服器沒有發現
第2個錯誤是主機伺服器沒有發現，urlopen將會發出URLError，由於伺服器是負責發出HTTP 狀態碼，所以HTTPError例外不會被丟出。

```python
from urllib.request import urlopen 
from urllib.error import HTTPError 
from urllib.error import URLError

try:
    html = urlopen('https://pythonscrapingthisurldoesnotexist.com')
except HTTPError as e:
    print(e)
except URLError as e:
    print("沒有發現伺服器主機")
else:
    print("沒有發生錯誤")
    
結果:==============================
沒有發現伺服器主機
```

就算上面的2個錯誤，也不能肯定你要找的元素標籤有存在，如果元素標籤不存在網頁內，BeautifulSoup會傳出一個None的物件，當操作None物件時，將會丟出AttributeError例外。

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(html.read(), 'html.parser')
print(bs.header) #沒有header這個標籤
print(bs.header.h1) #None存取屬性會丟出AttributeError


結果=====================
None
AttributeError: 'NoneType' object has no attribute 'h1'
```

### 解決沒有發現標籤的解決方式如下程式

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(html.read(), 'html.parser')

try:
    badContent = bs.header.h1
except AttributeError as e:
    print('標籤沒有發現')
else:
    if badContent == None:
        print('標籤沒有發現')
    else:
        print('找到標籤')

結果:=========================
標籤沒有發現
```

### 整合所有問題並簡化程式碼

```python
from urllib.request import urlopen 
from urllib.error import HTTPError 
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
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

