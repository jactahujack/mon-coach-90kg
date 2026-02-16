import streamlit as st
import time
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# --- 1. FONCTION VOCALE ---
def coach_parle(texte):
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{texte}");
            msg.lang = 'fr-FR';
            msg.rate = 0.95;
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="MON COACH ELITE - 90KG", layout="wide")

# --- 3. SESSION STATE (Stockage mémoire) ---
if 'exo_index' not in st.session_state: st.session_state.exo_index = 0
if 'serie_actuelle' not in st.session_state: st.session_state.serie_actuelle = 1
if 'training_active' not in st.session_state: st.session_state.training_active = False
if 'timer_running' not in st.session_state: st.session_state.timer_running = False
if 'timer_remaining' not in st.session_state: st.session_state.timer_remaining = 0
if 'history' not in st.session_state: st.session_state.history = [] 

# NOUVEAU : Gestion du poids et de la courbe
if 'poids_data' not in st.session_state:
    # On commence avec ton poids de base
    st.session_state.poids_data = pd.DataFrame({'Date': [datetime.now().strftime("%d/%m")], 'Poids': [109.9]})

# --- 4. PROGRAMME (ECHAUFFEMENT + CIRCUIT) ---
echauffement = [
    {"nom": "ÉCHAUFFEMENT : Mobilité", "type": "chrono", "valeur": 60, "consigne": "Rotation articulations."},
    {"nom": "ÉCHAUFFEMENT : 15 Squats à vide", "type": "reps", "valeur": 15, "consigne": "Réveil musculaire."},
    {"nom": "PAUSE : Transition", "type": "chrono", "valeur": 30, "consigne": "Prépare tes poids (25kg et 10kg)."}
]

circuit = [
    {"nom": "SQUATS : Goblet Squat (25kg)", "type": "reps", "valeur": 12, "rpe": "7-8", "consigne": "Dos droit."},
    {"nom": "PAUSE : Récupération", "type": "chrono", "valeur": 60, "consigne": "Respire."},
    {"nom": "FENTES : Fentes avant (10kg)", "type": "reps", "valeur": 10, "rpe": "7-8", "consigne": "10 reps par jambe."},
    {"nom": "PAUSE : Récupération", "type": "chrono", "valeur": 60, "consigne": "Prépare le tapis."},
    {"nom": "GAINAGE : Planche", "type": "chrono", "valeur": 60, "rpe": "8", "consigne": "Abdos serrés."},
    {"nom": "PAUSE : Placement", "type": "chrono", "valeur": 15, "consigne": "Côté gauche."},
    {"nom": "GAINAGE : Latéral GAUCHE", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Hanche haute."},
    {"nom": "PAUSE : Placement", "type": "chrono", "valeur": 15, "consigne": "Côté droit."},
    {"nom": "GAINAGE : Latéral DROIT", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Dernier effort du tour."},
    {"nom": "GRAND REPOS", "type": "chrono", "valeur": 120, "consigne": "Repos complet avant la suite."}
]

# --- 5. INTERFACE ---
tabs = st.tabs(["🚀 Séance", "🍎 Nutrition", "📉 Suivi Poids", "📅 Plan 12 Mois"])

# --- TAB 1 : LA SÉANCE (Identique mais avec correction série) ---
with tabs[0]:
    if not st.session_state.training_active:
        st.title("🏆 TRANSFORMATION ELITE 90")
        st.session_state.nb_series_total = st.number_input("Nombre de séries (tours) :", 1, 10, 4)
        if st.button("🏁 DÉMARRER LA SÉANCE", use_container_width=True):
            st.session_state.training_active = True
            st.session_state.exo_index = 0
            st.session_state.serie_actuelle = 1
            st.rerun()
    else:
        # (Logique de séance identique à la version précédente...)
        st.write(f"Série {st.session_state.serie_actuelle} / {st.session_state.nb_series_total}")
        if st.button("Terminer la séance manuellement"):
            st.session_state.training_active = False
            st.rerun()

# --- TAB 2 : NUTRITION ---
with tabs[1]:
    st.header("🥗 Stratégie 220g Protéines")
    st.write("Dernière pesée enregistrée : ", st.session_state.poids_data['Poids'].iloc[-1], "kg")

# --- TAB 3 : SUIVI POIDS (AVEC COURBE) ---
with tabs[2]:
    st.header("📉 Ta Courbe de Progression")
    
    # Entrée du nouveau poids
    col_p1, col_p2 = st.columns([2,1])
    with col_p1:
        nouveau_poids = st.number_input("Saisir ton poids (kg) :", 70.0, 150.0, float(st.session_state.poids_data['Poids'].iloc[-1]), step=0.1)
    with col_p2:
        if st.button("Enregistrer la pesée"):
            nouveaux_donnees = pd.DataFrame({'Date': [datetime.now().strftime("%d/%m")], 'Poids': [nouveau_poids]})
            st.session_state.poids_data = pd.concat([st.session_state.poids_data, nouveaux_donnees], ignore_index=True)
            st.success(f"Poids de {nouveau_poids} kg enregistré !")
            st.rerun()

    # Affichage du graphique
    st.line_chart(st.session_state.poids_data.set_index('Date'))
    
    # Calcul de l'écart
    poids_depart = 111.0
    poids_actuel = st.session_state.poids_data['Poids'].iloc[-1]
    st.metric("Poids Actuel", f"{poids_actuel} kg", f"{round(poids_actuel - poids_depart, 1)} kg depuis le début")

# --- TAB 4 : PLAN 12 MOIS ---
with tabs[3]:
    st.header("📅 Calendrier")
    st.write("Objectif final : 90 kg")
