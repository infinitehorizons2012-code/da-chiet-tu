import requests, bs4, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://xiehanzi.com/han-tu/化/'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = bs4.BeautifulSoup(r.text, 'html.parser')

print("=== ALL HEADINGS AND THEIR SIBLINGS ===")
for h in soup.find_all(['h2', 'h3']):
    heading_text = h.get_text(strip=True)
    if any(k in heading_text for k in ['Nghĩa', 'Loại từ', 'cách dùng']):
        print(f"Heading: <{h.name}> {heading_text}")
        parent = h.parent
        print("  Parent text:", parent.get_text(separator=' | ', strip=True)[:250])
        next_elem = parent.find_next_sibling()
        if next_elem:
            print("  Sibling text:", next_elem.get_text(separator=' | ', strip=True)[:250])
        print("-" * 50)
