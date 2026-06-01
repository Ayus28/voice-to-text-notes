import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.markdown("<style>body {background-color: #111; color: white;}</style>", unsafe_allow_html=True)

st.title("💡 Live Interview Hints")
st.subheader("Camera ke neeche phone rakh kar points dekhein")

# Gemini Setup
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("API Key missing in Settings.")

# Context aur Skills (Ise apne hisab se change kar sakte hain)
CONTEXT = """
Role: Python Developer
Skills: Django, FastAPI, PostgreSQL, AWS, Git
Projects: E-commerce Backend API, Student Management System
"""

SYSTEM_PROMPT = f"""
You are an interview assistant. Based on the interview question or topic in the audio, provide the user with clear answers.
Provide ONLY 3 short bullet points (max 6 words per point). No introductory or concluding remarks.
Context:
{CONTEXT}
"""

st.write("---")
# Streamlit ka official audio input handler (Sabse reliable feature)
audio_file = st.audio_input("Neeche diye gaye mic icon par click karein aur bolna shuru karein:")

if audio_file is not None:
    with st.spinner("Processing your audio with AI..."):
        try:
            # Direct audio chunks ko Gemini ke pass analyze hone ke liye bhejna
            audio_bytes = audio_file.read()
            response = model.generate_content([
                f"{SYSTEM_PROMPT}\nAnalyze this audio clip and provide the 3 short bullet points directly.",
                {"mime_type": "audio/wav", "data": audio_bytes}
            ])
            
            st.write("---")
            st.markdown("<h3 style='color: #00FF00;'>💡 Interview Hints:</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:24px; font-weight:bold; color:white; line-height: 1.6;'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error processing audio: {e}")
