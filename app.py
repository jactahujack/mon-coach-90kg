import streamlit as st
import time
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & STYLE CSS (POLICE PLUS PETITE) ---
st.set_page_config(page_title="COACH ELITE", layout="wide")

st.markdown("""
    <style>
    /* Réduction de la taille des titres pour éviter les coupures */
    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.4rem !important; }
    h3 { font-size: 1.1rem !important; }
    .stButton>button { font-size: 0.9rem !important; padding: 0.5rem; }
    /* Optimisation de l'affichage mobile */
    .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FONCTION VOCALE ---
def coach_parle(texte):
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{texte}");
            msg.lang = 'fr-FR';
            msg.rate = 0.95;
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 3. SESSION STATE (Mémoire robuste) ---
if 'poids_data' not in st.session_state:
    st.session_state.poids_data = pd.DataFrame({'Date': ['16/02'], 'Poids': [109.9]})
if 'exo_index' not in st.session_state: st.session_state.exo_index = 0
if 'serie_actuelle' not in st.session_state: st.session_state.serie_actuelle = 1
if 'nb_series_total' not in st.session_state: st.session_state.nb_series_total = 4
if 'training_active' not in st.session_state: st.session_state.training_active = False
if 'training_finished' not in st.session_state: st.session_state.training_finished = False
if 'timer_running' not in st.session_state: st.session_state.timer_running = False
if 'timer_remaining' not in st.session_state: st.session_state.timer_remaining = 0
if 'last_announced' not in st.session_state: st.session_state.last_announced = ""
if 'history' not in st.session_state: st.session_state.history = []

# --- 4. PROGRAMME ---
echauffement = [
    {"nom": "ÉCHAUFFEMENT : Mobilité", "type": "chrono", "valeur": 60, "consigne": "Rotation articulations."},
    {"nom": "ÉCHAUFFEMENT : 15 Squats à vide", "type": "reps", "valeur": 15, "consigne": "Réveil musculaire."},
    {"nom": "PAUSE : Transition", "type": "chrono", "valeur": 30, "consigne": "Prépare tes poids."}
]

circuit = [
    {"nom": "SQUATS : Goblet (25kg)", "type": "reps", "valeur": 12, "rpe": "7-8", "consigne": "Dos droit."},
    {"nom": "PAUSE : Récupération", "type": "chrono", "valeur": 60, "consigne": "Respire."},
    {"nom": "FENTES : Avant (10kg)", "type": "reps", "valeur": 10, "rpe": "7-8", "consigne": "10 reps/jambe."},
    {"nom": "PAUSE : Récupération", "type": "chrono", "valeur": 60, "consigne": "Tapis au sol."},
    {"nom": "GAINAGE : Planche", "type": "chrono", "valeur": 60, "rpe": "8", "consigne": "Abdos serrés."},
    {"nom": "PAUSE : Placement", "type": "chrono", "valeur": 15, "consigne": "Côté gauche."},
    {"nom": "GAINAGE : Latéral G", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Hanche haute."},
    {"nom": "PAUSE : Placement", "type": "chrono", "valeur": 15, "consigne": "Côté droit."},
    {"nom": "GAINAGE : Latéral D", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Dernier effort."},
    {"nom": "GRAND REPOS", "type": "chrono", "valeur": 120, "consigne": "Repos complet."}
]

# --- 5. INTERFACE ---
tabs = st.tabs(["🚀 Séance", "🍎 Nutrition", "📉 Poids", "📅 Plan"])

# --- ONGLET 1 : SÉANCE ---
with tabs[0]:
    if st.session_state.training_finished:
        st.success("🏆 SÉANCE VALIDÉE !")
        st.subheader("🌅 DEMAIN : MARDI 17 FÉVRIER")
        c1, c2 = st.columns(2)
        with c1: st.info("🧘 **REPOS ACTIF**\nMarche 20 min.")
        with c2: st.warning("🍎 **NUTRITION**\n220g Protéines.")
        if st.button("🔄 Accueil"): st.session_state.training_finished = False; st.rerun()

    elif not st.session_state.training_active:
        st.title("🏆 TRANSFORMATION ELITE 90")
        st.write(f"📅 **Aujourd'hui : {datetime.now().strftime('%d/%m/%Y')}**")
        st.session_state.nb_series_total = st.number_input("Nombre de séries :", 1, 10, 4)
        with st.expander("🔍 Détail du circuit"):
            for exo in circuit: st.write(f"• {exo['nom']}")
        if st.button("🏁 DÉMARRER", use_container_width=True):
            st.session_state.training_active = True; st.session_state.exo_index = 0
            st.session_state.serie_actuelle = 1; st.session_state.start_time = time.time(); st.rerun()
    else:
        if st.session_state.exo_index < len(echauffement):
            liste, phase = echauffement, "ÉCHAUFFEMENT"
            idx = st.session_state.exo_index
        else:
            liste, phase = circuit, f"SÉRIE {st.session_state.serie_actuelle}/{st.session_state.nb_series_total}"
            idx = st.session_state.exo_index - len(echauffement)

        col_a, col_b, col_c = st.columns(3)
        with col_a: 
            if st.button("🔄 RESET"): st.session_state.exo_index = 0; st.session_state.serie_actuelle = 1; st.rerun()
        with col_b:
            if st.button("⏭️ PASSER"): st.session_state.exo_index += 1; st.session_state.timer_running = False; st.rerun()
        with col_c:
            if st.session_state.timer_running and st.button("⏸️ PAUSE"): st.session_state.timer_running = False; st.rerun()

        if idx < len(liste):
            exo = liste[idx]
            st.write(f"**{phase}**")
            st.subheader(f"📍 {exo['nom']}")
            if exo['type'] == "reps":
                st.header(f"🔢 {exo['valeur']} RÉPS")
                if st.session_state.last_announced != f"{phase}_{exo['nom']}":
                    coach_parle(f"{exo['nom']}. {exo['valeur']} répétitions."); st.session_state.last_announced = f"{phase}_{exo['nom']}"
                if st.button("✅ VALIDER"): st.session_state.exo_index += 1; st.rerun()
            elif exo['type'] == "chrono":
                if not st.session_state.timer_running and st.session_state.timer_remaining <= 0: st.session_state.timer_remaining = exo['valeur']
                st.header(f"⏳ {st.session_state.timer_remaining} s")
                if st.session_state.last_announced != f"{phase}_{exo['nom']}":
                    coach_parle(f"{exo['nom']} : {exo['valeur']} secondes."); st.session_state.last_announced = f"{phase}_{exo['nom']}"
                placeholder = st.empty()
                if not st.session_state.timer_running and st.button("▶️ LANCER"): st.session_state.timer_running = True; st.rerun()
                if st.session_state.timer_running:
                    while st.session_state.timer_remaining > 0 and st.session_state.timer_running:
                        st.session_state.timer_remaining -= 1
                        placeholder.header(f"⏳ {st.session_state.timer_remaining} s")
                        if st.session_state.timer_remaining == 3: coach_parle("3. 2. 1.")
                        time.sleep(1)
                        if st.session_state.timer_remaining == 0: st.session_state.timer_running = False; st.session_state.exo_index += 1; st.rerun()
        else:
            if st.session_state.serie_actuelle < st.session_state.nb_series_total:
                st.session_state.serie_actuelle += 1; st.session_state.exo_index = len(echauffement); st.rerun()
            else:
                if st.button("💾 FINIR"):
                    st.session_state.history.append(datetime.now().strftime("%Y-%m-%d"))
                    st.session_state.training_active = False; st.session_state.training_finished = True; st.rerun()

# --- ONGLET 2 : NUTRITION ---
with tabs[1]:
    st.header("🍎 Nutrition 220g Protéines")
    st.write(f"Poids actuel : **{st.session_state.poids_data['Poids'].iloc[-1]} kg**")
    st.markdown("- **12h00 :** Poulet/Dinde + Riz + Courgettes\n- **16h30 :** Skyr (300g) + Whey\n- **19h30 :** Poisson blanc ou Omelette")
    st.checkbox("✅ Protéines")
    st.checkbox("✅ Eau (3.5L)")

# --- ONGLET 3 : POIDS ---
with tabs[2]:
    st.header("📉 Suivi de Poids")
    n_p = st.number_input("Poids (kg) :", 70.0, 150.0, float(st.session_state.poids_data['Poids'].iloc[-1]), step=0.1)
    if st.button("Enregistrer"):
        new_row = pd.DataFrame({'Date': [datetime.now().strftime("%d/%m")], 'Poids': [n_p]})
        st.session_state.poids_data = pd.concat([st.session_state.poids_data, new_row], ignore_index=True)
        st.rerun()
    st.line_chart(st.session_state.poids_data.set_index('Date'))

# --- ONGLET 4 : PLAN ---
with tabs[3]:
    st.header("📅 Assiduité")
    cols = st.columns(7); jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    start_week = datetime.now() - timedelta(days=datetime.now().weekday())
    for i, j in enumerate(jours):
        d_s = (start_week + timedelta(days=i)).strftime("%Y-%m-%d")
        with cols[i]: st.write(j); st.title("✅" if d_s in st.session_state.history else "⚪")
