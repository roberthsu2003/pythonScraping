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

下面為html標籤套用css的語法

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

透過網頁開發工具(chrome 開發人員工具)，可以搜尋到class="red"有29個標籤,class="green"有38個標籤。如下

#### 使用chrome搜尋步驟
1. 使用chrome
2. 進入網頁
3. 使用開發人員工具
4. 使用開發人員工具的Network
5. chrome重新載入網頁
6. 使用Network內的Search
7. 點選搜尋結果


```html
<span class="red">Heavens! what a virulent attack!</span> replied 
<span class="green">the prince</span>,
not in the least disconcerted by this reception.
```

## 學習如何透過屬性取得資料,元素串列中取得資料
#### 先取得所有頁面內容，並建立BeautifulSoup物件 

```python
import requests
from bs4 import BeautifulSoup

res = requests.get('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(res.text, 'html.parser')

結果:=======================
<class 'bs4.BeautifulSoup'>
```

以上為建立BeautifulSoup實體

#### 使用 find_all() function

語法: find_all(name, attrs, recursive, string, limit, **kwargs)

find_all()方法，可以取得所有符合條件的Tag實體，並被包裝於ResultSet實體內

```python
nameList = bs.find_all(name='span', attrs={'class':'green'})
print(type(nameList))
for name in nameList:
    print(type(name))
    print(name.get_text())
    
結果:=======================
<class 'bs4.element.ResultSet'>
<class 'bs4.element.Tag'>
Anna
Pavlovna Scherer
<class 'bs4.element.Tag'>
Empress Marya
Fedorovna
<class 'bs4.element.Tag'>
Prince Vasili Kuragin
...
```

使用BeautifulSoup實體find_all(標籤名稱, 標籤屬性)方法，取得ResultSet物件。

ResultSet內是Tag實體，再使用Tag實體的get_text()方法取得元素內容。

get_text()方法只會取得所有的元素內容，而排除標籤名稱和所有的標籤屬性

#### find() and find_all()

```
find_all()語法:find_all(name, attrs, recursive, string, limit, **kwargs)

find()語法:find(name, attrs, recursive, string, **kwargs)

````

2個方法非常相似，find()語法，沒有limit的引數，因為find()方法只可以取得一個Tag實體

2個方法，95%只會使用到name,attrs的引數名稱

#### find_all()方法，搜尋不同的標籤名稱

name引數也可以使用list的語法，一次取得多到不同的標籤名稱

```python
.find_all(['h1','h2','h3','h4','h5','h6'])
```

#### find_all(),搜尋不同的屬性名稱

attrs引數-做用是的dict的語法，可以一次搜尋多個條件
attrs引數的dict內的vlaue可以使用set, 搜尋不同的屬性value

```python
.find_all('span', {'class':{'green', 'red'}})
```

#### 引數 recursive

recursive引數預設是True，向內搜尋. 

#### 引數 text

text的目的是搜尋元素內容有the prince`有多少個?`
最終取得的是NavigableString實體

```
nameList = bs.find_all(text='the prince')
print(type(nameList))
print(len(nameList))
print("=================")
for name in nameList:
    print(type(name))
    print(name)
    
輸出:===================
<class 'bs4.element.ResultSet'>
7
=================
<class 'bs4.element.NavigableString'>
the prince
<class 'bs4.element.NavigableString'>
the prince
<class 'bs4.element.NavigableString'>
the prince
<class 'bs4.element.NavigableString'>
the prince
<class 'bs4.element.NavigableString'>
the prince
<class 'bs4.element.NavigableString'>
the prince
<class 'bs4.element.NavigableString'>
the prince
```

#### 引數 limit 限定取出的數量

預設為沒有限定

如果有設定是取出最前面幾個

#### 引數 keyword

keyword引數最常使用的是id,class_

```python
title = bs.find(id='title', class_='text')
```

上方範例，取出同時有屬性id='title'和class_='text'的元素

上方範例只會取出一個標籤，原因是html內的id屬性值是不可以重複的

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

下方是相同的功能, 只取出id屬性值為text的標籤:

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

### BeautifulSoup常用的物件
- BeautifulSoup 物件
	- 例如上方的bs實體
- ResultSet 物件
- Tag 物件
- NavigableString 物件
- Comment 物件


## 解析元素樹

find_all function功能是利用標籤名和屬性擷取資料。

但是如果要利用樹狀結構的位置取得資料，可以利用下方語法，使用連續串接的手法，這樣的手法主要是抓取子元素，並且只抓取第一個元素

```
bs.tag.subTag.anotherSubTag
```

以下的範例將介紹的是抓取父元素,同階層元素

##### 範例網頁

```
http://www.pythonscraping.com/pages/page3.html
```

![](./images/pic2.png)

##### html架構

![](images/pic1.png)

#### 操控子元素和子孫元素

子元素，代表是父元素的下一個元素，子孫元素代表的是父元素下的所有元素。

例如這個範例，tr是table的`子元素`，tr,th,td,img和span全部是table的`子孫元素`

一般BeautifulSoup function是使用子孫元素。

bs.body.h1 所代表的意思尋找body內所有的子孫元素的第一個h1元素。

相同的，bs.div.find_all('img') 將尋找整個html的第一個div內，所有的子孫元素img

所以如果只想要取得所有的子元素，請使用.children屬性

```python
import requests
from bs4 import BeautifulSoup

res = requests.get('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(res.text, 'html.parser')
print(bs.find('table',{'id':'giftList'}).__class__)
trList = bs.find('table',{'id':'giftList'}).children
print(trList.__class__)

for child in trList:
    print(child.__class__)
    print(child)
    print("================")
        
結果:=====================================
<class 'bs4.element.Tag'>
<class 'list_iterator'>
<class 'bs4.element.NavigableString'>


================
<class 'bs4.element.Tag'>
<tr><th>
Item Title
</th><th>
Description
</th><th>
Cost
</th><th>
Image
</th></tr>
================
<class 'bs4.element.NavigableString'>


================
<class 'bs4.element.Tag'>
<tr class="gift" id="gift1"><td>
Vegetable Basket
</td><td>
This vegetable basket is the perfect gift for your health conscious (or overweight) friends!
<span class="excitingNote">Now with super-colorful bell peppers!</span>
</td><td>
$15.00
</td><td>
<img src="../img/gifts/img1.jpg"/>
</td></tr>
================
<class 'bs4.element.NavigableString'>


.
.
.
```

如果使用 .descendants屬性,會依序尋找所有子元素

```python
import requests
from bs4 import BeautifulSoup

res = requests.get('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(res.text, 'html.parser')

trList = bs.find('table',{'id':'giftList'}).descendants
print(trList.__class__)

for child in trList:
    print(child.__class__)
    print(child)
    print("================")
    
        
結果:===========================
<class 'generator'>
<class 'bs4.element.NavigableString'>


================
<class 'bs4.element.Tag'>
<tr><th>
Item Title
</th><th>
Description
</th><th>
Cost
</th><th>
Image
</th></tr>
================
<class 'bs4.element.Tag'>
<th>
Item Title
</th>
================
<class 'bs4.element.NavigableString'>

Item Title

================
<class 'bs4.element.Tag'>
<th>
Description
</th>
================
<class 'bs4.element.NavigableString'>

Description

================
<class 'bs4.element.Tag'>
<th>
Cost
</th>
================
<class 'bs4.element.NavigableString'>

Cost

================
<class 'bs4.element.Tag'>
<th>
Image
</th>
================
<class 'bs4.element.NavigableString'>

Image

================
.
.
.
```

#### 操控同一階層元素

-next_siblings() 後面的同階層
-previous_siblings() 前面的同階層

```python
import requests
from bs4 import BeautifulSoup

res = requests.get('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(res.text, 'html.parser')

print(bs.find('table',{'id':'giftList'}).tr.next_siblings.__class__)

for child in bs.find('table',{'id':'giftList'}).tr.next_siblings: #table內,第一個tr,相同階層的tr, 並不包含第一個
    print(child)

結果:===========================
<class 'generator'>
<tr class="gift" id="gift1"><td>
Vegetable Basket
</td><td>
This vegetable basket is the perfect gift for your health conscious (or overweight) friends!
<span class="excitingNote">Now with super-colorful bell peppers!</span>
</td><td>
$15.00
</td><td>
<img src="../img/gifts/img1.jpg"/>
</td></tr>


<tr class="gift" id="gift2"><td>
Russian Nesting Dolls
</td><td>
Hand-painted by trained monkeys, these exquisite dolls are priceless! And by "priceless," we mean "extremely expensive"! <span class="excitingNote">8 entire dolls per set! Octuple the presents!</span>
</td><td>
$10,000.52
</td><td>
<img src="../img/gifts/img2.jpg"/>
</td></tr>

.
.
.
```

尋找多個的功能有:
- next_siblings,previous_siblings

尋找一個的功能有:
- next_sibling,previous_sibling

#### 操控父元素

使用 .parent 或 .parents

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

print(bs.find('img',{'src':'../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())

結果:==================
$15.00   
```

### 正規則運算式

尋找有規則的文字，例如手機號碼，email，...

例如:
1. 想要一個a開頭，並且最少一個a字完
2. a後一定要有5個b
3. b後要c，偶數數量
4. 最給一定要e或d結尾

如aaaabbbbbccccd, aabbbbbcce

正規則的寫法:
aa*bbbbb(cc)*(d|e)

[透過Regex Pal網站驗証](https://www.regexpal.com)

```
aa*

*a 代表0個以上的a
```

```
bbbbb

明確的5個b
```

```
(cc)*

代表0個以上的cc
```

```
(d|e)

代表d或e
```

- 正規表示式可以指定與給定字串進行比較的模式。
- 以下是正規表示式的基本模式

| 模式 |	描述 | 範例 | 符合結果 |
|:-- | :-- | :-- | :-- |
| ^ |	在字串開頭匹配 | ^a | apple, asdf, a |
|$	| 在字串的結尾處匹配| [A-Z] * [a-z] * $ | ABCabc,zzzyx,Bob |
|.|	匹配任意一個字元(包含符號,數字,空白但不包括換行符）| b.d | bad, bzd, b&d, b d |
|[]|	匹配括號內的單個字元| [A-Z]* | APPLE,CAPITALS,QWERTY |
|[ ^ ]|不匹配括號內的單個字元| [ ^A-Z]* | apple, lowercase, qwerty|
|()|一組|(a* b)*|aaabaab,abaaab,ababaaaaab|
| *	| 給定字串中出現 0 次或更多次 | a * b * | aaaaaa,aaabbbbb,bbbbb |
| +	| 給定字串中出現 1 次或多次前面的 | a+b+ | aaaaab,aaabbbbbb,abbb |
| ?	| 給定字串中出現 0 次或 1 次 | ... | ... |
| {n} |	匹配給定字串中出現次數為 n | ... | ... |
| {n,} | 匹配給定字串中出現次數為 n 次或多次 | ... | ... |
|{n,m}	| 匹配給定字串中的出現次數為至少 n 個，最多 m 個 | a{2,3}b{2,3} | aabbb,aaabbb,aabb |
|?!| 不包含 |^(?![A-Z].)*$| no-caps-here, $ymb0ls a4e f!ne|
| \ | 特定字元 | \ . \ \ | .\ |
| \w	 | 此模式用於匹配單詞 | ... | ... |
| \W |	此模式用於匹配非單詞 | ... | ... |
| \s	 | 它將匹配空格。\ s 等於[\ t \ n \ r \ n] | ... | ... |
| \S |	它將匹配非空格 | ... | ... |
| \d	 | \ d 等於 [0-9]。它匹配字串中的數字 | ... | ... |
| \D |	匹配非數字 | ... | ... |
| \A	 | 匹配字串的開頭 | ... | ... |
| \Z |	匹配字串的結尾。如果有任何換行符，它將在換行符之前匹配 | ... | ... |
| \z |	匹配字串的結尾 | ... | ... |
| \G	 | \G 用於匹配最後一次匹配結束的點 | ... | ... |
| \b	 | 匹配在開頭或者結尾的空字元 | ... | ... |
| \B |	匹配不在開頭或者結尾的空字元 | ... | ... |


### email正規則表示法驗証

[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)

| 規則 | 範例 |
|:--|:--|
| email的@前方可以包含所有大寫字母，小寫字母，1-9數字和.符號+符號-符號 | [a-zA-Z0-9\ ._+]+ |
| 包含一個@符號 | @ |
| @的後方至少包含1個以上的小寫英文字和大寫英文字母 | [A-Za-z]+ |
| 接著要有一個.符號 | \ .|
| 後面至少要有一個com,org,edu,net | (com 直線 org 直線 edu 直線 net) |

### BeautifulSout整合正規則運算

範例網頁
```
http://www.python‐ scraping.com/pages/page3.html
```

頁面包含下面元素:
```
<img src="../img/gifts/img3.jpg">
```

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img',
                    {'src':re.compile('\.\.\/img\/gifts\/img.*\.jpg')})
for image in images:
    print(image.attrs['src'])

結果:================================
../img/gifts/img1.jpg
../img/gifts/img2.jpg
../img/gifts/img3.jpg
../img/gifts/img4.jpg
../img/gifts/img6.jpg

```

#### 存取元素屬性

```
擷取所有屬性
myTag.attrs 

或

擷取屬性的'src'
myTag.attrs['src']
```

