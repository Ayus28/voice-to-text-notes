import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.markdown("<style>body {background-color: #111; color: white;}</style>", unsafe_allow_html=True)

st.title("💡 Live Interview Hints")
st.subheader("Camera ke neeche phone rakh kar points dekhein")

# Secrets se API Key nikalna
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing in Settings.")

CONTEXT = """
Role: Python Developer
Skills: Django, FastAPI, PostgreSQL, AWS, Git
Projects: E-commerce Backend API, Student Management System
"""

SYSTEM_PROMPT = f"""
You are an interview assistant. Provide ONLY 3 short bullet points (max 6 words per point) answering the question based on the candidate's context.
Do not include any introductory text, titles, explanations, or formatting other than 3 clean bullet points.
Context:
{CONTEXT}
"""

st.write("---")

# Text input box for mobile voice typing
question = st.text_input("Interviewer ka sawaal yahan bolein:")

if question and api_key:
    with st.spinner("AI is thinking..."):
        # Library skip karke direct endpoint par hit karna jisse 404 error nahi aayega
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"{SYSTEM_PROMPT}\nQuestion: {question}"}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            res_json = response.json()
            
            # API response se text nikalna
            output_text = res_json['candidates'][0]['content']['parts'][0]['text']
            
            st.write("---")
            st.markdown("<h3 style='color: #00FF00;'>💡 Interview Hints:</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:24px; font-weight:bold; color:white; line-height:1.8;'>{output_text}</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Error processing request. Check your API key or network connection.")
