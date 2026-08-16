import sys, io, bs4
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

soup = bs4.BeautifulSoup(open(r'C:\Users\DT.HANG\Downloads\DA chiet tu\chu_nho_tong_hop.html', encoding='utf-8').read(), 'html.parser')
trs = soup.find_all('tr')

html_data = {}
for tr in trs[1:]:  # Skip header
    tds = [td.get_text(separator=" ", strip=True) for td in tr.find_all(['td', 'th'])]
    if len(tds) >= 8:
        stt = tds[0]
        char = tds[1]
        am_han_viet = tds[2]
        pinyin = tds[3]
        nghia = tds[4]
        phan_loai = tds[5]
        linh_kien = tds[6]
        giai_thich = tds[7]
        
        if char and char not in html_data:
            html_data[char] = {
                'stt': stt,
                'am_han_viet': am_han_viet,
                'pinyin': pinyin,
                'nghia': nghia,
                'linh_kien': linh_kien,
                'giai_thich': giai_thich
            }

print(f"Parsed {len(html_data)} characters from HTML file!")
print("Sample entry for 南:", html_data.get('南'))
print("Sample entry for 一:", html_data.get('一'))
