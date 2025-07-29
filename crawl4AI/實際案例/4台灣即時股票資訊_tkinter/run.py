#!/usr/bin/env python3
"""
股票爬蟲工具啟動腳本
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from index import *
except ImportError as e:
    print(f"匯入錯誤: {e}")
    print("請確認所有依賴套件都已正確安裝")
    sys.exit(1)
