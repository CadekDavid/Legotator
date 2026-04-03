import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model


script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir, "models")

try:
    print("Načítám AI mozek a nástroje...")
    ai_model = load_model(os.path.join(models_dir, 'lego_multimodal.keras'))
    scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    tab_columns = joblib.load(os.path.join(models_dir, 'tab_columns.pkl'))
    print("✅ Všechny moduly úspěšně načteny!")
except Exception as e:
    print(f"❌ KRITICKÁ CHYBA: Nepodařilo se načíst modely. Zkontroluj složku 'models'. Detail: {e}")
    exit()

def load_image():
    """Bezpečné načtení obrázku od uživatele."""
    filepath = filedialog.askopenfilename(
        filetypes=[("Obrázky", "*.jpg *.jpeg *.png")]
    )
    if filepath:
        app.image_path = filepath
        img = Image.open(filepath)
        img.thumbnail((200, 200)) 
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        lbl_image_preview.configure(image=ctk_img, text="")
        lbl_result.configure(text="Obrázek načten. Zadej data a spusť AI.", text_color="white")

def predict_price():
    """Hlavní analytická funkce - propojení zraku a logiky."""
    try:
        if not getattr(app, "image_path", None):
            lbl_result.configure(text="⚠️ Chybí obrázek krabice!", text_color="orange")
            return
            
        pieces = float(entry_pieces.get())
        minifigs = float(entry_minifigs.get())
        theme = dropdown_theme.get()

        img = Image.open(app.image_path).convert('RGB')
        img_resized = img.resize((128, 128))
        img_array = np.array(img_resized).astype('float32') / 255.0
        img_input = np.expand_dims(img_array, axis=0)

        tab_data = pd.DataFrame(0.0, index=[0], columns=tab_columns)
        
        tab_data.at[0, 'pieces'] = pieces
        tab_data.at[0, 'minifigs'] = minifigs
        
        theme_col = f"theme_{theme}"
        if theme_col in tab_columns:
            tab_data.at[0, theme_col] = 1

        tab_data.iloc[:, :2] = scaler.transform(tab_data.iloc[:, :2])
        tab_input = tab_data.values.astype('float32')

        lbl_result.configure(text="Spojuji vizuální a datovou hemisféru...", text_color="white")
        app.update()
        
        prediction = ai_model.predict([img_input, tab_input])[0][0]
        
        lbl_result.configure(text=f"Férová AI cena: ${prediction:.2f}", text_color="#00FF00")

    except ValueError:
        lbl_result.configure(text="⚠️ Zadej platná čísla pro dílky a figurky!", text_color="red")
    except Exception as e:
        lbl_result.configure(text=f"❌ Nečekaná chyba: {e}", text_color="red")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("LEGO Advanced Predictor - Multimodální AI")
app.geometry("450x700")
app.image_path = None 

lbl_title = ctk.CTkLabel(app, text="Multimodální LEGO Skener", font=ctk.CTkFont(size=22, weight="bold"))
lbl_title.pack(pady=(20, 10))
frame_visual = ctk.CTkFrame(app)
frame_visual.pack(pady=10, padx=20, fill="x")

lbl_visual_title = ctk.CTkLabel(frame_visual, text="1. Vizuální vstup", font=ctk.CTkFont(weight="bold"))
lbl_visual_title.pack(pady=5)

btn_upload = ctk.CTkButton(frame_visual, text="Nahrát fotku krabice", command=load_image)
btn_upload.pack(pady=10)

lbl_image_preview = ctk.CTkLabel(frame_visual, text="Zatím nenahrána žádná fotka", width=200, height=200, fg_color="gray20")
lbl_image_preview.pack(pady=10)

frame_data = ctk.CTkFrame(app)
frame_data.pack(pady=10, padx=20, fill="x")

lbl_data_title = ctk.CTkLabel(frame_data, text="2. Datový vstup", font=ctk.CTkFont(weight="bold"))
lbl_data_title.pack(pady=5)

entry_pieces = ctk.CTkEntry(frame_data, placeholder_text="Počet dílků (např. 1500)")
entry_pieces.pack(pady=5)

entry_minifigs = ctk.CTkEntry(frame_data, placeholder_text="Počet figurek (např. 5)")
entry_minifigs.pack(pady=5)

themes = [col.replace('theme_', '') for col in tab_columns if col.startswith('theme_')]
dropdown_theme = ctk.CTkComboBox(frame_data, values=themes)
dropdown_theme.pack(pady=10)

btn_predict = ctk.CTkButton(app, text="⚡ Analyzovat a odhadnout cenu", height=40, font=ctk.CTkFont(weight="bold"), command=predict_price)
btn_predict.pack(pady=20)

lbl_result = ctk.CTkLabel(app, text="Čekám na vstupy...", font=ctk.CTkFont(size=18))
lbl_result.pack(pady=10)

app.mainloop()