import wantgoo
import asyncio
import sys
import os

# 嘗試導入 GUI 模組
try:
    from stock_gui import main as gui_main
    GUI_AVAILABLE = True
except ImportError as e:
    print(f"警告: GUI 模組載入失敗 - {e}")
    GUI_AVAILABLE = False





def main():
    urls = [
        "https://www.wantgoo.com/stock/2330/technical-chart",
        "https://www.wantgoo.com/stock/2317/technical-chart",
        "https://www.wantgoo.com/stock/2454/technical-chart",
        "https://www.wantgoo.com/stock/2303/technical-chart",
        "https://www.wantgoo.com/stock/2412/technical-chart",
        "https://www.wantgoo.com/stock/2884/technical-chart",
        "https://www.wantgoo.com/stock/2881/technical-chart",
        "https://www.wantgoo.com/stock/2308/technical-chart",
        "https://www.wantgoo.com/stock/2337/technical-chart",
        "https://www.wantgoo.com/stock/2882/technical-chart",
    ]
    reuslts:list[dict] = asyncio.run(wantgoo.get_stock_data(urls=urls))
    for stock in reuslts:
        print(stock)



if __name__ == "__main__":
    print("=" * 50)
    print("🚀 股票爬蟲工具")
    print("=" * 50)
    
    # 檢查 GUI 是否可用
    if GUI_AVAILABLE:
        print("1. 命令列模式 - 爬取預設股票")
        print("2. GUI 模式 - 圖形介面 ⭐ 推薦")
        print("3. 顯示股票清單")
        print("4. 離開程式")
    else:
        print("1. 命令列模式 - 爬取預設股票")
        print("2. 顯示股票清單")
        print("3. 離開程式")
        print("\n⚠️  注意: GUI 模式無法使用，請檢查 tkinter 安裝")
    
    print("-" * 50)
    
    try:
        if GUI_AVAILABLE:
            choice = input("請選擇執行模式 (1/2/3/4): ").strip()
        else:
            choice = input("請選擇執行模式 (1/2/3): ").strip()
        
        if choice == "1":
            print("\n🔄 啟動命令列模式...")
            main()
        elif choice == "2":
            if GUI_AVAILABLE:
                print("\n🖥️  啟動 GUI 模式...")
                gui_main()
            else:
                print("\n📊 顯示股票清單...")
                try:
                    stocks = wantgoo.get_stocks_with_twstock()
                    print(f"\n✅ 找到 {len(stocks)} 支股票:")
                    for i, stock in enumerate(stocks[:20], 1):
                        print(f"  {i:2d}. {stock['code']} - {stock['name']}")
                    if len(stocks) > 20:
                        print(f"     ... 還有 {len(stocks)-20} 支股票")
                except Exception as e:
                    print(f"❌ 載入股票清單失敗: {e}")
        elif choice == "3":
            if GUI_AVAILABLE:
                print("\n📊 顯示股票清單...")
                try:
                    stocks = wantgoo.get_stocks_with_twstock()
                    print(f"\n✅ 找到 {len(stocks)} 支股票:")
                    for i, stock in enumerate(stocks[:20], 1):
                        print(f"  {i:2d}. {stock['code']} - {stock['name']}")
                    if len(stocks) > 20:
                        print(f"     ... 還有 {len(stocks)-20} 支股票")
                except Exception as e:
                    print(f"❌ 載入股票清單失敗: {e}")
            else:
                print("\n👋 再見！")
                sys.exit(0)
        elif choice == "4" and GUI_AVAILABLE:
            print("\n👋 再見！")
            sys.exit(0)
        else:
            print(f"\n❌ 無效的選擇: {choice}")
            if GUI_AVAILABLE:
                print("🖥️  預設啟動 GUI 模式...")
                gui_main()
            else:
                print("📊 預設顯示股票清單...")
                stocks = wantgoo.get_stocks_with_twstock()
                print(f"\n找到 {len(stocks)} 支股票")
                
    except KeyboardInterrupt:
        print("\n\n👋 程式已被用戶中斷，再見！")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程式執行錯誤: {e}")
        sys.exit(1)