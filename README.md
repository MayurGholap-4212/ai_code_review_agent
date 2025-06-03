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

# 🧠 AI Code Review Agent

## 🧾 Arguments

| Argument         | Description                              | Default       |
|------------------|------------------------------------------|---------------|
| `--path`         | Path to codebase folder                  | `input/`      |
| `--output`       | Destination for improved code            | `output/`     |
| `--priority`     | Focus: readability, performance, security| `readability` |
| `--aggressiveness` | Level of improvement (1–10)            | `5`           |
| `--exclude`      | Folders/files to skip                    | `None`        |

---

## 🌐 REST API Interface

### Endpoint

```
POST /api/review
```

### Payload

```json
{
  "files": "ZIP file of codebase or multiple code files",
  "priority": "readability | performance | security",
  "aggressiveness": 1–10,
  "exclude": "comma-separated paths"
}
```

### Response

```json
{
  "message": "Codebase improved successfully.",
  "report_url": "/downloads/report.md",
  "improved_code_url": "/downloads/improved_code.zip"
}
```

---

## 🗂️ Project Structure

```
ai-code-review-agent/
│
├── analyzer/
│   ├── analyzer.py           # AST parsing, complexity, metrics
│   ├── improve.py            # Code improvement logic
│   ├── report_generator.py   # Markdown report generation
│   └── __init__.py
│
├── api/
│   ├── main_api.py           # REST API using FastAPI/Flask
│   └── ...
│
├── input/                    # Default input folder
├── output/                   # Improved code and reports
├── main.py                   # CLI entry point
├── requirements.txt
└── README.md
```

---

## 📈 How It Works

### Input

- Receives codebase from CLI or API

### Parsing

- Scans and parses all Python files using AST

### Analysis

- Metrics: LOC, comments %, cyclomatic complexity
- Checks for missing docstrings, long functions, nested blocks

### Improvement

- Adds docstrings where missing
- Reformats code using standard styling
- Annotates unclear logic with comments

### Output

- Saves to new folder
- Generates Markdown report (one per file)

### API

- Enables remote code submission and response

---

## 🧪 Example CLI Usage

```bash
python main.py --path ./myproject --output ./reviewed --priority readability --aggressiveness 7 --exclude tests
```

---

## 🔮 Future Roadmap

- ✅ ZIP file upload and Git repo cloning  
- ✅ Multi-language support (JavaScript, Java, Go, C++)  
- ✅ Advanced vulnerability scanning  
- ✅ Resource usage optimization (memory/CPU)  
- ✅ Side-by-side HTML/PDF before-after diff reports  
- ✅ CI/CD integration hooks  
- ✅ Web UI (dashboard + config)  
- ✅ Real-time progress tracking  

---

## 🧪 Acceptance Criteria

- ✅ Codebase is analyzed and known issues are detected  
- ✅ Output code maintains original functionality  
- ✅ Detailed reports summarize changes and improvements  
- ✅ CLI/API work as expected  
- ✅ Significant metrics improvement is measurable  

---

## 📚 Reports

Each report contains:

- File summary  
- Lines of code (before/after)  
- Function/class count  
- Complexity metrics  
- Missing/added documentation  
- Changes performed  
- Suggestions (if not implemented automatically)  

---

## 🧰 Requirements

- Python 3.8+

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Contributors

- **Mayur Subhash Gholap** – Developer  
(Add others as needed)

---

## 🛡 License

This project is licensed under the **MIT License**.

---

## 📬 Contact

- **Name:** Mayur Subhash Gholap  
- **Email:** mayurgholap2544@gmail.com  
