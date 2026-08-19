import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

research_def_regex = re.compile(r"function ResearchTab\(\{ globalLookupTerm, setGlobalLookupTerm \}\) \{")
new_research_def = "function ResearchTab({ globalLookupTerm, setGlobalLookupTerm, currentUser }) {"
content = research_def_regex.sub(new_research_def, content)

research_call_regex = re.compile(r"<ResearchTab globalLookupTerm=\{globalLookupTerm\} setGlobalLookupTerm=\{setGlobalLookupTerm\} />")
new_research_call = "<ResearchTab globalLookupTerm={globalLookupTerm} setGlobalLookupTerm={setGlobalLookupTerm} currentUser={currentUser} />"
content = research_call_regex.sub(new_research_call, content)

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected currentUser into ResearchTab!")
