# 儲存資料
## 下載多媒體檔案
### 下載一個檔案

```python
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com')
bs = BeautifulSoup(html, 'html.parser')
imageLocation = bs.find('a',{'id':'logo'}).find('img')['src']
urlretrieve(imageLocation, 'logo.jpg')
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