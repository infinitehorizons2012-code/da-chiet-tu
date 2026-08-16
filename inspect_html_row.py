import sys, io, bs4
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

soup = bs4.BeautifulSoup(open(r'C:\Users\DT.HANG\Downloads\DA chiet tu\chu_nho_tong_hop.html', encoding='utf-8').read(), 'html.parser')
trs = soup.find_all('tr')

for i, tr in enumerate(trs):
    tds = [td.get_text(separator=" ", strip=True) for td in tr.find_all(['td', 'th'])]
    if len(tds) > 1 and '南' in tds[1]:
        print(f"Row {i}:")
        for col_idx, text in enumerate(tds):
            print(f"  Col {col_idx}: {text}")
