import streamlit as st
import time
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. FONCTION VOCALE ---
def coach_parle(texte):
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{texte}");
            msg.lang = 'fr-FR';
            msg.rate = 0.9;
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="MON COACH ELITE - 90KG", layout="wide")

# --- 3. GESTION DE LA SÉANCE & RESET ---
if 'exo_index' not in st.session_state:
    st.session_state.exo_index = 0
if 'training_active' not in st.session_state:
    st.session_state.training_active = False
if 'last_announced' not in st.session_state:
    st.session_state.last_announced = ""

# PROGRAMME : ECHAUFFEMENT + SEANCE
programme = [
    {"nom": "ÉCHAUFFEMENT : Mobilité Articulaire", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Rotation chevilles, genoux et hanches."},
    {"nom": "ÉCHAUFFEMENT : 15 Squats à vide", "type": "reps", "valeur": "15 répétitions", "rpe": "3", "consigne": "Prépare tes articulations."},
    {"nom": "ÉCHAUFFEMENT : Cardio léger", "type": "chrono", "valeur": 45, "rpe": "4", "consigne": "Marche active sur place."},
    {"nom": "Repos de transition", "type": "chrono", "valeur": 30, "rpe": "-", "consigne": "Prends tes poids (25kg et 10kg)."},
    {"nom": "Goblet Squat (25kg)", "type": "reps", "valeur": "12 répétitions", "rpe": "7-8", "consigne": "Dos droit, descends bien bas."},
    {"nom": "Repos", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Respire bien."},
    {"nom": "Fentes avant (10kg)", "type": "reps", "valeur": "10 répétitions par jambe", "rpe": "7-8", "consigne": "Contrôle la descente."},
    {"nom": "Repos", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Prépare ton tapis."},
    {"nom": "Planche (Gainage)", "type": "chrono", "valeur": 60, "rpe": "8", "consigne": "Gainage total, serre les fessiers."},
    {"nom": "Repos", "type": "chrono", "valeur": 30, "rpe": "-", "consigne": "Dernier effort."},
    {"nom": "Gainage latéral", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Hanches bien hautes."}
]

# --- 4. INTERFACE ---
tabs = st.tabs(["🚀 Séance", "🍎 Nutrition", "📉 Suivi Poids", "📅 Plan 12 Mois"])

# --- TAB 1 : LA SÉANCE ---
with tabs[0]:
    # Bouton Reset toujours accessible si la séance est en cours
    if st.session_state.training_active:
        if st.button("🔄 REPRENDRE AU DÉBUT (RESET)"):
            st.session_state.exo_index = 0
            st.session_state.last_announced = ""
            st.rerun()

    if not st.session_state.training_active:
        st.header("Lundi 16 Février 2026")
        st.info("🎯 Objectif RPE 7-8 | 220g Protéines")
        if st.button("🏁 DÉMARRER LA SÉANCE"):
            st.session_state.training_active = True
            st.session_state.exo_index = 0
            st.rerun()
    else:
        index = st.session_state.exo_index
        if index < len(programme):
            exo = programme[index]
            col1, col2 = st.columns([3, 1])
            with col1: st.subheader(f"📍 {exo['nom']}")
            with col2: 
                if exo['rpe'] != "-": st.warning(f"🎯 RPE : {exo['rpe']}")
            
            st.write(f"👉 *{exo['consigne']}*")

            if exo['type'] == "reps":
                st.header(f"🔢 {exo['valeur']}")
                if st.session_state.last_announced != exo['nom']:
                    coach_parle(f"{exo['nom']}. {exo['valeur']}. R.P.E {exo['rpe']}.")
                    st.session_state.last_announced = exo['nom']
                if st.button("✅ Série terminée"):
                    st.session_state.exo_index += 1
                    st.rerun()

            elif exo['type'] == "chrono":
                st.header(f"⏳ {exo['valeur']} secondes")
                if st.session_state.last_announced != exo['nom']:
                    coach_parle(f"{exo['nom']} pendant {exo['valeur']} secondes.")
                    st.session_state.last_announced = exo['nom']
                ph = st.empty()
                if st.button("▶️ Lancer le chrono"):
                    for s in range(exo['valeur'], -1, -1):
                        ph.metric("Temps restant", f"{s}s")
                        if s == 3: coach_parle("3. 2. 1. Terminé.")
                        time.sleep(1)
                    st.session_state.exo_index += 1
                    st.rerun()
        else:
            st.success("🏆 Bravo ! Séance finie.")
            coach_parle("Séance terminée. Fier de toi champion.")
            if st.button("🔄 Nouvelle séance"):
                st.session_state.training_active = False
                st.rerun()

# --- TAB 2 : NUTRITION ---
with tabs[1]:
    st.header("🥗 Stratégie 220g Protéines")
    st.markdown("- 12h00 : Poulet/Riz\n- 16h30 : Collation Skyr/Whey\n- 19h30 : Poisson/Légumes")
    st.checkbox("✅ 220g de Protéines")
    st.checkbox("✅ 3L d'eau")

# --- TAB 3 : SUIVI POIDS ---
with tabs[2]:
    st.header("📉 Objectif 90 kg")
    st.number_input("Poids (kg)", 70.0, 150.0, 111.0)
    st.button("Enregistrer")

# --- TAB 4 : PLAN 12 MOIS ---
with tabs[3]:
    st.header("🗓️ Calendrier prévisionnel")
    dt = st.date_input("Voir le programme pour le :", datetime(2026, 11, 21))
    if dt.month >= 10:
        st.write("🔥 **Phase de Finition :** Circuit HIIT et Sèche finale.")
    else:
        st.write("💪 **Phase de Force :** Travail sur les charges.")
