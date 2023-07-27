import streamlit as st
from gTTS import gTTS 
import os
from os import path
import pydub
from pydub import AudioSegment
import shutil
import speech_recognition as sr
import pyttsx3
import vertexai
from vertexai.language_models import TextGenerationModel
from google.cloud import texttospeech

# @st.cache_data
def speech_text(text):
    language = 'en'
    speech = gTTS(text = text, lang = language, slow = False)
    speech.save("question.mp3")

    # PLACE CONTENT INTO NEW FILE => S T A R T
    shutil.move("question.mp3", "data/question1.mp3")
    # PLACE CONTENT INTO NEW FILE => E N D
    # files                                                                         
    src = "data/question1.mp3"
    dst = "data/question1.wav"

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

    return dst 

# @st.cache_data
def get_answer(input):
    vertexai.init(project="swzn-training", location="us-central1")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")


    #insert speech to text code here
    filename = '"'+input+'"'
    # initialize the recognizer
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)

    response = model.predict(
        '"""'+ text +'"""',
        **parameters
    )
    return response.text

# @st.cache_data
def text_speech(answer):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=answer)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("data/output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "data/output.mp3"')
    
    output = "data/output.mp3"

    return output

