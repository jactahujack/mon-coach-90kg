import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import time

st.set_page_config(page_title="Coach Élite 90kg - Discipline", layout="wide")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .motivation-text {
        font-size: 24px !important;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        padding: 10px;
        border: 2px solid #FF4B4B;
        border-radius: 10px;
        background-color: #FFF5F5;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
DB_DAILY = "suivi_quotidien.csv"
def charger_donnees():
    if os.path.exists(DB_DAILY): return pd.read_csv(DB_DAILY)
    return pd.DataFrame(columns=["Date", "Poids", "Notes"])

# --- LOGIQUE DE DATE ET MOTIVATION ---
d_view = st.date_input("Date de consultation :", date.today())
jour_nom = d_view.strftime('%A')

citations = {
    "Monday": "🚀 LUNDI : Nouvelle semaine, nouvelle opportunité de devenir l'homme que tu veux être. Ne lâche rien !",
    "Tuesday": "🔥 MARDI : La discipline, c'est choisir entre ce que tu veux maintenant et ce que tu veux le plus.",
    "Wednesday": "💪 MERCREDI : Mi-chemin ! La fatigue est temporaire, la fierté est éternelle.",
    "Thursday": "⚔️ JEUDI : C'est quand c'est dur que tu gagnes tes galons. Continue de pousser !",
    "Friday": "⚡ VENDREDI : Finis fort ! Ne laisse pas le week-end gâcher tes efforts de la semaine.",
    "Saturday": "🏆 SAMEDI : Les champions s'entraînent quand les autres dorment. Ta régularité fera la différence.",
    "Sunday": "🧘 DIMANCHE : Repose le corps, recharge l'esprit, mais garde l'objectif en vue. Prêt pour demain !"
}

# --- AFFICHAGE DE LA MOTIVATION ---
st.markdown(f'<div class="motivation-text">{citations.get(jour_nom)}</div>', unsafe_allow_html=True)

# --- NAVIGATION ---
tabs = st.tabs(["🏋️ Séance & Nutrition", "✅ Check-list Nutrition", "📊 Bilans Mensuels", "📈 Evolution"])

with tabs[0]:
    # Programme simplifié basé sur tes données
    prog = {
        "Monday": ["Renforcement Bas", "Goblet squat 3x12, Fentes 3x8, Planche 60s", "220g Prot / 180g Féc"],
        "Wednesday": ["Renforcement Haut", "Pompes lestées 4x6, Rowing 4x6", "220g Prot / 180g Féc"],
        "Friday": ["Marche Fractionnée", "6x2' rapide / 2' lente", "180-200g Prot / 100g Féc"]
    }
    current = prog.get(jour_nom, ["Repos Actif", "Marche modérée ou Étirements", "Protéines stables"])
    
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**SÉANCE : {current[0]}**\n\n{current[1]}")
    with c2:
        st.warning(f"**NUTRITION**\n\n{current[2]}")

with tabs[1]:
    st.subheader("✅ Check-list Nutritionnelle")
    col_a, col_b = st.columns(2)
    with col_a:
        st.checkbox("Protéines à chaque repas (4x)")
        st.checkbox("Légumes à chaque repas principal")
        st.checkbox("Fruit quotidien")
    with col_b:
        st.checkbox("Hydratation minimale (2L+)")
        st.checkbox("Pas d'écarts > 2/semaine")
        st.checkbox("Féculents adaptés à l'effort")

with tabs[2]:
    st.header("📊 Bilan Mensuel")
    with st.form("bilan_mensuel"):
        st.write("**Mesures & Énergie**")
        c_b1, c_b2 = st.columns(2)
        p_fin = c_b1.number_input("Poids de fin de mois (kg)", 70.0, 150.0)
        t_taille = c_b2.number_input("Tour de taille fin (cm)", 50, 150)
        
        st.divider()
        st.write("**Analyse Qualitative**")
        pos = st.text_area("✨ Points positifs (réussites)")
        neg = st.text_area("⚠️ Points à améliorer")
        obj_next = st.text_area("🎯 Objectifs pour le mois suivant")
        
        if st.form_submit_button("Valider le Bilan du Mois"):
            st.success("Bilan enregistré ! Bravo pour tes efforts.")

with tabs[3]:
    st.subheader("📈 Historique")
    poids_input = st.number_input("Enregistrer poids aujourd'hui (kg)", 70.0, 150.0, 111.0)
    if st.button("Enregistrer"):
        # Logique de sauvegarde
        st.balloons()