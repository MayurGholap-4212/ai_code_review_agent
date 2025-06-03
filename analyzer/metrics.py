import ast

def analyze_metrics(code):
    """
    Analyze Python source code and return static metrics.
    :param code: source code as string
    :return: dict with metrics
    """
    lines = code.splitlines()
    loc = len(lines)

    # Count comment lines (lines starting with # ignoring leading spaces)
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
    comment_density = comment_lines / loc if loc else 0

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {}

    # Count functions, classes, and average function length
    func_lengths = []
    func_count = 0
    class_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_count += 1
            # Function length = last line number - first line number + 1
            func_len = (node.body[-1].lineno - node.lineno + 1) if node.body else 0
            func_lengths.append(func_len)
        elif isinstance(node, ast.ClassDef):
            class_count += 1

    avg_func_length = sum(func_lengths)/func_count if func_count else 0

    return {
        "loc": loc,
        "comment_lines": comment_lines,
        "comment_density": round(comment_density, 2),
        "function_count": func_count,
        "class_count": class_count,
        "avg_function_length": round(avg_func_length, 2)
    }
