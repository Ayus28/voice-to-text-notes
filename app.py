import streamlit as st
import google.generativeai as genai

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
    st.error("API Key settings mein sahi se nahi daali gayi hai.")

# Aapka Resume aur Context
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

# NEW BUTTON: Yeh line phone mein microphone icon dikhayegi aur permission mangegi
audio_file = st.audio_input("Interview ke time is Mic icon par click karke chhod dein")

if audio_file is not None:
    st.write("Processing audio...")
    try:
        # Audio ko text mein badalna aur Gemini se answer lena
        # Streamlit ka naya feature direct audio file ko process kar sakta hai
        response = model.generate_content([
            f"{SYSTEM_PROMPT}\nListen to this audio and give 3 short bullet points based on the interview question/topic.",
            {"mime_type": "audio/wav", "data": audio_file.read()}
        ])
        
        st.write("---")
        st.markdown(f"<div style='font-size:24px; font-weight:bold; color:#00FF00;'>{response.text}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.write("Aawaaz saaf nahi thi, ya API key ka issue hai. Kripya dobara bolein.")
