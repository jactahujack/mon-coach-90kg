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

# PROGRAMME COMPLET : ECHAUFFEMENT + SEANCE
programme = [
    {"nom": "ÉCHAUFFEMENT : Mobilité Articulaire", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Rotation chevilles, genoux et hanches doucement."},
    {"nom": "ÉCHAUFFEMENT : 15 Squats à vide", "type": "reps", "valeur": "15 répétitions", "rpe": "3", "consigne": "Chauffe tes muscles sans poids."},
    {"nom": "ÉCHAUFFEMENT : Cardio léger", "type": "chrono", "valeur": 45, "rpe": "4", "consigne": "Marche active sur place."},
    {"nom": "Repos de transition", "type": "chrono", "valeur": 30, "rpe": "-", "consigne": "Prends tes poids de 25kg et 10kg."},
    {"nom": "Goblet Squat (25kg)", "type": "reps", "valeur": "12 répétitions", "rpe": "7-8", "consigne": "Dos droit, descends bien bas."},
    {"nom": "Repos", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Respire, bois une petite gorgée."},
    {"nom": "Fentes avant (10kg)", "type": "reps", "valeur": "10 répétitions par jambe", "rpe": "7-8", "consigne": "Contrôle la descente, ne cogne pas le genou."},
    {"nom": "Repos", "type": "chrono", "valeur": 60, "rpe": "-", "consigne": "Prépare-toi pour la planche."},
    {"nom": "Planche (Gainage)", "type": "chrono", "valeur": 60, "rpe": "8", "consigne": "Aspire le nombril, serre les fessiers."},
    {"nom": "Repos", "type": "chrono", "valeur": 30, "rpe": "-", "consigne": "Dernier effort latéral."},
    {"nom": "Gainage latéral", "type": "chrono", "valeur": 45, "rpe": "8", "consigne": "Hanches bien hautes."}
]

# --- 4. INTERFACE À 4 ONGLETS ---
tabs = st.tabs(["🚀 Séance", "🍎 Nutrition", "📉 Suivi Poids", "📅 Plan 12 Mois"])

# --- TAB 1 : LA SÉANCE ---
with tabs[0]:
    if not st.session_state.training_active:
        st.header("Lundi 16 Février 2026")
        st.info("💡 Objectif RPE 7-8 : Garde 2 répétitions en réserve. Ne force pas trop au début.")
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
                    phrase_rpe = f"Intensité R.P.E {exo['rpe']}." if exo['rpe'] != "-" else ""
                    coach_parle(f"{exo['nom']}. {exo['valeur']}. {phrase_rpe} {exo['consigne']}")
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
                        if s == 10 and exo['nom'] != "Repos": coach_parle("Encore 10 secondes !")
                        if s == 3: coach_parle("3. 2. 1. Terminé.")
                        time.sleep(1)
                    st.session_state.exo_index += 1
                    st.rerun()
        else:
            st.success("🏆 Séance terminée ! Bravo Champion !")
            coach_parle("Séance terminée. Fier de toi. N'oublie pas tes 220 grammes de protéines.")
            if st.button("🔄 Recommencer pour une autre séance"):
                st.session_state.training_active = False
                st.rerun()

# --- TAB 2 : NUTRITION ---
with tabs[1]:
    st.header("🥗 Stratégie 220g Protéines & Jeûne")
    st.markdown("""
    * **Matin :** Jeûne (Eau, Café noir, Thé sans sucre)
    * **12h00 (Rupture) :** Gros repas (Poulet / Riz / Poivrons / Aubergines)
    * **16h00 (Post-Séance) :** Shaker Whey + 300g Skyr
    * **19h30 (Léger) :** Poisson blanc ou Omelette + Courgettes vapeur
    """)
    st.checkbox("✅ Fenêtre 16/8 respectée")
    st.checkbox("✅ 220g de Protéines atteints")
    st.checkbox("✅ 3L d'eau bus")

# --- TAB 3 : SUIVI POIDS ---
with tabs[2]:
    st.header("📉 Objectif Final : 90 kg")
    poids = st.number_input("Poids du jour (kg)", 70.0, 150.0, 111.0)
    if st.button("Enregistrer le poids"):
        st.success(f"Poids de {poids} kg enregistré pour le lundi 16 février.")

# --- TAB 4 : PLAN 12 MOIS ---
with tabs[3]:
    st.header("🗓️ Programmation sur l'année")
    df_plan = pd.DataFrame({
        "Mois": ["1-2", "3-5", "6-9", "10-12"],
        "Phase": ["Adaptation (RPE 7-8)", "Force (RPE 8-9)", "Volume (RPE 9)", "Finition (RPE 9-10)"],
        "Focus": ["Technique & Habitudes", "Charges lourdes", "Hypertrophie", "Sèche & Cardio"]
    })
    st.table(df_plan)
