import requests, bs4, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://xiehanzi.com/han-tu/化/'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = bs4.BeautifulSoup(r.text, 'html.parser')

print("=== AUDIO LINKS / BUTTONS / MP3 ===")
for tag in soup.find_all(True):
    # Check attributes for mp3 or sound
    for attr, val in tag.attrs.items():
        val_str = str(val)
        if '.mp3' in val_str or 'audio' in val_str or 'sound' in val_str or 'play' in val_str:
            print(f"Tag <{tag.name}> attr {attr}={val_str}")

print("\n=== PINYIN & HAN VIET ===")
# Find pinyin / pronunciation block
h1_div = soup.find('h1')
if h1_div:
    print("H1 area:", h1_div.parent.get_text(separator=' | ', strip=True))

print("\n=== LOẠI TỪ & CÁCH DÙNG ===")
heading_lt = soup.find(lambda tag: tag.name in ['h2', 'h3'] and 'Loại từ' in tag.text)
if heading_lt:
    parent = heading_lt.parent
    if parent:
        print("Loại từ section:", parent.get_text(separator=' | ', strip=True)[:300])

print("\n=== NGHĨA & CÁCH DÙNG NHƯ MỘT TỪ ===")
heading_nghia = soup.find(lambda tag: tag.name in ['h2', 'h3'] and 'Nghĩa & cách dùng' in tag.text)
if heading_nghia:
    parent = heading_nghia.parent
    if parent:
        print("Nghĩa section:", parent.get_text(separator=' | ', strip=True)[:300])
