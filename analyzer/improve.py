import os
import shutil
import ast
import autopep8
import astor
import tempfile
import zipfile
from radon.complexity import cc_visit, cc_rank
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from enum import Enum, auto
from dataclasses import dataclass

class PriorityLevel(Enum):
    SECURITY = auto()
    PERFORMANCE = auto()
    READABILITY = auto()

@dataclass
class ImprovementResult:
    file_path: str
    improved_code: str
    metrics: Dict[str, Union[int, float, str]]
    improvements: List[str]
    warnings: List[str]

# Language processors registry
LANGUAGE_PROCESSORS = {}

def register_language(extensions: List[str]):
    """Decorator to register language processors"""
    def decorator(func):
        for ext in extensions:
            LANGUAGE_PROCESSORS[ext.lower()] = func
        return func
    return decorator

def analyze_security(file_path: str) -> List[str]:
    """Analyze code for security vulnerabilities"""
    # Implementation would use tools like bandit or custom rules
    security_issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        if 'pickle.loads(' in content:
            security_issues.append("Unsafe deserialization with pickle")
        if 'eval(' in content:
            security_issues.append("Dangerous eval() usage")
        if 'subprocess.call(' in content and any(c in content for c in [';', '&&', '|']):
            security_issues.append("Possible command injection vulnerability")
            
    return security_issues

@register_language(['.py'])
def improve_python_code(file_path: str, priority: PriorityLevel = PriorityLevel.READABILITY) -> ImprovementResult:
    """Enhanced Python code processor with priority-based improvements"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    security_issues = analyze_security(file_path)
    warnings = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return ImprovementResult(
            file_path=file_path,
            improved_code=code,
            metrics={},
            improvements=[f"Syntax error: {e.msg}"],
            warnings=["File could not be parsed"]
        )

    # Priority-based improvements
    improvements = []
    if priority in [PriorityLevel.READABILITY, PriorityLevel.SECURITY]:
        improved_functions = add_docstrings_to_functions(tree)
        improvements.extend(f"Added docstring to function '{func}'" for func in improved_functions)

    if priority == PriorityLevel.SECURITY:
        security_fixes = apply_security_fixes(tree)
        improvements.extend(security_fixes)

    # Convert AST back to source code
    improved_code = astor.to_source(tree)
    
    if priority == PriorityLevel.READABILITY:
        improved_code = autopep8.fix_code(improved_code)

    # Add security warnings
    if security_issues:
        security_header = "\n".join(f"# SECURITY WARNING: {issue}" for issue in security_issues)
        improved_code = f"{security_header}\n\n{improved_code}"
        warnings.extend(security_issues)

    # Analyze complexity
    complexity_results = analyze_complexity(improved_code)
    improvements.extend(
        f"Function '{func_name}' complexity: {complexity} ({rank})"
        for func_name, complexity, rank in complexity_results
    )

    metrics = compute_code_metrics(code, tree)
    
    return ImprovementResult(
        file_path=file_path,
        improved_code=improved_code,
        metrics=metrics,
        improvements=improvements,
        warnings=warnings
    )

@register_language(['.js', '.ts'])
def improve_javascript_code(file_path: str, priority: PriorityLevel = PriorityLevel.READABILITY) -> ImprovementResult:
    """Enhanced JavaScript/TypeScript processor"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    improvements = []
    warnings = []
    metrics = {
        "Lines of Code": len(code.splitlines()),
        "File Type": "JavaScript/TypeScript"
    }

    # Security checks
    if 'eval(' in code:
        warnings.append("Found eval() usage - potential security risk")
        if priority == PriorityLevel.SECURITY:
            improvements.append("Replaced eval() with safer alternative")
            code = code.replace('eval(', '// SECURITY REMOVED: eval(')

    # Readability improvements
    if priority == PriorityLevel.READABILITY and 'var ' in code:
        improvements.append("Converted 'var' to 'const'/'let' where possible")
        # Simple replacement - in real implementation would use proper parsing
        code = code.replace('var ', 'const ')

    return ImprovementResult(
        file_path=file_path,
        improved_code=code,
        metrics=metrics,
        improvements=improvements,
        warnings=warnings
    )

def process_generic_file(file_path: str) -> ImprovementResult:
    """Fallback processor for unsupported files"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    return ImprovementResult(
        file_path=file_path,
        improved_code=code,
        metrics={
            "Lines of Code": len(code.splitlines()),
            "File Type": "Generic"
        },
        improvements=[],
        warnings=[]
    )

def improve_codebase(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    languages: Optional[List[str]] = None,
    priority: PriorityLevel = PriorityLevel.READABILITY,
    exclude: Optional[List[str]] = None
) -> Dict[str, Union[List[Dict], str]]:
    """
    Process codebase with enhanced features for API integration
    
    Args:
        input_path: Path to directory or zip file
        output_path: Path to output directory
        languages: List of language extensions to process (e.g., ['py', 'js'])
        priority: Improvement priority level
        exclude: List of paths to exclude
        
    Returns:
        Dictionary containing:
        - results: List of improvement summaries
        - temp_dir: Temporary directory path (if zip was processed)
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    exclude = exclude or []
    
    # Handle zip file input
    temp_dir = None
    if input_path.suffix == '.zip':
        temp_dir = Path(tempfile.mkdtemp())
        input_path = temp_dir / "unzipped"
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(input_path)

    # Prepare output directory
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)

    results = []
    for root, dirs, files in os.walk(input_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if str(Path(root) / d) not in exclude]
        
        rel_path = Path(root).relative_to(input_path)
        output_root = output_path / rel_path
        output_root.mkdir(exist_ok=True)

        for file in files:
            file_path = Path(root) / file
            if str(file_path) in exclude:
                continue

            ext = file_path.suffix.lower()
            if languages and ext[1:] not in [lang.lower() for lang in languages]:
                shutil.copy2(file_path, output_root / file)
                continue

            processor = LANGUAGE_PROCESSORS.get(ext, process_generic_file)
            result = processor(file_path, priority)

            # Save improved code
            with open(output_root / file, 'w', encoding='utf-8') as f_out:
                f_out.write(result.improved_code)

            results.append({
                "file": str(file_path.relative_to(input_path)),
                "metrics": result.metrics,
                "improvements": result.improvements,
                "warnings": result.warnings
            })

    return {
        "results": results,
        "temp_dir": str(temp_dir) if temp_dir else None
    }

# Helper functions
def add_docstrings_to_functions(tree) -> List[str]:
    """Add missing docstrings to Python functions"""
    improved = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
            docstring = ast.Expr(value=ast.Constant(value="TODO: Add function description"))
            node.body.insert(0, docstring)
            improved.append(node.name)
    return improved

def apply_security_fixes(tree) -> List[str]:
    """Apply security-related fixes to Python AST"""
    fixes = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and 
            isinstance(node.func, ast.Name) and 
            node.func.id == 'eval'):
            # Replace eval() with safer alternative
            new_node = ast.Call(
                func=ast.Name(id='safe_eval', ctx=ast.Load()),
                args=node.args,
                keywords=node.keywords
            )
            ast.copy_location(new_node, node)
            node.func.id = 'safe_eval'
            fixes.append("Replaced eval() with safe_eval()")
    return fixes

def analyze_complexity(code: str) -> List[Tuple[str, int, str]]:
    """Analyze code complexity using radon"""
    try:
        return [
            (block.name, block.complexity, cc_rank(block.complexity))
            for block in cc_visit(code)
        ]
    except Exception:
        return []

def compute_code_metrics(code: str, tree: ast.AST) -> Dict[str, Union[int, float]]:
    """Compute comprehensive code metrics"""
    lines = code.splitlines()
    loc = len(lines)
    comments = sum(1 for line in lines if line.strip().startswith('#'))
    
    functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    
    func_lengths = []
    for func in functions:
        if func.body:
            last = func.body[-1]
            func_lengths.append(getattr(last, 'lineno', func.lineno) - func.lineno + 1)
    
    return {
        "lines_of_code": loc,
        "comment_lines": comments,
        "comment_density": round(comments / loc, 3) if loc else 0,
        "function_count": len(functions),
        "class_count": len(classes),
        "avg_function_length": round(sum(func_lengths) / len(func_lengths), 2) if func_lengths else 0,
        "max_function_length": max(func_lengths, default=0)
    }