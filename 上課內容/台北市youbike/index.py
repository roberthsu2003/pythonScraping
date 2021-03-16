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
        self.infoFrame.pack(padx=20,pady=20)
        rightFrame.pack(side=tk.RIGHT,fill=tk.Y)

    def userSelected(self,event):
        listbox = event.widget
        areaName = listbox.get(listbox.curselection())
        #得到選取區域的簡單資料
        #simpleInfo內容是list,裏面有tuple(站名,顏色)
        simpleInfo = dataSource.getAreaSimpleInfo(areaName)

        #改變右邊的區域內容,呼叫method,並傳送資料
        self.changeDisplayOfRightSide(simpleInfo, areaName)


    def changeDisplayOfRightSide(self,info,lableName):
        # info內容是list,裏面有tuple(站名,顏色)
        #先清除self.infoFrame內的內容
        print(info)
        self.infoFrame.configure(text=lableName)
        for widget in self.infoFrame.winfo_children():
            widget.destroy()

        print(self.infoFrame)
        for index,siteInfo in enumerate(info):
            print(siteInfo)
            print("===============")

            #一個row,5個cell
            if index % 5 == 0:
                #每5個cell,要有一個parentFrame
                parentFrame = tk.Frame(self.infoFrame)
                parentFrame.pack(anchor=tk.W,padx=20)

            #建立一個frame,內有canvas的圓點和button
            cellFrame = tk.Frame(parentFrame, bg='#cccccc', width=150, height=40, borderwidth=1, relief=tk.GROOVE)
            #建立圓點
            #siteInfo是tuple
            circleCanvas = dataSource.getColorCircle(cellFrame,siteInfo[1])
            circleCanvas.pack()
            cellFrame.pack(side=tk.LEFT)




if __name__ == "__main__":
    window = YoubikeWindow()
    window.mainloop()
