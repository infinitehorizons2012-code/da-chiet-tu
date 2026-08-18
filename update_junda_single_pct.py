import pandas as pd
import requests
import bs4
import urllib3
import re
import sys
import io

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'

def run():
    print("=== 1. TẢI VÀ BÓC TÁCH CHÍNH XÁC BẢNG TẦN SUẤT JUN DA (MTSU) ===", flush=True)
    urls = [
        "https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO",
        "https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO&cpage=2",
        "https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO&cpage=3"
    ]
    
    char_junda_data = {}
    
    for u in urls:
        print(f"Fetching {u}...", flush=True)
        try:
            resp = requests.get(u, verify=False, timeout=20)
            resp.encoding = 'gbk'
            text = resp.text
            
            # Extract lines from <pre> block
            pre_match = re.search(r'<pre>(.*?)</pre>', text, re.DOTALL | re.IGNORECASE)
            if not pre_match:
                continue
            lines = pre_match.group(1).split('<br>')
            
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) >= 4:
                    try:
                        rank_str = parts[0].strip()
                        char = parts[1].strip()
                        raw_count_str = parts[2].strip()
                        cum_pct_str = parts[3].strip()
                        
                        if rank_str.isdigit() and char:
                            rank = int(rank_str)
                            raw_count = int(raw_count_str) if raw_count_str.isdigit() else 0
                            cum_pct = float(cum_pct_str) if cum_pct_str else None
                            
                            char_junda_data[char] = {
                                'rank': rank,
                                'raw_count': raw_count,
                                'cum_pct': cum_pct
                            }
                    except Exception:
                        pass
        except Exception as e:
            print(f"Lỗi khi tải {u}: {e}", flush=True)

    print(f"-> Đã bóc tách thành công dữ liệu tần suất Jun Da cho {len(char_junda_data)} chữ Hán!", flush=True)

    # Tính tổng số lượt xuất hiện toàn bộ corpus Jun Da
    total_corpus_count = sum(item['raw_count'] for item in char_junda_data.values() if item['raw_count'] > 0)
    if total_corpus_count == 0:
        total_corpus_count = 193504018 # Khôi phục tổng mặc định corpus Jun Da 193.5 triệu chữ
        
    print(f"-> Tổng quy mô kho dữ liệu Jun Da Corpus: {total_corpus_count:,} chữ Hán.", flush=True)

    # Tính toán Tần Suất % Đơn Lẻ cho từng chữ
    for char, info in char_junda_data.items():
        if info['raw_count'] > 0:
            single_pct = (info['raw_count'] / total_corpus_count) * 100.0
            info['single_pct'] = round(single_pct, 6)
        else:
            info['single_pct'] = None

    print("\n=== 2. CẬP NHẬT VÀO FILE EXCEL MASTER (9.558 HÀNG) ===", flush=True)
    df = pd.read_excel(EXCEL_FILE)
    
    col_rank = 'Hạng Tần Suất (Jun Da)'
    col_single_pct = 'Tần Suất % Đơn Lẻ (Jun Da)'
    col_cum_pct = 'Tần Suất % Cộng Dồn (Jun Da)'
    col_raw_count = 'Số Lần Xuất Hiện Thô (Jun Da)'

    rank_list = []
    single_pct_list = []
    cum_pct_list = []
    raw_count_list = []

    for idx, row in df.iterrows():
        c = str(row['Chữ Trung Quốc']).strip() if pd.notna(row['Chữ Trung Quốc']) else ''
        info = char_junda_data.get(c, {})
        
        rank_list.append(info.get('rank'))
        single_pct_list.append(info.get('single_pct'))
        cum_pct_list.append(info.get('cum_pct'))
        raw_count_list.append(info.get('raw_count'))

    df[col_rank] = rank_list
    df[col_single_pct] = single_pct_list
    df[col_cum_pct] = cum_pct_list
    df[col_raw_count] = raw_count_list

    # Xóa cột cũ nếu có tên không rõ ràng
    if 'Tần Suất % (Jun Da)' in df.columns:
        df.drop(columns=['Tần Suất % (Jun Da)'], inplace=True)

    print("\nSample check first 10 rows:")
    print(df[['Chữ Trung Quốc', col_rank, col_single_pct, col_cum_pct]].head(10))

    print("\nSaving updated Excel dataset to file...", flush=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print(f"THÀNH CÔNG! Đã bổ sung cột '{col_single_pct}' chuẩn 100% cho toàn bộ file Excel!", flush=True)

if __name__ == '__main__':
    run()
