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

# --- 2. CONFIGURATION & STYLE ---
st.set_page_config(page_title="MON COACH ELITE - 90KG", layout="wide")
st.markdown("""
    <style>
    .motivation-box {
        font-size: 20px; font-weight: bold; color: #FFFFFF;
        text-align: center; padding: 15px; border-radius: 10px;
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIQUE DATE & MOTIVATION ---
d_view = st.date_input("📅 Date de l'entraînement :", datetime.now())
st.markdown('<div class="motivation-box">Lâche rien ! Objectif 90kg. La discipline bat la motivation.</div>', unsafe_allow_html=True)

# --- 4. PROGRAMME DES 12 MOIS ---
# On définit ici tes exercices du lundi 16 février
exos_lundi = [
    {"nom": "Goblet Squat (25kg)", "duree": 45, "rpe": "7", "consigne": "Dos droit, descends bien bas."},
    {"nom": "Repos", "duree": 60, "rpe": "-", "consigne": "Respire, bois une gorgée d'eau."},
    {"nom": "Fentes avant (10kg)", "duree": 40, "rpe": "7-8", "consigne": "Contrôle la descente."},
    {"nom": "Repos", "duree": 60, "rpe": "-", "consigne": "Prépare-toi pour la planche."},
    {"nom": "Planche (Gainage)", "duree": 60, "rpe": "8", "consigne": "Aspire le nombril."},
    {"nom": "Repos", "duree": 30, "rpe": "-", "consigne": "Dernier effort latéral."},
    {"nom": "Gainage latéral", "duree": 45, "rpe": "8", "consigne": "Hanches bien hautes."}
]

tabs = st.tabs(["🏋️ Séance du Jour", "🍎 Nutrition & Jeûne", "📊 Suivi Poids", "📅 Plan 12 Mois"])

# --- TAB 1 : LE COACH VOCAL ---
with tabs[0]:
    st.header("🏁 Ton Coaching Vocal")
    if st.button("▶️ DÉMARRER LA SÉANCE"):
        coach_parle("C'est parti Champion ! On vise les 90 kilos. Premier exercice : Goblet Squats.")
        
        for exo in exos_lundi:
            nom = exo["nom"]
            duree = exo["duree"]
            consigne = exo["consigne"]

            st.subheader(f"📍 En cours : {nom}")
            if nom != "Repos":
                coach_parle(f"{nom}. {consigne}")
            else:
                coach_parle("Repos. Détends-toi.")

            ph = st.empty()
            for s in range(duree, -1, -1):
                ph.metric(label=f"Chrono : {nom}", value=f"{s}s")
                if s == 10 and nom != "Repos": coach_parle("Encore 10 secondes !")
                if s == 3: coach_parle("3. 2. 1.")
                time.sleep(1)
            ph.empty()
            st.success(f"✅ {nom} validé")

        coach_parle("Séance terminée ! Fier de toi. N'oublie pas tes 220 grammes de protéines.")
        st.balloons()

# --- TAB 2 : NUTRITION (220g Prot / Jeûne) ---
with tabs[1]:
    st.header("🥗 Stratégie Nutritionnelle")
    st.warning("⚠️ Rappel : 220g de Protéines par jour")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Fenêtre Jeûne 16/8 :**")
        st.write("- 12h00 : Gros repas (Poulet/Légumes)")
        st.write("- 16h00 : Collation (Skyr + Whey)")
        st.write("- 19h30 : Repas Léger (Poisson/Oeufs)")
    with col2:
        st.checkbox("✅ Poulet/Poisson préparé")
        st.checkbox("✅ 3L d'eau bus")
        st.checkbox("✅ Skyr/Whey consommé")

# --- TAB 3 : SUIVI POIDS ---
with tabs[2]:
    st.header("📉 Objectif 111kg -> 90kg")
    poids = st.number_input("Poids du jour (kg)", 70.0, 150.0, 111.0)
    if st.button("Enregistrer le poids"):
        st.success(f"Poids de {poids}kg enregistré !")

# --- TAB 4 : PLAN 12 MOIS ---
with tabs[3]:
    st.header("🗓️ Ta Progression")
    st.table({
        "Mois": ["1-2", "3-5", "6-9", "10-12"],
        "Phase": ["Adaptation", "Force", "Volume", "Finition"],
        "RPE Cible": ["7-8", "8-9", "9", "9-10"]
    })
