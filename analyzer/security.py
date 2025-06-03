import re

# Define patterns for risky function and module usage
RISKY_PATTERNS = [
    (r"\beval\s*\(", "Use of 'eval' detected, which can execute arbitrary code."),
    (r"\bexec\s*\(", "Use of 'exec' detected, which can execute arbitrary code."),
    (r"\bsubprocess\.", "Use of subprocess module detected, check for unsanitized input."),
    (r"\bos\.system\s*\(", "Use of os.system detected, which may execute unsanitized input."),
    (r"\bpickle\.", "Use of pickle module detected, it is insecure with untrusted input."),
    (r"\binput\s*\(", "Use of input() without validation can lead to security risks.")
]

# Regex for detecting hardcoded secrets
SECRET_PATTERNS = [
    (r"(?i)(password|passwd|secret|token)[\s=]+['\"].{4,}['\"]", "Possible hardcoded secret detected.")
]

def analyze_security(file_path):
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        for pattern, message in RISKY_PATTERNS + SECRET_PATTERNS:
            if re.search(pattern, code):
                issues.append(message)

    except Exception as e:
        issues.append(f"Error scanning file: {str(e)}")

    return issues
