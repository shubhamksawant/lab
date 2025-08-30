#!/usr/bin/env python3
"""
Script to fix missing language specifiers in code blocks for Expected Output sections.
"""

import re
import os

def fix_code_blocks(file_path):
    """Fix missing language specifiers in code blocks."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to find code blocks that start with just ``` (no language)
    # and are preceded by **Expected Output:**
    pattern = r'(\*\*Expected Output:\*\*\s*\n)```\n(.*?)\n```'
    
    def replace_func(match):
        expected_output = match.group(1)
        content_part = match.group(2)
        
        # Determine the appropriate language for the code block
        if 'json' in content_part.lower() or '{' in content_part:
            lang = 'json'
        elif 'html' in content_part.lower() or '<' in content_part:
            lang = 'html'
        elif any(cmd in content_part.lower() for cmd in ['docker', 'kubectl', 'curl', 'psql', 'k3d', 'helm', 'INFO', 'NAME', 'STATUS']):
            lang = 'bash'
        else:
            lang = 'bash'
        
        return f'{expected_output}```{lang}\n{content_part}\n```'
    
    # Apply the fix
    fixed_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.write(fixed_content)
    
    return content != fixed_content

def main():
    """Main function to process all milestone documents."""
    # Process all milestone documents
    milestone_files = [f for f in os.listdir('docs') if f.startswith('0') and f.endswith('.md')]
    milestone_files.sort()
    
    print("Fixing missing language specifiers in code blocks...")
    
    for file in milestone_files:
        file_path = os.path.join('docs', file)
        print(f'Processing {file}...')
        try:
            changed = fix_code_blocks(file_path)
            if changed:
                print(f'  ✅ Fixed code blocks in {file}')
            else:
                print(f'  ℹ️  No changes needed in {file}')
        except Exception as e:
            print(f'  ❌ Error processing {file}: {e}')
    
    print('\n🎉 Code block fix complete!')

if __name__ == '__main__':
    main()
