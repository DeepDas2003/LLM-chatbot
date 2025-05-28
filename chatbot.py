import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
import google.generativeai as genai
import streamlit as st
import playsound
from gtts import gTTS
genai.configure(api_key="AIzaSyAxy-nYnK0sEsV1getpbNW72gLAZqBPX3s")
from langchain.prompts import PromptTemplate
st.title("Gemini AI Guide")
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")
st.title("💬 Gemini AI Guide")
import speech_recognition as sr
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")

def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Speech service is down."
if st.button("🎤 Speak"):
    user_input = voice_to_text()
else:
    user_input = st.chat_input("Ask anything about travel, career, etc...")

if user_input:   
    prompt = (
        "Please explain in detail. "
        "If the user is asking about travel, guide them about hotels, tourist places, routes, etc. "
        "If it's about career, explain what to study, how to proceed, and so on. "
        f"Now answer in detail for: {user_input}"
    )

    st.session_state.chat_history.append(("user", user_input))
    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
        st.session_state.chat_history.append(("bot", reply))
        if st.button("🔊 Play Gemini's voice"):
           speak_text(reply)
    except Exception as e:
        st.session_state.chat_history.append(("bot", f"Error: {e}"))
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)
