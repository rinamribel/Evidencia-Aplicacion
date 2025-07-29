
import streamlit as st
import joblib
import numpy as np

def main():
    st.title("📊 Resultados PredictMind")

    st.markdown("""
    En esta sección verás los resultados de tu perfil cognitivo y de personalidad
    generados por los modelos de inteligencia artificial entrenados con tus respuestas.
    """)

    requeridos = ["memoria_puntaje", "tiempo_reaccion_valor",
                  "respuestas_bigfive", "estilo_texto"]

    faltantes = [r for r in requeridos if r not in st.session_state]
    if faltantes:
        st.warning(f"Faltan datos para generar resultados: {', '.join(faltantes)}")
        st.info("Asegúrate de haber completado los juegos y cuestionario.")
        return

    try:
        modelo_vak = joblib.load("model/modelo_vak.pkl")
        vectorizador = joblib.load("model/vectorizer_vak.pkl")
        modelo_impulsividad = joblib.load("model/modelo_impulsividad.pkl")
        modelo_sociabilidad = joblib.load("model/modelo_sociabilidad.pkl")
    except Exception as e:
        st.error(f"❌ Error al cargar modelos: {e}")
        return

    # Estilo de aprendizaje
    texto = st.session_state.estilo_texto
    texto_vectorizado = vectorizador.transform([texto])
    estilo_predicho = modelo_vak.predict(texto_vectorizado)[0]

    # Big Five (20 features)
    ext = [st.session_state.respuestas_bigfive.get(f'EXT{i}', 0) for i in range(1, 11)]
    agr = [st.session_state.respuestas_bigfive.get(f'AGR{i}', 0) for i in range(1, 11)]
    bigfive_vals = ext + agr

    impulsividad_pred = modelo_impulsividad.predict([bigfive_vals])[0]
    sociabilidad_pred = modelo_sociabilidad.predict([bigfive_vals])[0]

    st.subheader("🎯 Tu perfil")

    st.markdown(f"""
    - **Estilo de aprendizaje dominante**: `{estilo_predicho}`
    - **Nivel de impulsividad**: `{impulsividad_pred}`
    - **Nivel de sociabilidad**: `{sociabilidad_pred}`
    - **Puntaje de memoria**: `{st.session_state.memoria_puntaje} / 5`
    - **Tiempo de reacción**: `{st.session_state.tiempo_reaccion_valor} segundos`
    """)

    st.subheader("🧠 Recomendaciones personalizadas")

    if estilo_predicho == "Visual":
        st.write("- Usa mapas mentales, esquemas y videos explicativos.")
    elif estilo_predicho == "Auditory":
        st.write("- Graba tus clases y escúchalas luego. Participa en debates.")
    else:
        st.write("- Aprende haciendo. Usa objetos, construye, dibuja.")

    if impulsividad_pred == "alta":
        st.write("- Practica ejercicios de control del impulso. Usa recordatorios para pausas.")
    elif impulsividad_pred == "media":
        st.write("- Estás equilibrado, pero procura no tomar decisiones apresuradas.")
    else:
        st.write("- Muy buen control. Puedes enfocarte en tareas largas sin problema.")

    if sociabilidad_pred == "baja":
        st.write("- Intenta participar en grupos pequeños para fortalecer tus habilidades sociales.")
    elif sociabilidad_pred == "media":
        st.write("- Estás en un punto ideal para trabajar en equipo o individual.")
    else:
        st.write("- Usa tu sociabilidad para colaborar y liderar en proyectos.")

    st.success("✅ Tus resultados han sido generados exitosamente.")
