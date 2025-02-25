import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key from .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
