import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.markdown("<style>body {background-color: #111; color: white;}</style>", unsafe_allow_html=True)

st.title("💡 Live Interview Hints")
st.subheader("Camera ke neeche phone rakh kar points dekhein")

# Gemini Key Setup
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Hum 'gemini-pro' use kar rahe hain kyunki text input ispe bina kisi error ke chalta hai
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("API Key missing in Settings.")

CONTEXT = """
Role: Python Developer
Skills: Django, FastAPI, PostgreSQL, AWS, Git
Projects: E-commerce Backend API, Student Management System
"""

SYSTEM_PROMPT = f"""
You are an interview assistant. Provide ONLY 3 short bullet points (max 6 words per point) based on the question.
Context: {CONTEXT}
"""

st.write("---")

# Text input box for mobile voice typing
question = st.text_input("Interviewer ka sawaal yahan likhein ya paste karein (ya voice typing keyboard ka use karein):")

if question:
    with st.spinner("AI is thinking..."):
        try:
            response = model.generate_content(f"{SYSTEM_PROMPT}\nQuestion: {question}")
            st.write("---")
            st.markdown("<h3 style='color: #00FF00;'>💡 Interview Hints:</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:24px; font-weight:bold; color:white;'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")
