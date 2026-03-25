import pandas as pd
import os


script_dir = os.path.dirname(os.path.abspath(__file__))


input_csv = os.path.join(script_dir, "../data/brickset_playwright_data.csv")
output_csv = os.path.join(script_dir, "../data/brickset_clean.csv")

print("🧹 Spouštím čištění datových záznamů...")

df = pd.read_csv(input_csv)
df_clean = df.copy()


df_clean['minifigs'] = df_clean['minifigs'].fillna('0')
df_clean['minifigs'] = df_clean['minifigs'].astype(str).str.extract(r'(\d+)')[0].astype(float)


df_clean['rrp_price'] = df_clean['rrp_price'].astype(str).str.extract(r'\$(\d+\.\d+)')[0].astype(float)
df_clean['current_value'] = df_clean['current_value'].astype(str).str.extract(r'\$(\d+\.\d+)')[0].astype(float)

df_clean['pieces'] = df_clean['pieces'].fillna(0).astype(float)

puvodni_pocet = len(df_clean)
df_clean = df_clean.dropna(subset=['rrp_price'])
df_clean = df_clean[df_clean['minifigs'] < 50]
novy_pocet = len(df_clean)


os.makedirs(os.path.dirname(output_csv), exist_ok=True)
df_clean.to_csv(output_csv, index=False)

print(f"✅ Čištění hotovo!")
print(f"📊 Z původních {puvodni_pocet} záznamů bylo vytvořeno {novy_pocet} vysoce kvalitních datových bodů.")
print(f"📁 Čistý soubor uložen jako: {os.path.abspath(output_csv)}")