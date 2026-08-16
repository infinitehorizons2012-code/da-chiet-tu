import requests, bs4, sys, io, re, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_xiehanzi_complete(char):
    url = f'https://xiehanzi.com/han-tu/{char}/'
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    if r.status_code != 200:
        return None
        
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    html_text = r.text
    
    # 1. Link âm thanh (Audio MP3)
    audio_link = ""
    mp3_matches = re.findall(r'(https?://static\.xiehanzi\.com/[^\s"\'<>]+\.mp3)', html_text)
    if mp3_matches:
        audio_link = mp3_matches[0]
        for m in mp3_matches:
            if 'word_audios' in m or 'female' in m or char in m:
                audio_link = m
                break
                
    # 2. Pinyin, Âm Hán Việt, Nghĩa tiếng Việt
    pinyin = ""
    am_han_viet = ""
    nghia_tv = ""
    
    text_blocks = [tag.get_text(separator=' | ', strip=True) for tag in soup.find_all(['div', 'p', 'span', 'header'])]
    for block in text_blocks:
        if 'Nghĩa tiếng Việt' in block and not nghia_tv:
            m = re.search(r'Nghĩa tiếng Việt\s*\|\s*([^\|]+)', block)
            if m:
                nghia_tv = m.group(1).strip()
        if 'Âm Hán Việt' in block and not am_han_viet:
            m = re.search(r'Âm Hán Việt\s*\|\s*([^\|]+)', block)
            if m:
                am_han_viet = m.group(1).strip()

    # Find pinyin near character
    for tag in soup.find_all(['span', 'div', 'p']):
        t = tag.get_text(strip=True)
        if re.match(r'^[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+\d*$', t, re.IGNORECASE) and len(t) <= 6:
            pinyin = t
            break

    # 3. Loại từ & cách dùng
    loai_tu_cach_dung = ""
    h3_loaitu = soup.find(lambda t: t.name in ['h2', 'h3'] and 'Loại từ' in t.text)
    if h3_loaitu:
        card = h3_loaitu.find_parent('div', class_=re.compile(r'card|rounded')) or h3_loaitu.parent
        if card:
            loai_tu_cach_dung = card.get_text(separator=' | ', strip=True)

    # 4. Nghĩa & cách dùng như một từ
    nghia_cach_dung_tu = ""
    h3_nghia = soup.find(lambda t: t.name in ['h2', 'h3'] and 'Nghĩa & cách dùng như một từ' in t.text)
    if h3_nghia:
        card = h3_nghia.find_parent('div', class_=re.compile(r'card|rounded')) or h3_nghia.parent
        if card:
            nghia_cach_dung_tu = card.get_text(separator=' | ', strip=True)

    return {
        'Chữ': char,
        'Pinyin_Xie': pinyin,
        'Âm_Hán_Việt_Xie': am_han_viet,
        'Nghĩa_Tiếng_Việt_Xie': nghia_tv,
        'Link_Âm_Thanh_Xie': audio_link,
        'Loại_từ_và_cách_dùng_Xie': loai_tu_cach_dung,
        'Nghĩa_và_cách_dùng_như_một_từ_Xie': nghia_cach_dung_tu
    }

for test_c in ['化', '是', '南']:
    res = parse_xiehanzi_complete(test_c)
    print(f"=== KẾT QUẢ CHO CHỮ [{test_c}] ===")
    print(json.dumps(res, ensure_ascii=False, indent=2))
