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

# --- 3. SESSION STATE (Mémoire) ---
if 'exo_index' not in st.session_state: st.session_state.exo_index = 0
if 'training_active' not in st.session_state: st.session_state.training_active = False
if 'last_announced' not in st.session_state: st.session_state.last_announced = ""
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'timer_running' not in st.session_state: st.session_state.timer_running = False
if 'timer_remaining' not in st.session_state: st.session_state.timer_remaining = 0
if 'history' not in st.session_state: st.session_state.history = [] # Pour les ✅
if 'poids_historique' not in st.session_state: st.session_state.poids_historique = 111.0

# --- 4. PROGRAMME ---
programme = [
    {"nom": "ÉCHAUFFEMENT : Mobilité", "type": "chrono", "valeur": 60, "consigne": "Rotation articulations."},
    {"nom": "ÉCHAUFFEMENT : 15 Squats à vide", "type": "reps", "valeur": 15, "consigne": "Réveil musculaire."},
    {"nom": "PAUSE : Transition", "type": "chrono", "valeur": 30, "consigne": "Prends tes poids (25kg et 10kg)."},
    {"nom": "SQUATS : Goblet Squat (25kg)", "type": "reps", "valeur": 12, "rpe": "7-8", "consigne": "Dos droit."},
    {"nom": "PAUSE : Récupération", "type": "chrono", "valeur": 60, "consigne": "Respire."},
    {"nom": "FENTES : Fentes avant (10kg)", "type": "reps", "valeur": 10, "rpe": "7-8", "consigne": "10 reps par jambe."},
    {"nom": "PAUSE : Récupération", "type": "chrono", "valeur": 60, "consigne": "Prépare le tapis."},
    {"nom": "GAINAGE : Planche", "type": "chrono", "valeur": 60, "rpe": "8", "consigne": "Abdos serrés."},
    {"nom": "PAUSE : Placement", "type": "chrono", "valeur": 15, "consigne": "Côté gauche."},
    {"nom": "GAINAGE : Latéral GAUCHE", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Hanche haute."},
    {"nom": "PAUSE : Placement", "type": "chrono", "valeur": 15, "consigne": "Côté droit."},
    {"nom": "GAINAGE : Latéral DROIT", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Dernier effort."},
    {"nom": "GRAND REPOS", "type": "chrono", "valeur": 120, "consigne": "Repos complet final."}
]

# --- 5. INTERFACE ---
tabs = st.tabs(["🚀 Séance", "🍎 Nutrition", "📉 Suivi Poids", "📅 Plan 12 Mois"])

# --- TAB 1 : LA SÉANCE ---
with tabs[0]:
    if st.session_state.training_active:
        c1, c2, c3 = st.columns(3)
        with c1: 
            if st.button("🔄 RESET"): st.session_state.exo_index = 0; st.session_state.timer_running = False; st.rerun()
        with c2:
            if st.button("⏭️ PASSER"): st.session_state.exo_index += 1; st.session_state.timer_running = False; st.rerun()
        with c3:
            if st.session_state.timer_running:
                if st.button("⏸️ PAUSE"): st.session_state.timer_running = False; st.rerun()

    if not st.session_state.training_active:
        st.header(f"Aujourd'hui : {datetime.now().strftime('%d/%m/%Y')}")
        if st.button("🏁 DÉMARRER LA SÉANCE"):
            st.session_state.training_active = True
            st.session_state.exo_index = 0
            st.session_state.start_time = time.time()
            st.rerun()
    else:
        index = st.session_state.exo_index
        if index < len(programme):
            exo = programme[index]
            st.subheader(f"📍 {exo['nom']}")
            
            if exo['type'] == "reps":
                st.title(f"🔢 {exo['valeur']} répétitions")
                if st.session_state.last_announced != exo['nom']:
                    coach_parle(f"{exo['nom']}. {exo['valeur']} répétitions."); st.session_state.last_announced = exo['nom']
                if st.button("✅ SÉRIE TERMINÉE"): st.session_state.exo_index += 1; st.rerun()

            elif exo['type'] == "chrono":
                if not st.session_state.timer_running and st.session_state.timer_remaining <= 0:
                    st.session_state.timer_remaining = exo['valeur']
                st.title(f"⏳ {st.session_state.timer_remaining} s")
                if st.session_state.last_announced != exo['nom']:
                    coach_parle(f"{exo['nom']} : {exo['valeur']} secondes."); st.session_state.last_announced = exo['nom']
                
                placeholder = st.empty()
                if not st.session_state.timer_running:
                    if st.button("▶️ LANCER"): st.session_state.timer_running = True; st.rerun()
                
                if st.session_state.timer_running:
                    while st.session_state.timer_remaining > 0 and st.session_state.timer_running:
                        st.session_state.timer_remaining -= 1
                        placeholder.title(f"⏳ {st.session_state.timer_remaining} s")
                        if st.session_state.timer_remaining == 3: coach_parle("3. 2. 1. Terminé.")
                        time.sleep(1)
                        if st.session_state.timer_remaining == 0:
                            st.session_state.timer_running = False; st.session_state.exo_index += 1; st.rerun()
        else:
            duree = int((time.time() - st.session_state.start_time) / 60)
            st.success(f"🏆 TERMINÉ EN {duree} MIN !")
            if st.button("💾 ENREGISTRER ET FINIR"):
                st.session_state.history.append(datetime.now().strftime("%Y-%m-%d"))
                st.session_state.training_active = False
                st.rerun()

# --- TAB 2 : NUTRITION ---
with tabs[1]:
    st.header("🍎 Nutrition & Protéines")
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.markdown("**Menu du jour :**\n- 12h: Poulet/Riz\n- 16h: Skyr/Whey\n- 19h: Poisson/Légumes")
    with col_n2:
        st.checkbox("✅ 220g Protéines")
        st.checkbox("✅ Fenêtre 16/8")

# --- TAB 3 : SUIVI POIDS ---
with tabs[2]:
    st.header("📉 Objectif 90 kg")
    poids = st.number_input("Poids actuel (kg)", 70.0, 150.0, st.session_state.poids_historique)
    if st.button("Enregistrer"):
        st.session_state.poids_historique = poids
        st.success("Poids mis à jour.")
    
    # Barre de progression
    progression = (111 - poids) / (111 - 90)
    st.write(f"Progression vers l'objectif : {min(100, int(progression*100))}%")
    st.progress(min(1.0, max(0.0, progression)))

# --- TAB 4 : PLAN 12 MOIS & VISUALISATION ---
with tabs[3]:
    st.header("📅 Calendrier de Transformation")
    
    # Affichage rapide de l'assiduité
    st.subheader("✅ Séances validées")
    cols = st.columns(7)
    jours_semaine = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    today = datetime.now()
    debut_semaine = today - timedelta(days=today.weekday())
    
    for i, jour in enumerate(jours_semaine):
        date_j = (debut_semaine + timedelta(days=i)).strftime("%Y-%m-%d")
        with cols[i]:
            st.write(jour)
            if date_j in st.session_state.history:
                st.title("✅")
            else:
                st.title("⚪")

    st.divider()
    # Recherche future
    dt_f = st.date_input("Vérifier le programme du :", datetime(2026, 11, 21))
    if dt_f.month >= 10:
        st.warning("🔥 PHASE FINALE : HIIT & SÈCHE. Tu es proche des 90kg !")
    else:
        st.info("💪 PHASE DE CONSTRUCTION : Focus charges et protéines.")
