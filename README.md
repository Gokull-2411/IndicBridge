# IndicBridge 🌉

IndicBridge accepts audio as well as text as input aud transcribes audio data into text using the **Groq Whisper API** translates text 
between Indian languages using **Google Gemini Flash** and converts the translated text into natural-sounding speech using **Sarvam AI Text-to-Speech**. 
Works well also with code-mixed languages (Tanglish,Hinglish,Manglish,etc). 
Langages Supported: Hindi,Tamil,Malayalam,Kannada,Telegu and their code-mixed counterparts.
---


## Architecture

Voice/Text Input
↓
Groq Whisper Large v3 (Speech Recognition)
↓
Gemini 2.5 Flash (Translation + Code-mixed handling)
↓
Sarvam AI bulbul:v2 (Text to Speech)
↓
FastAPI Backend + Streamlit Frontend

## Features
- Bidirectional translation across 5 Indic languages
- Voice input with automatic silence detection
- Code-mixed input support (Tanglish, Hinglish, Tenglish, Kanglish, Manglish)
- Live chunked transcription — updates every 3 seconds while speaking
- Auto-play translated audio output
- Text mode for direct typed input

---

## How It Works

User Input  
↓  
Gemini Flash Translation  
↓  
Translated Text  
↓  
Sarvam AI Text-to-Speech  
↓  
Audio Output

---

## Tech Stack
| Component | Tool |
|---|---|
| Speech Recognition | Groq Whisper Large v3 |
| Translation | Gemini 2.5 Flash |
| Text to Speech | Sarvam AI bulbul:v2 |
| Backend | FastAPI |
| Frontend | Streamlit |

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Gokull-2411/IndicBridge.git
cd IndicBridge
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file:
GEMINI_API_KEY=your_gemini_key

GROQ_API_KEY=your_groq_key

SARVAM_API_KEY=your_sarvam_key

### 5. Run the backend
```bash
uvicorn app:app --reload
```

### 6. Run the frontend
```bash
streamlit run frontend.py
```

Open `http://localhost:8501` in your browser.

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| POST | /translate | Text translation |
| POST | /transcribe | Speech to text |
| POST | /speak | Translate + generate audio |
| POST | /synthesize | Text to speech only |
| POST | /pipeline | Full voice to voice |


## Future Enhancements
- True real-time streaming with Deepgram WebSocket API
- GPU deployment for lower latency
- Mobile-friendly UI
- Fine-tuned translation for domain-specific terminology

## Author
Gokul S — [LinkedIn](https://www.linkedin.com/in/gokul-sathyan24) | [GitHub](https://github.com/Gokull-2411)
