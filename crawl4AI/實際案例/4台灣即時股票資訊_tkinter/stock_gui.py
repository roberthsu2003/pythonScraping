import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import asyncio
import wantgoo
from datetime import datetime


class StockCrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("股票爬蟲工具")
        self.root.geometry("1200x800")
        
        # 設定樣式
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        self.setup_ui()
        self.load_stock_list()
        
    def setup_ui(self):
        # 主標題
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, text="股票爬蟲工具", style='Title.TLabel')
        title_label.pack()
        
        # 建立主要容器
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 左側面板 - 股票選擇
        left_frame = ttk.LabelFrame(main_frame, text="股票選擇", padding=10)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        # 股票清單標籤
        stock_list_label = ttk.Label(left_frame, text="股票清單:", style='Header.TLabel')
        stock_list_label.pack(anchor='w')
        
        # 搜尋框
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', pady=(5, 10))
        
        ttk.Label(search_frame, text="搜尋:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_stocks)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        # 股票清單
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill='both', expand=True)
        
        # 建立 Treeview 來顯示股票清單
        columns = ('code', 'name', 'market')
        self.stock_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        # 設定欄位標題
        self.stock_tree.heading('#0', text='選擇')
        self.stock_tree.heading('code', text='代碼')
        self.stock_tree.heading('name', text='名稱')
        self.stock_tree.heading('market', text='市場')
        
        # 設定欄位寬度
        self.stock_tree.column('#0', width=50)
        self.stock_tree.column('code', width=80)
        self.stock_tree.column('name', width=150)
        self.stock_tree.column('market', width=80)
        
        # 新增滾動條
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stock_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 選擇/取消選擇按鈕
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        select_all_btn = ttk.Button(button_frame, text="全選", command=self.select_all)
        select_all_btn.pack(side='left', padx=(0, 5))
        
        deselect_all_btn = ttk.Button(button_frame, text="取消全選", command=self.deselect_all)
        deselect_all_btn.pack(side='left')
        
        # 右側面板 - 控制和結果
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # 控制面板
        control_frame = ttk.LabelFrame(right_frame, text="控制面板", padding=10)
        control_frame.pack(fill='x', pady=(0, 10))
        
        # 爬蟲按鈕
        self.crawl_btn = ttk.Button(control_frame, text="開始爬取股票資料", 
                                   command=self.start_crawling, state='normal')
        self.crawl_btn.pack(pady=5)
        
        # 進度條
        self.progress_var = tk.StringVar(value="準備就緒")
        progress_label = ttk.Label(control_frame, textvariable=self.progress_var)
        progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress_bar.pack(fill='x', pady=5)
        
        # 結果顯示面板
        result_frame = ttk.LabelFrame(right_frame, text="爬取結果", padding=10)
        result_frame.pack(fill='both', expand=True)
        
        # 結果顯示區域
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=25)
        self.result_text.pack(fill='both', expand=True)
        
        # 底部狀態列
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', side='bottom')
        
        self.status_var = tk.StringVar(value="就緒")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side='left', padx=10, pady=5)
        
    def load_stock_list(self):
        """載入股票清單"""
        try:
            self.stock_data = wantgoo.get_stocks_with_twstock()
            self.update_stock_tree()
            self.status_var.set(f"已載入 {len(self.stock_data)} 支股票")
        except Exception as e:
            messagebox.showerror("錯誤", f"載入股票清單失敗: {str(e)}")
            
    def update_stock_tree(self, filtered_data=None):
        """更新股票清單顯示"""
        # 清除現有項目
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
            
        # 使用過濾後的資料或原始資料
        data_to_show = filtered_data if filtered_data is not None else self.stock_data
        
        # 插入股票資料
        for stock in data_to_show:
            self.stock_tree.insert('', 'end', values=(stock['code'], stock['name'], stock['market']))
            
    def filter_stocks(self, *args):
        """根據搜尋條件過濾股票"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self.update_stock_tree()
            return
            
        filtered_data = []
        for stock in self.stock_data:
            if (search_term in stock['code'].lower() or 
                search_term in stock['name'].lower()):
                filtered_data.append(stock)
                
        self.update_stock_tree(filtered_data)
        
    def select_all(self):
        """選擇所有股票"""
        for item in self.stock_tree.get_children():
            self.stock_tree.selection_add(item)
            
    def deselect_all(self):
        """取消選擇所有股票"""
        self.stock_tree.selection_remove(self.stock_tree.selection())
        
    def get_selected_stocks(self):
        """取得選中的股票代碼"""
        selected_items = self.stock_tree.selection()
        selected_codes = []
        
        for item in selected_items:
            values = self.stock_tree.item(item, 'values')
            if values:
                selected_codes.append(values[0])  # 股票代碼在第一個位置
                
        return selected_codes
        
    def start_crawling(self):
        """開始爬取股票資料"""
        selected_codes = self.get_selected_stocks()
        
        if not selected_codes:
            messagebox.showwarning("警告", "請至少選擇一支股票")
            return
            
        if len(selected_codes) > 10:
            if not messagebox.askyesno("確認", f"您選擇了 {len(selected_codes)} 支股票，爬取可能需要較長時間，是否繼續？"):
                return
                
        # 在新線程中執行爬蟲任務
        threading.Thread(target=self.crawl_stocks, args=(selected_codes,), daemon=True).start()
        
    def crawl_stocks(self, stock_codes):
        """在背景線程中爬取股票資料"""
        try:
            # 更新 UI 狀態
            self.root.after(0, lambda: self.update_crawling_status(True))
            
            # 建立 URL 清單
            urls = [f"https://www.wantgoo.com/stock/{code}/technical-chart" for code in stock_codes]
            
            # 執行異步爬蟲
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(wantgoo.get_stock_data(urls))
            loop.close()
            
            # 在主線程中更新結果
            self.root.after(0, lambda: self.display_results(results))
            
        except Exception as e:
            self.root.after(0, lambda: self.handle_crawling_error(str(e)))
        finally:
            self.root.after(0, lambda: self.update_crawling_status(False))
            
    def update_crawling_status(self, is_crawling):
        """更新爬取狀態"""
        if is_crawling:
            self.crawl_btn.config(state='disabled')
            self.progress_var.set("正在爬取資料...")
            self.progress_bar.start()
            self.status_var.set("爬取中...")
        else:
            self.crawl_btn.config(state='normal')
            self.progress_var.set("爬取完成")
            self.progress_bar.stop()
            self.status_var.set("就緒")
            
    def display_results(self, results):
        """顯示爬取結果"""
        self.result_text.delete(1.0, tk.END)
        
        if not results:
            self.result_text.insert(tk.END, "沒有爬取到任何資料\n")
            return
            
        # 顯示爬取時間
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.result_text.insert(tk.END, f"爬取時間: {current_time}\n")
        self.result_text.insert(tk.END, f"爬取數量: {len(results)} 支股票\n")
        self.result_text.insert(tk.END, "="*80 + "\n\n")
        
        # 顯示每支股票的資料
        for i, stock in enumerate(results, 1):
            self.result_text.insert(tk.END, f"【第 {i} 支股票】\n")
            
            for key, value in stock.items():
                self.result_text.insert(tk.END, f"{key}: {value}\n")
                
            self.result_text.insert(tk.END, "-" * 50 + "\n\n")
            
        self.status_var.set(f"已成功爬取 {len(results)} 支股票資料")
        
    def handle_crawling_error(self, error_msg):
        """處理爬取錯誤"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"爬取失敗: {error_msg}\n")
        messagebox.showerror("錯誤", f"爬取失敗: {error_msg}")
        self.status_var.set("爬取失敗")


def main():
    root = tk.Tk()
    app = StockCrawlerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
