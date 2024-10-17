import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar la API de Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuración de seguridad para evitar contenido inapropiado
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Configuración del modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Función para consultar a Gemini
def gemini_consult(query):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=(
                "responder como una secretaria administrativa de un local de tatuajes "
                "para responder consultas sobre precios y turnos de sesiones de tatuajes. "
                "Si el usuario pregunta si hay turnos, primero preguntarle si ya tiene definido "
                "qué trabajo se quiere realizar. Si pregunta si hay promociones, responder que "
                "no somos el supermercado Dia, y si consulta por descuentos, saludar cordialmente."
            )
        )

        # Generar la respuesta del modelo
        response = model.generate(query)  # Ajustamos esta línea
        return response

    except Exception as e:
        st.error(f"Error al consultar el modelo: {e}")
        return None

# Configurar la página de Streamlit
st.set_page_config(page_title="Chatbot con Gemini AI", page_icon="🤖")

# Título de la app
st.title("Bienvenidos al ChatBot Py con :rainbow[Gemini AI]")
st.divider()

# Inicializar el estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

if "first_message" not in st.session_state:
    st.session_state.first_message = True

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖"):
        st.markdown(message["content"])

# Mostrar mensaje inicial de bienvenida si es la primera interacción
if st.session_state.first_message:
    with st.chat_message("ai", avatar="🤖"):
        st.markdown("Amigo, ¿cómo va? ¿Cómo puedo ayudarte hoy?")
    st.session_state.messages.append(
        {"role": "assistant", "content": "Hola, ¿cómo puedo ayudarte?"}
    )
    st.session_state.first_message = False

# Procesar la entrada del usuario
if prompt := st.chat_input("¿Cómo te ayudo?"):
    with st.chat_message("user", avatar="🙋🏻‍♂️"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Obtener respuesta del modelo Gemini
    response = gemini_consult(prompt)

    # Mostrar la respuesta generada por el modelo
    if response and "text" in response:
        with st.chat_message("ai", avatar="🤖"):
            st.markdown(response['text'])  # Ajustado para el objeto correcto
        st.session_state.messages.append({"role": "ai", "content": response['text']})
    else:
        st.error("No se pudo obtener una respuesta del modelo.")
