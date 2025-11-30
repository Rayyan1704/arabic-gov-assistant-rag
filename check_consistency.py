"""
Comprehensive consistency checker for all project files.
Checks for:
- Model name inconsistencies (Gemini 1.5 vs 2.0)
- Metric inconsistencies
- File path references
- Outdated information
"""

import os
import re
from pathlib import Path

# Define correct values
CORRECT_VALUES = {
    'gemini_model': 'gemini-2.0-flash',
    'accuracy': '96.0%',
    'accuracy_fraction': '96/100',
    'arabic_accuracy': '96.0%',
    'english_accuracy': '96.0%',
    'response_time': '0.16s',
    'documents': '51',
    'categories': '8',
    'p_value': 'p < 0.0001',
    'embedding_model': 'paraphrase-multilingual-mpnet-base-v2',
    'embedding_dim': '768',
}

# Patterns to check
PATTERNS = {
    'gemini_wrong': r'gemini[- ]1\.5[- ]flash',
    'gemini_correct': r'gemini[- ]2\.0[- ]flash',
    'old_accuracy': r'(90|85|84)%',
    'old_response_time': r'(3\.2|2\.1|3-5)s',
    'old_documents': r'50 documents',
    'deleted_files': [
        'test_production_system',
        'test_final_accuracy',
        'show_system_summary',
        'PROJECT_SETUP',
        'PROJECT_STRUCTURE',
        'DEPLOYMENT_GUIDE',
        'RESEARCH_ROADMAP',
        'FINAL_COMPLETE_STATUS',
    ]
}

issues = []

def check_file(filepath):
    """Check a single file for issues"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        file_issues = []
        
        # Check for wrong Gemini version
        if re.search(PATTERNS['gemini_wrong'], content, re.IGNORECASE):
            file_issues.append(f"  ❌ Found 'Gemini 1.5 Flash' (should be 2.0 Flash)")
        
        # Check for old accuracy values (in markdown files)
        if filepath.endswith('.md'):
            if re.search(r'\b90%\b.*accuracy', content, re.IGNORECASE):
                file_issues.append(f"  ⚠️  Found '90% accuracy' (should be 96%)")
            if re.search(r'\b85%\b.*accuracy', content, re.IGNORECASE):
                file_issues.append(f"  ⚠️  Found '85% accuracy' (should be 96%)")
        
        # Check for old response time
        if re.search(r'3-5\s*seconds', content):
            file_issues.append(f"  ⚠️  Found '3-5 seconds' (should be 0.16s)")
        
        # Check for references to deleted files
        for deleted_file in PATTERNS['deleted_files']:
            if deleted_file in content and not filepath.endswith('.py'):
                file_issues.append(f"  ⚠️  References deleted file: {deleted_file}")
        
        # Check for old document count
        if re.search(r'50\s+documents', content) and '51' not in content:
            file_issues.append(f"  ⚠️  Found '50 documents' (should be 51)")
        
        if file_issues:
            return filepath, file_issues
            
    except Exception as e:
        return filepath, [f"  ❌ Error reading file: {e}"]
    
    return None, []

def main():
    print("="*80)
    print("CONSISTENCY CHECK - Scanning all project files")
    print("="*80)
    
    # Files to check
    extensions = ['.md', '.py', '.txt', '.json']
    exclude_dirs = {'.venv', '.git', '__pycache__', 'node_modules'}
    
    files_checked = 0
    files_with_issues = 0
    
    for root, dirs, files in os.walk('.'):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                files_checked += 1
                
                file_path, file_issues = check_file(filepath)
                if file_issues:
                    files_with_issues += 1
                    print(f"\n📄 {filepath}")
                    for issue in file_issues:
                        print(issue)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Files checked: {files_checked}")
    print(f"Files with issues: {files_with_issues}")
    
    if files_with_issues == 0:
        print("\n✅ No issues found! Project is consistent.")
    else:
        print(f"\n⚠️  Found issues in {files_with_issues} files.")
        print("\nRecommendation: Review and fix the issues above.")

if __name__ == '__main__':
    main()
