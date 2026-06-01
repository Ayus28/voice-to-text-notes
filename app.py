import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.markdown("<style>body {background-color: #111; color: white;}</style>", unsafe_allow_html=True)

st.title("💡 Live Interview Hints")
st.subheader("Camera ke neeche phone rakh kar points dekhein")

# Gemini Setup - Directly using standard configuration mapping
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Using 'gemini-1.5-flash' explicitly for correct endpoints
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key missing in Settings.")

CONTEXT = """
Role: Python Developer
Skills: Django, FastAPI, PostgreSQL, AWS, Git
Projects: E-commerce Backend API, Student Management System
"""

SYSTEM_PROMPT = f"""
You are an interview assistant. Provide ONLY 3 short bullet points (max 6 words per point) answering the question based on the candidate's context.
Do not include any introductory text, titles, or formatting other than 3 clean bullet points.
Context:
{CONTEXT}
"""

st.write("---")

# Standard text input box
question = st.text_input("Interviewer ka sawaal yahan bolein:")

if question:
    with st.spinner("AI is thinking..."):
        try:
            # Explicit call for dynamic generation
            response = model.generate_content(f"{SYSTEM_PROMPT}\nQuestion: {question}")
            
            st.write("---")
            st.markdown("<h3 style='color: #00FF00;'>💡 Interview Hints:</h3>", unsafe_allow_html=True)
            
            # Formatting points nicely in big text
            st.markdown(f"<div style='font-size:24px; font-weight:bold; color:white; line-height:1.8;'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error processing text request: {e}")
