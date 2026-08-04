import pandas as pd

file_reordered = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard_reordered.xlsx'
file_9000 = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_9000.xlsx'

df_reordered = pd.read_excel(file_reordered)
df_9000 = pd.read_excel(file_9000)

# Filter df_9000 for STT >= 3501
df_9000_filtered = df_9000[df_9000['STT'] >= 3501].copy()

# Prepare new rows dataframe
df_new_rows = pd.DataFrame()
df_new_rows['Chữ Trung Quốc'] = df_9000_filtered['Chữ Hán']
df_new_rows['Link'] = df_9000_filtered['Link']
df_new_rows['Số thứ tự'] = None  # Column 3 left empty for the new rows
df_new_rows['9000'] = df_9000_filtered['STT']

# Append to df_reordered
df_combined = pd.concat([df_reordered, df_new_rows], ignore_index=True)

# Drop duplicates based on 'Chữ Trung Quốc' to ensure we don't have overlapping characters (keep the original ones)
# We only do this to be safe in case there are duplicates between dashboard and >= 3501 in 9000.
df_combined = df_combined.drop_duplicates(subset=['Chữ Trung Quốc'], keep='first')

with pd.ExcelWriter(file_reordered, engine='openpyxl') as writer:
    df_combined.to_excel(writer, index=False)

print(f"Combined data has {len(df_combined)} rows. Appended {len(df_new_rows)} rows from 9000 (>=3501).")
