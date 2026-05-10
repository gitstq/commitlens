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
  <strong>Lightweight Git Commit History Intelligent Analysis & Visualization Engine</strong>
</p>

<p align="center">
  <em>Zero Dependencies · Cross-Platform · Ready to Use</em>
</p>

---

## 🎉 Introduction

**CommitLens** is a lightweight Git commit history intelligent analysis and visualization engine designed for developers. It deeply analyzes your Git repository's commit history, generates multi-dimensional insight reports, and helps you better understand project evolution, team collaboration patterns, and code health.

### 💡 Core Value

- 🔍 **Deep Insights**: Comprehensive analysis of commit history, author contributions, file change patterns
- 📊 **Visual Reports**: Support for Markdown, HTML, JSON output formats
- 🏥 **Health Scoring**: Intelligent repository health assessment, identifying potential risks
- 👥 **Team Analysis**: Contributor statistics, collaboration networks, Bus Factor calculation
- 🔥 **Hotspot Detection**: Automatically identify frequently changed files, predict code hotspots

### ✨ Unique Features

- **Zero Dependencies**: Pure Python standard library implementation
- **Smart Classification**: Automatic recognition of Conventional Commits types
- **Health Score Algorithm**: Comprehensive multi-dimensional repository health assessment
- **Beautiful TUI**: Terminal color dashboard for intuitive result display

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Commit History Analysis** | Parse commit records, extract author, time, change statistics |
| 📝 **Commit Type Recognition** | Auto-detect feat/fix/docs/refactor Conventional Commits types |
| 👥 **Contributor Statistics** | Statistics per author: commits, lines, commit type distribution |
| 🔥 **Hot File Detection** | Identify frequently changed files, calculate hotness score |
| 📊 **Time Distribution** | Analyze commit distribution by hour/day/week/month |
| 🏥 **Repository Health Score** | Comprehensive assessment of activity, author diversity, Bus Factor |
| 📈 **Trend Analysis** | Determine project activity trend |
| 📄 **Multi-format Reports** | Support Markdown, HTML, JSON output formats |
| 🖥️ **TUI Dashboard** | Terminal color interface for intuitive result display |

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- Git command-line tool

### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/commitlens.git
cd commitlens

# Run directly
python commitlens.py
```

### Quick Usage

```bash
# Analyze current directory's Git repository
commitlens

# Analyze specific repository
commitlens -p /path/to/repo

# Limit to last 100 commits
commitlens -l 100

# Generate HTML report
commitlens -o report.html

# Generate Markdown report
commitlens -o report.md

# Generate JSON report
commitlens -o report.json
```

---

## 📖 Detailed Usage Guide

### Command Line Arguments

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--path` | `-p` | Git repository path | `-p /path/to/repo` |
| `--limit` | `-l` | Limit number of commits | `-l 100` |
| `--since` | | Start date | `--since "2024-01-01"` |
| `--until` | | End date | `--until "2024-12-31"` |
| `--author` | `-a` | Filter by author | `-a "John"` |
| `--branch` | `-b` | Analyze specific branch | `-b develop` |
| `--output` | `-o` | Output file path | `-o report.html` |

---

## 🤝 Contributing

We welcome all forms of contributions! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by CommitLens Team
</p>
