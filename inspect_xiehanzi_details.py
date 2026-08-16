import requests, bs4, sys, io, re, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://xiehanzi.com/han-tu/化/'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

print("=== ALL REGEX MP3 / AUDIO URLS IN RAW HTML ===")
matches = re.findall(r'https?://[^\s"\'<>]+\.mp3[^\s"\'<>]*', r.text)
print("Found mp3 URLs:", matches)

print("\n=== SEARCHING FOR AUDIO IN NEXT.JS OR SCRIPT DATA ===")
scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
for s in scripts:
    if 'mp3' in s or 'audio' in s or 'sound' in s or 'pinyin' in s:
        pyn_matches = re.findall(r'"(https?://[^"]+\.mp3)"', s)
        if pyn_matches:
            print("Found in script:", pyn_matches)

print("\n=== TOP HEADER AREA (Hán Việt, Pinyin, Meaning) ===")
soup = bs4.BeautifulSoup(r.text, 'html.parser')
main = soup.find('main') or soup.find('body')
if main:
    # Print first few divs
    for div in main.find_all('div', recursive=True)[:20]:
        text = div.get_text(separator=' | ', strip=True)
        if 'huà' in text or 'hóa' in text or 'Hua' in text or 'Huà' in text:
            print("Header block candidate:", text[:200])
            print("---")
