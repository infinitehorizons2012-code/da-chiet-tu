import pandas as pd

file_reordered = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard_reordered.xlsx'
file_words = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_words.xlsx'

df_reordered = pd.read_excel(file_reordered)
df_words = pd.read_excel(file_words)

# mapping from 'Từ Trung Quốc' to 'Số thứ tự'
mapping_words = dict(zip(df_words['Từ Trung Quốc'], df_words['Số thứ tự']))

# create column 7 'Số thứ tự words'
df_reordered['Số thứ tự words'] = df_reordered['Chữ Trung Quốc'].map(mapping_words)

# Save the file
with pd.ExcelWriter(file_reordered, engine='openpyxl') as writer:
    df_reordered.to_excel(writer, index=False)
