#!/usr/bin/env python3
"""
測試 main.py 程式的基本功能
"""
import asyncio
import wantgoo

def test_basic_functions():
    """測試基本功能"""
    print("=== 測試基本功能 ===")
    
    # 1. 測試股票清單載入
    print("1. 測試股票清單載入...")
    try:
        stocks = wantgoo.get_stocks_with_twstock()
        print(f"   ✓ 成功載入 {len(stocks)} 支股票")
    except Exception as e:
        print(f"   ✗ 股票清單載入失敗: {e}")
        return False
    
    # 2. 測試爬蟲功能
    print("2. 測試爬蟲功能...")
    try:
        async def test_crawl():
            urls = [
                'https://www.wantgoo.com/stock/2330/technical-chart',  # 台積電
                'https://www.wantgoo.com/stock/2454/technical-chart'   # 聯發科
            ]
            return await wantgoo.get_stock_data(urls)
        
        results = asyncio.run(test_crawl())
        print(f"   ✓ 成功爬取 {len(results)} 支股票資料")
        
        for result in results:
            code = result.get('股票號碼')
            name = result.get('股票名稱') 
            price = result.get('即時價格')
            print(f"     - {code} {name}: {price}")
            
    except Exception as e:
        print(f"   ✗ 爬蟲功能測試失敗: {e}")
        return False
    
    # 3. 測試資料映射邏輯
    print("3. 測試資料映射邏輯...")
    try:
        stock_data_map = {d.get('股票號碼'): d for d in results}
        columns = ("股票號碼", "股票名稱", "即時價格", "漲跌", "漲跌百分比", "成交量(張)")
        
        for code in ['2330', '2454']:
            stock_data = stock_data_map.get(code)
            if stock_data:
                values = [stock_data.get(col, "-") for col in columns]
                print(f"   ✓ {code} 資料映射正常: {values}")
            else:
                print(f"   ✗ {code} 資料映射失敗")
                return False
                
    except Exception as e:
        print(f"   ✗ 資料映射測試失敗: {e}")
        return False
    
    print("\n=== 所有測試通過！main.py 應該能正常運作 ===")
    return True

if __name__ == "__main__":
    test_basic_functions()