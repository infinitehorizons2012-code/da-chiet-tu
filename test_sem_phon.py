import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from hanzipy.decomposer import HanziDecomposer

decomposer = HanziDecomposer()
test_chars = ['提', '晴', '请', '情', '清', '想', '休', '明', '国']

for c in test_chars:
    info = decomposer.characters.get(c, {})
    comps = info.get('components', [])
    if len(comps) >= 2:
        c0, c1 = comps[0], comps[1]
        is_rad0 = decomposer.is_radical(c0)
        is_rad1 = decomposer.is_radical(c1)
        
        sem = c0 if is_rad0 else (c1 if is_rad1 else c0)
        phon = c1 if is_rad0 else (c0 if is_rad1 else c1)
        print(f"Chữ {c}: comps={comps} -> Hình phù (Ý)={sem}, Thanh phù (Âm)={phon}")
    else:
        print(f"Chữ {c}: comps={comps} (Đơn thể)")
