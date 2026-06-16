from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from translator import translate
from speech import transcribe, text_to_speech
from models import TranslateRequest, TranslateResponse, TranscribeResponse, PipelineResponse,SynthesizeRequest
import io,os
import numpy as np
import soundfile as sf

app=FastAPI(title='IndcBridge API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def home():
    return {"status": "API running"}

@app.post("/translate",response_model=TranslateResponse)
async def translate_text(request:TranslateRequest):
    try:
        result=translate(
            request.text,
            request.source_lang,
            request.target_lang
        )
        return TranslateResponse(
            translated_text=result,
            source_lang=request.source_lang,
            target_lang=request.target_lang        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe",response_model=TranscribeResponse)

async def transcribe_audio(file:UploadFile=File(...)):

    try:
        contents=await file.read()
        buffer=io.BytesIO(contents)
        audio,sample_rate=sf.read(buffer)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        audio=audio.astype(np.float32)
        text=transcribe(audio,sample_rate)
        return TranscribeResponse(transcribed_text=text)

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@app.post("/speak")
async def speak(request: TranslateRequest):
    try:
        translated = translate(
            request.text,
            request.source_lang,
            request.target_lang
        )
        audio_path = text_to_speech(translated, request.target_lang)

        return FileResponse(
            audio_path,
            media_type="audio/wav",
            filename="output.wav"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pipeline", response_model=PipelineResponse)
async def full_pipeline(
    source_lang: str,
    target_lang: str,
    file: UploadFile = File(...)
):
    try:
        contents = await file.read()
        buffer = io.BytesIO(contents)
        audio, sample_rate = sf.read(buffer)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        audio = audio.astype(np.float32)

        transcribed = transcribe(audio, sample_rate)
        print(f"TRANSCRIBED: '{transcribed}'")

        translated = translate(transcribed, source_lang, target_lang)
        print(f"TRANSLATED: '{translated}'")

        audio_path = text_to_speech(translated, target_lang)
        print(f"AUDIO PATH: {audio_path}")

        return PipelineResponse(
            transcribed_text=transcribed,
            translated_text=translated,
            audio_path=audio_path
        )
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesize")
async def synthesize(request: SynthesizeRequest):
    try:
        audio_path = text_to_speech(request.text, request.target_lang)
        return FileResponse(
            audio_path,
            media_type="audio/wav",
            filename="output.wav"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))