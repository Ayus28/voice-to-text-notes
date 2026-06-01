import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.markdown("<style>body {background-color: #111; color: white;}</style>", unsafe_allow_html=True)

st.title("💡 Live Interview Hints")
st.subheader("Camera ke neeche phone rakh kar points dekhein")

# Secrets se API Key nikalna
api_key = st.secrets.get("GEMINI_API_KEY")

CONTEXT = """
Role: Python Developer
Skills: Django, FastAPI, PostgreSQL, AWS, Git
Projects: E-commerce Backend API, Student Management System
"""

# System prompt ko simplify kiya taaki JSON break na ho
prompt_data = f"You are an interview assistant. Based on this Context: {CONTEXT}. Answer the following question in exactly 3 short bullet points (max 6 words per point). Do not write anything else."

st.write("---")

# Ab box bilkul saaf (empty) rahega jab tak aap bolenge nahi
question = st.text_input("Interviewer ka sawaal yahan bolein:", value="")

if question:
    with st.spinner("AI is thinking..."):
        # Google's Standard API URL for Gemini 1.5 Flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
        # Plain text structural payload
        payload = {
            "contents": [{
                "parts": [{"text": f"{prompt_data}\nQuestion: {question}"}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            res_json = response.json()
            
            # Extracting text response
            output_text = res_json['candidates'][0]['content']['parts'][0]['text']
            
            st.write("---")
            st.markdown("<h3 style='color: #00FF00;'>💡 Interview Hints:</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:24px; font-weight:bold; color:white; line-height:1.8;'>{output_text}</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Sawaal clear karke dobara bolein aur enter dabayein.")
