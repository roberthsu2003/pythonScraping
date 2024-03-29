# BeautifulSoup
## 安裝BeautifulSoup套件

```
>>> pip install beautifulsoup4
```

## 快速導覽
### 手動建立Html Code

```python
html_doc = """
<html>
<head>
<title>A Useful Page</title>
</head>
<body>
<h1>An Interesting Title</h1>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
</a>
,
<a class="sister" href="http://example.com/lacie" id="link2">
 Lacie
</a>
and
<a class="sister" href="http://example.com/tillie" id="link3">
Tillie
</a>
and they lived at the bottom of a well.
</p>

<div class='article'>
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute 
irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
deserunt mollit anim id est laborum.
</div>
</body>
</html>
"""
```

### 載入BeautifulSoup套件

- 使用BeautifulSoup實體方法prettify(), 輸出修飾過的html

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc,'html.parser')
print(soup.prettify())

輸出結果:===========
<html>
 <head>
  <title>
   A Useful Page
  </title>
 </head>
 <body>
  <h1>
   An Interesting Title
  </h1>
  <p class="title">
   <b>
    The Dormouse's story
   </b>
  </p>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
   </a>
   ,
   <a class="sister" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister" href="http://example.com/tillie" id="link3">
    Tillie
   </a>
   and they lived at the bottom of a well.
  </p>
  <div class="article">
   Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute 
irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
deserunt mollit anim id est laborum.
  </div>
 </body>
</html>
```

### 導覽目前內容

- 一些簡單方式導覽內容

#### 型別bs4.element.Tag

```python

soup.title

輸出:===========
<title>A Useful Page</title>
```

#### Tag實體屬性name

```python

soup.title.name

輸出:===========
'title'
```

#### Tag實體屬性string

```python

soup.title.string

輸出:===========
'A Useful Page'
```

#### Tag實體屬性parent

```python
soup.title.parent.name

輸出:===========
'head'
```

```python
soup.h1

輸出:===========
<h1>An Interesting Title</h1>
```

```python
soup.p

輸出:===========
<p class="title"><b>The Dormouse's story</b></p>
```

#### Tag['標籤屬性'],傳出list

```python
soup.p['class']

輸出:===========
['title']
```

```python
soup.a

輸出:===========
<a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
</a>
```

#### BeautifulSoup實體方法find_all(), 傳出ResultSet實體
- find_all(name,attrs,recursive,string,limit,**kwargs)

```python
soup.find_all('a')

輸出:===========
[<a class="sister" href="http://example.com/elsie" id="link1">
     Elsie
 </a>,
 <a class="sister" href="http://example.com/lacie" id="link2">
  Lacie
 </a>,
 <a class="sister" href="http://example.com/tillie" id="link3">
 Tillie
 </a>]
```

#### BeautifulSoup實體方法find(), 傳出Tag實體
- find(name,attrs,recursive,string,**kwargs)

```python
soup.find(id='link3')

輸出:===========
<a class="sister" href="http://example.com/tillie" id="link3">
Tillie
</a>
```

### 取出< a >標籤所有連結網址

- ResultSet實體是集合物件
- 取出的物件是Tag實體
- Tag實體方法get(),取出標籤屬性值

```python
for link in soup.find_all('a'):
    print(link.get('href'))

輸出:===========
http://example.com/elsie
http://example.com/lacie
http://example.com/tillie
```

### 取出所有的標籤元素所有文字內容

#### BeautifulSoup實體方法get_text()

```python
print(soup.get_text())

輸出:===========



A Useful Page


An Interesting Title
The Dormouse's story
Once upon a time there were three little sisters; and their names were

    Elsie

,

 Lacie

and

Tillie

and they lived at the bottom of a well.


Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute 
irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
deserunt mollit anim id est laborum.

```

