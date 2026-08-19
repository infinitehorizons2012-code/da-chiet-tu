import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_excel("hanzicraft_dashboard_reordered.xlsx")
print(df.columns.tolist())
