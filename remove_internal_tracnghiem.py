import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add import
if 'import TracNghiemTab' not in content:
    content = "import TracNghiemTab from './TracNghiemTab';\n" + content

# 2. Remove function TracNghiemTab
start_idx = content.find('function TracNghiemTab')
if start_idx != -1:
    end_idx = content.find('export default App', start_idx)
    content = content[:start_idx] + content[end_idx:]

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed internal TracNghiemTab")
