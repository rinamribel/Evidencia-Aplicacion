import streamlit as st

st.set_page_config(page_title="PredictMind", layout="centered")

st.title("🧠 PredictMind")
st.subheader("Descubre tu personalidad y estilo de aprendizaje con inteligencia artificial")

pagina = st.sidebar.selectbox("Navegar", [
    "Inicio",
    "Juego de Memoria",
    "Juego de Reacción",
    "Cuestionario",
    "Resultados",
    "Explicación de la IA"
])


if pagina == "Inicio":
    st.write("""
    Bienvenido a PredictMind, una aplicación que analiza tu estilo de aprendizaje y rasgos de personalidad a través de mini juegos interactivos y un breve cuestionario.

    ### ¿Qué encontrarás aquí?
    - Juegos que recopilan tu comportamiento cognitivo
    - Preguntas basadas en tests reales (VAK y Big Five)
    - Un análisis generado con modelos de inteligencia artificial entrenados con datos reales

    Pulsa en el menú lateral para comenzar 🔍
    """)

elif pagina == "Juego de Memoria":
    from games import memoria
    memoria.main()

elif pagina == "Juego de Reacción":
    from games import tiempo_reaccion
    tiempo_reaccion.main()

elif pagina == "Cuestionario":
    from games import cuestionario
    cuestionario.main()

elif pagina == "Resultados":
    from games import resultados
    resultados.main()

elif pagina == "Explicación de la IA":
    st.markdown("## 🤖 ¿Cómo funciona la inteligencia artificial de PredictMind?")
    
    st.markdown("""
    Nuestra IA combina tus resultados en los juegos cognitivos y el cuestionario para analizar tu estilo de aprendizaje y ciertos rasgos de tu personalidad.

    ### 📊 Fuentes de información:
    - **Juegos cognitivos**: Miden memoria, atención y tiempo de reacción.
    - **Cuestionario adaptativo**: Basado en modelos de psicología como:
        - 🧠 **VAK** (Visual, Auditivo, Kinestésico)
        - 🧬 **Big Five** (Los 5 grandes rasgos de personalidad)

    ### 🧠 ¿Qué modelo usamos?
    Utilizamos un algoritmo de **Random Forest**, entrenado con datos reales, validado con precisión entre el **90% y 95%**.

    - Toma decisiones evaluando múltiples árboles de decisión.
    - Puede adaptarse a distintos patrones de comportamiento.
    - Es robusto ante datos atípicos o respuestas inconsistentes.

    ### 🧩 ¿Cómo se genera tu perfil?
    1. Tus respuestas y tiempos son transformados en vectores numéricos.
    2. El modelo analiza esos vectores.
    3. Se generan predicciones como:
        - Estilo de aprendizaje dominante
        - Nivel de impulsividad
        - Tendencias de personalidad (ej: apertura, responsabilidad)

    > 💡 *Mientras más interactúas con la app, más precisa será la predicción final.*
    """)
