import requests
from requests import ConnectionError,HTTPError,Timeout

url = "https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json"

def getAirData():
    try:
        response = requests.get(url)
        response.raise_for_status()
    except ConnectionError:
        print('找不到伺服器')
        return None
    except HTTPError:
        print('網頁找不到')
        return None
    except Timeout:
        print('超過時間沒有回應')
        return None
    else:
        if response.status_code == 200:
            print("下載成功")
        else:
            print("失敗")
            return None



    allData = response.json()  # dictinary
    records = allData['records']  # list
    for record in records:  # record是dictionary
        print("監測點:", record["SiteName"])
        print("城市:", record['County'])
        print("AQI:", record['AQI'])
        print("狀態:", record['Status'])
        print("時間:", record['ImportDate'])
        print("========")