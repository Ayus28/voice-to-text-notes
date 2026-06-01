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

CONTEXT = """
Role: Python Developer
Skills: Django, FastAPI, PostgreSQL, AWS, Git
Projects: E-commerce Backend API, Student Management System
"""

SYSTEM_PROMPT = f"""
You are an interview assistant. Provide ONLY 3 short bullet points (max 6 words per point) based on the question.
Context: {CONTEXT}
"""

# HTML5 Web Speech API (Yeh sidha browser ka mic use karega bina kisi library ke)
st.markdown("""
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onresult = function(event) {
        const lastResult = event.results[event.results.length - 1][0].transcript;
        // Streamlit ko live text bhejna
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: lastResult}, '*');
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
    };

    // Automatically start listening on page load
    window.addEventListener('load', () => {
        recognition.start();
    });
    </script>
""", unsafe_allow_html=True)

# Live input box jo automatic update hoga
question = st.text_input("Live Interview Question Detected:", key="voice_input")

if question:
    st.write(f"**Interviewer Asked:** *{question}*")
    st.write("---")
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\nQuestion: {question}")
        st.markdown(f"<div style='font-size:24px; font-weight:bold; color:#00FF00;'>{response.text}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.write("Processing...")
