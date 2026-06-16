import streamlit as st
import requests
import sounddevice as sd
import soundfile as sf
import numpy as np
import io
import os

API_URL = "http://127.0.0.1:8000"

LANGUAGES = ["Hindi", "Tamil", "Telugu", "Kannada", "Malayalam"]

CODE_MIXED = {
    "Hindi": "Hinglish",
    "Tamil": "Tanglish",
    "Telugu": "Tenglish",
    "Kannada": "Kanglish",
    "Malayalam": "Manglish"
}

st.set_page_config(
    page_title="IndicBridge",
    page_icon="🌉",
    layout="centered"
)

st.title("🌉 IndicBridge")
st.caption("Bidirectional Indic Language Translation")

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Source Language", LANGUAGES)

with col2:
    target_lang = st.selectbox(
        "Target Language",
        [lang for lang in LANGUAGES if lang != source_lang]
    )

is_code_mixed = st.toggle(f"Input is {CODE_MIXED[source_lang]} (code-mixed)")

input_mode = st.radio("Input Mode", ["Text", "Voice"], horizontal=True)

if input_mode == "Text":
    placeholder = (
        f"Type in {CODE_MIXED[source_lang]}..."
        if is_code_mixed
        else f"Type in {source_lang}..."
    )
    input_text = st.text_area("Enter text", placeholder=placeholder, height=120)

    if st.button("Translate", type="primary"):
        if input_text.strip():
            with st.spinner("Translating..."):
                source = (
                    f"{CODE_MIXED[source_lang]} (code-mixed {source_lang} and English)"
                    if is_code_mixed
                    else source_lang
                )

                response = requests.post(
                    f"{API_URL}/translate",
                    json={
                        "text": input_text,
                        "source_lang": source,
                        "target_lang": target_lang
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    st.subheader("Translation")
                    st.write(result["translated_text"])
                else:
                    st.error(f"Error: {response.text}")
        else:
            st.warning("Please enter some text")

else:  # Voice mode
    st.subheader("🎙️ Live Voice Translation")
    st.caption("Speak naturally — stops automatically when you pause")

    if "live_transcript" not in st.session_state:
        st.session_state.live_transcript = ""
        st.session_state.live_translation = ""

    transcript_box = st.empty()
    translation_box = st.empty()

    transcript_box.markdown(f"**You said:** {st.session_state.live_transcript}")
    translation_box.markdown(f"**Translation:** {st.session_state.live_translation}")

    chunk_duration = 3
    SILENCE_THRESHOLD = 0.01
    MAX_SILENT_CHUNKS = 2
    max_chunks = 20  # safety limit — 60 sec max

    if st.button("🎤 Start Listening", type="primary"):
        st.session_state.live_transcript = ""
        st.session_state.live_translation = ""

        source = (
            f"{CODE_MIXED[source_lang]} (code-mixed {source_lang} and English)"
            if is_code_mixed
            else source_lang
        )

        has_spoken = False
        silent_count = 0

        for i in range(max_chunks):
            audio = sd.rec(
                int(chunk_duration * 16000),
                samplerate=16000,
                channels=1,
                dtype="float32",
                device=1
            )
            sd.wait()

            rms = np.sqrt(np.mean(audio**2))

            if rms < SILENCE_THRESHOLD:
                if has_spoken:
                    silent_count += 1
                    if silent_count >= MAX_SILENT_CHUNKS:
                        break
                continue
            else:
                has_spoken = True
                silent_count = 0

            buffer = io.BytesIO()
            sf.write(buffer, audio, 16000, format="WAV")
            buffer.seek(0)

            resp = requests.post(
                f"{API_URL}/transcribe",
                files={"file": ("chunk.wav", buffer, "audio/wav")}
            )

            if resp.status_code == 200:
                chunk_text = resp.json()["transcribed_text"]

                if chunk_text.strip():
                    st.session_state.live_transcript += " " + chunk_text

                    trans_resp = requests.post(
                        f"{API_URL}/translate",
                        json={
                            "text": chunk_text,
                            "source_lang": source,
                            "target_lang": target_lang
                        }
                    )

                    if trans_resp.status_code == 200:
                        chunk_translation = trans_resp.json()["translated_text"]
                        st.session_state.live_translation += " " + chunk_translation

            transcript_box.markdown(f"**You said:** {st.session_state.live_transcript}")
            translation_box.markdown(f"**Translation:** {st.session_state.live_translation}")

        if st.session_state.live_translation.strip():
            with st.spinner("Generating audio..."):
                audio_resp = requests.post(
                    f"{API_URL}/synthesize",
                    json={
                        "text": st.session_state.live_translation,
                        "target_lang": target_lang
                    }
                )
                if audio_resp.status_code == 200:
                    st.audio(audio_resp.content, format="audio/wav", autoplay=True)
                else:
                    st.error(f"Error: {audio_resp.text}")