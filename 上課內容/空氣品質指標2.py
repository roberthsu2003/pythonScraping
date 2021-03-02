#!/usr/bin/python3
'''
應用程式說明
'''

from tkinter import *
from tkinter import ttk
import dataSource


class AirWindow(Tk):
    def __init__(self):
        super().__init__()
        #取得資料
        self.airData=dataSource.getAirData()
        if self.airData == None:
            print("下載錯誤")
        else:
           print(self.airData)

        #建立視窗
        self.title("台灣各地空氣品質指標")
        #self.geometry('300x100+200+200')
        self.resizable(width=0, height=0)

        #建立label Frame
        labelFrame = Frame(self)
        Label(labelFrame,text='台灣各地空氣品質指標',font=("Arial", 20)).pack(side=LEFT,padx=20,pady=20)
        Label(labelFrame, text=f'日期時間:{self.airData[0]["時間"]}', font=("Arial", 14)).pack(side=RIGHT,padx=20, pady=20)
        labelFrame.pack()

        #建立display Frame
        displayFrame = Frame(self)
        positionSelected = ttk.Combobox(displayFrame, width=10, font=("Arial", 20))
        positionSelected['values'] = dataSource.getPositionList()
        positionSelected.pack(side=LEFT)
        displayFrame.pack(fill=X)



if __name__ == '__main__':
    window = AirWindow()
    window.mainloop()