import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

st.set_page_config(page_title="Objectif 90kg", layout="wide")

# --- GESTION DE LA BASE DE DONNÉES (FICHIER EXCEL) ---
DB_FILE = "suivi_sport.csv"

def charger_donnees():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Poids", "Taille", "Notes", "Statut"])

def sauvegarder_donnee(poids, taille, notes):
    df = charger_donnees()
    nouvelle_ligne = {
        "Date": str(date.today()),
        "Poids": poids,
        "Taille": taille,
        "Notes": notes,
        "Statut": "Validé ✅"
    }
    df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# --- INTERFACE ---
st.title("🔥 Mon Coach Elite : Objectif 90kg")

with st.sidebar:
    st.header("⚖️ Ma Pesée")
    p_saisi = st.number_input("Poids actuel (kg)", 80.0, 150.0, 105.0, step=0.1)
    t_saisi = st.number_input("Tour de taille (cm)", 70, 130, 100)
    notes_jour = st.text_area("Notes (énergie, ressentis...)")
    
    if st.button("Enregistrer ma journée"):
        sauvegarder_donnee(p_saisi, t_saisi, notes_jour)
        st.success("Données enregistrées !")
        st.balloons()

# --- PROGRAMME DU JOUR ---
date_focus = st.date_input("Consulter le programme du :", date(2026, 2, 16))

# (Ici la logique du programme reste la même que précédemment...)
prog = {
    "Monday": ["Renforcement", "Goblet squat 3×12 (25kg), Fentes 3×8, Planche 60s", "220g Prot / 180g Féculents"],
    "Tuesday": ["Marche Fractionnée", "6×2′ rapide / 2′ lente - RPE 8", "180-200g Prot / 100-120g Féculents"],
    "Wednesday": ["Renforcement", "Pompes lestées 4×6, Rowing 4×6 (20kg)", "220g Prot / 180g Féculents"],
    "Thursday": ["Marche Modérée", "5 km - Rythme régulier", "180-200g Prot / 100-120g Féculents"],
    "Friday": ["Marche Fractionnée", "6×2′ rapide / 2′ lente", "180-200g Prot / 100-120g Féculents"],
    "Saturday": ["Core & Mobilité", "Planche 60s, Hollow hold 30s", "220g Prot / 180g Féculents"],
    "Sunday": ["Repos Actif", "Étirements + marche 3km", "180-200g Prot / 100-120g Féculents"]
}

jour_semaine = date_focus.strftime('%A')
if date(2026, 2, 16) <= date_focus <= date(2026, 3, 15):
    infos = prog.get(jour_semaine)
    col1, col2 = st.columns(2)
    with col1: st.info(f"🏋️ **{infos[0]}**\n\n{infos[1]}")
    with col2: st.warning(f"🍎 **Nutrition**\n\n{infos[2]}")

# --- HISTORIQUE ---
st.divider()
st.subheader("📈 Mon Historique")
donnees = charger_donnees()
if not donnees.empty:
    st.dataframe(donnees.tail(7)) # Affiche les 7 derniers jours
else:
    st.write("Aucune donnée enregistrée pour le moment.")