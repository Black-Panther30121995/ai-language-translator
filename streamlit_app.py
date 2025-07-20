import streamlit as st
from transformers import pipeline
from langdetect import detect
from gtts import gTTS
import tempfile

st.set_page_config(page_title="AI Multi-Language Translator", layout="centered")
st.title("🌐 AI-Powered Multi-Language Translator with Voice Output 🔊")

model_map = {
    "French": "Helsinki-NLP/opus-mt-en-fr",
    "German": "Helsinki-NLP/opus-mt-en-de",
    "Spanish": "Helsinki-NLP/opus-mt-en-es",
    "Hindi": "Helsinki-NLP/opus-mt-en-hi"
}

language_code_map = {
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Hindi": "hi"
}

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

st.write("Detect, Translate and Listen! 🎧")

input_text = st.text_area("Enter your text:")
target_language = st.selectbox("Select Target Language", list(model_map.keys()))

if st.button("Translate and Speak"):
    if input_text.strip():
        source_lang = detect_language(input_text)
        st.info(f"Detected Language: {source_lang}")

        model_name = model_map[target_language]
        translator = pipeline("translation", model=model_name)

        translated_text = translator(input_text)[0]['translation_text']
        st.success(f"Translated to {target_language}: {translated_text}")

        tgt_lang_code = language_code_map[target_language]
        audio_file = text_to_speech(translated_text, tgt_lang_code)
        audio_bytes = open(audio_file, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("Please enter some text first.")
