from pydantic import BaseModel

class TranslateRequest(BaseModel):
    text: str
    source_lang : str
    target_lang : str

class TranslateResponse(BaseModel):
    translated_text : str
    source_lang : str
    target_lang : str

class TranscribeResponse(BaseModel):
    transcribed_text : str

class PipelineRequest(BaseModel):
    source_lang : str
    target_lang : str

class PipelineResponse(BaseModel):

    transcribed_text:str
    translated_text:str
    audio_path:str

class SpeakRequest(BaseModel):
    text: str
    target_lang: str

class SpeakResponse(BaseModel):
    audio_path: str

class SynthesizeRequest(BaseModel):
    text: str
    target_lang: str