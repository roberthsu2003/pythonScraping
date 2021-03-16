import dataSource
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.simpledialog import Dialog

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
        self.infoFrame = ttk.LabelFrame(rightFrame,text='文山區',style='Red.TLabelframe')
        self.infoFrame.pack(padx=20,pady=20)
        rightFrame.pack(side=tk.RIGHT,fill=tk.Y)

        #進入時,右邊顯示的區域
        simpleInfo = dataSource.getAreaSimpleInfo('文山區')
        self.changeDisplayOfRightSide(simpleInfo,'文山區')

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
            #一個row,5個cell
            if index % 5 == 0:
                #每5個cell,要有一個parentFrame
                parentFrame = tk.Frame(self.infoFrame)
                parentFrame.pack(anchor=tk.W,padx=20)

            #建立一個frame,內有canvas的圓點和button
            cellFrame = tk.Frame(parentFrame, bg='#cccccc', width=150, height=40, borderwidth=1, relief=tk.GROOVE)
            #建立圓點
            #siteInfo是tuple
            dataSource.getColorCircle(cellFrame,siteInfo[1]).pack()
            nameButton = tk.Button(cellFrame,text=siteInfo[0],width=20,font=(13,))
            nameButton.bind('<Button-1>',self.buttonAction)
            nameButton.pack()

            cellFrame.pack(side=tk.LEFT)

    def buttonAction(self,event=None):
        #使用cget('text'),取出button的text
        siteName = event.widget.cget('text')

        #取出單一站點detail資料
        #print(dataSource.getDetailInfoOfSite(siteName))
        info = dataSource.getDetailInfoOfSite(siteName)
        singleSiteInfo = SingleSiteInfo(self,title="站場資訊",info=info)


class SingleSiteInfo(Dialog):
    def __init__(self, parent, title=None, info=None):
        self.info = info #必需要寫在前面
        super().__init__(parent,title)

    def body(self, master):
        '''
        create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        print(self.info)
        fontStyle = {'font':('arial',13)}
        tk.Label(master, text=f'站場編號:{self.info["sno"]}', **fontStyle).grid(row=0, sticky=tk.W)
        tk.Label(master, text=f'站場名稱:{self.info["sna"]}', **fontStyle).grid(row=1, sticky=tk.W)
        tk.Label(master, text=f'車輛總數:{self.info["tot"]}', **fontStyle).grid(row=2, sticky=tk.W)
        tk.Label(master, text=f'可借車數:{self.info["sbi"]}', **fontStyle).grid(row=3, sticky=tk.W)
        tk.Label(master, text=f'站場地址:{self.info["ar"]}', **fontStyle).grid(row=4, sticky=tk.W)
        tk.Label(master, text=f'可還車位:{self.info["bemp"]}', **fontStyle).grid(row=5, sticky=tk.W)
        if self.info['act'] == '1':
            state = '營運中'
        else:
            state = '維修中'
        tk.Label(master, text=state,**fontStyle).grid(row=6, sticky=tk.W)

    def buttonbox(self):
        '''
        add standard button box.
        如果不要使用正常的按鈕,必需覆寫這個method
         '''
        box = tk.Frame(self)
        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        box.pack()



if __name__ == "__main__":
    window = YoubikeWindow()
    window.mainloop()
