import bs4
import pandas as pd
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'
HTML_FILE = 'chu_nho_tong_hop.html'

print("Loading Excel dataset...")
df_excel = pd.read_excel(EXCEL_FILE)
excel_chars = set(df_excel['Chữ Trung Quốc'].dropna().astype(str).str.strip())
print(f"Excel has {len(excel_chars)} unique characters.")

print("Parsing chu_nho_tong_hop.html...")
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html_text = f.read()

soup = bs4.BeautifulSoup(html_text, 'html.parser')

# Inspect structure of chu_nho_tong_hop.html
# Usually entries are cards or table rows or div items
entries = []

# Let's find character cards / rows in HTML
cards = soup.find_all(class_=re.compile(r'card|item|char|row|box', re.I)) or soup.find_all(['tr', 'div'])

print(f"Found {len(cards)} elements to inspect in chu_nho_tong_hop.html.")

# Let's write a regex or tag extractor to find STT, Character, Radical, Mnemonics/Explanation from chu_nho_tong_hop.html
# Let's inspect raw text or structure first
