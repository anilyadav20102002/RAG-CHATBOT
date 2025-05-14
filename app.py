import streamlit as st
import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Set your Gemini API key
GOOGLE_API_KEY = "AIzaSyBdryy1A2mZ31BRMwMUL1dj5rT7-GUsRRg"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to extract website content
def extract_website_content(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "iframe"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:15000]
    except Exception as e:
        return f"Error fetching website: {e}"

# Function to get response from Gemini
def chat_about_website(url, user_question):
    content = extract_website_content(url)
    prompt = f"Website content:\n{content}\n\nUser question: {user_question}"
    response = model.generate_content(prompt)
    return response.text

# --- ✨ White Background CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    .stApp {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Poppins', sans-serif;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #004080;
        margin-bottom: 20px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #444444;
        margin-bottom: 30px;
    }

    .stTextInput input {
        background-color: #f2f2f2;
        color: #333333;
        border: 1px solid #cccccc;
    }

    .stButton button {
        background-color: #004080;
        color: white;
        font-weight: bold;
        border-radius: 25px;
        padding: 0.5em 2em;
        transition: 0.3s ease;
    }

    .stButton button:hover {
        background-color: #003366;
        box-shadow: 0 0 10px rgba(0, 64, 128, 0.3);
    }

    .stSpinner {
        color: #004080;
    }
    </style>
""", unsafe_allow_html=True)

# --- 🖼️ Logo & Title ---
st.image("sreyas_logo.png", width=220)  # Replace with actual logo if available
st.markdown("<div class='title'>Sreyas College AI Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>🤖 Ask anything about the Sreyas Institute of Engineering & Technology website</div>", unsafe_allow_html=True)

# --- 🗨️ Chat Interface ---
url = "https://sreyas.ac.in/"
question = st.text_input("🔍 Enter your question here:")

if st.button("Ask the AI"):
    if question:
        with st.spinner("Thinking... 💭"):
            answer = chat_about_website(url, question)
        st.success("Here’s what I found:")
        st.markdown(f"<div style='background:#f9f9f9;padding:15px;border-radius:10px;border:1px solid #e0e0e0;'>{answer}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a question.")
