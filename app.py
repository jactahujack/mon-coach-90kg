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
if 'training_active' not in st.session_state: st.session_state.training_active = False
if 'last_announced' not in st.session_state: st.session_state.last_announced = ""
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'timer_running' not in st.session_state: st.session_state.timer_running = False
if 'timer_remaining' not in st.session_state: st.session_state.timer_remaining = 0
if 'history' not in st.session_state: st.session_state.history = [] 
if 'poids_historique' not in st.session_state: st.session_state.poids_historique = 111.0

# --- 4. PROGRAMME ---
programme = [
    {"nom": "ÉCHAUFFEMENT : Mobilité", "type": "chrono", "valeur": 60, "consigne": "Rotation articulations."},
    {"nom": "ÉCHAUFFEMENT : 15 Squats à vide", "type": "reps", "valeur": 15, "consigne": "Réveil musculaire."},
    {"nom": "PAUSE : Transition", "type": "chrono", "valeur": 30, "consigne": "Prépare tes poids (25kg et 10kg)."},
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

# --- 5. INTERFACE À 4 ONGLETS ---
tabs = st.tabs(["🚀 Séance", "🍎 Nutrition", "📉 Suivi Poids", "📅 Plan 12 Mois"])

# --- TAB 1 : LA SÉANCE (ACCUEIL) ---
with tabs[0]:
    if not st.session_state.training_active:
        # --- TITRE DU PROGRAMME ANNUEL ---
        st.title("🏆 PROGRAMME ANNUEL : TRANSFORMATION ELITE 90")
        st.subheader("Phase actuelle : Adaptation & Technique (RPE 7-8)")
        
        st.divider()
        
        # --- DÉTAIL PROCHAINE SÉANCE ---
        st.header(f"📅 Séance du {datetime.now().strftime('%d/%m/%Y')}")
        
        with st.expander("🔍 Voir le détail des exercices de cette séance", expanded=True):
            for exo in programme:
                if "SQUATS" in exo['nom'] or "FENTES" in exo['nom'] or "GAINAGE" in exo['nom']:
                    type_val = f"{exo['valeur']} reps" if exo['type'] == 'reps' else f"{exo['valeur']} sec"
                    st.write(f"• **{exo['nom']}** : {type_val} (RPE: {exo.get('rpe', '-')})")
        
        st.info("💡 N'oublie pas ton échauffement et ton eau. Spotify prêt ?")
        
        if st.button("🏁 DÉMARRER LA SÉANCE MAINTENANT", use_container_width=True):
            st.session_state.training_active = True
            st.session_state.exo_index = 0
            st.session_state.start_time = time.time()
            st.rerun()

    else:
        # --- MODE ENTRAÎNEMENT ACTIF ---
        index = st.session_state.exo_index
        
        # Boutons de contrôle
        c1, c2, c3 = st.columns(3)
        with c1: 
            if st.button("🔄 RESET"): st.session_state.exo_index = 0; st.session_state.timer_running = False; st.rerun()
        with c2:
            if st.button("⏭️ PASSER"): st.session_state.exo_index += 1; st.session_state.timer_running = False; st.rerun()
        with c3:
            if st.session_state.timer_running:
                if st.button("⏸️ PAUSE"): st.session_state.timer_running = False; st.rerun()

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

# --- LES AUTRES ONGLETS (RESTENT IDENTIQUES) ---
with tabs[1]:
    st.header("🍎 Nutrition & Protéines")
    st.markdown("- 12h: Poulet/Riz | - 16h: Skyr/Whey | - 19h: Poisson/Légumes")
    st.checkbox("✅ 220g Protéines")

with tabs[2]:
    st.header("📉 Objectif 90 kg")
    poids = st.number_input("Poids actuel (kg)", 70.0, 150.0, st.session_state.poids_historique)
    st.progress((111 - poids) / (111 - 90))

with tabs[3]:
    st.header("📅 Calendrier de Transformation")
    st.subheader("Suivi de la semaine")
    st.write(st.session_state.history) # Affiche les dates validées
