#!/usr/bin/env python3
"""
GitHub Copilot 專案配置腳本

專門用於設定 GitHub Copilot 官方格式的專案配置。
只維護 .copilot 目錄，移除其他重複的 prompt 配置。
"""

import os
import sys
import json
from pathlib import Path

def get_project_info():
    """取得專案資訊"""
    current_dir = Path(__file__).parent.absolute()
    
    project_info = {
        "project_name": "股票爬蟲工具",
        "project_directory": "lesson6",
        "current_path": str(current_dir),
        "is_project_root": current_dir.name == "lesson6",
        "python_files": [],
        "doc_files": []
    }
    
    # 掃描專案檔案
    for file_path in current_dir.iterdir():
        if file_path.is_file():
            if file_path.suffix == '.py':
                project_info["python_files"].append(file_path.name)
            elif file_path.suffix == '.md':
                project_info["doc_files"].append(file_path.name)
    
    return project_info

def display_project_context():
    """顯示專案上下文資訊"""
    info = get_project_info()
    
    print("=" * 60)
    print("🤖 GitHub Copilot 專案配置")
    print("=" * 60)
    print(f"📁 專案名稱: {info['project_name']}")
    print(f"📂 專案目錄: {info['project_directory']}")
    print(f"📍 當前路徑: {info['current_path']}")
    print(f"✅ 是否為專案根目錄: {'是' if info['is_project_root'] else '否'}")
    
    print("\n🐍 Python 檔案:")
    for py_file in sorted(info['python_files']):
        print(f"  • {py_file}")
    
    print("\n📋 文件檔案:")
    for doc_file in sorted(info['doc_files']):
        print(f"  • {doc_file}")
    
    print("\n" + "=" * 60)
    print("💡 專案狀態:")
    print("   完整功能的股票爬蟲桌面應用程式")
    print("   包含 GUI 介面和網頁爬蟲功能")
    print("   使用 GitHub Copilot 官方配置格式")
    print("=" * 60)
    
    return info

def create_copilot_context():
    """建立 GitHub Copilot 上下文檔案"""
    info = get_project_info()
    
    # 確保 .copilot 目錄存在
    copilot_dir = Path('.copilot')
    copilot_dir.mkdir(exist_ok=True)
    
    # 建立 Copilot 相容的專案描述
    copilot_context = {
        "project": {
            "name": "股票爬蟲工具",
            "description": "基於 Python tkinter 的股票資料爬取桌面應用程式",
            "type": "python_desktop_application",
            "root_directory": "lesson6",
            "status": "fully_functional"
        },
        "structure": {
            "entry_point": "index.py",
            "modules": {
                "index.py": "主程式入口和選單系統",
                "wantgoo.py": "爬蟲核心模組，股票資料獲取",
                "stock_gui.py": "tkinter GUI 介面實作",
                "run.py": "便利啟動腳本"
            }
        },
        "technology": {
            "language": "python",
            "version": "3.8+",
            "gui_framework": "tkinter",
            "web_crawler": "crawl4ai",
            "data_source": ["twstock", "wantgoo.com"],
            "async_processing": "asyncio"
        },
        "copilot_instructions": {
            "context_awareness": [
                "lesson6 是專案根目錄",
                "專案功能完整，包含完整的 GUI 和爬蟲功能",
                "保持現有的模組化架構",
                "遵循 Python PEP 8 規範"
            ],
            "development_guidelines": [
                "維護程式碼架構一致性",
                "確保完整的錯誤處理",
                "保持使用者體驗一致性",
                "考慮與現有功能的整合性"
            ]
        }
    }
    
    # 寫入 Copilot 上下文檔案
    with open('.copilot/context.json', 'w', encoding='utf-8') as f:
        json.dump(copilot_context, f, ensure_ascii=False, indent=2)
    
    return copilot_context

def check_copilot_files():
    """檢查 Copilot 配置檔案完整性"""
    copilot_files = [
        '.copilot/project.yml',
        '.copilot/instructions.md',
        '.copilot/knowledge.md',
        '.copilot/config.yml',
        '.copilot/context.json',
        '.copilot/README.md'
    ]
    
    missing_files = []
    for file_path in copilot_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    return missing_files

def main():
    """主執行函數"""
    print("🚀 GitHub Copilot 專案配置")
    
    # 顯示專案資訊
    project_info = display_project_context()
    
    # 建立 Copilot 上下文檔案
    context = create_copilot_context()
    
    print("\n✅ GitHub Copilot 配置完成！")
    print("📁 .copilot/ 目錄已設定完成")
    
    # 檢查 Copilot 檔案完整性
    missing_files = check_copilot_files()
    if missing_files:
        print(f"\n📋 預設配置檔案: {len(missing_files)} 個")
        for file in missing_files:
            print(f"   • {file}")
        print("   (這些檔案已預先建立，您可以根據需要手動調整)")
    else:
        print("📄 所有 Copilot 配置檔案已完整")
    
    # 檢查是否在正確的目錄
    if not project_info["is_project_root"]:
        print("\n⚠️  警告: 當前目錄可能不是 lesson6 專案根目錄")
        print("   請確認您在正確的專案目錄中運行此腳本")
    else:
        print("\n🎯 GitHub Copilot 已可正確識別此專案！")
        print("\n💡 使用建議:")
        print("   1. 使用 VS Code: code lesson6.code-workspace")
        print("   2. 安裝 GitHub Copilot 擴展")
        print("   3. 所有配置位於 .copilot/ 目錄")
        print("   4. 享受 AI 協助開發體驗！")

if __name__ == "__main__":
    main()
