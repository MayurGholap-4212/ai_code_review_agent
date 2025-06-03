import os
from collections import defaultdict
from pathlib import Path

# Mapping of file extensions to languages
EXTENSION_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.cs': 'C#',
    '.rb': 'Ruby',
    '.go': 'Go',
    '.php': 'PHP',
    '.ts': 'TypeScript',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.rs': 'Rust',
    '.sh': 'Shell',
    '.html': 'HTML',
    '.css': 'CSS',
    '.json': 'JSON',
    '.xml': 'XML',
    # Add more as needed
}
def detect_language(file_path: Path):
    return EXTENSION_MAP.get(file_path.suffix.lower(), 'Unknown')

def count_loc(file_path: Path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def analyze_codebase(input_dir='input'):
    language_stats = defaultdict(lambda: {'files': 0, 'loc': 0, 'files_list': []})
    total_files = 0

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            total_files += 1
            file_path = Path(root) / file
            lang = detect_language(file_path)
            loc = count_loc(file_path)

            language_stats[lang]['files'] += 1
            language_stats[lang]['loc'] += loc
            language_stats[lang]['files_list'].append(str(file_path.relative_to(input_dir)))

    return {
        'total_files': total_files,
        'language_stats': dict(language_stats),  # Convert defaultdict to regular dict
        'input_directory': input_dir
    }

if __name__ == "__main__":
    # Keep this for standalone analysis runs
    results = analyze_codebase()
    print(f"Total files scanned: {results['total_files']}\n")
    for lang, stats in results['language_stats'].items():
        print(f"Language: {lang}")
        print(f"  Files: {stats['files']}")
        print(f"  LOC: {stats['loc']}")
        print(f"  Example files: {stats['files_list'][:3]}{'...' if len(stats['files_list']) > 3 else ''}\n")