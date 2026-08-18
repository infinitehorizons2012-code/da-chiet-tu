import requests, bs4, sys, io, re, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://xiehanzi.com/tra-chu/'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = bs4.BeautifulSoup(r.text, 'html.parser')

print("=== ALL LINKS ON /tra-chu/ ===")
links = soup.find_all('a')
print(f"Total links: {len(links)}")

categories = {}
for a in links:
    href = a.get('href', '')
    text = a.get_text(separator=' ', strip=True)
    if '/tra-chu/' in href or '/thu-vien-new-hsk/' in href or '/thu-vien-hsk/' in href:
        categories[href] = text

print(json.dumps(categories, ensure_ascii=False, indent=2))
