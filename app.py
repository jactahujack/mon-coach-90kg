st.divider()
    st.subheader("⏱️ Minuteur Coach (Préparation + Bips)")
    duree_exo = st.radio("Temps d'effort :", [30, 45, 60], horizontal=True)
    
    if st.button(f"🚀 LANCER LA SÉRIE ({duree_exo}s)"):
        # Fonction pour le BIP sonore
        def faire_bip():
            st.markdown(
                """<audio autoplay><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>""",
                unsafe_allow_html=True
            )

        # 1. PHASE DE PRÉPARATION (3 SECONDES)
        placeholder = st.empty()
        for i in range(3, 0, -1):
            placeholder.error(f"⚠️ PRÉPARATION : {i}...")
            faire_bip()
            time.sleep(1)
        
        placeholder.success("🔥 C'EST PARTI ! TRAVAILLE !")
        faire_bip() # Bip de départ long (théoriquement)

        # 2. PHASE D'EFFORT
        bar = st.progress(0)
        for t in range(duree_exo):
            time.sleep(1)
            restant = duree_exo - (t + 1)
            bar.progress((t + 1) / duree_exo)
            
            # Annonce des 3 dernières secondes
            if restant <= 3 and restant > 0:
                placeholder.warning(f"⚡ DERNIER EFFORT : {restant}...")
                faire_bip()
        
        # 3. FIN
        st.balloons()
        placeholder.success("✅ REPOS ! SÉRIE TERMINÉE.")
        faire_bip()