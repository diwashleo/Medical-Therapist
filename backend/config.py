import os
from dotenv import load_dotenv
load_dotenv()

# Get all required API keys and configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER')
EMERGENCY_CONTACT = os.getenv('EMERGENCY_CONTACT')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
