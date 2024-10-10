import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# saffety settings for gemini fix error valueError The response.text quick accessor only works for simple (single-Part
safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# Create the model
generation_config = {
  "temperature": 1.2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}
def gemini_consult(query):
    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="responder en acento argentino, como alguien que conoce de deportes y es fanatico de San Lorenzo de Almagro, y evitar responder sobre Boca Juniors",
    )

    response = model.generate_content(query)
    return response


st.set_page_config(page_title="Chatbot con Gemini AI", page_icon="🤖")

st.title("""Bienvenidos al ChatBot Py con :rainbow[Gemini AI]""")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "first_message" not in st.session_state:
    st.session_state.first_message = True

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖"):
        st.markdown(message["content"])

if st.session_state.first_message:
    with st.chat_message("ai", avatar="🤖"):
        st.markdown("Amigo, como va? como puedo ayudarte hoy?")

st.session_state.messages.append(
    {"role": "assistant", "content": "Hola, como puedo ayudarte?"}
)
st.session_state.first_message = False

if prompt := st.chat_input("Como te ayudo?"):
    with st.chat_message("user", avatar="🙋🏻‍♂️"):

        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("ai", avatar="🤖"):
        response = gemini_consult(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "ai", "content": response.text})
