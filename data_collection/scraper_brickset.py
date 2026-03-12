import os
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

target_records = 2000
all_sets = []
# Procházíme nedávné roky
years = [2023, 2022, 2021, 2020, 2019] 

# Příprava složky a cesty pro soubor
os.makedirs("../data", exist_ok=True)
csv_path = "../data/brickset_playwright_data.csv"

print("🚀 Spouštím vylepšený Playwright s opraveným načítáním ID a témat...")

with sync_playwright() as p:
    # Otevře viditelný prohlížeč
    browser = p.chromium.launch(headless=False) 
    context = browser.new_context()
    page = context.new_page()

    for year in years:
        for page_num in range(1, 40):
            if len(all_sets) >= target_records:
                break
                
            url = f"https://brickset.com/sets/year-{year}/page-{page_num}"
            print(f"Načítám rok {year}, stránku {page_num}...")
            
            try:
                page.goto(url, timeout=60000)
                
                # 1. CHYTRÉ ČEKÁNÍ na obsah
                try:
                    page.wait_for_selector('article.set', timeout=10000)
                except Exception:
                    print(f"⚠️ Stránka je prázdná (Soft-ban nebo konec roku). Skáču na další rok.")
                    break 
                
                # 2. LIDSKÉ CHOVÁNÍ: Náhodná pauza
                time.sleep(random.uniform(2.0, 4.5)) 
                
                soup = BeautifulSoup(page.content(), 'html.parser')
                articles = soup.find_all('article', class_='set')

                # 3. EXTRAKCE DAT
                for article in articles:
                    if len(all_sets) >= target_records:
                        break
                        
                    name_tag = article.find('h1')
                    name = name_tag.text.strip() if name_tag else "Neznámý název"
                    
                    # --- OPRAVENÁ EXTRAKCE ID A TÉMATU ---
                    set_num = "Neznámé"
                    theme = "Neznámé"
                    
                    tags_div = article.find('div', class_='tags')
                    if tags_div:
                        tags = tags_div.find_all('a')
                        if len(tags) >= 2:
                            set_num = tags[0].text.strip() # První štítek je ID
                            theme = tags[1].text.strip()   # Druhý štítek je téma
                    
                    set_data = {
                        "set_num": set_num,
                        "theme": theme,
                        "name": name,
                        "year": year,
                        "pieces": None,
                        "minifigs": None,
                        "rrp_price": None,
                        "current_value": None
                    }
                    
                    dl = article.find('dl')
                    if dl:
                        for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
                            label = dt.text.strip().lower()
                            value = dd.text.strip()
                            if label == "pieces": set_data["pieces"] = value
                            elif label == "minifigs": set_data["minifigs"] = value
                            elif label == "rrp": set_data["rrp_price"] = value
                            elif label == "value new": set_data["current_value"] = value
                                
                    all_sets.append(set_data)
                    
                print(f"✅ Úspěch. Celkem už máme: {len(all_sets)} setů.")
                
                # 4. PRŮBĚŽNÉ UKLÁDÁNÍ
                pd.DataFrame(all_sets).to_csv(csv_path, index=False)
                
            except Exception as e:
                print(f"Kritická chyba sítě: {e}")
                break

        if len(all_sets) >= target_records:
            break

    browser.close()

print(f"\n🎉 HOTOVO! Staženo a uloženo {len(all_sets)} záznamů do {csv_path}")