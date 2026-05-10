<p align="center">
  <a href="README.md">简体中文</a> | 
  <a href="README_EN.md">English</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg" alt="Dependencies">
</p>

<h1 align="center">🔍 CommitLens</h1>

<p align="center">
  <strong>輕量級 Git 提交歷史智能分析與視覺化引擎</strong>
</p>

<p align="center">
  <em>零依賴 · 跨平台 · 開箱即用</em>
</p>

---

## 🎉 專案介紹

**CommitLens** 是一款輕量級的 Git 提交歷史智能分析與視覺化引擎，專為開發者打造。它能夠深入分析您的 Git 倉庫提交歷史，生成多維度的洞察報告，幫助您更好地理解專案演進、團隊協作模式和程式碼健康度。

### 💡 核心價值

- 🔍 **深度洞察**：全面分析提交歷史、作者貢獻、檔案變更模式
- 📊 **視覺化報告**：支援 Markdown、HTML、JSON 多種格式輸出
- 🏥 **健康評分**：智能評估倉庫健康度，識別潛在風險
- 👥 **團隊分析**：貢獻者統計、協作網路、Bus Factor 計算
- 🔥 **熱點識別**：自動識別高頻變更檔案，預測程式碼熱點

### ✨ 自研差異化亮點

- **零依賴**：純 Python 標準庫實現，無需安裝任何第三方套件
- **智能分類**：自動識別 Conventional Commits 規範的提交類型
- **健康評分演算法**：綜合多維度指標計算倉庫健康度
- **熱點預測**：基於變更頻率和程式碼量的檔案熱度評分
- **精美 TUI**：終端彩色儀表板，直觀展示分析結果

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **提交歷史分析** | 解析提交記錄，提取作者、時間、變更統計等資訊 |
| 📝 **提交類型識別** | 自動識別 feat/fix/docs/refactor 等 Conventional Commits 類型 |
| 👥 **貢獻者統計** | 統計每位作者的提交數、程式碼行數、提交類型分佈 |
| 🔥 **熱點檔案識別** | 識別高頻變更檔案，計算檔案熱度評分 |
| 📊 **時間分佈分析** | 按小時/天/週/月統計提交分佈 |
| 🏥 **倉庫健康評分** | 綜合評估倉庫活躍度、作者多樣性、Bus Factor 等 |
| 📈 **趨勢分析** | 判斷專案活動趨勢（增長/下降/穩定） |
| 📄 **多格式報告** | 支援 Markdown、HTML、JSON 格式輸出 |
| 🖥️ **TUI 儀表板** | 終端彩色介面，直觀展示分析結果 |

---

## 🚀 快速開始

### 環境要求

- Python 3.8 或更高版本
- Git 命令列工具

### 安裝方式

```bash
# 複製倉庫
git clone https://github.com/gitstq/commitlens.git
cd commitlens

# 直接執行
python commitlens.py
```

### 快速使用

```bash
# 分析當前目錄的 Git 倉庫
commitlens

# 分析指定倉庫
commitlens -p /path/to/repo

# 限制分析最近 100 條提交
commitlens -l 100

# 生成 HTML 報告
commitlens -o report.html

# 生成 Markdown 報告
commitlens -o report.md

# 生成 JSON 報告
commitlens -o report.json
```

---

## 📖 詳細使用指南

### 命令列參數

| 參數 | 簡寫 | 說明 | 範例 |
|------|------|------|------|
| `--path` | `-p` | Git 倉庫路徑 | `-p /path/to/repo` |
| `--limit` | `-l` | 限制提交數量 | `-l 100` |
| `--since` | | 起始日期 | `--since "2024-01-01"` |
| `--until` | | 結束日期 | `--until "2024-12-31"` |
| `--author` | `-a` | 按作者篩選 | `-a "張三"` |
| `--branch` | `-b` | 分析指定分支 | `-b develop` |
| `--output` | `-o` | 輸出檔案路徑 | `-o report.html` |

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！請查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳情。

---

## 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

<p align="center">
  Made with ❤️ by CommitLens Team
</p>
