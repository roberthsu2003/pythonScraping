import dataSource
import tkinter as tk
import tkinter.ttk as ttk

class YoubikeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("台北市youbike及時資訊")
        mediumFont = {'font':('Arial', 20)}
        s = ttk.Style()
        s.configure('Red.TLabelframe.Label', font=('Arial', 20))


        #display interface
        #leftSide
        leftFrame = ttk.LabelFrame(self,text='台北市行政區',style='Red.TLabelframe')
        areaList = tk.Listbox(leftFrame,height=12,selectbackground='#888888',**mediumFont)
        areaList.bind('<<ListboxSelect>>',self.userSelected)
        for name in dataSource.areas:
            areaList.insert(tk.END,name)
        areaList.pack(padx=10,pady=10)
        leftFrame.pack(side=tk.LEFT,padx=30,pady=30)

        #rightSide
        rightFrame= tk.Frame(self)
        infoCanvas = dataSource.getInfoCanvas(rightFrame)
        infoCanvas.pack(anchor=tk.NE)
        self.infoFrame = ttk.LabelFrame(rightFrame,text='景美區',style='Red.TLabelframe')
        self.infoFrame.pack()
        rightFrame.pack(side=tk.RIGHT,fill=tk.Y)

    def userSelected(self,event):
        listbox = event.widget
        areaName = listbox.get(listbox.curselection())
        #得到選取區域的簡單資料
        #simpleInfo內容是list,裏面有tuple(站名,顏色)
        simpleInfo = dataSource.getAreaSimpleInfo(areaName)

        #改變右邊的區域內容,呼叫method,並傳送資料
        self.changeDisplayOfRightSide(simpleInfo)


    def changeDisplayOfRightSide(self,info):
        # info內容是list,裏面有tuple(站名,顏色)
        print(info)




if __name__ == "__main__":
    window = YoubikeWindow()
    window.mainloop()
