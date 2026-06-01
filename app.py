import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import threading
import queue

# Page Configuration (Bada text aur dark mode ke liye)
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.markdown("<style>body {background-color: #111; color: white;}</style>", unsafe_allow_html=True)

st.title("💡 Live Interview Hints")
st.subheader("Camera ke neeche phone rakh kar points dekhein")

# Gemini API Setup (Streamlit Secrets se key lega)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("API Key not set up yet in Advanced Settings.")

# Aapka Resume aur Context (Ise aap baad mein edit kar sakte hain)
CONTEXT = """
Role: Python Developer
Skills: Django, FastAPI, PostgreSQL, AWS, Git
Projects: E-commerce Backend API, Student Management System
"""

SYSTEM_PROMPT = f"""
You are an interview assistant. Based on the context below, answer the interviewer's question.
Provide ONLY 3 short bullet points (max 6 words per point). No intro, no outro.

Context:
{CONTEXT}
"""

# Audio processing ke liye queue
if 'queue' not in st.session_state:
    st.session_state.queue = queue.Queue()

def listen_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=7)
                text = recognizer.recognize_google(audio)
                st.session_state.queue.put(text)
            except:
                pass

# Background thread shuru karna jo phone ka mic on rakhega
if 'started' not in st.session_state:
    st.session_state.started = True
    threading.Thread(target=listen_audio, daemon=True).start()

# UI display area
placeholder = st.empty()

while True:
    if not st.session_state.queue.empty():
        question = st.session_state.queue.get()
        with placeholder.container():
            st.write(f"**Interviewer Asked:** *{question}*")
            st.write("---")
            
            try:
                response = model.generate_content(f"{SYSTEM_PROMPT}\nQuestion: {question}")
                st.markdown(f"<div style='font-size:24px; font-weight:bold; color:#00FF00;'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.write("Processing...")
