import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def translate(text, source_lang, target_lang):
    prompt = f"""
    You are an expert translator specializing in Indian languages.
    
    Source language: {source_lang}
    Target language: {target_lang}
    Input text: {text}
    
    Instructions:
    - Input may be code-mixed with English (Tanglish, Hinglish etc.)
    - Understand code-mixed input naturally
    - Translate accurately preserving meaning and tone
    - Output ONLY in {target_lang} native script
    - STRICTLY Do not include transliteration, explanation, or any other text
    """
    response = model.generate_content(prompt)
    return response.text.strip()