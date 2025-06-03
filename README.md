# 🧠 AI Code Review Agent

## 📌 Overview

The **AI Code Review Agent** is an intelligent system that automatically analyzes, reviews, and improves codebases. It enhances software quality by identifying issues and applying code enhancements such as refactoring, documentation improvements, and best-practice enforcement.

This tool processes entire projects and produces a new version of the codebase with improvements, accompanied by detailed reports. It supports both command-line interface (CLI) and REST APIs.

---

## 🎯 Purpose

The purpose of this system is to automate the process of code reviews by:

- Identifying syntax errors, code smells, security flaws, and style inconsistencies
- Improving code quality with refactoring and best practice implementations
- Supporting configuration-based customization for different review priorities

---

## 📦 Functional Scope

- Accept full codebases (folder format; ZIP and Git repo coming soon)
- Multi-language support (Python implemented, others planned)
- Code structure parsing and dependency recognition
- Code analysis: complexity, style, bugs, smells, vulnerabilities
- Code improvement: refactoring, docstrings, security practices, performance
- Output generation: improved code + detailed comparison reports
- CLI and REST API support
- Configuration and thresholds for customization

---

## ✅ Functional Requirements Fulfilled

### Input Processing

- ✔ Accepts full codebases in folder format (ZIP and Git support planned)
- ✔ Parses and categorizes Python files
- ✔ Detects structure and functional boundaries in code
- ⚙ Multi-language parsing to be implemented

### Code Analysis

- ✔ Syntax checking (AST parsing, try-except safety)
- ✔ Complexity analysis using AST metrics
- ✔ Missing documentation detection
- ✔ Maintainability scoring (lines of code, comments, etc.)
- ✔ Detection of potential refactoring opportunities

### Code Improvement

- ✔ Adds docstrings to functions/classes
- ✔ Refactors code for clarity and readability
- ✔ Standardizes Python code style (PEP8 compatible)
- ✔ Enhances in-line documentation
- ⚙ Performance optimization (planned)
- ⚙ Security remediation (planned)

### Output Generation

- ✔ New folder structure for improved code (`output/`)
- ✔ Maintains original hierarchy
- ✔ Generates Markdown report per file
- ✔ Summarizes metrics, issues, and improvements

### Configuration and Customization

- ✔ Priority control via `--priority` flag (`readability`, `performance`, `security`)
- ✔ `--aggressiveness` level (1–10)
- ✔ `--exclude` flag to skip specific folders/files
- ✔ Configurable via both CLI and API

---

## ⚙ Non-Functional Features Implemented

- 📄 Handles up to ~1GB codebases (tested up to 300MB)
- ⚡ Parallel processing (to be optimized)
- 🔐 No data storage unless configured
- 📃 Human-readable reports (Markdown)
- 🛠 Compatible with Windows, macOS, Linux
- 🔧 Operates on standard hardware

---

## 🖥️ Interfaces

### CLI Interface

Run from terminal:

```bash
python main.py --path path/to/codebase --output path/to/output --priority readability --aggressiveness 5 --exclude tests docs
