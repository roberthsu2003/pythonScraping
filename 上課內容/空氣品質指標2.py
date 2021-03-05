#!/usr/bin/python3
'''
應用程式說明
'''

from tkinter import *
from tkinter import ttk
from dataSource import *
import time
import locale


class AirWindow(Tk):
    def __init__(self):
        super().__init__()
        #取得資料
        self.airData=getAirData()
        if self.airData == None:
            print("下載錯誤")


        #建立視窗
        self.title("台灣各地空氣品質指標")
        #self.geometry('300x100+200+200')
        self.resizable(width=0, height=0)

        #建立main Frame
        mainFrame = Frame(self,relief="groove",borderwidth=2)

        #建立label Frame
        titleFrame = Frame(mainFrame)
        Label(titleFrame,text='台灣各地空氣品質指標',font=("Arial", 20)).pack(padx=20,pady=20)
        fomatTime = AirWindow.convertDateFormat(self.airData[0]["時間"])
        Label(titleFrame, text=f'{fomatTime}', font=("Arial", 14)).pack(padx=20, pady=20)
        titleFrame.pack()

        #建立display Frame
        displayFrame = Frame(mainFrame)
        Label(displayFrame, text='請選擇監測點:', font=("Arial", 20)).pack(side=LEFT, padx=10, pady=20)
        positionSelected = ttk.Combobox(displayFrame, width=10, font=("Arial", 20))
        positionSelected['values'] = getPositionList()
        positionSelected.pack(side=LEFT)
        positionSelected.current(0) #選擇預設第一筆資料
        selectedSiteName = positionSelected.get()
        selectedSiteData = getOneSiteData(selectedSiteName)
        positionSelected.bind("<<ComboboxSelected>>",self.userSelected)
        displayFrame.pack(fill=X)

        # 建立list Frame
        listFrame = Frame(mainFrame)

        Label(listFrame,text='監測點:', font=("Arial", 14)).grid(row=0,column=0,sticky=E,padx=10,pady=10)
        self.moniterLabel = Label(listFrame, text=selectedSiteData['監測點'], font=("Arial", 14))
        self.moniterLabel.grid(row=0, column=1,sticky=W,padx=10,pady=10)
        Label(listFrame, text='城市:', font=("Arial", 14)).grid(row=1, column=0,sticky=E,padx=10,pady=10)
        self.cityLabel = Label(listFrame, text=selectedSiteData['城市'], font=("Arial", 14))
        self.cityLabel.grid(row=1, column=1,sticky=W,padx=10,pady=10)
        Label(listFrame, text='AQI:', font=("Arial", 14)).grid(row=2, column=0,sticky=E,padx=10,pady=10)
        self.aqiLabel = Label(listFrame, text=selectedSiteData['AQI'], font=("Arial", 14))
        self.aqiLabel.grid(row=2, column=1,sticky=W,padx=10,pady=10)
        Label(listFrame, text='狀態:', font=("Arial", 14)).grid(row=3, column=0,sticky=E,padx=10,pady=10)
        self.stateLabel = Label(listFrame, text=selectedSiteData['狀態'], font=("Arial", 14))
        self.stateLabel.grid(row=3, column=1,sticky=W,padx=10,pady=10)
        Label(listFrame, text='時間:', font=("Arial", 14)).grid(row=4, column=0,sticky=E,padx=10,pady=10)
        self.timeLabel = Label(listFrame, text=selectedSiteData['時間'], font=("Arial", 14))
        self.timeLabel.grid(row=4, column=1,sticky=W,padx=10,pady=10)
        listFrame.pack(side=LEFT)

        mainFrame.pack(padx=30,pady=30,ipadx=20,ipady=20)

    #combobox的事件接收
    def userSelected(self,event):
        selectedSiteName = event.widget.get()
        selectedSiteData = getOneSiteData(selectedSiteName)
        self.moniterLabel.configure(text=selectedSiteData['監測點'])
        self.cityLabel.configure(text=selectedSiteData['城市'])
        self.aqiLabel.configure(text=selectedSiteData['AQI'])
        self.stateLabel.configure(text=selectedSiteData['狀態'])
        self.timeLabel.configure(text=selectedSiteData['時間'])

    @classmethod
    def convertDateFormat(cls,dateString):
        print(dateString[:19])
        locale.setlocale(locale.LC_TIME, 'zh_tw')
        sft = "%Y-%m-%d %H:%M:%S"
        monitorTime = time.strptime(dateString[:19],sft)
        fmt = "觀測時間:%Y年%b%d日%A %p%I:%M:%S"
        return time.strftime(fmt,monitorTime)




if __name__ == '__main__':
    window = AirWindow()
    window.mainloop()