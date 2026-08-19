import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Modify isFieldEditable
old_editable = "const isFieldEditable = (key) => key.startsWith('App_Comp_') || key === 'App_Mnemonic';"
new_editable = "const isFieldEditable = (key) => currentUser === 'admin' && (key.startsWith('App_Comp_') || key === 'App_Mnemonic');"

if old_editable in content:
    content = content.replace(old_editable, new_editable)
    with open("src/App.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Modified isFieldEditable to check for admin!")
else:
    print("Could not find isFieldEditable")
