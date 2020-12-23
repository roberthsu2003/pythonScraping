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

先取得所有頁面內容，並建立BeautifulSoup物件

