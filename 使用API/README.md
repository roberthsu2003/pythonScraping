## 使用API
### 氣象開放平台

[氣象開放平台開發指南](https://opendata.cwb.gov.tw/devManual/insrtuction)

```python
import requests
import json

urlPath = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization=rdec-key-123-45678-011121314&format=JSON'
response = requests.get(urlPath)
response.encoding = 'utf-8'
if response.status_code == 200:
    try:
        jsonObj=response.json()
    except ValueError as e:
        print('格式不符合json')

        
#轉換成要使用的資料
usefulData = [];
opendata = jsonObj['cwbopendata']['location']
for location in opendata:
    oneLocation = {}
    oneLocation['縣市']=location['parameter'][0]['parameterValue']
    oneLocation['區域']=location['parameter'][2]['parameterValue']
    oneLocation['時間']=location['time']['obsTime']
    oneLocation['溫度']=float(location['weatherElement'][3]['elementValue']['value'])
    usefulData.append(oneLocation)

for one in usefulData:
    print(one['縣市'])
    print(one['區域'])
    print(one['時間'])
    print(one['溫度'])
    print('=====================')
    
    
輸出結果:=====================
雲林縣
臺西鄉
2021-02-20T15:00:00+08:00
18.6
=====================
臺南市
七股區
2021-02-20T15:00:00+08:00
19.8
=====================
臺東縣
成功鎮
2021-02-20T15:00:00+08:00
21.9
=====================
南投縣
南投市
2021-02-20T15:00:00+08:00
23.3
```

#### 建立sqlite資料庫

```python
#sqlite 資料庫
import sqlite3
query = """
CREATE TABLE 氣象觀測資料(縣市 VARCHAR(20), 區域 VARCHAR(20), 時間 VARCHAR(30), 溫度 REAL);
"""

#建立方法只能建立一次，無法覆蓋原來檔案
con = sqlite3.connect('氣象觀測資料.sqlite')
con.execute(query)
con.commit()
```

#### 新增資料

```python

for one in usefulData:    
    stmt = "INSERT INTO 氣象觀測資料 VALUES(?,?,?,?)"
    con.execute(stmt,(one['縣市'],one['區域'],one['時間'],one['溫度']))
    con.commit()
con.close()
```

#### 讀取資料

```python
con = sqlite3.connect('氣象觀測資料.sqlite')
cursor=con.execute('select * from 氣象觀測資料')
rows=cursor.fetchall()
rows
```