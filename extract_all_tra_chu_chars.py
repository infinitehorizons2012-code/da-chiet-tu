import requests, bs4, sys, io, re, json, time
import concurrent.futures

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

base_url = 'https://xiehanzi.com'
print("Fetching main /tra-chu/ page...", flush=True)
r = requests.get(base_url + '/tra-chu/', headers={'User-Agent': 'Mozilla/5.0'})
soup = bs4.BeautifulSoup(r.text, 'html.parser')

sub_urls = set()
for a in soup.find_all('a'):
    href = a.get('href', '')
    if href.startswith('/tra-chu/') or href.startswith('/thu-vien-hsk/') or href.startswith('/thu-vien-new-hsk/'):
        sub_urls.add(base_url + href)

print(f"Found {len(sub_urls)} sub-pages under /tra-chu/...", flush=True)

all_chars = set()

def process_sub_page(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if res.status_code != 200:
            return []
        sp = bs4.BeautifulSoup(res.text, 'html.parser')
        
        found = []
        for a in sp.find_all('a'):
            href = a.get('href', '')
            if '/han-tu/' in href:
                # Extract the Chinese character from href or text
                # Format: /han-tu/chữ/ or /han-tu/name-%E5%8C%96/
                text = a.get_text(strip=True)
                c_matches = re.findall(r'[\u4e00-\u9fff]', text)
                for char in c_matches:
                    found.append(char)
        return found
    except Exception as e:
        return []

completed = 0
total_urls = len(sub_urls)

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(process_sub_page, url): url for url in sub_urls}
    for future in concurrent.futures.as_completed(futures):
        completed += 1
        items = future.result()
        for char in items:
            all_chars.add(char)
        if completed % 20 == 0 or completed == total_urls:
            print(f"Scanned {completed}/{total_urls} sub-pages | Found {len(all_chars)} unique characters so far...", flush=True)

print(f"TOTAL UNIQUE CHARACTERS FOUND ON /tra-chu/: {len(all_chars)}", flush=True)
