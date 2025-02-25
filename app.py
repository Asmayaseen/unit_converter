import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ API Key not found! Please check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Use Correct Model
model_name = "gemini-1.5-pro"  # 🔄 Change if needed
model = genai.GenerativeModel(model_name)

# Light/Dark Mode Toggle
st.set_page_config(page_title="Unit Converter", layout="wide")
mode = st.sidebar.radio("Select Mode", ["Light", "Dark"], index=0)

# Apply CSS for Light and Dark Mode
custom_css = f"""
    <style>
        body {{ background-color: {'#f5f5f5' if mode == 'Light' else '#181818'}; color: {'black' if mode == 'Light' else 'white'}; }}
        .stTabs [data-baseweb="tab"] {{ background-color: {'#e0e0e0' if mode == 'Light' else '#444'}; padding: 10px; border-radius: 5px; }}
        .stButton > button {{ background-color: {'#007BFF' if mode == 'Light' else '#555'}; color: white; border-radius: 5px; }}
        .stSelectbox, .stNumberInput {{ width: 100% !important; }}
        h2 {{ text-align: center; color: {'black' if mode == 'Light' else 'white'}; }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# UI Layout
st.markdown("<h2>🔢 AI-Powered Unit Converter</h2>", unsafe_allow_html=True)
tabs = st.tabs(["📏 Length", "🌡️ Temperature", "📐 Area", "🧪 Volume", "⚖️ Weight", "⏳ Time"])

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

        convert_btn = st.button("🔄 Convert", key=f"convert_{category}")

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
