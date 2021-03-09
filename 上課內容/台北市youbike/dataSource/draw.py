import tkinter as tk
def getInfoCanvas(parent):
    infoCanvas=tk.Canvas(parent,width=200,height=100,bg='#ffffff')
    infoCanvas.create_oval(10,10,30,30,fill='red')
    infoCanvas.create_oval(10,60,30,30,fill='orange')
    return infoCanvas