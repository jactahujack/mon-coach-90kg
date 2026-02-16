import streamlit as st
import time
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. LE MOTEUR VOCAL ---
def coach_parle(texte):
    # Cette fonction fait parler ton téléphone/ordi directement
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{texte}");
            msg.lang = 'fr-FR';
            msg.rate = 0.9; // Vitesse légèrement plus lente pour plus de clarté
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="MON COACH ELITE - 90KG", layout="wide")

# --- 3. TON PROGRAMME DU LUNDI 16 FÉVRIER ---
exercices = [
    {"nom": "Goblet Squat (25kg)", "duree": 45, "rpe": "7", "consigne": "Dos droit, descends bien bas."},
    {"nom": "Repos", "duree": 60, "rpe": "-", "consigne": "Respire, bois une gorgée."},
    {"nom": "Fentes avant (10kg)", "duree": 40, "rpe": "7-8", "consigne": "Contrôle la descente, ne cogne pas le genou."},
    {"nom": "Repos", "duree": 60, "rpe": "-", "consigne": "Prépare-toi pour le gainage."},
    {"nom": "Planche (Gainage)", "duree": 60, "rpe": "8", "consigne": "Aspire le nombril, ne creuse pas le dos."},
    {"nom": "Repos", "duree": 30, "rpe": "-", "consigne": "Dernier effort sur le côté."},
    {"nom": "Gainage latéral", "duree": 45, "rpe": "8", "consigne": "Hanches bien hautes."}
]

st.title("🚀 Coach Vocal : Séance du Lundi 16/02")
st.info("Objectif : 220g de Protéines | Jeûne 16/8")

# --- 4. LE CHRONO VOCAL ---
if st.button("🏁 LANCER LE COACHING VOCAL"):
    coach_parle("C'est parti Champion ! On commence avec les Goblet Squats à 25 kilos.")
    
    for exo in exercices:
        nom = exo["nom"]
        duree = exo["duree"]
        consigne = exo["consigne"]

        st.subheader(f"📍 En cours : {nom}")
        st.write(f"💡 *{consigne}*")
        
        # Annonce vocale de l'exercice
        if nom != "Repos":
            coach_parle(f"Exercice suivant : {nom}. {consigne}")
        else:
            coach_parle("Repos bien mérité. Respire.")

        # Affichage du chrono
        placeholder = st.empty()
        for s in range(duree, -1, -1):
            placeholder.metric(label=f"Chrono : {nom}", value=f"{s}s")
            
            # Alertes vocales pendant l'effort
            if s == 10 and nom != "Repos":
                coach_parle("Encore 10 secondes, tiens bon !")
            if s == 3:
                coach_parle("3, 2, 1...")
            
            time.sleep(1)
        
        placeholder.empty()
        st.success(f"✅ {nom} validé !")

    coach_parle("Séance terminée ! Bravo Champion. N'oublie pas tes protéines et bois 3 litres d'eau aujourd'hui.")
    st.balloons()

# --- 5. RAPPEL NUTRITION ---
with st.expander("🍎 Rappel Nutrition du jour"):
    st.write("- **12h00 :** Gros repas (Poulet/Légumes rôtis)")
    st.write("- **16h00 :** Collation (Skyr + Whey)")
    st.write("- **19h30 :** Repas léger (Poisson/Omelette)")
