import streamlit as st
import time
import random

def main():
    if "fase" not in st.session_state:
        st.session_state.fase = "inicio"
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0.0
    if "tiempo_reaccion" not in st.session_state:
        st.session_state.tiempo_reaccion = None
    if "tiempo_reaccion_valor" not in st.session_state:
        st.session_state.tiempo_reaccion_valor = None
    if "mensaje_mostrado" not in st.session_state:
        st.session_state.mensaje_mostrado = False
    if "reaccion_fallo" not in st.session_state:
        st.session_state.reaccion_fallo = False

    st.markdown("""
    <style>
    .reaction-box {
        font-size: 28px;
        padding: 20px;
        text-align: center;
        border-radius: 12px;
        margin: 20px 0;
        background-color: #2b2d42;
        color: white;
    }
    .reaction-title {
        font-size: 36px;
        color: #fcbf49;
        font-weight: bold;
    }
    .reaction-info {
        font-size: 18px;
        color: #d6d6d6;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='reaction-title'>⚡ Juego de Tiempo de Reacción</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='reaction-info'>
    En este juego mediremos tu <strong>tiempo de reacción</strong> ante un estímulo visual.<br><br>
    Este valor será utilizado por nuestra <strong>IA</strong> para estimar tu <strong>nivel de impulsividad</strong>.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.fase == "inicio":
        if st.button("🎮 Comenzar prueba"):
            st.session_state.fase = "esperando"
            st.session_state.tiempo_reaccion = None
            st.session_state.tiempo_reaccion_valor = None
            st.session_state.reaccion_fallo = False
            st.session_state.mensaje_mostrado = False
            st.rerun()

    elif st.session_state.fase == "esperando":
        if st.session_state.mensaje_mostrado:
            st.markdown("<div class='reaction-box'>🟢 ¡Haz clic ahora!</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='reaction-box'>⏳ Espera el estímulo...</div>", unsafe_allow_html=True)

        if st.button("¡Haz clic!"):
            if not st.session_state.mensaje_mostrado:
                st.session_state.reaccion_fallo = True
                st.session_state.fase = "resultado"
                st.rerun()
            else:
                end_time = time.time()
                reaction_time = round(end_time - st.session_state.start_time, 3)
                st.session_state.tiempo_reaccion = reaction_time
                st.session_state.tiempo_reaccion_valor = reaction_time
                st.session_state.fase = "resultado"
                st.rerun()

        if not st.session_state.mensaje_mostrado:
            wait_time = random.uniform(2, 5)
            time.sleep(wait_time)
            st.session_state.start_time = time.time()
            st.session_state.mensaje_mostrado = True
            st.rerun()

    elif st.session_state.fase == "resultado":
        if st.session_state.reaccion_fallo or st.session_state.tiempo_reaccion is None:
            st.error("⛔ Hiciste clic antes del estímulo. Se registró como impulsividad.")
        else:
            tiempo = st.session_state.tiempo_reaccion
            st.success(f"⏱️ Tu tiempo de reacción fue de {tiempo} segundos.")
            if tiempo < 0.25:
                st.markdown("🧠 <strong>Increíblemente rápido</strong>", unsafe_allow_html=True)
            elif tiempo < 0.4:
                st.markdown("👍 <strong>Muy buen tiempo</strong>", unsafe_allow_html=True)
            elif tiempo < 0.6:
                st.markdown("👌 <strong>Promedio normal</strong>", unsafe_allow_html=True)
            else:
                st.markdown("🕓 <strong>Tiempo elevado</strong>", unsafe_allow_html=True)
            st.caption("✅ Este valor será registrado como parte de tu perfil cognitivo.")

        if st.button("🔁 Volver a intentarlo"):
            for key in ['fase', 'start_time', 'tiempo_reaccion', 'tiempo_reaccion_valor', 'mensaje_mostrado', 'reaccion_fallo']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
