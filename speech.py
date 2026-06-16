import sounddevice as sd
import soundfile as sf
import io
import os
from gtts import gTTS
import tempfile
from groq import Groq
from dotenv import load_dotenv
from sarvamai import SarvamAI
import base64


load_dotenv()

sarvam_client=SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SARVAM_LANG_CODES = {
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN"
}

def record_audio(duration=5, sample_rate=16000):
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        device=1
    )
    sd.wait()
    print("Recording complete.")
    return audio.flatten()

def transcribe(audio, sample_rate=16000):
    print("Transcribing...")
    buffer = io.BytesIO()
    sf.write(buffer, audio, sample_rate, format="wav")
    buffer.seek(0)
    buffer.name = "audio.wav"
    result = groq_client.audio.transcriptions.create(
        file=buffer,
        model="whisper-large-v3",
        response_format="text"
    )
    return result.strip()


def text_to_speech(text, target_lang):
    print(f"Generating {target_lang} audio...")
    lang_code = SARVAM_LANG_CODES[target_lang]
    response = sarvam_client.text_to_speech.convert(
        text=text,
        target_language_code=lang_code,
        speaker="anushka",
        model="bulbul:v2"
    )
    audio_bytes = base64.b64decode(response.audios[0])
    tmp = tempfile.mktemp(suffix=".wav")
    with open(tmp, "wb") as f:
        f.write(audio_bytes)
    return tmp