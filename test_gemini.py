"""
Test Gemini API connection
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    print("\nPlease:")
    print("1. Get your API key from: https://makersuite.google.com/app/apikey")
    print("2. Create a .env file with: GEMINI_API_KEY=your_key_here")
    exit(1)

# Configure Gemini
genai.configure(api_key=api_key)

# Test API
print("Testing Gemini API...")
print("="*80)

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("اشرح لي ما هو الذكاء الاصطناعي")

print("\nQuery: اشرح لي ما هو الذكاء الاصطناعي")
print("\nResponse:")
print(response.text)
print("\n" + "="*80)
print("✅ Gemini API working correctly!")
