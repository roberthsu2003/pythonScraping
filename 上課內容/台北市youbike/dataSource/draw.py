import tkinter as tk
def getInfoCanvas(parent):
    infoCanvas=tk.Canvas(parent,width=200,height=100,bg='#ffffff')
    infoCanvas.create_oval(10,10,30,30,fill='red')
    infoCanvas.create_oval(10,60,30,40,fill='orange')
    infoCanvas.create_oval(10,90, 30, 70, fill='green')
    return infoCanvas