from gtts import gTTS
import os

def generate_audio(scene_text, scene_number):
    filename = f"static/audio/scene{scene_number}.mp3"
    tts = gTTS(text=scene_text, lang='en')
    tts.save(filename)
    return filename
