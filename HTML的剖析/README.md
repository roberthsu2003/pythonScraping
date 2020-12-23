## HTML的剖析

```python
bs.find_all('table')[4].find_all('tr')[2].find('td').find_all('div')[1].find('a')
```

當要擷取的資料，是位於比較深層的標籤，盡量不要使用上面的語法，這樣的方式，只要網頁內容稍有改變，這個擷取的語法可能會失敗。

在擷取標籤內容時，要考慮所在的位置，整體的內容，元素的屬性，元素的內容

### BeautifulSout的其它工具

- 學習如何透過屬性取得資料
- 學習如何從元素串列中取得資料
- 學習如何解析元素樹

```html
<span class="green"></span>

<span class="red"></span>
```

可以透過元素屬性class="xxx"或id="xxx"取得所有符合的標籤

> 範列來源
>
```
http://www.pythonscraping.com/pages/warandpeace.html
```

透過網頁開發工具(chrome 開發人員工具)，可以搜尋到class="red"有45個標籤,class="green"有42個標籤。如下

```html
<span class="red">Heavens! what a virulent attack!</span> replied 
<span class="green">the prince</span>,
not in the least disconcerted by this reception.
```

## 學習如何透過屬性取得資料,元素串列中取得資料

#### 先取得所有頁面內容，並建立BeautifulSoup物件 

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html.read(), 'html.parser')
print(type(bs))

結果:=======================
<class 'bs4.BeautifulSoup'>
```

建立BeautifulSoup實體

#### 使用 find_all function

```python
nameList = bs.findAll('span', {'class':'green'})
for name in nameList:
    print(type(name))
    print(name.get_text())
    
結果:=======================
<class 'bs4.element.Tag'>
Anna
Pavlovna Scherer
<class 'bs4.element.Tag'>
Empress Marya
Fedorovna
<class 'bs4.element.Tag'>
Prince Vasili Kuragin
<class 'bs4.element.Tag'>
Anna Pavlovna
<class 'bs4.element.Tag'>
St. Petersburg
<class 'bs4.element.Tag'>
the prince
...
```

使用BeautifulSoup實體findAll(標籤名稱, 標籤屬性)方法，取得list物件。list內是Tag實體，再使用Tag實體的get_text()方法取得元素內容。

#### find() and find_all()

官方文件說明find(),find_all(),2個的功能幾乎一樣

```
find_all(tag, attributes, recursive, text, limit, keywords)
find(tag, attributes, recursive, text, keywords)
```

#### find_all()取得多個標籤

```python
.find_all(['h1','h2','h3','h4','h5','h6'])
```

#### find_all()取得多屬性內容

```python
.find_all('span', {'class':{'green', 'red'}})
```

#### 引數 recursive

recursive引數預設是False，就是只搜尋最上層的標籤，不搜尋標籤內容的內容. 

#### 引數 text
搜尋元素內容有包含text內容的標籤

```
nameList = bs.find_all(text='the prince')
print(len(nameList))

結果:==========================
7
```

#### 引數 limit 限定取出的數量

預設為沒有限定

#### 引數 keyword

```python
title = bs.find(id='title')
```

取出有屬性id="title"的元素

範例:  

```python
title = bs.find(id='text')
print(title.getText())

結果:===================
"Well, Prince, so Genoa and Lucca are now just family estates of the
Buonapartes. But I warn you, if you don't tell me that this means war,
if you still try to defend the infamies and horrors perpetrated by
that Antichrist- I really believe he is Antichrist- I will have
nothing more to do with you and you are no longer my friend, no longer
my 'faithful slave,' as you call yourself! But how do you do? I see
I have frightened you- sit down and tell me all the news."

It was in July, 1805, and the speaker was the well-known Anna
Pavlovna Scherer, maid of honor and favorite of the Empress Marya
Fedorovna. With these words she greeted Prince Vasili Kuragin, a man
of high rank and importance, who was the first to arrive at her
reception. Anna Pavlovna had had a cough for some days. She was, as
she said, suffering from la grippe; grippe being then a new word in
St. Petersburg, used only by the elite.

All her invitations without exception, written in French, and
delivered by a scarlet-liveried footman that morning, ran as follows:

"If you have nothing better to do, Count [or Prince], and if the
prospect of spending an evening with a poor invalid is not too
terrible, I shall be very charmed to see you tonight between 7 and 10-
Annette Scherer."
```

get_text()，取出的內容如果有標籤，會全部移除

下方是相同的功能:

```python
bs.find_all(id='text')
bs.find_all('', {'id':'text'})
```

#### 下方是相同的功能:

```
bs.find_all(class='green') #會出錯

bs.find_all(class_='green')
bs.find_all('', {'class':'green'})
```

#### 取出有多個屬性的元素

```python
title = bs.find_all(id='title', class_='text')
```

## 解析元素樹

```
bs.tag.subTag.anotherSubTag
```

##### 範例網頁
```
http://www.pythonscraping.com/pages/page3.html
```

##### html架構

![](images/pic1.png)
