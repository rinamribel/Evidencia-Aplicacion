import streamlit as st

def main():
    st.title("📝 Cuestionario de Perfil Cognitivo")

    st.markdown("""
    Responde las siguientes preguntas. Tu comportamiento será analizado junto con tus resultados en los minijuegos para predecir tu estilo de aprendizaje y rasgos de personalidad.
    """)

    st.subheader("📚 Estilo de Aprendizaje (VAK)")

    opciones = {
        "Visual": [
            "Ver ejemplos y diagramas",
            "Veo imágenes",
            "Usa la pizarra o diapositivas"
        ],
        "Auditory": [
            "Escucharlo explicado",
            "Lo escucho",
            "Explica con su voz"
        ],
        "Kinesthetic": [
            "Probarlo yo mismo",
            "Lo practico",
            "Nos pone a hacer ejercicios"
        ]
    }

    respuestas = [
        st.radio("1. Cuando aprendo algo nuevo, prefiero:", opciones["Visual"] + opciones["Auditory"] + opciones["Kinesthetic"]),
        st.radio("2. Me resulta más fácil recordar información cuando:", opciones["Visual"][1:] + opciones["Auditory"][1:] + opciones["Kinesthetic"][1:]),
        st.radio("3. En clases, pongo más atención cuando el profesor:", opciones["Visual"][2:] + opciones["Auditory"][2:] + opciones["Kinesthetic"][2:])
    ]

    estilo_votos = {"Visual": 0, "Auditory": 0, "Kinesthetic": 0}
    for r in respuestas:
        for estilo, frases in opciones.items():
            if r in frases:
                estilo_votos[estilo] += 1

    estilo_predicho = max(estilo_votos, key=estilo_votos.get)
    texto_ejemplo = " ".join(respuestas)

    st.subheader("🧠 Rasgos de Personalidad (Big Five - Versión corta)")

    respuestas_bigfive = {
        "extroversion": st.slider("4. Me considero una persona sociable", 1, 5, 3),
        "organizacion": st.slider("5. Suelo ser organizado y cumplir mis tareas a tiempo", 1, 5, 3),
        "impulsividad": st.slider("6. A veces actúo sin pensar en las consecuencias", 1, 5, 3),
        "empatia": st.slider("7. Me preocupo por los sentimientos de los demás", 1, 5, 3),
        "curiosidad": st.slider("8. Me gusta aprender cosas nuevas y explorar ideas", 1, 5, 3)
    }

    if st.button("Enviar respuestas"):
        st.session_state.estilo_texto = texto_ejemplo
        st.session_state.respuestas_bigfive = respuestas_bigfive
        st.success("✅ Tus respuestas han sido guardadas para el análisis del modelo.")
