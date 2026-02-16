st.divider()
    st.subheader("🎮 Mode Entraînement Immersif")
    duree_exo = st.radio("Temps d'effort :", [30, 45, 60], horizontal=True)
    
    if st.button(f"🚀 LANCER LA SÉRIE ({duree_exo}s)"):
        # Sons ludiques
        SOUND_PREP = "https://actions.google.com/sounds/v1/foley/clock_ticking.ogg"
        SOUND_GO = "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
        SOUND_FINAL = "https://actions.google.com/sounds/v1/human/cheering_and_clapping.ogg"
        SOUND_TICK = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"

        def play(url):
            st.markdown(f"""<audio autoplay><source src="{url}" type="audio/ogg"></audio>""", unsafe_allow_html=True)

        ph = st.empty()
        # 1. PRÉPARATION LUDIQUE
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