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

# --- 3. GESTION DE LA SÉANCE ---
if 'exo_index' not in st.session_state:
    st.session_state.exo_index = 0
    st.session_state.training_active = False

programme = [
    {"nom": "Goblet Squat (25kg)", "type": "reps", "valeur": "12 répétitions", "rpe": "7-8", "consigne": "Dos droit, contrôle la descente."},
    {"nom": "Repos", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Respire bien."},
    {"nom": "Fentes avant (10kg)", "type": "reps", "valeur": "10 répétitions par jambe", "rpe": "7-8", "consigne": "Garde l'équilibre."},
    {"nom": "Repos", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Prépare-toi pour la planche."},
    {"nom": "Planche (Gainage)", "type": "chrono", "valeur": 60, "rpe": "8", "consigne": "Aspire le nombril."},
    {"nom": "Repos", "type": "chrono", "valeur": 30, "rpe": "-", "consigne": "Dernier effort."},
    {"nom": "Gainage latéral", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Hanches bien hautes."}
]

# --- 4. INTERFACE À 4 ONGLETS ---
tabs = st.tabs(["🚀 Séance", "🍎 Nutrition", "📉 Suivi Poids", "📅 Plan 12 Mois"])

# --- TAB 1 : LA SÉANCE ---
with tabs[0]:
    if not st.session_state.training_active:
        st.header("Lundi 16 Février")
        st.info("💡 Objectif RPE 7-8 : Garde 2 répétitions en réserve.")
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
                if 'last_announced' not in st.session_state or st.session_state.last_announced != exo['nom']:
                    coach_parle(f"{exo['nom']}. Fais {exo['valeur']}. Intensité R.P.E {exo['rpe']}.")
                    st.session_state.last_announced = exo['nom']
                if st.button("✅ Série terminée"):
                    st.session_state.exo_index += 1
                    st.rerun()

            elif exo['type'] == "chrono":
                st.header(f"⏳ {exo['valeur']} secondes")
                if 'last_announced' not in st.session_state or st.session_state.last_announced != exo['nom']:
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
            st.success("🏆 Bravo Champion !")
            coach_parle("Séance terminée. Fier de toi.")
            if st.button("🔄 Recommencer"):
                st.session_state.training_active = False
                st.rerun()

# --- TAB 2 : NUTRITION ---
with tabs[1]:
    st.header("🥗 Stratégie 220g Protéines")
    st.markdown("""
    * **12h00 :** Gros repas (Poulet / Riz / Légumes rôtis)
    * **16h00 :** Collation (Skyr + Whey)
    * **19h30 :** Repas LÉGER (Poisson ou Omelette + Courgettes)
    """)
    st.checkbox("✅ Fenêtre 16/8 respectée")
    st.checkbox("✅ 3L d'eau bus")

# --- TAB 3 : SUIVI POIDS ---
with tabs[2]:
    st.header("📉 Objectif 90 kg")
    poids = st.number_input("Poids du jour (kg)", 70.0, 150.0, 111.0)
    if st.button("Enregistrer"):
        st.success(f"Poids de {poids} kg enregistré pour le 16/02.")

# --- TAB 4 : PLAN 12 MOIS ---
with tabs[3]:
    st.header("🗓️ Programmation Annuelle")
    df_plan = pd.DataFrame({
        "Mois": ["1-2", "3-5", "6-9", "10-12"],
        "Phase": ["Adaptation", "Force", "Volume", "Finition"],
        "RPE Cible": ["7-8", "8-9", "9", "9-10"]
    })
    st.table(df_plan)
