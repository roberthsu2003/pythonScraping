# 儲存資料
資料只是顯示在終端機上是不夠，最好的方式是將收集的資料可以永久保持下來，這個方式就是儲存成為檔案。

有時希望收集大量資料，並且可能一天收集一次，也希望收集的資料完成的動作可以有通知的動作，例如發送line或是email

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

## 儲存資料至sqlite

### SQLite
QLite 和 MySQL 都是一種 RDBMS，資料庫是一種以表格（Table）作為基礎的資料儲存系統，每個表格由許多的行（Column，也稱 Field）與列（Row，也稱 Reocrd）所組成。

### SQLite優點及缺點

SQLite 如同它名稱中的 Lite，意指它在設定、管理和所需的資源方面都更加輕量。

#### 優點

 1. 容易設定。基於無伺服器的特性，你非常的容易安裝且零配置。
 2. 可攜且跨平台。SQLite 是基於單一文件所組成且格式定義明確的資料庫，使得它的可攜性和跨平台性極佳，備份也極度方便（你只需要使用 cp ）。
 3. 適合開發及測試。由於其自包含特性，在開發階段中你可以使用 SQLite 作為替代手段。

#### 缺點

 1. 不提供網路訪問
 2. 不適用大型應用程式
 3. 缺少提升效能的手段
 4. 沒有用戶管理

#### 應用場景
1. 應用場景
2. 嵌入式設備及物聯網
3. 作為磁碟文件的替代儲存格式
4. 中低流量網站
5. 資料分析。你能輕易地使用者種格式處理資料集，且輕易地將其分享給其他人使用。
6. 資料緩存。許多場景中會將 SQLite 作為資料緩存的手段，避免了網路往返和中央資料庫伺服器的負載。
7. 伺服器端資料庫。你可以使用 SQLite 作為伺服器端資料庫的底層儲存引擎。
8. 開發或測試階段的替代及臨時方案
9. 適合教育及培訓。輕易地設置性很適合用於 SQL 的教學引擎。

### MySQL的優點及缺點
MySQL 是最熱門的 RDBMS 之一，許多的網站及應用程式都使用它。你能使用 TCP / IP 協議來從資料庫接受或發送資料。

#### 優點

1. 功能豐富及強大。MySQL 支援絕大多數 RDBMS 都應有的功能。
2. 用戶管理功能
3. 內置許多安全功能
4. 更精細的交易及鎖定（ Transaction & Locking）
5. 更好的同步執行（Concurrency）

#### 缺點

1. 可攜性及跨平台性較差。
2. 可靠性問題。MySQL 針對某些功能的實現，相較其他 RDBMS 缺少些可靠性。
3. 開發速度放緩。儘管 MySQL 仍是開源的，但自從被收購以後開發進展已經緩慢。

#### 應用場景
1. Client/Serve 需通過網路連接資料庫的場景。SQLite 在網路文件系統的場景下有一定程度的延遲，且文件鎖定邏輯並不適用在許多網路文件系統的實現中，因此你應該考慮如 MySQL 這樣的 RDBMS。
2. 需要多個客戶訪問及使用同一個資料庫
3. 高流量網站
4. 需要高度的資料寫入量。SQLite 受到了單個寫入的局限，因此寫入量表現較差。
5. 更大規模的資料。如果你的資料增長到單個磁盤無法容入的大小，你應該考慮 MySQL 這類的 RDBMS，SQLite 僅支持最大 140 TB 的資料庫

> [參考來源](https://medium.com/erens-tech-book/sqlite-%E8%88%87-mysql-%E7%9A%84%E5%B7%AE%E5%88%A5-a14926030ddd)
> 
### 參考資料
#### sqlite [官方網站](https://docs.python.org/3/library/sqlite3.html)
#### sqlite [語法參考](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)
#### sqlite GUI視覺化工具 [DB Browser for SQLite](https://sqlitebrowser.org/dl/)

### 建立資料庫

```python
import sqlite3
conn = sqlite3.connect('example.db')
print("開啟資料庫成功")
結果:===================
開啟資料庫成功
```

### 建立資料表

```python
import sqlite3
conn = sqlite3.connect('example.db')
print("開啟資料庫成功")

c = conn.cursor()
c.execute('''CREATE TABLE COMPANY
(ID INT PRIMARY KEY NOT NULL,
NAME TEXT NOT NULL,
AGE INT NOT NULL,
ADDRESS CHAR(50),
SALARY REAL);
''')
print("company資料表建立")
conn.commit()
conn.close()

結果:=====================
開啟資料庫成功
company資料表建立
```

### insert 操作

```python
import sqlite3
conn = sqlite3.connect('example.db')
print("開啟資料庫成功")

c = conn.cursor()

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2, 'Allen', 25, 'Texas', 15000.00)")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3, 'Teddy', 23, 'Norway', 20000.00)")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00)")
conn.commit()
print("4筆資料建立成功")
conn.close()

結果:=================
開啟資料庫成功
4筆資料建立成功
```

### 選取資料

```python
import sqlite3
conn = sqlite3.connect('example.db')
print("開啟資料庫成功")

c = conn.cursor()
cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID={:d},Name={:s},ADDRESS={:s},SALARY={:.2f}\n".format(row[0], row[1], row[2], row[3]))
print("select 成功")
conn.close()

結果:======================
開啟資料庫成功
ID=1,Name=Paul,ADDRESS=California,SALARY=20000.00

ID=2,Name=Allen,ADDRESS=Texas,SALARY=15000.00

ID=3,Name=Teddy,ADDRESS=Norway,SALARY=20000.00

ID=4,Name=Mark,ADDRESS=Rich-Mond ,SALARY=65000.00

select 成功
```

### UPDATE操作

```python
import sqlite3
conn = sqlite3.connect('example.db')
print("開啟資料庫成功")
c = conn.cursor()
c.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
conn.commit()
print("總共更改的筆數:", conn.total_changes)
cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID={:d},Name={:s},ADDRESS={:s},SALARY={:.2f}\n".format(row[0], row[1], row[2], row[3]))
print("select 成功")
conn.close()

結果:====================
開啟資料庫成功
總共更改的筆數: 1
ID=1,Name=Paul,ADDRESS=California,SALARY=25000.00

ID=2,Name=Allen,ADDRESS=Texas,SALARY=15000.00

ID=3,Name=Teddy,ADDRESS=Norway,SALARY=20000.00

ID=4,Name=Mark,ADDRESS=Rich-Mond ,SALARY=65000.00

select 成功
```

### DELETE操作

```python
import sqlite3
conn = sqlite3.connect('example.db')
print("開啟資料庫成功")
c = conn.cursor()

c.execute("DELETE from COMPANY where ID=2;")
conn.commit()
print("總共刪除的筆數:", conn.total_changes)
cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID={:d},Name={:s},ADDRESS={:s},SALARY={:.2f}\n".format(row[0], row[1], row[2], row[3]))
print("select 成功")
conn.close()

結果:======================
開啟資料庫成功
總共刪除的筆數: 1
ID=1,Name=Paul,ADDRESS=California,SALARY=25000.00

ID=3,Name=Teddy,ADDRESS=Norway,SALARY=20000.00

ID=4,Name=Mark,ADDRESS=Rich-Mond ,SALARY=65000.00

select 成功
```

