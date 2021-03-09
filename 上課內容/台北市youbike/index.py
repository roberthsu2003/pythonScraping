from dataSource import *
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
        leftFrame = ttk.LabelFrame(self,text='台北市行政區',style='Red.TLabelframe')
        areaList = tk.Listbox(leftFrame,height=12,**mediumFont)
        for name in areas:
            areaList.insert(tk.END,name)
        areaList.pack(padx=10,pady=10)
        leftFrame.pack(side=tk.LEFT,padx=30,pady=30)



if __name__ == "__main__":
    window = YoubikeWindow()
    window.mainloop()
