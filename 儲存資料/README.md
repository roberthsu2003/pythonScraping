# 儲存資料
資料只是顯示在終端機上是不夠，最好的方式是將收集的資料可以永久保持下來，這個方式就是儲存成為檔案。
## 下載多媒體檔案
下載多媒體的檔案有2種方式，一種是下載儲存在電腦上，一種是儲存這些媒體所在的網址。
僅儲存多媒體所在的位址的優點:

- 收集速度加快，並僅需要很少的頻寬
- 由於只是儲存網址，所以所占的空間將會很小
- 撰寫的程式將會比較容易，因為只有儲存網址，不需要下載檔案
- 可避免下載到大型的檔案


### 下載一個檔案

使用urllib.request.urlretrieve

使用這樣的方式適合下載一個已知的檔案，並知道檔案名稱和副檔名

```python
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup

res = requests.get('http://www.pythonscraping.com')
bs = BeautifulSoup(res.text, 'html.parser')
imageLocation = bs.find('a',{'id':'logo'}).find('img')['src']
urlretrieve(imageLocation, 'logo.jpg')

輸出:=================
('logo.jpg', <http.client.HTTPMessage at 0x7fbf94091c70>)
```

### 下載多個檔案，並自動依路徑存檔

```python
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

downloadDirectory = 'downloaded'
baseUrl = 'http://pythonscraping.com'

def getAbsoluteURL(baseUrl, source):
    if source.startswith('http://www.'):
        url = 'http://{}'.format(source[11:])
    elif source.startswith('http://'):
        url = source
    elif source.startswith('www.'):
        url = source[4:]
        url = 'http://{}'.format(source)
    else:
        url = '{}/{}'.format(baseUrl, source)
    
    if baseUrl not in url:
        return None
    
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace('www.','')
    path = path.replace(baseUrl, '')
    path = downloadDirectory + path
    directory = os.path.dirname(path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    return path
    
html = urlopen('http://www.pythonscraping.com')
bs = BeautifulSoup(html, 'html.parser')
downloadList = bs.findAll(src=True)

for download in downloadList:
    #print(download['src'])
    fileUrl = getAbsoluteURL(baseUrl,download['src'])
    if fileUrl is not None:
        print(fileUrl)
    
urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))
        
```

## 儲存資料至CSV
- Excel軟體可以支援CSV檔案

手動建立csv檔案

```python
import csv
csvFile = open('test.csv', 'w+')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))
finally:
    csvFile.close()
    
結果:=============
建立一個test.csv檔案，內容如下:
number,number plus 2,number times 2
0,2,0
1,3,2
2,4,4
3,5,6
4,6,8
5,7,10
6,8,12
7,9,14
8,10,16
9,11,18

```

取出表格資料，並儲為CSV檔案

```python
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bs = BeautifulSoup(html, 'html.parser')
table = bs.findAll('table', {'class':'wikitable'})[0]
rows = table.findAll('tr')

csvFile = open('editors.csv','wt+')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text().strip())
        writer.writerow(csvRow)
finally:
    csvFile.close()

結果:=============
產生editors.csv
```