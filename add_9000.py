import pandas as pd

file_reordered = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard_reordered.xlsx'
file_9000 = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_9000.xlsx'

df_reordered = pd.read_excel(file_reordered)
df_9000 = pd.read_excel(file_9000)

# Create a mapping from Character to STT
# Assuming columns in df_9000 are 'STT', 'Chữ Hán', 'Link'
mapping_9000 = dict(zip(df_9000['Chữ Hán'], df_9000['STT']))

# Map to create column '9000'
df_reordered['9000'] = df_reordered['Chữ Trung Quốc'].map(mapping_9000)

# Save the file
with pd.ExcelWriter(file_reordered, engine='openpyxl') as writer:
    df_reordered.to_excel(writer, index=False)
