with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    for line in f:
        if "Link" in line and "Cloudinary" in line:
            print(repr(line.strip()))
