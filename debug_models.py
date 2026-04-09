import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"DEBUG: API Key present: {bool(api_key)}")

if api_key:
    genai.configure(api_key=api_key)
    
    # Try listing models
    print("DEBUG: Listing models...")
    try:
        models = genai.list_models()
        for m in models:
            print(f"MODEL: {m.name} | METHODS: {m.supported_generation_methods}")
    except Exception as e:
        print(f"ERROR listing: {e}")

    # Try specific names
    candidates = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro', 'gemini-1.0-pro', 'models/gemini-1.5-flash']
    for m_name in candidates:
        print(f"\nDEBUG: Testing {m_name}...")
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content('hi')
            print(f"SUCCESS: {m_name} responded with: {response.text}")
            break
        except Exception as e:
            print(f"FAIL: {m_name} error: {e}")
else:
    print("CRITICAL: GEMINI_API_KEY not found in .env")
