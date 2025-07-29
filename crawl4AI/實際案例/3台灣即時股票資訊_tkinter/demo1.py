#請建立tkinter視窗的基本結構
# This code creates a simple Tkinter window with a label.
# 請建立一個Window繼承自tkinter的Tk類別

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MyWindow(tk.Tk):
    def __init__(self):
        """
        初始化主視窗及其元件。
        """
        super().__init__()
        self.title("My Tkinter Window")
        self.geometry("800x300")
        #在這裏增加一個ttk的標籤,內容為"Hello, Tkinter!"
        #加大字體大小,並且居中顯示,粗體字
        label = ttk.Label(self, text="Hello, Tkinter!", font=("Arial", 20, "bold"), anchor="center")
        label.pack(pady=20, expand=True, fill="both")
        #在視窗的左邊和右邊各放一個按鈕,點擊後顯示訊息
        #左邊按鈕顯示"左按鈕被點擊了！",右邊按鈕顯示"右按鈕被點擊了！"
        #按鈕的文字分別為"點擊我"和"點擊我也是"
        #按鈕的大小為20x2,並且有20像素的內邊距
        #按鈕的文字為粗體字
        #按鈕的背景色為淺藍色,文字顏色為暗灰色
        #左右2邊的Frame各自有20像素的外邊距,並且一樣的寬度
        # 使用一個父容器 frame 並用 grid 佈局確保左右寬度一致
        container = tk.Frame(self)
        container.pack(side="bottom", fill="x", pady=20)
        
        # 配置 grid 權重，確保左右相等寬度
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        left_frame = tk.Frame(container)
        left_frame.grid(row=0, column=0, padx=20, sticky="ew")
        left_button = self.create_custom_button(
            parent=left_frame,
            text="點擊我",
            command=self.show_message_left
        )
        left_button.pack()

        right_frame = tk.Frame(container)
        right_frame.grid(row=0, column=1, padx=20, sticky="ew")
        right_button = self.create_custom_button(
            parent=right_frame,
            text="點擊我也是",
            command=self.show_message_right
        )
        right_button.pack()

    def show_message_left(self):
        messagebox.showinfo("訊息", "左按鈕被點擊了！")

    def show_message_right(self):
        messagebox.showinfo("訊息", "右按鈕被點擊了！")

    def create_custom_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=20,
            height=2,
            font=("Arial", 12, "bold"),
            bg="#ADD8E6",
            fg="#333333"
        )

if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()