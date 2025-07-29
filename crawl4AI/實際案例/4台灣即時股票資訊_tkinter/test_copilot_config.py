#!/usr/bin/env python3
"""
GitHub Copilot 配置驗證腳本

驗證所有 Copilot 相關配置檔案是否正確設定
"""

import json
import yaml
import os
from pathlib import Path

def test_copilot_config():
    """測試 GitHub Copilot 配置完整性"""
    print("🔍 驗證 GitHub Copilot 配置...")
    
    current_dir = Path(__file__).parent.absolute()
    copilot_dir = current_dir / '.copilot'
    
    # 檢查 .copilot 目錄
    if not copilot_dir.exists():
        print("❌ .copilot 目錄不存在")
        return False
    
    # 必要的配置檔案
    required_files = {
        'project.yml': 'YAML',
        'instructions.md': 'Markdown',
        'knowledge.md': 'Markdown', 
        'config.yml': 'YAML',
        'context.json': 'JSON',
        'README.md': 'Markdown'
    }
    
    missing_files = []
    invalid_files = []
    
    for file_name, file_type in required_files.items():
        file_path = copilot_dir / file_name
        
        if not file_path.exists():
            missing_files.append(file_name)
            continue
            
        # 驗證檔案格式
        try:
            if file_type == 'JSON':
                with open(file_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            elif file_type == 'YAML':
                with open(file_path, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
            # Markdown 檔案只檢查是否可讀取
            elif file_type == 'Markdown':
                with open(file_path, 'r', encoding='utf-8') as f:
                    f.read()
                    
        except Exception as e:
            invalid_files.append(f"{file_name}: {e}")
    
    # 報告結果
    if missing_files:
        print(f"❌ 缺少檔案: {', '.join(missing_files)}")
        return False
        
    if invalid_files:
        print(f"❌ 無效檔案: {'; '.join(invalid_files)}")
        return False
    
    print("✅ 所有 Copilot 配置檔案格式正確！")
    return True

def test_project_structure():
    """驗證專案結構識別"""
    print("\n🏗️ 驗證專案結構識別...")
    
    current_dir = Path(__file__).parent.absolute()
    
    # 檢查是否為 lesson6 目錄
    if current_dir.name != 'lesson6':
        print(f"❌ 當前目錄不是 lesson6，而是 {current_dir.name}")
        return False
    
    # 檢查核心檔案
    core_files = ['index.py', 'wantgoo.py', 'stock_gui.py', 'README.md', 'prd.md']
    missing_core = []
    
    for file_name in core_files:
        if not (current_dir / file_name).exists():
            missing_core.append(file_name)
    
    if missing_core:
        print(f"❌ 缺少核心檔案: {', '.join(missing_core)}")
        return False
    
    print("✅ 專案結構識別正確！")
    return True

def test_copilot_context():
    """測試 Copilot 上下文內容"""
    print("\n📋 驗證 Copilot 上下文內容...")
    
    try:
        # 檢查 context.json
        with open('.copilot/context.json', 'r', encoding='utf-8') as f:
            context = json.load(f)
        
        # 驗證必要欄位
        project = context.get('project', {})
        if project.get('root_directory') != 'lesson6':
            print("❌ 專案根目錄設定錯誤")
            return False
        
        if project.get('type') != 'python_desktop_application':
            print("❌ 專案類型設定錯誤") 
            return False
        
        # 檢查模組定義
        structure = context.get('structure', {})
        if structure.get('entry_point') != 'index.py':
            print("❌ 入口點設定錯誤")
            return False
        
        print("✅ Copilot 上下文內容正確！")
        return True
        
    except Exception as e:
        print(f"❌ 讀取 Copilot 上下文失敗: {e}")
        return False

def show_copilot_summary():
    """顯示 Copilot 配置摘要"""
    print("\n📊 GitHub Copilot 配置摘要:")
    print("=" * 50)
    
    # 讀取專案資訊
    try:
        with open('.copilot/context.json', 'r', encoding='utf-8') as f:
            context = json.load(f)
        
        project = context.get('project', {})
        print(f"📁 專案名稱: {project.get('name', 'N/A')}")
        print(f"📂 專案目錄: {project.get('root_directory', 'N/A')}")
        print(f"🎯 專案類型: {project.get('type', 'N/A')}")
        print(f"📍 專案狀態: {project.get('status', 'N/A')}")
        
        technology = context.get('technology', {})
        print(f"🐍 程式語言: {technology.get('language', 'N/A')}")
        print(f"🖥️ GUI 框架: {technology.get('gui_framework', 'N/A')}")
        print(f"🕷️ 爬蟲框架: {technology.get('web_crawler', 'N/A')}")
        
    except Exception as e:
        print(f"❌ 無法讀取專案資訊: {e}")
    
    print("=" * 50)
    
    # 配置檔案統計
    copilot_dir = Path('.copilot')
    if copilot_dir.exists():
        files = list(copilot_dir.glob('*'))
        print(f"📄 配置檔案數量: {len(files)}")
        for file_path in sorted(files):
            print(f"   • {file_path.name}")

def main():
    """主執行函數"""
    print("🤖 GitHub Copilot 配置驗證工具")
    print("=" * 60)
    
    # 執行所有測試
    tests = [
        test_project_structure,
        test_copilot_config,
        test_copilot_context
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 所有驗證通過！GitHub Copilot 配置完整正確。")
        show_copilot_summary()
        print("\n💡 使用建議:")
        print("   1. 在 VS Code 中開啟 lesson6.code-workspace")
        print("   2. 確保已安裝 GitHub Copilot 擴展")
        print("   3. 開始享受 AI 協助開發！")
    else:
        print("❌ 驗證失敗！請修復上述問題後重新執行。")
        print("💡 修復建議:")
        print("   1. 重新執行 python3 setup_ai_context.py")
        print("   2. 檢查檔案權限和格式")
        print("   3. 確認在正確的專案目錄中")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
