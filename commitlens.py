#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CommitLens - Git Commit History Intelligent Analysis & Visualization Engine
Lightweight CLI tool for analyzing Git commit history with zero dependencies.

Author: CommitLens Team
License: MIT
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

__version__ = "1.0.0"
__author__ = "CommitLens Team"

# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class CommitInfo:
    """Represents a single commit's information."""
    hash: str
    short_hash: str
    author: str
    author_email: str
    date: datetime
    message: str
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0
    commit_type: str = "other"
    scope: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            **asdict(self),
            "date": self.date.isoformat()
        }


@dataclass
class AuthorStats:
    """Statistics for a single author."""
    name: str
    email: str
    commits: int = 0
    insertions: int = 0
    deletions: int = 0
    files_changed: int = 0
    commit_types: Dict[str, int] = field(default_factory=dict)
    
    @property
    def lines_changed(self) -> int:
        return self.insertions + self.deletions
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FileStats:
    """Statistics for a single file."""
    path: str
    changes: int = 0
    insertions: int = 0
    deletions: int = 0
    contributors: List[str] = field(default_factory=list)
    
    @property
    def hotness_score(self) -> float:
        """Calculate file hotness score based on change frequency."""
        return self.changes * 0.5 + (self.insertions + self.deletions) * 0.01
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "hotness_score": round(self.hotness_score, 2)
        }


@dataclass
class RepositoryHealth:
    """Repository health metrics."""
    total_commits: int = 0
    total_authors: int = 0
    total_files_changed: int = 0
    total_lines_added: int = 0
    total_lines_removed: int = 0
    avg_commits_per_author: float = 0.0
    avg_files_per_commit: float = 0.0
    commit_type_distribution: Dict[str, int] = field(default_factory=dict)
    bus_factor: int = 0
    health_score: float = 0.0
    activity_trend: str = "stable"
    
    def calculate_health_score(self) -> float:
        """Calculate overall repository health score (0-100)."""
        score = 50.0
        if self.total_authors > 0:
            diversity = min(self.total_authors / 10, 1.0) * 20
            score += diversity
        if self.bus_factor == 1:
            score -= 20
        elif self.bus_factor == 2:
            score -= 10
        if self.activity_trend == "increasing":
            score += 10
        elif self.activity_trend == "decreasing":
            score -= 5
        if self.commit_type_distribution:
            total = sum(self.commit_type_distribution.values())
            if total > 0:
                feat_ratio = self.commit_type_distribution.get("feat", 0) / total
                fix_ratio = self.commit_type_distribution.get("fix", 0) / total
                if 0.2 <= feat_ratio <= 0.5 and fix_ratio >= 0.1:
                    score += 10
        self.health_score = max(0, min(100, score))
        return self.health_score
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "health_score": round(self.health_score, 2)
        }


# =============================================================================
# Git Parser
# =============================================================================

class GitParser:
    """Parse Git repository data using git commands."""
    
    COMMIT_TYPES = {
        "feat": re.compile(r"^(feat|feature)(\(.+\))?\s*:", re.IGNORECASE),
        "fix": re.compile(r"^fix(\(.+\))?\s*:", re.IGNORECASE),
        "docs": re.compile(r"^(docs|documentation)(\(.+\))?\s*:", re.IGNORECASE),
        "style": re.compile(r"^style(\(.+\))?\s*:", re.IGNORECASE),
        "refactor": re.compile(r"^refactor(\(.+\))?\s*:", re.IGNORECASE),
        "test": re.compile(r"^test(\(.+\))?\s*:", re.IGNORECASE),
        "chore": re.compile(r"^chore(\(.+\))?\s*:", re.IGNORECASE),
        "perf": re.compile(r"^(perf|performance)(\(.+\))?\s*:", re.IGNORECASE),
        "ci": re.compile(r"^ci(\(.+\))?\s*:", re.IGNORECASE),
        "build": re.compile(r"^build(\(.+\))?\s*:", re.IGNORECASE),
        "revert": re.compile(r"^revert(\(.+\))?\s*:", re.IGNORECASE),
    }
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self._validate_repo()
    
    def _validate_repo(self) -> None:
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            raise ValueError(f"Not a Git repository: {self.repo_path}")
    
    def _run_git(self, args: List[str]) -> str:
        cmd = ["git", "-C", str(self.repo_path)] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="replace"
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {' '.join(cmd)}\n{e.stderr}")
    
    def _parse_commit_type(self, message: str) -> Tuple[str, str]:
        first_line = message.split("\n")[0].strip()
        for commit_type, pattern in self.COMMIT_TYPES.items():
            match = pattern.match(first_line)
            if match:
                scope_match = re.search(r"\((.+)\)", first_line)
                scope = scope_match.group(1) if scope_match else ""
                return commit_type, scope
        return "other", ""
    
    def get_commits(self, limit: Optional[int] = None, since: Optional[str] = None,
                    until: Optional[str] = None, author: Optional[str] = None,
                    branch: Optional[str] = None) -> List[CommitInfo]:
        fmt = "%H|%h|%an|%ae|%aI|%s"
        args = ["log", f"--format={fmt}", "--numstat"]
        if limit:
            args.append(f"-{limit}")
        if since:
            args.extend(["--since", since])
        if until:
            args.extend(["--until", until])
        if author:
            args.extend(["--author", author])
        if branch:
            args.append(branch)
        output = self._run_git(args)
        commits = []
        current_commit = None
        for line in output.split("\n"):
            if not line.strip():
                continue
            if "|" in line and line.count("|") >= 5:
                if current_commit:
                    commits.append(current_commit)
                parts = line.split("|", 5)
                if len(parts) >= 6:
                    try:
                        date_str = parts[4]
                        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    except (ValueError, IndexError):
                        date = datetime.now()
                    message = parts[5]
                    commit_type, scope = self._parse_commit_type(message)
                    current_commit = CommitInfo(
                        hash=parts[0],
                        short_hash=parts[1],
                        author=parts[2],
                        author_email=parts[3],
                        date=date,
                        message=message,
                        commit_type=commit_type,
                        scope=scope
                    )
            elif current_commit and "\t" in line:
                parts = line.split("\t")
                if len(parts) >= 3:
                    try:
                        insertions = int(parts[0]) if parts[0] != "-" else 0
                        deletions = int(parts[1]) if parts[1] != "-" else 0
                        current_commit.insertions += insertions
                        current_commit.deletions += deletions
                        current_commit.files_changed += 1
                    except ValueError:
                        pass
        if current_commit:
            commits.append(current_commit)
        return commits
    
    def get_file_stats(self, commits: List[CommitInfo]) -> Dict[str, FileStats]:
        file_stats: Dict[str, FileStats] = {}
        for commit in commits:
            try:
                output = self._run_git([
                    "diff-tree", "--no-commit-id", "--numstat", "-r", commit.hash
                ])
                for line in output.split("\n"):
                    if not line.strip():
                        continue
                    parts = line.split("\t")
                    if len(parts) >= 3:
                        file_path = parts[2]
                        if file_path not in file_stats:
                            file_stats[file_path] = FileStats(path=file_path)
                        try:
                            insertions = int(parts[0]) if parts[0] != "-" else 0
                            deletions = int(parts[1]) if parts[1] != "-" else 0
                            file_stats[file_path].insertions += insertions
                            file_stats[file_path].deletions += deletions
                        except ValueError:
                            pass
                        file_stats[file_path].changes += 1
                        if commit.author not in file_stats[file_path].contributors:
                            file_stats[file_path].contributors.append(commit.author)
            except RuntimeError:
                continue
        return file_stats


# =============================================================================
# Analyzer
# =============================================================================

class CommitAnalyzer:
    """Analyze Git commit history and generate insights."""
    
    def __init__(self, commits: List[CommitInfo], file_stats: Dict[str, FileStats]):
        self.commits = commits
        self.file_stats = file_stats
        self._author_stats: Dict[str, AuthorStats] = {}
        self._calculate_author_stats()
    
    def _calculate_author_stats(self) -> None:
        for commit in self.commits:
            key = f"{commit.author} <{commit.author_email}>"
            if key not in self._author_stats:
                self._author_stats[key] = AuthorStats(
                    name=commit.author,
                    email=commit.author_email
                )
            stats = self._author_stats[key]
            stats.commits += 1
            stats.insertions += commit.insertions
            stats.deletions += commit.deletions
            stats.files_changed += commit.files_changed
            if commit.commit_type not in stats.commit_types:
                stats.commit_types[commit.commit_type] = 0
            stats.commit_types[commit.commit_type] += 1
    
    def get_author_stats(self) -> Dict[str, AuthorStats]:
        return self._author_stats
    
    def get_time_distribution(self, granularity: str = "day") -> Dict[str, int]:
        distribution: Dict[str, int] = defaultdict(int)
        for commit in self.commits:
            if granularity == "hour":
                key = commit.date.strftime("%H:00")
            elif granularity == "day":
                key = commit.date.strftime("%Y-%m-%d")
            elif granularity == "week":
                key = commit.date.strftime("%Y-W%W")
            elif granularity == "month":
                key = commit.date.strftime("%Y-%m")
            else:
                key = commit.date.strftime("%Y")
            distribution[key] += 1
        return dict(sorted(distribution.items()))
    
    def get_commit_type_distribution(self) -> Dict[str, int]:
        distribution: Dict[str, int] = defaultdict(int)
        for commit in self.commits:
            distribution[commit.commit_type] += 1
        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
    
    def get_hot_files(self, top_n: int = 10) -> List[FileStats]:
        sorted_files = sorted(
            self.file_stats.values(),
            key=lambda f: f.hotness_score,
            reverse=True
        )
        return sorted_files[:top_n]
    
    def calculate_bus_factor(self) -> int:
        if not self._author_stats:
            return 0
        sorted_authors = sorted(
            self._author_stats.values(),
            key=lambda a: a.commits,
            reverse=True
        )
        total_commits = sum(a.commits for a in sorted_authors)
        if total_commits == 0:
            return 0
        cumulative = 0
        bus_factor = 0
        for author in sorted_authors:
            cumulative += author.commits
            bus_factor += 1
            if cumulative >= total_commits * 0.5:
                break
        return bus_factor
    
    def calculate_activity_trend(self) -> str:
        if len(self.commits) < 10:
            return "stable"
        mid = len(self.commits) // 2
        recent_commits = self.commits[:mid]
        older_commits = self.commits[mid:]
        def commits_per_day(commits: List[CommitInfo]) -> float:
            if not commits:
                return 0
            dates = [c.date.date() for c in commits]
            unique_days = len(set(dates))
            return len(commits) / max(unique_days, 1)
        recent_rate = commits_per_day(recent_commits)
        older_rate = commits_per_day(older_commits)
        if older_rate == 0:
            return "increasing" if recent_rate > 0 else "stable"
        ratio = recent_rate / older_rate
        if ratio > 1.2:
            return "increasing"
        elif ratio < 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def calculate_repository_health(self) -> RepositoryHealth:
        health = RepositoryHealth()
        health.total_commits = len(self.commits)
        health.total_authors = len(self._author_stats)
        health.total_files_changed = len(self.file_stats)
        health.total_lines_added = sum(c.insertions for c in self.commits)
        health.total_lines_removed = sum(c.deletions for c in self.commits)
        if health.total_authors > 0:
            health.avg_commits_per_author = health.total_commits / health.total_authors
        if health.total_commits > 0:
            health.avg_files_per_commit = sum(c.files_changed for c in self.commits) / health.total_commits
        health.commit_type_distribution = self.get_commit_type_distribution()
        health.bus_factor = self.calculate_bus_factor()
        health.activity_trend = self.calculate_activity_trend()
        health.calculate_health_score()
        return health


# =============================================================================
# Report Generator
# =============================================================================

class ReportGenerator:
    """Generate reports in various formats."""
    
    def __init__(self, analyzer: CommitAnalyzer, repo_name: str = "Repository"):
        self.analyzer = analyzer
        self.repo_name = repo_name
    
    def generate_markdown(self) -> str:
        health = self.analyzer.calculate_repository_health()
        author_stats = self.analyzer.get_author_stats()
        hot_files = self.analyzer.get_hot_files()
        commit_types = self.analyzer.get_commit_type_distribution()
        time_dist = self.analyzer.get_time_distribution("month")
        lines = [
            f"# 📊 CommitLens Report: {self.repo_name}",
            "",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 🏥 Repository Health Score",
            "",
            f"**Score**: {health.health_score:.1f}/100",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Commits | {health.total_commits} |",
            f"| Total Authors | {health.total_authors} |",
            f"| Files Changed | {health.total_files_changed} |",
            f"| Lines Added | {health.total_lines_added:,} |",
            f"| Lines Removed | {health.total_lines_removed:,} |",
            f"| Bus Factor | {health.bus_factor} |",
            f"| Activity Trend | {health.activity_trend} |",
            "",
            "---",
            "",
            "## 👥 Top Contributors",
            "",
            "| Author | Commits | Lines Changed |",
            "|--------|---------|---------------|",
        ]
        sorted_authors = sorted(author_stats.values(), key=lambda a: a.commits, reverse=True)[:10]
        for author in sorted_authors:
            lines.append(f"| {author.name} | {author.commits} | {author.lines_changed:,} |")
        lines.extend([
            "",
            "---",
            "",
            "## 📝 Commit Types Distribution",
            "",
            "| Type | Count | Percentage |",
            "|------|-------|------------|",
        ])
        total_commits = sum(commit_types.values())
        for ctype, count in commit_types:
            pct = (count / total_commits * 100) if total_commits > 0 else 0
            lines.append(f"| {ctype} | {count} | {pct:.1f}% |")
        lines.extend([
            "",
            "---",
            "",
            "## 🔥 Hot Files (Most Changed)",
            "",
            "| File | Changes | Hotness Score |",
            "|------|---------|---------------|",
        ])
        for f in hot_files:
            lines.append(f"| {f.path} | {f.changes} | {f.hotness_score:.2f} |")
        lines.extend([
            "",
            "---",
            "",
            f"*Generated by CommitLens v{__version__}*",
        ])
        return "\n".join(lines)
    
    def generate_html(self) -> str:
        health = self.analyzer.calculate_repository_health()
        author_stats = self.analyzer.get_author_stats()
        hot_files = self.analyzer.get_hot_files()
        commit_types = self.analyzer.get_commit_type_distribution()
        if health.health_score >= 80:
            score_color = "#28a745"
        elif health.health_score >= 60:
            score_color = "#ffc107"
        else:
            score_color = "#dc3545"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CommitLens Report - {self.repo_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f6f8fa; color: #24292e; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .score-card {{ background: white; border-radius: 10px; padding: 30px; text-align: center; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .score-value {{ font-size: 4em; font-weight: bold; color: {score_color}; }}
        .score-label {{ color: #586069; font-size: 1.2em; margin-top: 10px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .card h2 {{ color: #24292e; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #e1e4e8; }}
        .metric {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e1e4e8; }}
        .metric:last-child {{ border-bottom: none; }}
        .metric-label {{ color: #586069; }}
        .metric-value {{ font-weight: 600; color: #24292e; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e1e4e8; }}
        th {{ background: #f6f8fa; font-weight: 600; }}
        tr:hover {{ background: #f6f8fa; }}
        .footer {{ text-align: center; padding: 20px; color: #586069; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 CommitLens Report</h1>
            <p>{self.repo_name}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        <div class="score-card">
            <div class="score-value">{health.health_score:.1f}</div>
            <div class="score-label">Repository Health Score</div>
        </div>
        <div class="grid">
            <div class="card">
                <h2>📈 Overview</h2>
                <div class="metric"><span class="metric-label">Total Commits</span><span class="metric-value">{health.total_commits}</span></div>
                <div class="metric"><span class="metric-label">Total Authors</span><span class="metric-value">{health.total_authors}</span></div>
                <div class="metric"><span class="metric-label">Files Changed</span><span class="metric-value">{health.total_files_changed}</span></div>
                <div class="metric"><span class="metric-label">Lines Added</span><span class="metric-value">{health.total_lines_added:,}</span></div>
                <div class="metric"><span class="metric-label">Lines Removed</span><span class="metric-value">{health.total_lines_removed:,}</span></div>
                <div class="metric"><span class="metric-label">Bus Factor</span><span class="metric-value">{health.bus_factor}</span></div>
                <div class="metric"><span class="metric-label">Activity Trend</span><span class="metric-value">{health.activity_trend}</span></div>
            </div>
            <div class="card">
                <h2>👥 Top Contributors</h2>
                <table><thead><tr><th>Author</th><th>Commits</th><th>Lines Changed</th></tr></thead><tbody>
"""
        sorted_authors = sorted(author_stats.values(), key=lambda a: a.commits, reverse=True)[:10]
        for author in sorted_authors:
            html += f'                    <tr><td>{author.name}</td><td>{author.commits}</td><td>{author.lines_changed:,}</td></tr>\n'
        html += f"""                </tbody></table>
            </div>
        </div>
        <div class="footer">
            Generated by <strong>CommitLens</strong> v{__version__} | MIT License
        </div>
    </div>
</body>
</html>"""
        return html
    
    def generate_json(self) -> str:
        health = self.analyzer.calculate_repository_health()
        author_stats = self.analyzer.get_author_stats()
        hot_files = self.analyzer.get_hot_files()
        commit_types = self.analyzer.get_commit_type_distribution()
        report = {
            "repository": self.repo_name,
            "generated_at": datetime.now().isoformat(),
            "version": __version__,
            "health": health.to_dict(),
            "commit_types": commit_types,
            "top_contributors": [
                {"name": a.name, "email": a.email, "commits": a.commits, "lines_changed": a.lines_changed}
                for a in sorted(author_stats.values(), key=lambda x: x.commits, reverse=True)[:20]
            ],
            "hot_files": [f.to_dict() for f in hot_files[:20]],
        }
        return json.dumps(report, indent=2, ensure_ascii=False)


# =============================================================================
# TUI Dashboard
# =============================================================================

class TUIDashboard:
    """Simple Terminal User Interface for displaying analysis results."""
    
    COLORS = {
        "reset": "\033[0m", "bold": "\033[1m", "red": "\033[91m", "green": "\033[92m",
        "yellow": "\033[93m", "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
        "white": "\033[97m", "dim": "\033[2m",
    }
    
    EMOJIS = {
        "feat": "✨", "fix": "🐛", "docs": "📚", "style": "💎", "refactor": "♻️",
        "test": "🧪", "chore": "🔧", "perf": "⚡", "ci": "👷", "build": "📦",
        "revert": "⏪", "other": "📝",
    }
    
    def __init__(self, analyzer: CommitAnalyzer, repo_name: str = "Repository"):
        self.analyzer = analyzer
        self.repo_name = repo_name
    
    def _color(self, text: str, color: str) -> str:
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
    
    def _progress_bar(self, value: float, max_value: float, width: int = 20) -> str:
        if max_value == 0:
            filled = 0
        else:
            filled = int((value / max_value) * width)
        bar = "█" * filled + "░" * (width - filled)
        return self._color(bar, "cyan")
    
    def render(self) -> str:
        health = self.analyzer.calculate_repository_health()
        author_stats = self.analyzer.get_author_stats()
        hot_files = self.analyzer.get_hot_files()
        commit_types = self.analyzer.get_commit_type_distribution()
        lines = []
        lines.append("")
        lines.append(self._color("╔══════════════════════════════════════════════════════════════════╗", "cyan"))
        lines.append(self._color("║", "cyan") + self._color(f"  📊 CommitLens Dashboard: {self.repo_name}", "bold").center(66) + self._color("║", "cyan"))
        lines.append(self._color("╚══════════════════════════════════════════════════════════════════╝", "cyan"))
        lines.append("")
        score_color = "green" if health.health_score >= 80 else ("yellow" if health.health_score >= 60 else "red")
        lines.append(f"  {self._color('🏥 Repository Health Score', 'bold')}")
        lines.append(f"  ┌─────────────────────────────────────────────────────────────────┐")
        lines.append(f"  │  Score: {self._color(f'{health.health_score:.1f}/100', score_color)}  │  Trend: {self._color(health.activity_trend, 'blue')}  │  Bus Factor: {self._color(str(health.bus_factor), 'magenta')}  │")
        lines.append(f"  └─────────────────────────────────────────────────────────────────┘")
        lines.append("")
        lines.append(f"  {self._color('📈 Overview Statistics', 'bold')}")
        lines.append(f"  ┌──────────────────┬──────────────────┬──────────────────┐")
        lines.append(f"  │ Total Commits    │ Total Authors    │ Files Changed    │")
        lines.append(f"  │  {self._color(str(health.total_commits), 'green'):>14}  │  {self._color(str(health.total_authors), 'green'):>14}  │  {self._color(str(health.total_files_changed), 'green'):>14}  │")
        lines.append(f"  ├──────────────────┼──────────────────┼──────────────────┤")
        lines.append(f"  │ Lines Added      │ Lines Removed    │ Net Lines        │")
        net_lines = health.total_lines_added - health.total_lines_removed
        lines.append(f"  │  {self._color(f'{health.total_lines_added:,}', 'green'):>14}  │  {self._color(f'{health.total_lines_removed:,}', 'red'):>14}  │  {self._color(f'{net_lines:+,}', 'yellow'):>14}  │")
        lines.append(f"  └──────────────────┴──────────────────┴──────────────────┘")
        lines.append("")
        lines.append(f"  {self._color('📝 Commit Types Distribution', 'bold')}")
        total_commits = sum(commit_types.values())
        max_count = max(commit_types.values()) if commit_types else 1
        for ctype, count in list(commit_types.items())[:6]:
            emoji = self.EMOJIS.get(ctype, "📝")
            pct = (count / total_commits * 100) if total_commits > 0 else 0
            bar = self._progress_bar(count, max_count, 15)
            lines.append(f"  {emoji} {ctype:10} {bar} {self._color(str(count), 'cyan'):>5} ({pct:>5.1f}%)")
        lines.append("")
        lines.append(f"  {self._color('👥 Top Contributors', 'bold')}")
        lines.append(f"  ┌────────────────────────────────┬─────────┬──────────────┐")
        lines.append(f"  │ Author                         │ Commits │ Lines Changed│")
        lines.append(f"  ├────────────────────────────────┼─────────┼──────────────┤")
        sorted_authors = sorted(author_stats.values(), key=lambda a: a.commits, reverse=True)[:5]
        for author in sorted_authors:
            name = author.name[:28] + "..." if len(author.name) > 28 else author.name
            lines.append(f"  │ {name:30} │ {author.commits:>7} │ {author.lines_changed:>12,} │")
        lines.append(f"  └────────────────────────────────┴─────────┴──────────────┘")
        lines.append("")
        lines.append(self._color(f"  Generated by CommitLens v{__version__}", "dim"))
        lines.append("")
        return "\n".join(lines)


# =============================================================================
# CLI Interface
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="commitlens",
        description="🔍 CommitLens - Git Commit History Intelligent Analysis & Visualization Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  commitlens                          Analyze current repository
  commitlens -p /path/to/repo         Analyze specific repository
  commitlens -l 100                   Analyze last 100 commits
  commitlens --since "2024-01-01"     Analyze commits since date
  commitlens -o report.html           Generate HTML report
  commitlens -o report.md             Generate Markdown report
  commitlens -o report.json           Generate JSON report
        """
    )
    parser.add_argument("-p", "--path", default=".", help="Path to Git repository")
    parser.add_argument("-l", "--limit", type=int, default=None, help="Limit number of commits")
    parser.add_argument("--since", default=None, help="Analyze commits since date")
    parser.add_argument("--until", default=None, help="Analyze commits until date")
    parser.add_argument("-a", "--author", default=None, help="Filter by author")
    parser.add_argument("-b", "--branch", default=None, help="Analyze specific branch")
    parser.add_argument("-o", "--output", default=None, help="Output file path")
    parser.add_argument("--tui", action="store_true", help="Show TUI dashboard")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        git_parser = GitParser(args.path)
        repo_name = git_parser.repo_path.name
        print(f"🔍 Analyzing repository: {repo_name}", file=sys.stderr)
        commits = git_parser.get_commits(
            limit=args.limit, since=args.since, until=args.until,
            author=args.author, branch=args.branch
        )
        if not commits:
            print("⚠️ No commits found matching the criteria.", file=sys.stderr)
            sys.exit(0)
        print(f"📊 Found {len(commits)} commits", file=sys.stderr)
        print("📁 Analyzing file statistics...", file=sys.stderr)
        file_stats = git_parser.get_file_stats(commits)
        analyzer = CommitAnalyzer(commits, file_stats)
        generator = ReportGenerator(analyzer, repo_name)
        if args.output:
            output_path = Path(args.output)
            ext = output_path.suffix.lower()
            if ext == ".md":
                content = generator.generate_markdown()
            elif ext == ".html":
                content = generator.generate_html()
            elif ext == ".json":
                content = generator.generate_json()
            else:
                print(f"❌ Unsupported output format: {ext}", file=sys.stderr)
                sys.exit(1)
            output_path.write_text(content, encoding="utf-8")
            print(f"✅ Report saved to: {output_path}", file=sys.stderr)
        elif args.json:
            print(generator.generate_json())
        else:
            dashboard = TUIDashboard(analyzer, repo_name)
            print(dashboard.render())
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ Git error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
