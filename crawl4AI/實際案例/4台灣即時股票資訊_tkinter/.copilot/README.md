# GitHub Copilot 配置說明

## 概述

本目錄包含針對 **lesson6 股票爬蟲工具專案** 的 GitHub Copilot 配置檔案，讓 AI 助手能夠更好地理解專案結構和提供相關的開發協助。

## 檔案結構

```
.copilot/
├── README.md           # 本檔案，Copilot 配置說明
├── project.yml         # 專案基本資訊和結構定義
├── instructions.md     # 系統指令和 AI 助手行為準則  
├── knowledge.md        # 專案知識庫和參考資料
├── config.yml          # Copilot 工作區配置
└── context.json        # 動態生成的專案上下文
```

## 配置檔案說明

### 📋 project.yml
定義專案的基本資訊：
- 專案名稱和描述
- 技術棧和架構
- 模組結構和功能
- 資料模型

### 📖 instructions.md  
包含 AI 助手的系統指令：
- 角色定義和專案上下文
- 開發指導原則
- 常見任務和限制條件
- 範例對話模式

### 📚 knowledge.md
專案知識庫：
- 程式碼模組說明
- API 參考資料
- 設計模式
- 故障排除指南
- 最佳實踐

### ⚙️ config.yml
Copilot 工作區配置：
- 專案感知設定
- 程式碼補全配置
- 聊天助手設定
- 語言特定配置

### 🔄 context.json
動態上下文（由 `setup_ai_context.py` 生成）：
- 即時專案狀態
- 檔案結構映射
- Copilot 指令集

## 使用方式

### 1. 初始化配置
```bash
# 在 lesson6 目錄中執行
python3 setup_ai_context.py
```

### 2. VS Code 整合
開啟 `lesson6.code-workspace` 工作區以獲得最佳 Copilot 體驗：
```bash
code lesson6.code-workspace
```

### 3. Copilot 聊天
在 VS Code 中使用 Copilot Chat 時，AI 會自動載入這些配置，提供專案相關的協助。

## AI 助手能力

配置完成後，GitHub Copilot 將能夠：

✅ **專案識別**
- 正確識別 lesson6 為股票爬蟲專案根目錄
- 理解專案的完整功能和架構

✅ **程式碼理解**  
- 了解各模組的職責和關係
- 提供符合專案風格的程式碼建議

✅ **開發協助**
- 基於現有架構提供功能擴展建議
- 協助除錯和問題解決
- 提供最佳實踐指導

✅ **上下文感知**
- 維護專案一致性
- 避免破壞現有功能
- 考慮模組間的整合

## 自訂配置

如需修改 Copilot 行為，可以編輯相應的配置檔案：

- **修改專案資訊**: 編輯 `project.yml`
- **調整 AI 行為**: 編輯 `instructions.md`  
- **更新知識庫**: 編輯 `knowledge.md`
- **改變工作區設定**: 編輯 `config.yml`

修改後重新執行 `setup_ai_context.py` 以更新動態上下文。

## 注意事項

1. **檔案完整性**: 確保所有配置檔案都存在且格式正確
2. **路徑相對性**: 所有路徑都相對於 lesson6 專案根目錄
3. **版本同步**: 專案更新時記得同步更新配置檔案
4. **隱私安全**: 配置檔案中不包含敏感資訊

## 故障排除

### Copilot 無法識別專案
- 檢查是否在 lesson6 目錄中
- 確認 `.copilot/` 目錄和檔案存在
- 重新執行 `setup_ai_context.py`

### 程式碼建議不相關
- 檢查 `instructions.md` 中的指令是否正確
- 更新 `knowledge.md` 中的專案資訊
- 確認 VS Code 中的 Copilot 擴展已啟用

### 配置檔案錯誤
- 檢查 YAML 和 JSON 格式是否正確
- 使用線上工具驗證檔案格式
- 重新生成配置檔案

---

**配置版本**: 1.0  
**最後更新**: 2025年7月29日  
**相容性**: GitHub Copilot 官方格式
