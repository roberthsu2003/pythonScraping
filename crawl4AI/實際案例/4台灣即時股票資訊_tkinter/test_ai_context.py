#!/usr/bin/env python3
"""
AI 上下文驗證腳本

驗證 AI 助手是否能正確識別專案上下文
"""

import json
import os
from pathlib import Path

def test_ai_context():
    """測試 AI 上下文設定"""
    print("🔍 驗證 AI 上下文設定...")
    
    current_dir = Path(__file__).parent.absolute()
    
    # 檢查必要檔案
    required_files = [
        '.ai_context.json',
        '.ai_prompt.md', 
        '.project_context.md',
        '.project_config.json'
    ]
    
    missing_files = []
    for file_name in required_files:
        if not (current_dir / file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ 缺少必要檔案: {', '.join(missing_files)}")
        return False
    
    # 檢查 AI 上下文檔案內容
    try:
        with open('.ai_context.json', 'r', encoding='utf-8') as f:
            context = json.load(f)
        
        ai_context = context.get('ai_assistant_context', {})
        project_id = ai_context.get('project_identification', {})
        
        # 驗證關鍵資訊
        if project_id.get('directory') != 'lesson6':
            print("❌ 專案目錄識別錯誤")
            return False
            
        if not ai_context.get('working_environment', {}).get('is_project_root'):
            print("❌ 專案根目錄識別錯誤")
            return False
            
        print("✅ AI 上下文設定正確！")
        print(f"📁 專案名稱: {project_id.get('name')}")
        print(f"📂 專案目錄: {project_id.get('directory')}")
        print(f"🎯 專案類型: {project_id.get('type')}")
        print(f"📍 當前路徑: {current_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ 讀取 AI 上下文檔案失敗: {e}")
        return False

def show_ai_instructions():
    """顯示 AI 指令摘要"""
    print("\n📋 AI 助手指令摘要:")
    print("   • 識別 lesson6 為專案根目錄")
    print("   • 理解完整的檔案結構")
    print("   • 維護現有程式碼風格")
    print("   • 提供符合專案架構的建議")

if __name__ == "__main__":
    print("🤖 AI 上下文驗證工具")
    print("=" * 40)
    
    if test_ai_context():
        show_ai_instructions()
        print("\n🎉 驗證完成！AI 助手可以正確識別此專案。")
    else:
        print("\n⚠️  請執行 setup_ai_context.py 來重新設定上下文。")
    
    print("=" * 40)
