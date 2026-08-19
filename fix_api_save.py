import re

with open("functions/api/save.js", "r", encoding="utf-8") as f:
    content = f.read()

old_srs = """    // Lu SRS vAo user_progress
    if (srs) {
       await db.prepare('INSERT INTO user_progress (username, char, srs_data, updated_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(username, char) DO UPDATE SET srs_data = excluded.srs_data, updated_at = CURRENT_TIMESTAMP').bind(username, char, JSON.stringify(srs)).run();
    }"""
# Note: since the file might have encoding issues when read normally, we'll replace via regex

srs_regex = re.compile(r"if\s*\(srs\)\s*\{\s*await db\.prepare\('INSERT INTO user_progress.*?\}\n", re.DOTALL)

new_srs = """    if (srs !== undefined) {
       if (srs === null) {
          await db.prepare('DELETE FROM user_progress WHERE username = ? AND char = ?').bind(username, char).run();
       } else {
          await db.prepare('INSERT INTO user_progress (username, char, srs_data, updated_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(username, char) DO UPDATE SET srs_data = excluded.srs_data, updated_at = CURRENT_TIMESTAMP').bind(username, char, JSON.stringify(srs)).run();
       }
    }\n"""

if srs_regex.search(content):
    content = srs_regex.sub(new_srs, content)
    with open("functions/api/save.js", "w", encoding="utf-8") as f:
        f.write(content)
    print("Modified functions/api/save.js!")
else:
    print("Failed to find srs block in save.js")
