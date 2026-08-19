import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

filter_regex = re.compile(r"if \(activeTab\.startsWith\('Chữ Nho - Nhóm'\)\) \{.*?return true;", re.DOTALL)

new_filter = """if (activeTab.startsWith('Chữ Nho - Nhóm')) {
            const groupNum = parseInt(activeTab.replace('Chữ Nho - Nhóm ', ''));
            const stt = parseFloat(val);
            let min, max;
            
            if (groupNum === 1) { min = 1; max = 5; }
            else if (groupNum === 2) { min = 6; max = 11; }
            else if (groupNum === 3) { min = 12; max = 16; }
            else {
                // Nhóm 4 trở đi mặc định mỗi nhóm 5 chữ nối tiếp
                min = (groupNum - 4) * 5 + 17;
                max = min + 4;
            }

            if (stt < min || stt > max) return false;
        }
        return true;"""

if filter_regex.search(content):
    content = filter_regex.sub(new_filter, content)
    with open("src/App.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected custom group ranges!")
else:
    print("Failed to find filter block.")
