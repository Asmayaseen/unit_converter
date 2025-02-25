import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("API Key not found! Please check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Select model
model = genai.GenerativeModel("gemini-pro")

# UI Design
st.set_page_config(page_title="AI-Powered Unit Converter", page_icon="🔢", layout="centered")

# Light/Dark Mode Toggle
mode = st.sidebar.radio("Select Mode:", ["Light", "Dark"])
if mode == "Dark":
    st.markdown("""
        <style>
            body {
                background-color: #2E2E2E;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

st.title("🔢 AI-Powered Unit Converter")
st.write("Convert different units using Google Gemini AI!")

# User Inputs
from_unit = st.selectbox("From Unit:", ["kg", "m", "miles", "cm", "feet", "liters", "grams", "Fahrenheit", "Celsius"])
to_unit = st.selectbox("To Unit:", ["lbs", "km", "feet", "inches", "gallons", "ounces", "Kelvin"])
value = st.number_input("Enter the value to convert:", min_value=0.0, format="%.2f")

if st.button("Convert"):
    if not from_unit or not to_unit:
        st.warning("Please select both units!")
    else:
        prompt = f"Convert {value} {from_unit} to {to_unit}."
        
        # Corrected method
        response = model.generate_content(prompt)
        
        if response and response.text:
            st.success(f"Converted Value: {response.text}")
        else:
            st.error("Error: Could not generate response. Please try again.")

# Run App Command
# streamlit run app.py
