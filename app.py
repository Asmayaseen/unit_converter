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

# ✅ Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Use Correct Model (Fix Applied)
try:
    model_name = "gemini-1.5-pro"  # 🔄 Change if needed
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"❌ Failed to initialize model: {e}")
    st.stop()

# ✅ Set Page Config
st.set_page_config(page_title="Unit Converter", layout="wide")

# ✅ Sidebar Mode Selection
mode = st.sidebar.radio("🌗 Select Mode", ["Light", "Dark"], index=0)

# ✅ Dynamic CSS for Light/Dark Mode
if mode == "Light":
    background_color = "#f5f5f5"
    text_color = "#000000"
    button_color = "#007BFF"
    tab_color = "#e0e0e0"
else:
    background_color = "#181818"
    text_color = "#FFFFFF"
    button_color = "#555555"
    tab_color = "#444444"

custom_css = f"""
    <style>
        body, .stApp {{ background-color: {background_color}; color: {text_color}; }}
        .stTabs [data-baseweb="tab"] {{ background-color: {tab_color}; padding: 10px; border-radius: 5px; }}
        .stButton > button {{ background-color: {button_color}; color: white; border-radius: 5px; }}
        .stSelectbox, .stNumberInput, .stTextInput, .stTextArea, .stFileUploader {{ color: {text_color}; background-color: {background_color}; border: 1px solid {tab_color}; }}
        h2, h3, h4, h5, h6, p, label, span {{ color: {text_color} !important; }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ✅ UI Layout
st.markdown(f"<h2 style='color: {text_color}; text-align: center;'>🔢 AI-Powered Unit Converter</h2>", unsafe_allow_html=True)
tabs = st.tabs(["📏 Length", "🌡️ Temperature", "📐 Area", "🧪 Volume", "⚖️ Weight", "⏳ Time"])

# ✅ Units Mapping
unit_categories = {
    "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Area": ["Square Meter", "Hectare", "Acre", "Square Foot"],
    "Volume": ["Liter", "Milliliter", "Gallon", "Cubic Meter"],
    "Weight": ["Kilogram", "Gram", "Pound", "Ounce"],
    "Time": ["Second", "Minute", "Hour", "Day"]
}

# ✅ Conversion Logic
for i, category in enumerate(unit_categories.keys()):
    with tabs[i]:
        st.subheader(f"{category} Converter", divider="rainbow")

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
