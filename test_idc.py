import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from hanzipy.decomposer import HanziDecomposer

decomposer = HanziDecomposer()
test_chars = ['是', '提', '国', '问', '想', '休', '明', '森', '品', '回']
for c in test_chars:
    info = decomposer.characters.get(c, {})
    dtype = info.get('decomposition_type', '')
    comps = info.get('components', [])
    print(f"Chữ {c}: Mã IDC thô='{dtype}', Linh kiện={comps}")
