import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="MON COACH ELITE - 90KG", layout="wide")

# --- STYLE CSS (MOTIVATION EN COULEUR) ---
st.markdown("""
    <style>
    .motivation-box {
        font-size: 24px; font-weight: bold; color: #FFFFFF;
        text-align: center; padding: 20px; border-radius: 15px;
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        border: none; box-shadow: 0 4px 15px rgba(255, 75, 43, 0.3);
        margin-bottom: 25px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f8f9fa; border-radius: 10px; padding: 12px 20px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE DATE & MOTIVATION ---
d_view = st.date_input("📅 Date de l'entraînement :", date.today())
jour_nom = d_view.strftime('%A')

citations = {
    "Monday": "🚀 LUNDI : Nouvelle semaine, nouveau combat. L'homme que tu seras dans 12 mois se construit aujourd'hui.",
    "Tuesday": "🔥 MARDI : La discipline est le pont entre tes objectifs et tes accomplissements. Traverse-le.",
    "Wednesday": "💪 MERCREDI : Mi-chemin. Ne regarde pas combien il reste, regarde le chemin déjà parcouru.",
    "Thursday": "⚔️ JEUDI : La douleur de la discipline est bien moindre que celle du regret. Pousse !",
    "Friday": "⚡ VENDREDI : Termine la semaine avec honneur. Pas d'excuses, juste des résultats.",
    "Saturday": "🏆 SAMEDI : Les champions ne s'arrêtent pas quand ils sont fatigués, ils s'arrêtent quand ils ont fini.",
    "Sunday": "🧘 DIMANCHE : Récupère et analyse. Demain, on repart à l'assaut plus fort."
}
st.markdown(f'<div class="motivation-box">{citations.get(jour_nom)}</div>', unsafe_allow_html=True)

# --- PROGRAMME PRÉCIS MOIS 1 ---
def obtenir_details_programme(jour):
    prog = {
        "Monday": {
            "titre": "🏋️ RENFORCEMENT A (Bas du corps & Core)",
            "exos": """
            - **Goblet Squat** : 3 séries × 12 reps (Poids : 25 kg)
            - **Fentes avant** : 3 séries × 8 reps/jambe (Poids : 10 kg)
            - **Planche (gainage frontal)** : 60 secondes
            - **Gainage latéral** : 45 secondes par côté
            """,
            "nutri": "**220g Protéines** | 180g Féculents | Graisses: 20-25g | Eau: ≥2,5L"
        },
        "Wednesday": {
            "titre": "🏋️ RENFORCEMENT B (Haut du corps & Core)",
            "exos": """
            - **Pompes lestées** : 4 séries × 6 reps (Lest : 5-10 kg)
            - **Rowing** : 4 séries × 6 reps (Poids : 20 kg)
            - **Hollow Hold** : 30 secondes
            - **Mountain Climbers** : 30 secondes
            """,
            "nutri": "**220g Protéines** | 180g Féculents | Graisses: 20-25g | Eau: ≥2,5L"
        },
        "Saturday": {
            "titre": "🧘 CORE + MOBILITÉ (Stabilité)",
            "exos": """
            - **Planche** : 60 secondes
            - **Hollow Hold** : 30 secondes
            - **Mountain Climbers** : 30 secondes
            - **Étirements bas du corps** : 10 minutes
            """,
            "nutri": "**220g Protéines** | 180g Féculents | Graisses: 20-25g | Eau: ≥2,5L"
        },
        "Tuesday": {
            "titre": "🏃 MARCHE FRACTIONNÉE (Cardio)",
            "exos": "- **Fractionné** : 6 × (2' rapide / 2' lente)\n- **Intensité** : RPE 8 (Essoufflé mais capable de parler brièvement)",
            "nutri": "**180-200g Protéines** | 100-120g Féculents | Eau: ≥2L"
        },
        "Friday": {
            "titre": "🏃 MARCHE FRACTIONNÉE (Cardio)",
            "exos": "- **Fractionné** : 6 × (2' rapide / 2' lente)\n- **Intensité** : RPE 8",
            "nutri": "**180-200g Protéines** | 100-120g Féculents | Eau: ≥2L"
        },
        "Thursday": {
            "titre": "🚶 MARCHE MODÉRÉE (Récupération active)",
            "exos": "- **Marche continue** : 5 km\n- **Intensité** : RPE 5-6 (Rythme soutenu)",
            "nutri": "**180-200g Protéines** | 100-120g Féculents | Eau: ≥2L"
        },
        "Sunday": {
            "titre": "🛌 REPOS ACTIF",
            "exos": "- **Marche plaisir** : 3 km\n- **Étirements complets** : 15 minutes",
            "nutri": "**180-200g Protéines** | 100-120g Féculents | Eau: ≥2L"
        }
    }
    return prog.get(jour)

# --- AFFICHAGE ---
tabs = st.tabs(["🏋️ SÉANCE", "✅ CHECK-LIST NUTRITION", "📊 BILAN MENSUEL", "📈 ÉVOLUTION"])

with tabs[0]:
    p = obtenir_details_programme(jour_nom)
    st.header(p["titre"])
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"### 📝 Exercices précis\n{p['exos']}")
    with c2:
        st.warning(f"### 🥩 Objectifs Nutrition\n{p['nutri']}")
    
    st.divider()
    st.subheader("⏱️ Minuteur Chrono")
    duree = st.radio("Temps :", [30, 45, 60], horizontal=True)
    if st.button(f"LANCER {duree} SECONDES"):
        bar = st.progress(0)
        for i in range(duree):
            time.sleep(1)
            bar.progress((i + 1) / duree)
        st.success("SÉRIE TERMINÉE !")

with tabs[1]:
    st.header("✅ Check-list quotidienne")
    st.checkbox("🥩 Protéines à chaque repas (4x)")
    st.checkbox("🥦 Légumes aux repas principaux")
    st.checkbox("🍎 1 Fruit aujourd'hui")
    st.checkbox("💧 Hydratation (2,5L+)")
    st.checkbox("🚫 Zéro écart alimentaire")

with tabs[2]:
    st.header("📊 Bilan Mensuel de fin de phase")
    with st.form("bilan_final"):
        st.subheader("Mesures physiques")
        col1, col2 = st.columns(2)
        p_fin = col1.number_input("Poids fin de mois (kg)", 70.0, 150.0)
        t_fin = col2.number_input("Tour de taille fin (cm)", 50, 150)
        
        st.subheader("Analyse qualitative")
        pos = st.text_area("✅ Points positifs (Mes réussites)")
        neg = st.text_area("⚠️ Points à améliorer (Mes difficultés)")
        obj = st.text_area("🎯 Objectifs pour le mois suivant")
        
        if st.form_submit_button("SAUVEGARDER LE BILAN"):
            st.balloons()
            st.success("Bilan enregistré. Analyse tes erreurs pour ne plus les refaire !")

with tabs[3]:
    st.header("📈 Suivi du Poids")
    poids_saisi = st.number_input("Poids du jour (kg)", 70.0, 150.0, 111.0)
    notes_saisies = st.text_area("Note sur la séance ou l'énergie")
    if st.button("Enregistrer la pesée"):
        st.success("Données enregistrées dans l'historique.")