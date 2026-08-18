import pandas as pd
import sys
import io

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'

def run():
    print("=== 1. ĐỌC MASTER EXCEL (9.558 HÀNG) ===", flush=True)
    df = pd.read_excel(EXCEL_FILE)
    print(f"Tổng số cột trước khi xóa: {len(df.columns)}")

    cols_to_remove = ['Breakdown', 'Components_Hanzicraft', 'Appears_In']
    
    found_to_remove = [c for c in cols_to_remove if c in df.columns]
    print(f"Các cột sẽ bị xóa: {found_to_remove}")

    df.drop(columns=found_to_remove, inplace=True)
    print(f"Tổng số cột sau khi xóa: {len(df.columns)}")

    print("\n=== 2. LƯU CẬP NHẬT VÀO FILE EXCEL MASTER ===", flush=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    print("THÀNH CÔNG! Đã loại bỏ hoàn toàn các cột Q, R, S khỏi file Excel!", flush=True)

if __name__ == '__main__':
    run()
