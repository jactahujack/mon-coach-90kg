import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import time

st.set_page_config(page_title="Coach Élite - 90kg", layout="wide", initial_sidebar_state="expanded")

# --- BASE DE DONNÉES ---
DB_FILE = "suivi_sport.csv"
def charger_donnees():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Date", "Poids", "Notes"])

# --- STYLE ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE DES 12 MOIS ---
def obtenir_phase(d):
    # Liste des dates de début de chaque mois (tous les 16 du mois)
    dates_debut = [date(2026, 2, 16) + timedelta(days=30*i) for i in range(12)]
    
    if d < dates_debut[0]:
        return "Préparation", "Repos & Mobilité", "Équilibre", "Prêt pour le 16 février ?"
    
    # Détermination du mois actuel (1 à 12)
    m = 1
    for i, start_date in enumerate(dates_debut):
        if d >= start_date:
            m = i + 1
    
    # Définition des cycles
    if m <= 3:
        titre = f"🔥 PHASE 1 : FONDATIONS (Mois {m}/12)"
        exos = {
            "Monday": ["Renforcement A", "Goblet Squat 3x12, Fentes 3x8, Planche 60s", "220g Protéines"],
            "Wednesday": ["Renforcement B", "Pompes 4x8, Rowing 4x10, Gainage 45s", "220g Protéines"],
            "Friday": ["Cardio Base", "Marche active 40min ou 6x2' rapide", "180g Protéines"]
        }
    elif m <= 6:
        titre = f"⚡ PHASE 2 : PUISSANCE (Mois {m}/12)"
        exos = {
            "Monday": ["Force Bas", "Squat Lourd 4x8, Fentes Bulgares 3x10, Planche 90s", "230g Protéines"],
            "Wednesday": ["Force Haut", "Pompes Diamant 4x10, Rowing Lourd 4x8, Dips 3x12", "230g Protéines"],
            "Friday": ["HIIT", "8x1' sprint / 1' repos", "200g Protéines"]
        }
    elif m <= 9:
        titre = f"💪 PHASE 3 : HYPERTROPHIE (Mois {m}/12)"
        exos = {
            "Monday": ["Volume Bas", "Squat 4x12, Soulevé de terre partiel 4x10, Planche lestée", "240g Protéines"],
            "Wednesday": ["Volume Haut", "Pompes Large 4x15, Tractions 4xMAX, Dips 4x12", "240g Protéines"],
            "Friday": ["Endurance Dynamique", "Course 45min ou Corde à sauter", "210g Protéines"]
        }
    else:
        titre = f"⚔️ PHASE 4 : DÉFINITION FINALE (Mois {m}/12)"
        exos = {
            "Monday": ["Circuit Brûle-Gras", "Squat-Pompes-Burpees (4 tours)", "220g Protéines (Low Carb)"],
            "Wednesday": ["Densité Musculaire", "Séries combinées Haut/Bas, Gainage total", "220g Protéines (Low Carb)"],
            "Friday": ["Cardio HIIT Final", "10x30'' Sprint / 30'' Repos", "180g Protéines (Low Carb)"]
        }

    jour = d.strftime('%A')
    p_jour = exos.get(jour, ["Repos Récupération", "Marche 30min & Étirements", "Protéines stables"])
    return titre, p_jour[0], p_jour[1], p_jour[2]

# --- INTERFACE ---
with st.sidebar:
    st.header("📊 Suivi Quotidien")
    poids_saisi = st.number_input("Poids (kg)", 70.0, 150.0, 111.0)
    notes_saisies = st.text_area("Notes")
    if st.button("Valider la journée"):
        df = charger_donnees()
        nl = {"Date": str(date.today()), "Poids": poids_saisi, "Notes": notes_saisies}
        pd.concat([df, pd.DataFrame([nl])]).to_csv(DB_FILE, index=False)
        st.success("C'est noté !")
        st.balloons()

st.title("🛡️ Programme Élite : Objectif 90kg")

t1, t2, t3, t4 = st.tabs(["🏋️ Séance", "⏱️ Chrono", "🛒 Liste de Courses", "📈 Historique"])

with t1:
    d_view = st.date_input("Afficher le programme du :", date.today())
    phase_titre, s_nom, s_detail, s_nutri = obtenir_phase(d_view)
    st.subheader(phase_titre)
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**{s_nom}**\n\n{s_detail}")
    with col2:
        st.warning(f"**Nutrition**\n\n{s_nutri}")

with t2:
    st.subheader("⏱️ Minuteur Planche / Repos")
    sec = st.slider("Secondes", 30, 180, 60)
    if st.button("Lancer"):
        progress_bar = st.progress(0)
        for i in range(sec):
            time.sleep(1)
            progress_bar.progress((i + 1) / sec)
        st.success("Terminé !")

with t3:
    st.subheader("🛒 Indispensables")
    cols = st.columns(3)
    with cols[0]: st.write("**Protéines**\n- Poulet\n- Œufs\n- Poisson\n- Fromage Blanc")
    with cols[1]: st.write("**Glucides**\n- Riz\n- Quinoa\n- Flocons d'avoine\n- Patates douces")
    with cols[2]: st.write("**Autres**\n- Brocolis\n- Épinards\n- Avocat\n- Amandes")

with t4:
    st.subheader("📉 Ta progression")
    donnees = charger_donnees()
    if not donnees.empty:
        st.line_chart(donnees.set_index("Date")["Poids"])
        st.write(donnees.tail(5))