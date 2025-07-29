import tkinter as tk
from tkinter import ttk, font, messagebox
import asyncio
import threading
import queue
from datetime import datetime
from wantgoo import get_stock_data

# 為了讓 get_stocks_with_twstock 能被呼叫，我們需要從 wantgoo.py 匯入它
from wantgoo import get_stocks_with_twstock

class StockTickerAppV7(tk.Tk):
    """
    (已還原) 一個視覺化改進的股票資訊看板應用程式 (v7)。
    - 使用 crawl4ai 瀏覽器爬蟲。
    - 上漲文字顯示為紅色，下跌為綠色。
    """
    def __init__(self):
        super().__init__()

        # --- 初始化設定 ---
        self.title("股票資訊看板 v7 - (漲跌顏色)")
        self.geometry("900x650")

        self.data_queue = queue.Queue()
        self.all_stocks = []
        self.persistent_selection = set()
        self.treeview_stocks = {}
        self.search_var = tk.StringVar()

        # --- 樣式與字體設定 ---
        self.setup_styles_and_fonts()

        # --- 建立 UI ---
        self.setup_ui()

        # --- 載入資料與啟動更新 ---
        self.load_stock_list()
        self.process_queue()
        self.schedule_next_update()

    def setup_styles_and_fonts(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.header_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.body_font = font.Font(family="Arial", size=11)
        self.status_font = font.Font(family="Arial", size=9)
        self.style.configure("Treeview.Heading", font=self.header_font, padding=(10, 5))
        self.style.configure("Treeview", rowheight=28, font=self.body_font)
        self.style.map("Treeview", background=[('selected', '#a0c4ff')])

    def setup_ui(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        left_pane = self._create_left_pane(paned_window)
        paned_window.add(left_pane, weight=1)
        right_pane = self._create_right_pane(paned_window)
        paned_window.add(right_pane, weight=3)
        self.status_label = ttk.Label(main_frame, text="歡迎使用！", anchor=tk.W, font=self.status_font)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

    def _create_left_pane(self, parent):
        frame = ttk.Frame(parent, padding=5)
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(search_frame, text="搜尋:", font=self.body_font).pack(side=tk.LEFT, padx=(0, 5))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_var.trace_add("write", self.filter_stock_list)
        clear_button = ttk.Button(frame, text="清除所有選取", command=self.clear_all_selections)
        clear_button.pack(fill=tk.X, pady=5)
        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        self.stock_listbox = tk.Listbox(listbox_frame, selectmode=tk.EXTENDED, font=self.body_font, borderwidth=0, highlightthickness=0)
        self.stock_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.stock_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stock_listbox.config(yscrollcommand=scrollbar.set)
        self.stock_listbox.bind("<<ListboxSelect>>", self.on_stock_select)
        return frame

    def _create_right_pane(self, parent):
        frame = ttk.Frame(parent, padding=5)
        self.columns = ("股票號碼", "股票名稱", "即時價格", "漲跌", "漲跌百分比", "成交量(張)")
        self.tree = ttk.Treeview(frame, columns=self.columns, show="headings")
        for col in self.columns:
            align = tk.W if col == "股票名稱" else tk.CENTER
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor=align)
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='#ffffff')
        self.tree.tag_configure('up', foreground='red')
        self.tree.tag_configure('down', foreground='green')
        self.tree.pack(fill=tk.BOTH, expand=True)
        return frame

    def clear_all_selections(self):
        self.persistent_selection.clear()
        self.stock_listbox.selection_clear(0, tk.END)
        self.tree.delete(*self.tree.get_children())
        self.treeview_stocks.clear()
        self.update_status_bar()

    def filter_stock_list(self, *args):
        search_term = self.search_var.get().lower().strip()
        self.stock_listbox.delete(0, tk.END)
        filtered_stocks = [s for s in self.all_stocks if not search_term or search_term in s['code'] or search_term in s['name'].lower()]
        for stock in filtered_stocks:
            self.stock_listbox.insert(tk.END, f"{stock['code']} {stock['name']}")
        self.apply_persistent_selection()

    def apply_persistent_selection(self):
        for i, item_text in enumerate(self.stock_listbox.get(0, tk.END)):
            if item_text in self.persistent_selection:
                self.stock_listbox.selection_set(i)

    def load_stock_list(self):
        self.stock_listbox.insert(tk.END, " 正在載入股票列表...")
        threading.Thread(target=self._fetch_stock_list_worker, daemon=True).start()

    def _fetch_stock_list_worker(self):
        try:
            self.data_queue.put(("stock_list_success", get_stocks_with_twstock()))
        except Exception as e:
            self.data_queue.put(("stock_list_error", e))

    def on_stock_select(self, event):
        current_selections = {self.stock_listbox.get(i) for i in self.stock_listbox.curselection()}
        newly_added = False
        for item_text in current_selections:
            stock_code = item_text.split(' ')[0]
            if stock_code not in self.treeview_stocks:
                stock_name = item_text.split(' ', 1)[1]
                tag = 'oddrow' if len(self.treeview_stocks) % 2 else 'evenrow'
                iid = self.tree.insert("", tk.END, values=(stock_code, stock_name, "讀取中...", "", "", ""), tags=(tag,))
                self.treeview_stocks[stock_code] = iid
                newly_added = True
        self.persistent_selection.update(current_selections)
        if newly_added:
            self.update_stock_data()

    def update_stock_data(self):
        stock_codes = list(self.treeview_stocks.keys())
        if not stock_codes:
            self.update_status_bar()
            return
        urls = [f"https://www.wantgoo.com/stock/{code}/technical-chart" for code in stock_codes]
        threading.Thread(target=self._fetch_stock_data_worker, args=(urls,), daemon=True).start()

    def _fetch_stock_data_worker(self, urls):
        try:
            # 還原成使用 asyncio 的版本
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data = loop.run_until_complete(get_stock_data(urls))
            loop.close()
            if data:
                self.data_queue.put(("stock_data_success", data))
            else:
                self.data_queue.put(("stock_data_success", []))
        except Exception as e:
            self.data_queue.put(("stock_data_error", e))

    def process_queue(self):
        try:
            message_type, data = self.data_queue.get_nowait()
            if message_type == "stock_list_success":
                self.all_stocks = data
                self.filter_stock_list()
                self.status_label.config(text=f"股票列表載入完成，共 {len(data)} 支股票。")
            elif message_type == "stock_list_error":
                messagebox.showerror("錯誤", f"無法載入股票列表:\n{data}")
            elif message_type == "stock_data_success":
                stock_data_map = {d.get('股票號碼'): d for d in data}
                sorted_iids = sorted(self.treeview_stocks.values(), key=lambda iid: self.tree.index(iid))
                for i, iid in enumerate(sorted_iids):
                    current_values = self.tree.item(iid)['values']
                    code = str(current_values[0])  # 確保轉換為字符串以匹配爬蟲返回的鍵
                    stock_data = stock_data_map.get(code)
                    row_tag = 'oddrow' if i % 2 else 'evenrow'
                    color_tag = ''
                    if stock_data:
                        try:
                            change_str = stock_data.get('漲跌', '0')
                            # 處理帶有 +/- 符號的字符串
                            if change_str.startswith('+'):
                                change_value = float(change_str[1:])
                                color_tag = 'up'  # 上漲用紅色
                            elif change_str.startswith('-'):
                                change_value = float(change_str[1:])
                                color_tag = 'down'  # 下跌用綠色
                            else:
                                change_value = float(change_str)
                                if change_value > 0:
                                    color_tag = 'up'  # 上漲用紅色
                                elif change_value < 0:
                                    color_tag = 'down'  # 下跌用綠色
                        except (ValueError, TypeError):
                            pass
                        values = [stock_data.get(col, "-") for col in self.columns]
                        self.tree.item(iid, values=values, tags=(row_tag, color_tag))
                    else:
                        self.tree.item(iid, values=(current_values[0], current_values[1], "獲取失敗", "-", "-", "-"), tags=(row_tag,))
                self.update_status_bar(updated=True)
            elif message_type == "stock_data_error":
                messagebox.showerror("錯誤", f"無法獲取股票資料:\n{data}")
                self.update_status_bar(error=True)
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def update_status_bar(self, updated=False, error=False):
        count = len(self.treeview_stocks)
        if error:
            self.status_label.config(text="部分或全部股票資料獲取失敗！")
        elif updated:
            now = datetime.now().strftime("%H:%M:%S")
            self.status_label.config(text=f"最後更新於 {now} | 共 {count} 支股票")
        elif count == 0:
            self.status_label.config(text="請從左側選擇股票新增至儀表板。")
        else:
            self.status_label.config(text=f"共 {count} 支股票在儀表板中")

    def schedule_next_update(self):
        self.update_stock_data()
        self.after(60000, self.schedule_next_update) # 維持 60 秒更新

if __name__ == "__main__":
    try:
        from asyncio import WindowsSelectorEventLoopPolicy
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    except ImportError:
        pass
    app = StockTickerAppV7()
    app.mainloop()