import pandas as pd
df = pd.read_excel("hanzicraft_dashboard_reordered.xlsx", nrows=0)
with open("cols.txt", "w", encoding="utf-8") as f:
    for c in df.columns:
        f.write(c + "\n")
