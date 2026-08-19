with open("src/TracNghiemTab.jsx", "rb") as f:
    content = f.read()

idx = content.find(b"Link ")
if idx != -1:
    print(content[idx:idx+40].hex())
