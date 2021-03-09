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
        for name in dataSource.areas:
            areaList.insert(tk.END,name)
        areaList.pack(padx=10,pady=10)
        leftFrame.pack(side=tk.LEFT,padx=30,pady=30)

        #rightSide
        rightFrame= tk.Frame(self)
        infoCanvas = dataSource.getInfoCanvas(rightFrame)
        infoCanvas.pack(anchor=tk.NE)
        infoFrame = ttk.LabelFrame(rightFrame,text='景美區',style='Red.TLabelframe')
        infoFrame.pack()
        rightFrame.pack(side=tk.RIGHT,fill=tk.Y)



if __name__ == "__main__":
    window = YoubikeWindow()
    window.mainloop()
