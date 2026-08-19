import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inject handleRemoveFromPractice
revert_regex = re.compile(r"const handleRevertToBatDau = async \(charObj\) => \{")
new_revert = """const handleRemoveFromPractice = async (charObj) => {
        if (!window.confirm(`Bạn có chắc muốn hủy chọn chữ "${charObj['Chữ Trung Quốc']}" (xóa khỏi danh sách Luyện tập)?`)) return;
        const originalSrs = charObj.srs;
        charObj.srs = null;
        setRenderTrigger(v => v + 1);
        await saveSrs(charObj, originalSrs, null);
      };

      const handleRevertToBatDau = async (charObj) => {"""

if revert_regex.search(content):
    content = revert_regex.sub(new_revert, content)
    print("Injected handleRemoveFromPractice")
else:
    print("Failed to find handleRevertToBatDau")

# 2. Inject the button
actions_regex = re.compile(r'\{SKILLS\.some\(skill => \[\'hat_mam\', \'cay\', \'hoa\'\]\.includes\(getSrsStatus\(item, skill\.id\)\)\) && \(\s*<button onClick=\{\(\) => handleRevertToSanSangThi\(item\)\}.*?</button>\s*\)\}', re.DOTALL)

new_actions = """{SKILLS.some(skill => ['hat_mam', 'cay', 'hoa'].includes(getSrsStatus(item, skill.id))) && (
                          <button onClick={() => handleRevertToSanSangThi(item)} style={{background: '#f59e0b', color: 'white', border: 'none', padding: '8px 12px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem', fontWeight: '500'}}>🔙 Sẵn sàng thi</button>
                        )}
                        {activeTab === 'bat_dau' && (
                          <button onClick={() => handleRemoveFromPractice(item)} style={{background: '#94a3b8', color: 'white', border: 'none', padding: '8px 12px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem', fontWeight: '500'}}>✖ Hủy chọn</button>
                        )}"""

if actions_regex.search(content):
    content = actions_regex.sub(new_actions, content)
    print("Injected Huy chon button")
else:
    print("Failed to find hat_mam button")

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

