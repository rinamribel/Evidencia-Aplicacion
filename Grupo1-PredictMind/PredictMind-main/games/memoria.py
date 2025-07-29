import streamlit as st
import random
import time

def main():
    if 'fase' not in st.session_state:
        st.session_state.fase = 'introduccion'
    if 'secuencia' not in st.session_state:
        st.session_state.secuencia = []
    if 'respuesta' not in st.session_state:
        st.session_state.respuesta = []
    if 'aciertos' not in st.session_state:
        st.session_state.aciertos = 0
    if 'mostrado' not in st.session_state:
        st.session_state.mostrado = False

    st.markdown("""
    <style>
    .color-box {
        font-size: 40px;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background-color: #2b2d42;
        margin: 10px;
        display: inline-block;
    }
    .title-section {
        font-size: 32px;
        color: #fcbf49;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .instructions {
        font-size: 18px;
        color: #d6d6d6;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title-section'>🧠 Juego de Memoria Visual</div>", unsafe_allow_html=True)

    if st.session_state.fase == 'introduccion':
        st.markdown("""
        <div class='instructions'>
        Este ejercicio mide tu <strong>memoria visual a corto plazo</strong>.<br><br>
        Memoriza una secuencia de colores y reprodúcela correctamente.<br>
        Este resultado será parte de tu perfil cognitivo.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎮 Empezar"):
            st.session_state.secuencia = random.choices(['🟥', '🟦', '🟩', '🟨'], k=5)
            st.session_state.fase = 'mostrar'
            st.session_state.mostrado = False
            st.rerun()

    elif st.session_state.fase == 'mostrar':
        st.markdown("### 👁️ Memoriza esta secuencia:")

        if not st.session_state.mostrado:
            placeholder = st.empty()
            for c in st.session_state.secuencia:
                placeholder.markdown(f"<div class='color-box'>{c}</div>", unsafe_allow_html=True)
                time.sleep(0.8)
                placeholder.markdown("<div class='color-box'> </div>", unsafe_allow_html=True)
                time.sleep(0.3)
            st.session_state.mostrado = True

        st.info("🧠 La secuencia ya fue mostrada.")
        if st.button("✅ Estoy listo"):
            st.session_state.fase = 'reproducir'
            st.rerun()

    elif st.session_state.fase == 'reproducir':
        st.markdown("### ✍️ Reproduce la secuencia en orden:")

        if len(st.session_state.respuesta) != len(st.session_state.secuencia):
            st.session_state.respuesta = ['🟥'] * len(st.session_state.secuencia)

        for i in range(len(st.session_state.secuencia)):
            st.session_state.respuesta[i] = st.selectbox(
                f"Paso {i+1}",
                ['🟥', '🟦', '🟩', '🟨'],
                key=f"resp_{i}",
                index=['🟥', '🟦', '🟩', '🟨'].index(st.session_state.respuesta[i])
            )

        if st.button("🔍 Verificar"):
            correctos = sum([
                1 for i in range(len(st.session_state.secuencia))
                if st.session_state.respuesta[i] == st.session_state.secuencia[i]
            ])
            st.session_state.aciertos = correctos
            st.session_state.memoria_puntaje = correctos
            st.session_state.fase = 'resultado'
            st.rerun()

    elif st.session_state.fase == 'resultado':
        st.markdown("### 🧾 Resultado del juego de memoria:")
        total = len(st.session_state.secuencia)
        aciertos = st.session_state.aciertos

        if aciertos == total:
            st.success(f"🎉 ¡Perfecto! Reprodujiste toda la secuencia correctamente ({aciertos}/{total}).")
            st.balloons()
        else:
            st.warning(f"🔍 Aciertos: {aciertos} de {total}")

        st.markdown("""
        <hr>
        🧠 <strong>Dato importante:</strong><br>
        Este puntaje será utilizado por la IA para afinar tu perfil cognitivo.
        """, unsafe_allow_html=True)

        if st.button("🔁 Jugar de nuevo"):
            for key in ['fase', 'secuencia', 'respuesta', 'aciertos', 'mostrado']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
