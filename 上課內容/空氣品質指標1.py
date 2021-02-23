#!/usr/bin/python3.x
'''
這是下載政府開放平台內的資料
使用視窗顯示
'''

from tkinter import *
import requests

class AirWindow(Tk):
    pass

url = "https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json"
def buttonClick():
    response = requests.get(url)
    if response.status_code == 200:
        print("下載成功")
    else:
        print("失敗")
    allData = response.json()  # dictinary
    records = allData['records']  # list
    for record in records:  # record是dictionary
        print("監測點:", record["SiteName"])
        print("城市:", record['County'])
        print("AQI:", record['AQI'])
        print("狀態:", record['Status'])
        print("時間:", record['ImportDate'])
        print("========")

def createWindow(w):
    btn = Button(w,text="取得目前AQI指數",padx=20,pady=20,command=buttonClick)
    btn.pack()


if __name__ == "__main__":
    window=AirWindow()
    window.title("空氣品質指標")
    window.geometry("400x150")
    createWindow(window)
    window.mainloop()