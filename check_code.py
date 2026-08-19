with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if "Link" in line or "playAudio" in line or "Audio" in line or "audio" in line:
            print(f"{i+1}: {line.strip()}")
