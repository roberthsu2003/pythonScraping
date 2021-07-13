# 使用requests
## [文件參考](https://requests.readthedocs.io/en/master/)

## 安裝requests
```python
$ pip install requests
```

## 請求網頁(Request)
### 建立一個網頁get請求

```python

import requests
res = requests.get('https://api.github.com/events')
```

現在，我們得到一個名為res的response物件，所有網站回應的資訊全部儲存於res內，稍後再學習如何透過res取出內容

### 建立一個網頁post請求

```python
res = requests.post('https://httpbin.org/post', data={'key':'value'})
```

### 建立put,delete,head,options的請求

```python
 res = requests.put('https://httpbin.org/put', data = {'key':'value'})
 res = requests.delete('https://httpbin.org/delete')
 res = requests.head('https://httpbin.org/get')
 res = requests.options('https://httpbin.org/get')
```

### 傳遞參數給網址
網址有時有詢問字串(URL's query string),這詢問字串是一組一組所組合而成的，緊接在網址的後方，httpbin.org/get?`key=val&key1=val1&key2=val2`，這一組一組的詢問字串也可以用程式的方式產生。

```python
 payload = {'key1': 'value1', 'key2': 'value2'}
 r = requests.get('https://httpbin.org/get', params=payload)
 
 #查看請求時的URL字串
 print(r.url)
 
 結果:====================
 https://httpbin.org/get?key2=value2&key1=value1
```


## 回應文字內容(Response)

response物件內的txt就是傳回的內容

```python
import requests
res = requests.get('https://api.github.com/events')
print(res.text)

結果:===================
[{"id":"14750819243","type":"ForkEvent","actor":{"id":7353208,"login":"mlefrancois19","display_login":"mlefrancois19","gravatar_id":"","url":"https://api.github.com/users/mlefrancois19","avatar_url":"https://avatars.githubusercontent.com/u/7353208?"},"repo":{"id":323625568,"name":"hotwired/hotwire-rails-demo-chat","url":"https://api.github.com/repos/hotwired/hotwire-rails-demo-chat"},"payload":{"forkee":{"id":327786383,"node_id":"MDEwOlJlcG9zaXRvcnkzMjc3ODYzODM=","name":"hotwire-rails-demo-chat","full_name":"mlefrancois19/hotwire-rails-demo-chat","private":false,"owner":{"login":"mlefrancois19","....
```

傳回的內容會自動解碼，如果自動解碼的格式不正確，可以使用手動的方式設定解碼格式

查詢解碼格式:

```python
res.encoding

結果:==============
'utf-8'
```

手動更改解碼格式:

```python
res.encoding = 'ISO-8859-1'
```

### 回應位元組內容
使用r.content回應位元組內容

```python
res.content

結果:=======================
b'[{"id":"14750819243","type":"ForkEvent","actor":{"id":7353208,"login":"mlefrancois19","display_login":"mlefrancois19","gravatar_id":"","url":"https://api.github.com/users/mlefrancois19","avatar_url":"https://avatars.githubusercontent.com/u/7353208?"}....
```

> 注意:第一個字是`b'xxx'`代表是位元組內容

下載一個圖檔，並建立一個圖檔
```python
from PIL import Image
from io import BytesIO
r = requests.get('https://res.klook.com/image/upload/c_crop,h_668,w_1687,x_0,y_0/c_fill,w_960,h_460,f_auto/w_80,x_15,y_15,g_south_west,l_klook_water/activities/orq6ulmzbtxshu1yb2dp.jpg')
i = Image.open(BytesIO(r.content))
i
結果:================
顯示一張圖片
```


### 回應JSON內容

```
import requests

r = requests.get('https://api.github.com/events')
r.json()
```

r.json()下載, 如果格式不符合會拋出錯誤`ValueError: No JSON object could be decoded`。

### 回應原生(Raw)內容
- r.raw
- stream=True

```python
>>> r = requests.get('https://api.github.com/events', stream=True)

>>> r.raw
<urllib3.response.HTTPResponse object at 0x101194810>

>>> r.raw.read(10)
'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'
```

存檔方式
```python
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
```

### 自訂請求的Headers
有時爬蟲時，會被網站拒絕，這時使用自訂的header就很重要

```python
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}

r = requests.get(url, headers=headers)
```

### 回應狀態Codes

檢查狀態code

```
r = requests.get('https://httpbin.org/get')
r.status_code

結果:============
200
```

如果回應狀態碼是4xx,5xx的錯誤，可以要求拋出錯誤

```python
>>> bad_r = requests.get('https://httpbin.org/status/404')
>>> bad_r.status_code

結果:=====
404
=======

>>> bad_r.raise_for_status()
結果:==========
Traceback (most recent call last):
  File "requests/models.py", line 832, in raise_for_status
    raise http_error
requests.exceptions.HTTPError: 404 Client Error
```

## 錯誤和例外處理
- 伺服器找人到，或網路錯誤會throw requests.ConnectionError
- 如果傳回的status code 不是 200,執行Response.raise_for_status()會throw requests.HTTPError
- Timeout會傳出requests.Timeout
- 所有的exception都繼承requests.exceptions.RequestException

```python
import requests
from requests import ConnectionError,HTTPError,Timeout

try:
    res = requests.get("http://www.pythonscraping.com/pages/page1.html")    
    res.raise_for_status()    
except ConnectionError:
    print('找不到伺服器')
except HTTPError:
    print('網頁找不到')
except Timeout:
    print('超過時間沒有回應')
else:
    print('沒有發生問題')
```

## 實際操作
1. 讀取雲端json(API)

```python
import requests
r = requests.get('https://api.github.com/events')
r.json()
結果:======
得到list物件
```

2. 讀取雲端csv檔(當看到最後的副檔名有csv檔時),當在瀏灠器內，只要點選就會下載檔案

```python
import requests
import csv

csv_url = 'http://www.taisugar.com.tw/Upload/UserFiles/台糖休閒遊憩事業部各據點簡介.csv'
response = requests.get(csv_url)
csv_text = response.text

#splitlines(),切割換行,傳回list物件
csvObj = csv.reader(csv_text.splitlines())
for row in csvObj:
    print(row)
```

3. 讀取雲端json檔(當看到最後的副檔名有json檔時),當在瀏灠器內，只要點選就會下載檔案

```python
import requests
import json

json_url = 'https://quality.data.gov.tw/dq_download_json.php?nid=6056&md5_url=0072acc4d89f426c77bff6b92aaa700d'

response=requests.get(json_url)
response.json()
```

4. 下載雲端csv檔(當看到最後的副檔名有csv檔時),當在瀏灠器內，只要點選就會下載檔案

```python
import requests

csv_url = 'http://www.taisugar.com.tw/Upload/UserFiles/台糖休閒遊憩事業部各據點簡介.csv'
r = requests.get(csv_url, stream=True)
with open('station.csv', 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
結果:===================
檔案station.csv已經下載
```

5. 下載雲端json檔(當看到最後的副檔名有csv檔時),當在瀏灠器內，只要點選就會下載檔案

```python
import requests

json_url = 'https://quality.data.gov.tw/dq_download_json.php?nid=6056&md5_url=0072acc4d89f426c77bff6b92aaa700d'
r = requests.get(json_url, stream=True)
with open('holtels.json','wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
```

6. 下載網路圖片

```python
import requests
image_url = 'https://res.klook.com/image/upload/c_crop,h_668,w_1687,x_0,y_0/c_fill,w_960,h_460,f_auto/w_80,x_15,y_15,g_south_west,l_klook_water/activities/orq6ulmzbtxshu1yb2dp.jpg'

r = requests.get(image_url, stream=True)
filename = r.url.split('/')[-1:]

with open(filename[0],'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
        
結果:===========
下載圖片
```



