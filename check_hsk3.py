import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"const hsk3Vocab = \{.*?\};", content, re.DOTALL)
if match:
    print(match.group(0).encode('utf-8'))
