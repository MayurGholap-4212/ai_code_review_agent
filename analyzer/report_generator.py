import os
from datetime import datetime

def generate_report(improvements_summary, analysis_results=None, report_dir="reports"):
    """
    Generate comprehensive Markdown and HTML reports from code review and analysis results.
    
    Args:
        improvements_summary (list): List of dictionaries containing file-specific improvements
        analysis_results (dict): Results from analyze_codebase() containing:
            - total_files: int
            - language_stats: dict
            - input_directory: str
        report_dir (str): Directory to save reports (default: "reports")
    
    Returns:
        tuple: Paths to generated Markdown and HTML files
    """
    os.makedirs(report_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = os.path.join(report_dir, f"report_{timestamp}.md")
    html_path = os.path.join(report_dir, f"report_{timestamp}.html")

    # Generate Markdown report
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write("# AI Code Review Report\n\n")
        md_file.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        # Add analysis overview if available
        if analysis_results:
            md_file.write("## Codebase Overview\n\n")
            md_file.write(f"- **Total Files Analyzed**: {analysis_results['total_files']}\n")
            md_file.write(f"- **Source Directory**: `{analysis_results['input_directory']}`\n\n")
            
            md_file.write("### Language Distribution\n")
            md_file.write("| Language | Files | Lines of Code |\n")
            md_file.write("|----------|-------|---------------|\n")
            for lang, stats in analysis_results['language_stats'].items():
                md_file.write(f"| {lang} | {stats['files']} | {stats['loc']} |\n")
            md_file.write("\n---\n\n")

        # Add detailed file-by-file review
        md_file.write("## Detailed Review\n\n")
        for item in improvements_summary:
            md_file.write(f"### File: `{item['file']}`\n\n")

            if 'metrics' in item and item['metrics']:
                md_file.write("#### Code Metrics\n")
                md_file.write("| Metric | Value |\n")
                md_file.write("|--------|-------|\n")
                for key, value in item['metrics'].items():
                    md_file.write(f"| {key} | {value} |\n")
                md_file.write("\n")

            if 'improvements' in item and item['improvements']:
                md_file.write("#### Suggested Improvements\n")
                for imp in item['improvements']:
                    md_file.write(f"- {imp}\n")
            else:
                md_file.write("No improvements suggested.\n")
            
            md_file.write("\n---\n\n")

    # Generate HTML report
    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Code Review Report</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0 auto; max-width: 900px; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { color: #2980b9; margin-top: 30px; }
        h3 { color: #16a085; }
        h4 { color: #8e44ad; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        ul { padding-left: 20px; }
        .timestamp { color: #7f8c8d; font-style: italic; }
        .file-path { font-family: monospace; background-color: #f5f5f5; padding: 2px 5px; }
        .overview-card { 
            background: #f8f9fa; 
            border-left: 4px solid #3498db; 
            padding: 15px; 
            margin-bottom: 20px; 
        }
        hr { border: 0; height: 1px; background: #ddd; margin: 30px 0; }
    </style>
</head>
<body>
    <h1>AI Code Review Report</h1>
    <p class="timestamp">Generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
""")
        
        # Add analysis overview if available
        if analysis_results:
            html_file.write("""
    <div class="overview-card">
        <h2>Codebase Overview</h2>
        <p><strong>Total Files Analyzed:</strong> """ + str(analysis_results['total_files']) + """</p>
        <p><strong>Source Directory:</strong> <span class="file-path">""" + analysis_results['input_directory'] + """</span></p>
        
        <h3>Language Distribution</h3>
        <table>
            <thead>
                <tr>
                    <th>Language</th>
                    <th>Files</th>
                    <th>Lines of Code</th>
                </tr>
            </thead>
            <tbody>
""")
            for lang, stats in analysis_results['language_stats'].items():
                html_file.write(f"""
                <tr>
                    <td>{lang}</td>
                    <td>{stats['files']}</td>
                    <td>{stats['loc']}</td>
                </tr>
""")
            html_file.write("""
            </tbody>
        </table>
    </div>
    <hr />
""")

        # Add detailed file-by-file review
        html_file.write("""
    <h2>Detailed Review</h2>
""")
        for item in improvements_summary:
            html_file.write(f"""
    <div class="file-review">
        <h3>File: <span class="file-path">{item['file']}</span></h3>
""")

            if 'metrics' in item and item['metrics']:
                html_file.write("""
        <h4>Code Metrics</h4>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
""")
                for key, value in item['metrics'].items():
                    html_file.write(f"""
                <tr>
                    <td>{key}</td>
                    <td>{value}</td>
                </tr>
""")
                html_file.write("""
            </tbody>
        </table>
""")

            if 'improvements' in item and item['improvements']:
                html_file.write("""
        <h4>Suggested Improvements</h4>
        <ul>
""")
                for imp in item['improvements']:
                    html_file.write(f"""
            <li>{imp}</li>
""")
                html_file.write("""
        </ul>
""")
            else:
                html_file.write("""
        <p>No improvements suggested.</p>
""")
            
            html_file.write("""
    </div>
    <hr />
""")

        html_file.write("""
</body>
</html>
""")

    return md_path, html_path


# Example usage with both analysis and improvements data
if __name__ == "__main__":
    sample_analysis = {
        'total_files': 42,
        'input_directory': 'input',
        'language_stats': {
            'Python': {'files': 35, 'loc': 4200, 'files_list': ['main.py', 'utils.py']},
            'JavaScript': {'files': 7, 'loc': 1200, 'files_list': ['app.js']}
        }
    }
    
    sample_improvements = [
        {
            'file': 'src/main.py',
            'metrics': {'Complexity': 8, 'LOC': 120},
            'improvements': ['Add docstrings', 'Reduce function length']
        }
    ]
    
    md, html = generate_report(sample_improvements, sample_analysis)
    print(f"Generated reports:\n- Markdown: {md}\n- HTML: {html}")