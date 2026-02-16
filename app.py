import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="MON COACH ELITE - 90KG", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .motivation-box {
        font-size: 24px; font-weight: bold; color: #FFFFFF;
        text-align: center; padding: 20px; border-radius: 15px;
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE DATE & MOTIVATION ---
d_view = st.date_input("📅 Date de l'entraînement :", date.today())
jour_nom = d_view.strftime('%A')

citations = {
    "Monday": "🚀 LUNDI : Nouvelle semaine, nouveau combat. Forge l'homme que tu veux être.",
    "Tuesday": "🔥 MARDI : La discipline bat la motivation. Reste focus.",
    "Wednesday": "💪 MERCREDI : Mi-chemin. Ne lâche rien, la fierté t'attend.",
    "Thursday": "⚔️ JEUDI : La douleur est temporaire, l'abandon est définitif.",
    "Friday": "⚡ VENDREDI : Finis fort. Protège tes gains de la semaine.",
    "Saturday": "🏆 SAMEDI : Fais aujourd'hui ce que les autres ne font pas.",
    "Sunday": "🧘 DIMANCHE : Récupère et prépare l'assaut de demain."
}
st.markdown(f'<div class="motivation-box">{citations.get(jour_nom)}</div>', unsafe_allow_html=True)

# --- PROGRAMME PRÉCIS MOIS 1 ---
def obtenir_details_programme(jour):
    prog = {
        "Monday": {
            "titre": "🏋️ RENFORCEMENT A (Bas & Core)",
            "exos": "- **Goblet Squat** : 3×12 (25 kg)\n- **Fentes avant** : 3×8/j (10 kg)\n- **Planche** : 60''\n- **Gainage latéral** : 45''/côté",
            "nutri": "**220g Protéines** | 180g Féculents | Eau: ≥2,5L"
        },
        "Wednesday": {
            "titre": "🏋️ RENFORCEMENT B (Haut & Core)",
            "exos": "- **Pompes lestées** : 4×6 (5-10 kg)\n- **Rowing** : 4×6 (20 kg)\n- **Hollow Hold** : 30''\n- **Mountain Climbers** : 30''",
            "nutri": "**220g Protéines** | 180g Féculents | Eau: ≥2,5L"
        },
        "Saturday": {
            "titre": "🧘 CORE + MOBILITÉ",
            "exos": "- **Planche** : 60''\n- **Hollow Hold** : 30''\n- **Mountain Climbers** : 30''",
            "nutri": "**220g Protéines** | 180g Féculents | Eau: ≥2,5L"
        },
        "Tuesday": {"titre": "🏃 MARCHE FRACTIONNÉE", "exos": "6 × (2' rapide / 2' lente) - RPE 8", "nutri": "180-200g Protéines | 100-120g Féc"},
        "Friday": {"titre": "🏃 MARCHE FRACTIONNÉE", "exos": "6 × (2' rapide / 2' lente) - RPE 8", "nutri": "180-200g Protéines | 100-120g Féc"},
        "Thursday": {"titre": "🚶 MARCHE MODÉRÉE", "exos": "5 km - RPE 5-6", "nutri": "180-200g Protéines | 100-120g Féc"},
        "Sunday": {"titre": "🛌 REPOS ACTIF", "exos": "Marche 3 km + Étirements", "nutri": "180-200g Protéines | 100-120g Féc"}
    }
    return prog.get(jour, {"titre": "Repos", "exos": "Détente", "nutri": "Stable"})

# --- INTERFACE ---
tabs = st.tabs(["🏋️ SÉANCE", "✅ CHECK-LIST", "📊 BILAN", "📈 SUIVI"])

with tabs[0]:
    p = obtenir_details_programme(jour_nom)
    st.header(p["titre"])
    c1, c2 = st.columns(2)
    with c1: st.info(f"### 📝 Exercices\n{p['exos']}")
    with c2: st.warning(f"### 🥩 Nutrition\n{p['nutri']}")
    
    st.divider()
    st.subheader("🎮 Mode Entraînement Immersif")
    duree_exo = st.radio("Temps d'effort :", [30, 45, 60], horizontal=True)
    
    if st.button(f"🚀 LANCER LA SÉRIE ({duree_exo}s)"):
        # Sons ludiques
        SOUND_GO = "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
        SOUND_FINAL = "https://actions.google.com/sounds/v1/human/cheering_and_clapping.ogg"
        SOUND_TICK = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"

        def play(url):
            st.markdown(f'<audio autoplay><source src="{url}" type="audio/ogg"></audio>', unsafe_allow_html=True)

        ph = st.empty()
        # 1. PRÉPARATION
        for i in range(3, 0, -1):
            ph.error(f"✨ PRÉPARE-TOI... {i}")
            play(SOUND_TICK)
            time.sleep(1)
        
        ph.success("🔥 ACTION ! DONNE TOUT !")
        play(SOUND_GO)

        # 2. EFFORT
        bar = st.progress(0)
        for t in range(duree_exo):
            time.sleep(1)
            bar.progress((t + 1) / duree_exo)
            restant = duree_exo - (t + 1)
            if restant <= 3 and restant > 0:
                ph.warning(f"⚡ FINIS FORT : {restant}...")
                play(SOUND_TICK)
        
        # 3. VICTOIRE
        st.balloons()
        ph.success("🏆 BIEN JOUÉ CHAMPION ! REPOS.")
        play(SOUND_FINAL)

with tabs[1]:
    st.header("✅ Check-list")
    st.checkbox("🥩 Protéines (4x)")
    st.checkbox("🥦 Légumes")
    st.checkbox("💧 Eau (2,5L+)")

with tabs[2]:
    st.header("📊 Bilan Mensuel")
    with st.form("bilan_f"):
        st.text_area("✅ Points positifs")
        st.text_area("⚠️ À améliorer")
        st.form_submit_button("Sauvegarder")

with tabs[3]:
    st.header("📈 Poids")
    st.number_input("Poids (kg)", 70.0, 150.0, 111.0)
    st.button("Enregistrer")
