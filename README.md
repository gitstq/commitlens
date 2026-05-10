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
  <strong>轻量级 Git 提交历史智能分析与可视化引擎</strong>
</p>

<p align="center">
  <em>零依赖 · 跨平台 · 开箱即用</em>
</p>

---

## 🎉 项目介绍

**CommitLens** 是一款轻量级的 Git 提交历史智能分析与可视化引擎，专为开发者打造。它能够深入分析您的 Git 仓库提交历史，生成多维度的洞察报告，帮助您更好地理解项目演进、团队协作模式和代码健康度。

### 💡 核心价值

- 🔍 **深度洞察**：全面分析提交历史、作者贡献、文件变更模式
- 📊 **可视化报告**：支持 Markdown、HTML、JSON 多种格式输出
- 🏥 **健康评分**：智能评估仓库健康度，识别潜在风险
- 👥 **团队分析**：贡献者统计、协作网络、Bus Factor 计算
- 🔥 **热点识别**：自动识别高频变更文件，预测代码热点

### ✨ 自研差异化亮点

- **零依赖**：纯 Python 标准库实现，无需安装任何第三方包
- **智能分类**：自动识别 Conventional Commits 规范的提交类型
- **健康评分算法**：综合多维度指标计算仓库健康度
- **热点预测**：基于变更频率和代码量的文件热度评分
- **精美 TUI**：终端彩色仪表盘，直观展示分析结果

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **提交历史分析** | 解析提交记录，提取作者、时间、变更统计等信息 |
| 📝 **提交类型识别** | 自动识别 feat/fix/docs/refactor 等 Conventional Commits 类型 |
| 👥 **贡献者统计** | 统计每位作者的提交数、代码行数、提交类型分布 |
| 🔥 **热点文件识别** | 识别高频变更文件，计算文件热度评分 |
| 📊 **时间分布分析** | 按小时/天/周/月统计提交分布 |
| 🏥 **仓库健康评分** | 综合评估仓库活跃度、作者多样性、Bus Factor 等 |
| 📈 **趋势分析** | 判断项目活动趋势（增长/下降/稳定） |
| 📄 **多格式报告** | 支持 Markdown、HTML、JSON 格式输出 |
| 🖥️ **TUI 仪表盘** | 终端彩色界面，直观展示分析结果 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- Git 命令行工具

### 安装方式

**方式一：直接运行（推荐）**

```bash
# 克隆仓库
git clone https://github.com/gitstq/commitlens.git
cd commitlens

# 直接运行
python commitlens.py
```

**方式二：pip 安装**

```bash
# 从源码安装
pip install -e .
```

### 快速使用

```bash
# 分析当前目录的 Git 仓库
commitlens

# 分析指定仓库
commitlens -p /path/to/repo

# 限制分析最近 100 条提交
commitlens -l 100

# 分析指定时间范围的提交
commitlens --since "2024-01-01" --until "2024-12-31"

# 生成 HTML 报告
commitlens -o report.html

# 生成 Markdown 报告
commitlens -o report.md

# 生成 JSON 报告
commitlens -o report.json
```

---

## 📖 详细使用指南

### 命令行参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--path` | `-p` | Git 仓库路径 | `-p /path/to/repo` |
| `--limit` | `-l` | 限制提交数量 | `-l 100` |
| `--since` | | 起始日期 | `--since "2024-01-01"` |
| `--until` | | 结束日期 | `--until "2024-12-31"` |
| `--author` | `-a` | 按作者筛选 | `-a "张三"` |
| `--branch` | `-b` | 分析指定分支 | `-b develop` |
| `--output` | `-o` | 输出文件路径 | `-o report.html` |
| `--tui` | | 显示 TUI 仪表盘 | `--tui` |
| `--json` | | JSON 格式输出 | `--json` |

---

## 💡 设计思路与迭代规划

### 设计理念

1. **零依赖优先**：使用 Python 标准库，避免依赖地狱
2. **性能优先**：高效解析 Git 数据，支持大型仓库
3. **易用优先**：简洁的命令行接口，开箱即用

### 后续迭代计划

- [ ] 支持更多报告模板
- [ ] 添加代码复杂度分析
- [ ] 支持多仓库对比分析
- [ ] 添加 Web Dashboard

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<p align="center">
  Made with ❤️ by CommitLens Team
</p>
