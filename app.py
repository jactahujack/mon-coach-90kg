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
st.set_page_config(page_title="MON COACH ELITE", layout="wide")

# --- 3. PROGRAMME HYBRIDE AVEC RPE ---
if 'exo_index' not in st.session_state:
    st.session_state.exo_index = 0
    st.session_state.training_active = False

# RPE cible pour demain : 7-8 (Phase Adaptation)
programme = [
    {"nom": "Goblet Squat (25kg)", "type": "reps", "valeur": "12 répétitions", "rpe": "7-8", "consigne": "Dos droit, contrôle la descente."},
    {"nom": "Repos", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Respire, bois un peu d'eau."},
    {"nom": "Fentes avant (10kg)", "type": "reps", "valeur": "10 répétitions par jambe", "rpe": "7-8", "consigne": "Garde l'équilibre, ne touche pas le sol trop fort."},
    {"nom": "Repos", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Prépare-toi pour le gainage."},
    {"nom": "Planche (Gainage)", "type": "chrono", "valeur": 60, "rpe": "8", "consigne": "Aspire le nombril, fessiers serrés."},
    {"nom": "Repos", "type": "chrono", "valeur": 30, "rpe": "-", "consigne": "Dernier effort sur le côté."},
    {"nom": "Gainage latéral", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Hanches bien hautes."}
]

st.title("🏋️‍♂️ Coaching Intelligent & RPE")

tabs = st.tabs(["🚀 Séance", "🍎 Nutrition", "📉 Poids"])

with tabs[0]:
    if not st.session_state.training_active:
        st.info("💡 Rappel RPE 7-8 : Tu dois finir la série en sentant que tu pourrais encore en faire 2 ou 3.")
        if st.button("🏁 DÉMARRER LA SÉANCE"):
            st.session_state.training_active = True
            st.session_state.exo_index = 0
            st.rerun()
    else:
        index = st.session_state.exo_index
        if index < len(programme):
            exo = programme[index]
            
            # Affichage en-tête
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"📍 {exo['nom']}")
            with col2:
                if exo['rpe'] != "-":
                    st.warning(f"🎯 RPE : {exo['rpe']}")

            st.write(f"👉 *{exo['consigne']}*")

            # --- CAS 1 : RÉPÉTITIONS ---
            if exo['type'] == "reps":
                st.header(f"🔢 {exo['valeur']}")
                if 'last_announced' not in st.session_state or st.session_state.last_announced != exo['nom']:
                    # Le coach annonce l'exercice ET le RPE attendu
                    coach_parle(f"{exo['nom']}. Objectif {exo['valeur']}. Intensité R.P.E. {exo['rpe']}. {exo['consigne']}")
                    st.session_state.last_announced = exo['nom']
                
                if st.button("✅ Série terminée"):
                    st.session_state.exo_index += 1
                    st.rerun()

            # --- CAS 2 : CHRONO ---
            elif exo['type'] == "chrono":
                st.header(f"⏳ {exo['valeur']} secondes")
                if 'last_announced' not in st.session_state or st.session_state.last_announced != exo['nom']:
                    phrase_rpe = f"Intensité R.P.E. {exo['rpe']}" if exo['rpe'] != "-" else ""
                    coach_parle(f"{exo['nom']} pendant {exo['valeur']} secondes. {phrase_rpe}")
                    st.session_state.last_announced = exo['nom']

                ph = st.empty()
                if st.button("▶️ Lancer le chrono"):
                    for s in range(exo['valeur'], -1, -1):
                        ph.metric("Temps restant", f"{s}s")
                        if s == 10: coach_parle("Encore 10 secondes !")
                        if s == 3: coach_parle("3. 2. 1. Terminé.")
                        time.sleep(1)
                    st.session_state.exo_index += 1
                    st.rerun()
        else:
            st.success("🏆 Séance terminée ! Beau boulot.")
            coach_parle("Séance terminée. Bravo pour ton intensité. N'oublie pas de noter ton poids et tes protéines.")
            if st.button("🔄 Recommencer"):
                st.session_state.training_active = False
                st.rerun()

with tabs[1]:
    st.write("Objectif : 220g Protéines / Jeûne 16/8")
    st.write("Repas du soir : LÉGER (Poisson/Oeufs)")
