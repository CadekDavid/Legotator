# Legotator: Multimodální AI Prediktor Ceny LEGO® Setů

**Autor:** David Čadek  
**Verze:** 1.0  
**Technologie:** `Python`, `TensorFlow/Keras`, `Scikit-learn`, `CustomTkinter`

## 1. O projektu
Legotator je pokročilý analytický nástroj využívající umělou inteligenci k odhadu férové tržní ceny LEGO setů. Na rozdíl od běžných modelů, které pracují pouze s textovými daty, využívá Legotator tzv. **multimodální neurónovou síť**.

Aplikace simuluje lidské rozhodování tím, že kombinuje dva různé vstupy:
* **Vizuální vjem:** Analýza fotografie setu (nebo jeho krabice) pomocí počítačového vidění.
* **Faktická data:** Zohlednění počtu dílků, počtu minifigurek a konkrétního tématu (např. Star Wars, Technic).

Výsledkem je robustní predikční model, který je odolnější vůči vizuálnímu šumu i datovým anomáliím.

## 2. Instalace a spuštění na jiném PC
Pro úspěšné spuštění aplikace na jiném zařízení postupujte podle následujících kroků:

### Prerekvizity
Je vyžadován nainstalovaný **Python 3.10+**. 
*(Z hlediska bezpečnosti a stability doporučujeme vytvořit virtuální prostředí `venv`, aby nedošlo ke konfliktům s jinými globálními knihovnami ve vašem systému.)*

### Klonování a příprava
1. Stáhněte/Klonujte repozitář z GitHubu.
2. Otevřete terminál ve složce projektu.
3. Nainstalujte potřebné knihovny (včetně TensorFlow, který zajišťuje běh AI):

```bash
pip install -r requirements.txt
```

### Spuštění aplikace

* **Přes terminál:** `python app.py`


> **Poznámka:** Při prvním spuštění může trvat několik sekund, než se do paměti načte neurónová síť (TensorFlow engine).

## 3. Sběr a příprava dat (Data Pipeline)
Data byla získána vlastními nástroji v rámci dvou fází:

### A. Scraping tabulkových dat
Pomocí knihovny **Playwright** byl vytvořen automatizovaný scraper, který prošel databázi Brickset a extrahoval klíčové parametry u více než 1 500 setů (ID setu, téma, rok vydání, počet dílků, počet figurek a oficiální cenu).

### B. Sběr obrazových dat
Následně byl vyvinut skript využívající knihovnu **Requests**, který na základě ID setů stáhl oficiální produktové fotografie. Pro trénink byly záměrně zvoleny čisté fotografie modelů na bílém pozadí. Tento proces (tzv. **Data Sanitization**) zajistil, že se AI naučila rozpoznávat tvary a složitost modelů bez rušivých vlivů (loga na krabicích, nápisy).

### C. Čištění a filtrace
Surová data byla očištěna od anomálií (sety s nulovou cenou, chybějící fotografie). Výsledný dataset obsahuje přes 800 vysoce kvalitních záznamů připravených pro hluboké učení.

## 4. Postup řešení a trénování
Vývoj probíhal v cloudovém prostředí Google Colab s využitím GPU akcelerace.

### Architektura modelu
Model se skládá ze dvou větví, které se v závěru spojují (**Fusion**):
* **Vizuální větev (CNN):** Využívá technologii *Transfer Learning* s modelem **MobileNetV2** od společnosti Google. Tento model je předtrénován na milionech obrázků a v Legotatoru slouží jako extraktor vizuálních příznaků.
* **Datová větev (Dense):** Plně propojená síť zpracovávající číselné parametry a kategorická data (témata převedená pomocí One-Hot Encoding).

### Parametry trénování
* **Normalizace:** Všechny číselné vstupy byly zmenšeny do rozsahu 0–1 pomocí `MinMaxScaler`.
* **Optimalizátor:** Adam (learning rate 0.01).
* **Ztrátová funkce:** MAE (Mean Absolute Error).

### Výsledek
Model byl trénován po dobu 30 epoch. Finální odchylka (Validation Loss) dosáhla hodnoty **$24.75**. Vzhledem k širokému cenovému rozpětí LEGO setů (od $10 do $800) jde o vysokou přesnost, která potvrzuje správnost zvolené multimodální cesty.

## 5. Klíčové části kódu
Projekt je rozdělen do modulů pro snadnou údržbu a bezpečnost. Je dbáno na prevenci běhových chyb:
* `cleaner.py`: Zajišťuje matematickou čistotu dat a ošetření chyb v CSV souborech.
* `image_downloader.py`: Robustní stahovač s ošetřením síťových timeoutů a výpadků spojení.
* `app.py`: Grafické rozhraní postavené na CustomTkinter. Obsahuje logiku pro předzpracování uživatelské fotografie v reálném čase předtím, než je bezpečně odeslána do modelu.
* `models/`: Složka obsahující "zmrazený" stav neurónové sítě (`.keras`) a konfigurační soubory pro transformaci dat (`.pkl`).

## 6. Finální výsledek a reálné využití
Legotator není jen akademický experiment, ale plnohodnotný nástroj pro praktické využití na sekundárním trhu s hračkami:
* **Určení ceny pro prodej:** Majitelé starších setů, kteří neznají aktuální tržní hodnotu, mohou jednoduše nahrát fotku svého setu a zadat základní údaje. AI jim okamžitě vypočítá férovou cenu, za kterou by se měl set nabízet na bazarech.
* **Investiční analýza:** Nástroj pomáhá identifikovat sety, které jsou aktuálně podhodnocené nebo nadhodnocené vzhledem ke své složitosti a tématu.
* **Zabezpečení proti lidským chybám:** Díky kombinaci vizuálu a dat aplikace eliminuje lidské omyly při manuálním dohledávání cen v rozsáhlých katalozích.

---
*Prohlášení: Tento projekt vznikl jako součást studia a slouží k demonstraci pokročilých technik strojového učení a datové analýzy v jazyce Python.*
