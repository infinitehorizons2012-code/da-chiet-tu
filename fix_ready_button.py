import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_actions = """                   <div className="tonghop-actions">
                      <button className="study-btn" onClick={() => handleStudy(item['Chữ Trung Quốc'])}>Học</button>
                      {activeTab === 'bat_dau' && (
                        <button className="ready-btn" onClick={() => handleMoveAllToReady(item)}>Sẵn sàng thi</button>
                      )}
                   </div>"""

new_actions = """                   <div className="tonghop-actions">
                      <button className="study-btn" onClick={() => handleStudy(item['Chữ Trung Quốc'])}>Học</button>
                      {SKILLS.some(skill => getSrsStatus(item, skill.id) === 'bat_dau') && (
                        <button className="ready-btn" onClick={() => handleMoveAllToReady(item)}>Sẵn sàng thi</button>
                      )}
                   </div>"""

content = content.replace(old_actions, new_actions)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated ready button condition")
