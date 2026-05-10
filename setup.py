#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CommitLens - Git Commit History Intelligent Analysis & Visualization Engine"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="commitlens",
    version="1.0.0",
    author="CommitLens Team",
    author_email="commitlens@example.com",
    description="🔍 Git Commit History Intelligent Analysis & Visualization Engine - Zero dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/commitlens",
    license="MIT",
    py_modules=["commitlens"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "commitlens=commitlens:main",
        ],
    },
    keywords="git commit analysis visualization cli dashboard",
)
