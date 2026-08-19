import json
import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the beginning of TracNghiemTab
start_idx = content.find('function TracNghiemTab(')

if start_idx != -1:
    print("Found TracNghiemTab")
    
    before_trac = content[:start_idx]
    trac_content = content[start_idx:]
    
    # We will replace the entire TracNghiemTab with our newly read file, but we must use a robust way.
    # Actually, let's just make the changes directly to 	rac_content using regex or string replace.
