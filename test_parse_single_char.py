import requests, bs4, sys, io, re, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_xiehanzi_full(char):
    url = f'https://xiehanzi.com/han-tu/{char}/'
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    if r.status_code != 200:
        return None
        
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    html_text = r.text
    
    # 1. Audio Link (mp3)
    audio_link = ""
    mp3_matches = re.findall(r'(https?://static\.xiehanzi\.com/[^\s"\'<>]+\.mp3)', html_text)
    if mp3_matches:
        # Prefer word_audios or female/male audio
        audio_link = mp3_matches[0]
        for m in mp3_matches:
            if 'female' in m or 'word_audios' in m or char in m:
                audio_link = m
                break
                
    # 2. Pinyin, Âm Hán Việt, Nghĩa Tiếng Việt, Loại từ
    pinyin = ""
    am_han_viet = ""
    nghia_tv = ""
    loai_tu = ""
    
    # Parse header blocks
    text_blocks = [tag.get_text(separator=' | ', strip=True) for tag in soup.find_all(['div', 'p', 'span', 'header'])]
    
    for block in text_blocks:
        if 'Nghĩa tiếng Việt' in block and not nghia_tv:
            # Extract Nghĩa tiếng Việt
            m = re.search(r'Nghĩa tiếng Việt\s*\|\s*([^\|]+)', block)
            if m:
                nghia_tv = m.group(1).strip()
        if 'Âm Hán Việt' in block and not am_han_viet:
            m = re.search(r'Âm Hán Việt\s*\|\s*([^\|]+)', block)
            if m:
                am_han_viet = m.group(1).strip()
        if ('Động từ' in block or 'Danh từ' in block or 'Tính từ' in block or 'Phó từ' in block or 'Loại từ' in block) and not loai_tu:
            m = re.search(r'(Động từ|Danh từ|Tính từ|Phó từ|Giới từ|Liên từ|Thán từ|Trợ từ|Lượng từ)(\s*\|\s*[\u4e00-\u9fff]+)?', block)
            if m:
                loai_tu = m.group(0).strip()
                
    # Parse Pinyin directly
    for tag in soup.find_all(['span', 'div', 'p']):
        t = tag.get_text(strip=True)
        # Check if t looks like pinyin with tone mark (e.g. huà, nāng, shì, nán)
        if re.match(r'^[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+\d*$', t, re.IGNORECASE) and len(t) <= 6:
            pinyin = t
            break

    # 3. Section: Nghĩa & cách dùng như một từ
    nghia_cach_dung_tu = ""
    h3_nghia = soup.find(lambda tag: tag.name in ['h2', 'h3'] and 'Nghĩa & cách dùng như một từ' in tag.text)
    if h3_nghia:
        header_div = h3_nghia.parent
        if header_div:
            content_div = header_div.find_next_sibling('div')
            if content_div:
                nghia_cach_dung_tu = content_div.get_text(separator=' | ', strip=True)
                
    return {
        'char': char,
        'audio': audio_link,
        'pinyin': pinyin,
        'am_han_viet': am_han_viet,
        'nghia_tv': nghia_tv,
        'loai_tu': loai_tu,
        'nghia_cach_dung_tu': nghia_cach_dung_tu
    }

res = parse_xiehanzi_full('化')
print(json.dumps(res, ensure_ascii=False, indent=2))
