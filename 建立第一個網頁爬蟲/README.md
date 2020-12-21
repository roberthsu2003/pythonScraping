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

=======================================
<h1>An Interesting Title</h1>
<h1>An Interesting Title</h1>
<h1>An Interesting Title</h1>
<h1>An Interesting Title</h1>
```

### bs = BeautifulSoup(html.read(), 'html.parser')
BeautifulSoup必需使用2個引數,第一個引數是html的內容,第二個引數是解析方式,這裏使用的是基本的html.parser,另外還有2種方式方式

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