import streamlit as st
import speech_recognition as sr
import pyttsx3
import os

from google import genai
from google.genai import types

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Voice Chatbot", page_icon="🎙️")
st.title("🎙️ E-Commerce Return & Refund Explainer Voice Chatbot")
st.write("Click the button and speak")

# -----------------------------
# INIT
# -----------------------------
recognizer = sr.Recognizer()
tts = pyttsx3.init()

# -----------------------------
# API KEY
# -----------------------------
API_KEY = "AIzaSyDNLGALtNUiKnEJHxwMYG6hNbYvpsobkGE"

client = genai.Client(api_key=API_KEY)


SYSTEM_PROMPT = "You are a helpful voice assistant. Answer clearly and briefly."

# -----------------------------
# FUNCTIONS
# -----------------------------
def speak(text):
    tts.say(text)
    tts.runAndWait()

def generate_response(user_text):
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"{SYSTEM_PROMPT}\n\nUser: {user_text}"
                )
            ],
        )
    ]

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH"
        )
    )

    response_text = ""

    for chunk in client.models.generate_content_stream(
        model="gemini-3-flash-preview",
        contents=contents,
        config=config
    ):
        if chunk.text:
            response_text += chunk.text

    return response_text.strip()

# -----------------------------
# STREAMLIT UI
# -----------------------------
if st.button("🎤 Speak"):
    with sr.Microphone() as source:
        st.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            user_text = recognizer.recognize_google(audio)
            st.success(f"You said: {user_text}")

            bot_reply = generate_response(user_text)

            st.markdown("### 🤖 Bot Response")
            st.write(bot_reply)

            speak(bot_reply)

        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.error("Speech recognition service error.")
        except Exception as e:
            st.error(f"Error: {e}")
