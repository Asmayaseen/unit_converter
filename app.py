import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("\U0000274C API Key not found! Please check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Model
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    st.error(f"\U0000274C Failed to initialize model: {e}")
    st.stop()

# Set Page Config
st.set_page_config(page_title="Unit Converter", layout="wide")

# Sidebar Light/Dark Mode Selection
mode = st.sidebar.radio("\U0001F319 Select Mode", ["Light", "Dark"], index=0)

# Dynamic Theme Colors
theme = {
    "Light": {"bg": "#f5f5f5", "text": "#000000", "button": "#007BFF", "tab": "#e0e0e0"},
    "Dark": {"bg": "#181818", "text": "#FFFFFF", "button": "#555555", "tab": "#444444"}
}

theme_colors = theme[mode]

# Apply Custom CSS
st.markdown(f"""
    <style>
        .stApp {{ background-color: {theme_colors['bg']}; color: {theme_colors['text']}; }}
        .stTabs [data-baseweb="tab"] {{ background-color: {theme_colors['tab']}; padding: 10px; border-radius: 5px; }}
        .stButton > button {{ background-color: {theme_colors['button']}; color: white; border-radius: 5px; }}
        h2, h3, h4, h5, h6, p, label, span {{ color: {theme_colors['text']} !important; }}
    </style>
""", unsafe_allow_html=True)

# UI Layout
st.markdown(f"""<h2 style='color: {theme_colors['text']}; text-align: center;'>
    \U0001F522 AI-Powered Unit Converter</h2>""", unsafe_allow_html=True)

tabs = st.tabs(["\U0001F4CF Length", "\U0001F321️ Temperature", "\U0001F4C8 Area", "\U0001F9EA Volume", "⚖️ Weight", "⏳ Time"])

# Units Mapping
unit_categories = {
    "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Area": ["Square Meter", "Hectare", "Acre", "Square Foot"],
    "Volume": ["Liter", "Milliliter", "Gallon", "Cubic Meter"],
    "Weight": ["Kilogram", "Gram", "Pound", "Ounce"],
    "Time": ["Second", "Minute", "Hour", "Day"]
}

# Conversion Logic
for i, category in enumerate(unit_categories.keys()):
    with tabs[i]:
        st.subheader(f"{category} Converter")
        
        col1, col2 = st.columns(2)
        with col1:
            from_unit = st.selectbox("From:", unit_categories[category], key=f"from_{category}")
        with col2:
            to_unit = st.selectbox("To:", unit_categories[category], key=f"to_{category}")
        
        value = st.number_input("Enter value:", min_value=0.0, format="%.2f", key=f"value_{category}")
        convert_btn = st.button("\U0001F504 Convert", key=f"convert_{category}")

        if convert_btn:
            if not from_unit or not to_unit:
                st.warning("⚠️ Please select both units!")
            else:
                prompt = f"Convert {value} {from_unit} to {to_unit}."
                try:
                    response = model.generate_content(prompt)
                    if response and response.text:
                        st.success(f"✅ Converted Value: {response.text}")
                    else:
                        st.error("❌ Error: Could not generate response. Please try again.")
                except Exception as e:
                    st.error(f"❌ API Error: {e}")
