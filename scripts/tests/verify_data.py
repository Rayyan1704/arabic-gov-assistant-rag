"""Data quality verification script"""
import os
import glob

def verify_data():
    categories = ['health', 'education', 'business', 'transportation', 'justice', 'housing', 'culture', 'info']
    
    total_files = 0
    issues_found = 0
    
    for cat in categories:
        files = glob.glob(f'data/{cat}/*.txt')
        print(f"\n{'='*60}")
        print(f"📁 {cat.upper()}: {len(files)} files")
        print(f"{'='*60}")
        
        total_files += len(files)
        
        for f in files:
            filename = os.path.basename(f)
            has_issues = False
            
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Check minimum length
                if len(content) < 500:
                    print(f"  ❌ {filename} - Too short ({len(content)} chars)")
                    has_issues = True
                    issues_found += 1
                
                # Check for English remnants
                english_ui = ['provider', 'service type', 'click here', 'submit', 'login']
                found_english = [x for x in english_ui if x.lower() in content.lower()]
                if found_english:
                    print(f"  ⚠️ {filename} - Contains English UI text: {found_english}")
                    has_issues = True
                    issues_found += 1
                
                # Check Arabic content
                arabic_chars = len([c for c in content if '\u0600' <= c <= '\u06FF'])
                if arabic_chars < 200:
                    print(f"  ❌ {filename} - Not enough Arabic ({arabic_chars} chars)")
                    has_issues = True
                    issues_found += 1
                
                # Check for required sections
                required_sections = ['وصف الخدمة', 'المستندات المطلوبة']
                missing_sections = [s for s in required_sections if s not in content]
                if missing_sections:
                    print(f"  ⚠️ {filename} - Missing sections: {missing_sections}")
                    has_issues = True
                    issues_found += 1
                
                if not has_issues:
                    print(f"  ✅ {filename} - OK ({len(content)} chars, {arabic_chars} Arabic)")
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"Total files checked: {total_files}")
    print(f"Issues found: {issues_found}")
    if issues_found == 0:
        print("✅ All files passed verification!")
    else:
        print(f"⚠️ {issues_found} issues need attention")

if __name__ == "__main__":
    verify_data()
