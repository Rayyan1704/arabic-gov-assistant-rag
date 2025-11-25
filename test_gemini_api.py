"""Test Gemini API"""
import os
from google import generativeai as genai
from dotenv import load_dotenv

print("=" * 60)
print("🧪 Testing Gemini API")
print("=" * 60)

# Load API key
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

print(f"✅ API key found: {api_key[:10]}...")

# Configure Gemini
genai.configure(api_key=api_key)

# Test with Arabic
print("\n📝 Testing with Arabic query...")
model = genai.GenerativeModel('gemini-2.0-flash')

response = model.generate_content("اشرح لي ما هو الذكاء الاصطناعي في جملتين")

print("\n📄 Response:")
print("=" * 60)
print(response.text)
print("=" * 60)

print("\n✅ Gemini API test successful!")
print("✅ Arabic output works perfectly!")
