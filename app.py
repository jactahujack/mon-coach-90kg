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

# --- 3. SESSION STATE ---
if 'exo_index' not in st.session_state: st.session_state.exo_index = 0
if 'serie_actuelle' not in st.session_state: st.session_state.serie_actuelle = 1
if 'training_active' not in st.session_state: st.session_state.training_active = False
if 'training_finished' not in st.session_state: st.session_state.training_finished = False
if 'timer_running' not in st.session_state: st.session_state.timer_running = False
if 'timer_remaining' not in st.session_state: st.session_state.timer_remaining = 0
if 'history' not in st.session_state: st.session_state.history = [] 
if 'poids_data' not in st.session_state:
    st.session_state.poids_data = pd.DataFrame({'Date': [datetime.now().strftime("%d/%m")], 'Poids': [109.9]})

# --- 4. PROGRAMME ---
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

with tabs[0]:
    # --- CAS 1 : SÉANCE TERMINÉE (AFFICHER DEMAIN) ---
    if st.session_state.training_finished:
        st.balloons()
        st.success("🏆 SÉANCE VALIDÉE ! TU AS ASSURÉ.")
        
        st.divider()
        st.header("🌅 APERÇU DE TA JOURNÉE DE DEMAIN")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.subheader("📅 Mardi 17 Février")
            st.info("🧘 **Type : RÉCUPÉRATION ACTIVE**")
            st.write("""
            - **Activité :** 20 min de marche légère ou étirements.
            - **Focus :** Laisser les fibres musculaires se reconstruire.
            - **Sommeil :** Vise 8h pour maximiser la perte de gras.
            """)
        
        with col_d2:
            st.subheader("🍎 Nutrition Demain")
            st.write("""
            - **Jeûne :** Rupture à 12h00.
            - **Hydratation :** 3.5L d'eau (élimination des toxines).
            - **Protéines :** Garder le cap des 220g même sans muscu.
            """)
            
        if st.button("🔄 Revenir à l'accueil (Nouvelle séance)"):
            st.session_state.training_finished = False
            st.rerun()

    # --- CAS 2 : PAS DE SÉANCE EN COURS ---
    elif not st.session_state.training_active:
        st.title("🏆 TRANSFORMATION ELITE 90")
        st.header(f"📅 Séance du {datetime.now().strftime('%d/%m/%Y')}")
        st.session_state.nb_series_total = st.number_input("Nombre de séries :", 1, 10, 4)
        
        if st.button("🏁 DÉMARRER LA SÉANCE", use_container_width=True):
            st.session_state.training_active = True
            st.session_state.exo_index = 0
            st.session_state.serie_actuelle = 1
            st.session_state.start_time = time.time()
            st.rerun()

    # --- CAS 3 : SÉANCE EN COURS ---
    else:
        # (Logique de timer/reps identique à la version précédente)
        # [...] 
        # Une fois arrivé à la fin du circuit :
        if st.button("💾 ENREGISTRER ET FINIR"):
            st.session_state.history.append(datetime.now().strftime("%Y-%m-%d"))
            st.session_state.training_active = False
            st.session_state.training_finished = True # Active l'écran "Demain"
            st.rerun()

# (Les onglets Nutrition, Poids et Plan restent identiques)
