from dataSource import *
import tkinter as tk
import tkinter.ttk as ttk

class YoubikeWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        #display interface
        leftFrame = ttk.LabelFrame(self,text='台北市行政區')
        areaList = tk.Listbox(leftFrame)
        for name in areas:
            areaList.insert(tk.END,name)
        areaList.pack(padx=10,pady=10)
        leftFrame.pack(side=tk.LEFT,padx=30,pady=30)


if __name__ == "__main__":
    window = YoubikeWindow()
    window.mainloop()
