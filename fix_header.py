with open("src/App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("src/App.jsx", "w", encoding="utf-8") as f:
    for line in lines:
        if 'className="user-xp"' not in line and '{currentUser ||' not in line:
            f.write(line)
print("Deleted hardcoded XP and hang!")
