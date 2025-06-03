# import argparse
# import os
# import shutil
# import zipfile
# from git import Repo
# from pathlib import Path

# from analyzer.analyze import analyze_codebase  # 🔹 Imported analyzer
# from analyzer.improve import improve_codebase

# improve_codebase("input", "output")

# INPUT_DIR = "input"

# def clear_input_folder():
#     if os.path.exists(INPUT_DIR):
#         shutil.rmtree(INPUT_DIR)
#     os.makedirs(INPUT_DIR)

# def extract_zip(zip_path):
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(INPUT_DIR)

# def clone_git_repo(repo_url):
#     Repo.clone_from(repo_url, INPUT_DIR)

# def copy_local_folder(folder_path):
#     shutil.copytree(folder_path, INPUT_DIR, dirs_exist_ok=True)

# def main():
#     parser = argparse.ArgumentParser(description="AI Code Review Agent")
#     parser.add_argument("--zip", help="Path to ZIP file")
#     parser.add_argument("--git", help="Git repository URL")
#     parser.add_argument("--path", help="Local folder path")

#     args = parser.parse_args()
#     clear_input_folder()

#     if args.zip:
#         print(f"📦 Extracting ZIP file: {args.zip}")
#         extract_zip(args.zip)

#     elif args.git:
#         print(f"🔄 Cloning Git repo: {args.git}")
#         clone_git_repo(args.git)

#     elif args.path:
#         print(f"📁 Copying from local path: {args.path}")
#         copy_local_folder(args.path)

#     else:
#         print("❌ Error: Provide --zip, --git, or --path")
#         exit(1)

#     print(f"\n✅ Codebase loaded into `{INPUT_DIR}` folder")

#     # 🔍 Run Analyzer
#     print("\n🔍 Analyzing codebase...")
#     language_stats = analyze_codebase(INPUT_DIR)

# if __name__ == "__main__":
#     main()
from analyzer.improve import improve_codebase
from analyzer.report_generator import generate_report

from analyzer.improve import improve_codebase
from analyzer.report_generator import generate_report
import argparse
from analyzer.improve import improve_codebase
from analyzer.analyze import analyze_codebase
# from analyzer.report_generator import generate_markdown_report, generate_html_report

def run_with_args():
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument("--path", required=True, help="Input code directory path")
    parser.add_argument("--output", required=True, help="Output directory path")
    parser.add_argument("--priority", default="readability", choices=["security", "performance", "readability"])
    parser.add_argument("--exclude", nargs="*", default=[], help="List of paths to exclude")
    parser.add_argument("--aggressiveness", type=int, default=5, choices=range(1, 11), help="Improvement aggressiveness level (1-10)")

    args = parser.parse_args()

    summary = improve_codebase(args.path, args.output, args.priority, args.exclude, args.aggressiveness)

    print("\n✅ Reports generated:")
    generate_report(summary)

def run_direct():
    input_path = "input"
    output_path = "output"

    summary = improve_codebase(input_path, output_path)
    
    print("\n🔍 Running Code Analysis...")
    language_stats = analyze_codebase(input_path)
    print("\n📄 Summary Report:")
    for item in summary:
        print(f"\nFile: {item['file']}")
        for imp in item["improvements"]:
            print(f"  - {imp}")

    print("\n✅ Reports generated:")
    generate_report(summary)
    
    print("\n📊 Generating Reports...")
    generate_report(summary, language_stats)
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_with_args()
    else:
        run_direct()
