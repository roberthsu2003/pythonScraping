import tkinter as tk
import asyncio
import wantgoo


class SimpleApp:
    def __init__(self, root):
        self.root = root
        try:
            self.stock_codes: list[dict] = wantgoo.get_stocks_with_twstock()
            if not isinstance(self.stock_codes, list):
                raise ValueError("wantgoo.get_stocks_with_twstock() 應回傳一個股票字典的 list。")
        except Exception as e:
            self.stock_codes = []
            print(f"取得股票資料時發生錯誤: {e}")


        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="即時股票資訊", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)        
        
        # 建立root_left_frame來包含左側的內容 
        root_left_frame = tk.Frame(self.root)
        root_left_frame.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.BOTH, expand=True)

        # 建立左側的標題
        # left_title的文字靠左        
        left_title = tk.Label(root_left_frame, text="請選擇股票(可多選)", font=("Arial"), anchor="w", justify="left")
        left_title.pack(pady=(10,0), fill=tk.X,padx=10)

        # 建立leftFrame來包含 listbox 和 scrollbar
        left_frame = tk.Frame(root_left_frame)
        left_frame.pack(pady=10, padx=10,fill=tk.BOTH, expand=True)

        

        # 增加left_frame內的內容
        self.scrollbar = tk.Scrollbar(left_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.stock_listbox = tk.Listbox(left_frame,
                                        selectmode=tk.MULTIPLE,
                                        yscrollcommand=self.scrollbar.set,
                                        width=15,
                                        height=20)
        #抓取stock_listbox的選取事件
        self.stock_listbox.bind('<<ListboxSelect>>', self.on_stock_select)
        
        # 手動插入股票資料
        for stock in self.stock_codes:
            self.stock_listbox.insert(tk.END, f"{stock['code']} - {stock['name']}")
            
        self.stock_listbox.pack(side=tk.LEFT)
        self.scrollbar.config(command=self.stock_listbox.yview)

        
        # cancel_button,改變寬度和高度
        cancel_button = tk.Button(root_left_frame, text="取消", command=self.clear_selection)
        cancel_button.pack(side=tk.BOTTOM, pady=(0,10), fill=tk.X, expand=True)

        # 建立root_right_frame來包含選取股票的資訊
        root_right_frame = tk.Frame(self.root)
        root_right_frame.pack(side=tk.RIGHT, pady=10,padx=10,fill=tk.BOTH, expand=True)
        # 在右側顯示選取的股票資訊
        # 增加self.selected_button按鈕click功能
        self.selected_button = tk.Button(
            root_right_frame,
            text="選取的股票數量是0筆",
            font=("Arial", 12, "bold"))
        self.selected_button.pack(pady=10, padx=10, fill=tk.X, expand=True)
        self.selected_button.config(state=tk.DISABLED)
        self.selected_button.bind("<Button-1>", self.start_crawling)

    def on_stock_select(self, _=None):
        """當股票被選取時，更新右側顯示的資訊"""
        self.selected_stocks = [self.stock_listbox.get(i) for i in self.stock_listbox.curselection()]        
        self.selected_button.config(text=f"選取的股票數量是:{len(self.selected_stocks)}筆")
        if len(self.selected_stocks) == 0:
            self.selected_button.config(state=tk.DISABLED)
        else:
            self.selected_button.config(state=tk.NORMAL)

    def on_selected_button_click(self):
                
        """當股票被選取時，更新右側顯示的資訊"""
        self.selected_stocks = [self.stock_listbox.get(i) for i in self.stock_listbox.curselection()]        
        self.selected_button.config(text=f"選取的股票數量是:{len(self.selected_stocks)}筆")
        if len(self.selected_stocks) == 0:
            self.selected_button.config(state=tk.DISABLED)
        else:
            self.selected_button.config(state=tk.NORMAL)


    def clear_selection(self):
        """清除選取的股票資訊"""
        self.stock_listbox.selection_clear(0, tk.END)
        self.on_stock_select()  # 更新右側顯示的資訊

    def start_crawling(self, event=None):
        """開始爬蟲"""
        # 在這裡可以加入爬蟲邏輯
        # 例如: wantgoo.crawl_stocks(self.selected_stocks)
        urls:list[str] = []
        for info in self.selected_stocks:
            code, name = info.split(' - ')
            url_template = f'https://www.wantgoo.com/stock/{code}/technical-chart'
            urls.append(url_template)
        result:list[dict] = asyncio.run(wantgoo.get_stock_data(urls))
        print(f"爬取到的股票資料: {result}")



if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()