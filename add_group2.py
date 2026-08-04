import pandas as pd

file_reordered = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard_reordered.xlsx'
file_groups_v4 = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_groups_v4.xlsx'

df_reordered = pd.read_excel(file_reordered)
df_groups_v4 = pd.read_excel(file_groups_v4)

# mapping from 'Chữ' to 'Group'
mapping_groups_v4 = dict(zip(df_groups_v4['Chữ'], df_groups_v4['Group']))

# create column 'group2'
df_reordered['group2'] = df_reordered['Chữ Trung Quốc'].map(mapping_groups_v4)

# Save the file
with pd.ExcelWriter(file_reordered, engine='openpyxl') as writer:
    df_reordered.to_excel(writer, index=False)
