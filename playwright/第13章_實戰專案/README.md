# 第十三章：實戰專案

整合所學知識，完成實際的專案。

## 13.1 專案一：新聞網站爬蟲

### 專案目標
- 爬取新聞標題與內容
- 儲存到 CSV 檔案
- 處理分頁

### 完整程式碼

```python
from playwright.sync_api import sync_playwright
import csv
from datetime import datetime

class NewsScraper:
    def __init__(self):
        self.news_data = []
    
    def scrape_news(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto(url)
            page.wait_for_selector("article.news-item")
            
            # 爬取新聞
            articles = page.locator("article.news-item").all()
            
            for article in articles:
                try:
                    news = {
                        "title": article.locator("h2.title").inner_text(),
                        "summary": article.locator("p.summary").inner_text(),
                        "date": article.locator("time").get_attribute("datetime"),
                        "category": article.locator("span.category").inner_text(),
                        "link": article.locator("a").get_attribute("href"),
                        "scraped_at": datetime.now().isoformat()
                    }
                    self.news_data.append(news)
                except Exception as e:
                    print(f"擷取新聞失敗: {e}")
            
            browser.close()
    
    def save_to_csv(self, filename="news.csv"):
        if not self.news_data:
            print("沒有資料可儲存")
            return
        
        with open(filename, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["title", "summary", "date", "category", "link", "scraped_at"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(self.news_data)
        
        print(f"已儲存 {len(self.news_data)} 則新聞到 {filename}")

def main():
    scraper = NewsScraper()
    
    # 爬取多個分類
    categories = ["politics", "business", "tech"]
    
    for category in categories:
        url = f"https://news-example.com/{category}"
        print(f"爬取 {category} 新聞...")
        scraper.scrape_news(url)
    
    scraper.save_to_csv("news_data.csv")

if __name__ == "__main__":
    main()
```

---

## 13.2 專案二：電商價格監控

### 專案目標
- 定期抓取商品價格
- 價格變動通知
- 記錄價格歷史

### 完整程式碼

```python
from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime

class PriceMonitor:
    def __init__(self, db_file="prices.json"):
        self.db_file = db_file
        self.prices = self.load_prices()
    
    def load_prices(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_prices(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.prices, f, ensure_ascii=False, indent=2)
    
    def get_product_price(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto(url)
            page.wait_for_selector(".product-price")
            
            # 擷取商品資訊
            product = {
                "name": page.locator("h1.product-title").inner_text(),
                "price": page.locator(".product-price").inner_text(),
                "in_stock": page.locator(".stock-status").inner_text(),
                "timestamp": datetime.now().isoformat()
            }
            
            browser.close()
            return product
    
    def monitor_product(self, url, product_id):
        print(f"監控商品: {product_id}")
        
        current = self.get_product_price(url)
        
        # 初始化商品記錄
        if product_id not in self.prices:
            self.prices[product_id] = {
                "url": url,
                "history": []
            }
        
        # 檢查價格變動
        history = self.prices[product_id]["history"]
        
        if history:
            last_price = history[-1]["price"]
            if current["price"] != last_price:
                print(f"⚠️ 價格變動！")
                print(f"  {last_price} → {current['price']}")
        
        # 記錄歷史
        history.append(current)
        self.save_prices()
        
        print(f"✓ 已記錄價格: {current['price']}")
    
    def get_price_trend(self, product_id):
        if product_id not in self.prices:
            return None
        
        history = self.prices[product_id]["history"]
        return [
            {
                "date": h["timestamp"][:10],
                "price": h["price"]
            }
            for h in history
        ]

def main():
    monitor = PriceMonitor()
    
    # 要監控的商品
    products = {
        "iphone": "https://shop.example.com/iphone-15",
        "macbook": "https://shop.example.com/macbook-pro"
    }
    
    # 監控所有商品
    for product_id, url in products.items():
        monitor.monitor_product(url, product_id)
    
    # 顯示價格趨勢
    print("\n價格趨勢:")
    for product_id in products:
        trend = monitor.get_price_trend(product_id)
        print(f"\n{product_id}:")
        for record in trend[-5:]:  # 顯示最近 5 筆
            print(f"  {record['date']}: {record['price']}")

if __name__ == "__main__":
    main()
```

---

## 13.3 專案三：社群媒體自動化

### 專案目標
- 自動發文
- 批量操作

### 範例程式碼

```python
from playwright.sync_api import sync_playwright
import time

class SocialMediaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.playwright = None
        self.browser = None
        self.page = None
    
    def login(self):
        with sync_playwright() as p:
            self.playwright = p
            self.browser = p.chromium.launch(headless=False)
            self.page = self.browser.new_page()
            
            # 登入
            self.page.goto("https://social-media.example.com/login")
            self.page.fill("input[name='username']", self.username)
            self.page.fill("input[name='password']", self.password)
            self.page.click("button[type='submit']")
            self.page.wait_for_url("**/home")
            
            print("✓ 登入成功")
    
    def post_message(self, message, image_path=None):
        # 點擊發文按鈕
        self.page.click("button#new-post")
        self.page.wait_for_selector("textarea#post-content")
        
        # 輸入內容
        self.page.fill("textarea#post-content", message)
        
        # 上傳圖片（如果有）
        if image_path:
            self.page.set_input_files("input[type='file']", image_path)
            time.sleep(2)
        
        # 發布
        self.page.click("button#publish")
        self.page.wait_for_selector(".post-success")
        
        print(f"✓ 已發布: {message[:30]}...")
    
    def batch_post(self, posts):
        for i, post in enumerate(posts, 1):
            print(f"發布第 {i}/{len(posts)} 則貼文")
            self.post_message(post["message"], post.get("image"))
            time.sleep(5)  # 延遲避免觸發限制
    
    def close(self):
        if self.browser:
            self.browser.close()

def main():
    bot = SocialMediaBot("username", "password")
    bot.login()
    
    posts = [
        {"message": "這是第一則自動發文 #自動化"},
        {"message": "這是第二則自動發文 #Playwright", "image": "image.jpg"},
        {"message": "這是第三則自動發文 #Python"}
    ]
    
    bot.batch_post(posts)
    bot.close()

if __name__ == "__main__":
    main()
```

---

## 13.4 專案四：網頁自動化測試

### 專案目標
- 測試表單提交
- 驗證頁面元素

### 測試框架範例

```python
from playwright.sync_api import sync_playwright
import unittest

class WebsiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
    
    def setUp(self):
        self.page = self.browser.new_page()
    
    def tearDown(self):
        self.page.close()
    
    def test_homepage_title(self):
        """測試首頁標題"""
        self.page.goto("https://example.com")
        title = self.page.title()
        self.assertEqual(title, "Example Domain")
    
    def test_login_form(self):
        """測試登入表單"""
        self.page.goto("https://example.com/login")
        
        # 填寫表單
        self.page.fill("input#username", "testuser")
        self.page.fill("input#password", "testpass")
        self.page.click("button#login")
        
        # 驗證結果
        self.page.wait_for_selector(".dashboard")
        self.assertTrue(self.page.is_visible(".user-info"))
    
    def test_search_functionality(self):
        """測試搜尋功能"""
        self.page.goto("https://example.com")
        
        # 執行搜尋
        self.page.fill("input#search", "Playwright")
        self.page.press("input#search", "Enter")
        
        # 驗證結果
        self.page.wait_for_selector(".search-results")
        results = self.page.locator(".result-item").count()
        self.assertGreater(results, 0)
    
    def test_form_validation(self):
        """測試表單驗證"""
        self.page.goto("https://example.com/contact")
        
        # 提交空表單
        self.page.click("button#submit")
        
        # 驗證錯誤訊息
        error = self.page.locator(".error-message").inner_text()
        self.assertIn("必填", error)

if __name__ == "__main__":
    unittest.main()
```

---

## 總結

完成這些專案後，你應該能夠：

1. ✅ 獨立開發爬蟲程式
2. ✅ 處理複雜的網頁互動
3. ✅ 實作資料儲存和處理
4. ✅ 應對反爬蟲機制
5. ✅ 優化程式效能
6. ✅ 編寫自動化測試

---

## 延伸學習

- 整合資料庫（SQLite、MongoDB）
- 建立定時任務（cron、schedule）
- 建立 Web API 提供資料
- 資料視覺化（matplotlib、plotly）
- 機器學習應用（分類、預測）

---

[← 上一章：效能優化](../第12章_效能優化/README.md) | [返回目錄](../README.md)
