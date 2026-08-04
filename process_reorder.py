import pandas as pd

input_file = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard.xlsx'
output_file = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard_reordered.xlsx'

df = pd.read_excel(input_file)

# reorder and rename
df_new = pd.DataFrame()
df_new['Chữ Trung Quốc'] = df['Chữ Hán']
df_new['Link'] = df['Link']
df_new['Số thứ tự'] = df['STT']

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_new.to_excel(writer, index=False)

print(f"Successfully created {output_file} with columns {df_new.columns.tolist()}")
