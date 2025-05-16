import streamlit as st
import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Set your Gemini API key
GOOGLE_API_KEY = "AIzaSyBdryy1A2mZ31BRMwMUL1dj5rT7-GUsRRg"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to extract in-depth website content
def extract_website_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        # Get the website content
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary tags such as scripts, styles, etc.
        for tag in soup(["script", "style", "noscript", "iframe", "footer", "header", "nav"]):
            tag.decompose()

        # Extract all text content from the page, cleaned up
        text = soup.get_text(separator="\n", strip=True)

        # Fetch the metadata, like description, keywords, etc.
        meta_tags = soup.find_all("meta")
        meta_info = "\n".join([str(tag) for tag in meta_tags if 'name' in tag.attrs and tag.attrs['name'].lower() in ['description', 'keywords']])

        # Fetch headings (H1, H2, H3, etc.)
        headings = "\n".join([str(tag.get_text()) for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])])

        # Combine text content, metadata, and headings for rich context
        full_text = text + "\n\nMetadata:\n" + meta_info + "\n\nHeadings:\n" + headings

        # Limit the content to the first 20000 characters to keep it manageable
        return full_text[:20000]
    except Exception as e:
        return f"Error fetching website: {e}"

# Function to get a response from Gemini
def chat_about_website(url, user_question):
    content = extract_website_content(url)
    if content.startswith("Error"):
        return content  # Return the error message directly
    prompt = f"Website content:\n{content}\n\nUser question: {user_question}"
    response = model.generate_content(prompt)
    return response.text

# --- ✨ Background CSS with Adjustments ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    .stApp {
        background-color: #f0f8ff; /* Light blue background */
        color: #333333;
        font-family: 'Poppins', sans-serif;
    }

    .title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        color: #004080;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    .subtitle {
        text-align: center;
        font-size: 22px;
        color: #555555;
        margin-bottom: 40px;
    }

    .stTextInput input {
        background-color: #e0f7fa; /* Light cyan for the input */
        color: #333333;
        border: 1px solid #cccccc;
        border-radius: 5px;
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

    .stMarkdown {
        font-size: 18px;
        color: #333333;
    }

    .answer-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #cccccc;
    }
    </style>
""", unsafe_allow_html=True)

# --- 🖼️ Logo & Title ---
st.image("https://facultytub.com/wp-content/uploads/2024/01/sreyas_logo_ygezen-800x445.png", width=220)
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
        st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a question.")
