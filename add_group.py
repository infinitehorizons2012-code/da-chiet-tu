import pandas as pd

file_reordered = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard_reordered.xlsx'
file_groups = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_groups.xlsx'

df_reordered = pd.read_excel(file_reordered)
df_groups = pd.read_excel(file_groups)

# Create a mapping from 'Chữ' to 'Group'
mapping_groups = dict(zip(df_groups['Chữ'], df_groups['Group']))

# Map to create column 'Group'
df_reordered['Group'] = df_reordered['Chữ Trung Quốc'].map(mapping_groups)

# Save the file
with pd.ExcelWriter(file_reordered, engine='openpyxl') as writer:
    df_reordered.to_excel(writer, index=False)
