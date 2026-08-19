with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("React.useRef", "useRef")

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced React.useRef with useRef!")
