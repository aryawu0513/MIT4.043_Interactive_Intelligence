import os
import io
import sys
import argparse
import pyaudio
import wave
from google.cloud import speech
from google.cloud import texttospeech
import ast

import os
from pathlib import Path
from openai import OpenAI

import openai
import time
from pydub import AudioSegment

# Set your OpenAI API key here
api_key = ""
# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

import pygame

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def speech_to_text(speech_file):
    audio_file= open(speech_file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    print(transcription.text)

    return transcription.text


def text_to_speech(tts):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    #output.mp3
    # with open("result.wav", "wb") as out:
    #     # Write the response to the output file.
    #     out.write(response.audio_content)
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=tts
    )
    response.stream_to_file(speech_file_path)
    return


def record_wav():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 4096
    record_secs = 10      
    # dev_index = 1
    wav_output_filename = 'input.wav'

    audio = pyaudio.PyAudio()

    # Create pyaudio stream.
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = None,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []

    # Loop through stream and append audio chunks to frame array.
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # Stop the stream, close it, and terminate the pyaudio instantiation.
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio frames as .wav file.
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    return

import torchaudio
from audiocraft.models import MusicGen

from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=8) 

from audiocraft.models import AudioGen

model_audio = AudioGen.get_pretrained('facebook/audiogen-medium')
model_audio.set_generation_params(duration=7)


def chatbot():
    # Define the initial prompt
    prompt = """
        You are an assistant who will guide me through the process of reflecting on my day. 
        Start by asking me: "Do you want to share your day?"

        You can prompt me then a total of two questions, choosing one from the following each time:
        1. "Were there any times today when you felt calm, relaxed, or at peace?";
        2. "Did you have any moments of fear or anxiety today? What were you afraid of?";
        3. "Were there any moments today when you felt completely present and engaged in the moment?";
        4. "What time today were you the most happy?";
        5. "Were there any times today when you felt angry and acted out of character?";
        6. "Were there any times today where you made decisions that you now regret?";
        7. "When did the most meaningful interaction with others happen today, and what happened?";
        
        At the end, say Goodnight and exit.
    """

        # Start the conversation
    print("Starting conversation...")

    messages = [{"role": "system", "content": prompt}]

    while True:
        # Get user input
        #user_input = input("You: ")
        # Get WAV from microphone.
        record_wav()
        # Convert audio into text.
        user_input = speech_to_text("input.wav")
        
        # Check if the user wants to exit the chat
        if user_input.lower() == "exit":
            print("Exiting chat...")
            break  # Exit the loop to end the conversation

        # Update the conversation history with the user's message
        messages.append({"role": "user", "content": user_input})

        try:
            # Get GPT's response
            response = client.chat.completions.create(
                messages=messages,
                model="gpt-4",
            )

            # Extract the GPT response and print it
            gpt_response = response.choices[0].message.content
            print(f"Bot: {gpt_response}")

            # Update the conversation history with GPT's response
            messages.append({"role": "assistant", "content": gpt_response})

            # Convert ChatGPT response into audio.
            text_to_speech(gpt_response)

            # Play audio of reponse.
            play_audio("speech.mp3")
             # Wait for the audio to finish playing before starting recording
            while pygame.mixer.music.get_busy():
                # pygame.time.delay(100)
                pygame.time.Clock().tick(1)

            if "Goodnight" in gpt_response:
                # start_index = gpt_response.find("The recommended music genre is")
                # music_genre = gpt_response[start_index + len("The recommended music genre is "):].strip(".")
                # print(music_genre)
                print("Exiting chat...")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
    print("chathistory:", messages)
    return messages

def analyze(chathistory):
    prompt="""

        You are an assistant who will receive a chat history between me and a chatbot about my reflection of my day. 
        The chatbot would have asked two questions, and for each question, please analyze the user's answer to the question and map it to a tuple of an emotion and a time. For example, if the question is about anxiety and I said I was a little anxious in the late afternoon, map it to {emotion: anxiety, time: 17:00}. 
        Also identify a element that makes ambient sounds, think of objects that might appear in the setting i was in from my answer, for example tree leaves or racing heartbeats. 
        Also, store a music genre that fits my description of the event that happened at that time. Some examples of music genre prompts are '80s pop track with bassy drums and synth' or 'Bluesy guitar instrumental with soulful licks and a driving rhythm section'. 
        For each of my answers to one of the chatbot's questions, store a dictionary of time, emotion, ambiend sound, and genre prompt. For example: {emotion: anxiety, time: 17:00, ambient:'raining sound', prompt: 'Relaxing jazz track with raining sounds and a gentle rhythm section'}.
        Return me a list of dictionaries, one for each question and answer.

        For each dictionary, also parse the emotion field into a value between 1-10, and parse the time field into a numeric value also from 1-10.
        For emotion value, 10 is the most positive, and 1 is the most negative.
        Some examples of the scoring of emotions: happy = 10, fulfillment/connectedness = 9, present/engaged = 8, relief/comfort=7, calm = 6, bored = 5, anxiety = 4, fear = 3, sad,Regretful = 2, anger = 1, 
        Also come up with a color that reflects the emotion, give back to me in rgb tuple format.

        For time value, now is always the latest time at night and has the value = 10, morning = 1, noon = 4, afternoon = 6, evening = 8, if one event says an hour ago, then it is 9

        
        The format of your response should be exactly like this, with no extra words of your own!!:
        [{'emotion':'', 'emotion_value':1-10, 'emotion_rgb':(r-value,g-value,b-value), 'time': '', 'time_value': 1-10 , 'ambient':'', 'prompt':''},{'emotion':'', 'emotion_value':1-10, 'emotion_rgb':(r-value,g-value,b-value), 'time': '', 'time_value': 1-10 , 'ambient':'', 'prompt':''},...]
        Any extra word other than this list of dictionaries is not allowed and you will be penalized
        
    """
    print("Starting analysis...")

    messages = [{"role": "system", "content": prompt}]
    for qa in chathistory:
        messages.append(qa)

    response = client.chat.completions.create(
                messages=messages,
                model="gpt-4",
            )

            # Extract the GPT response and print it
    gpt_response = response.choices[0].message.content
    
    return gpt_response

def generateMusic(i,moment):
    description = [moment['prompt']]
    print("generating music ", description, " for ",i)
    
    # melody, sr = torchaudio.load('sample2.wav')
    melody, sr = torchaudio.load('samplehuman.wav')
    # generates using the melody from the given audio and the provided descriptions.
    wav = model.generate_with_chroma(description, melody[None], sr)

    audio_write(f'music_{i}', wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    return


def overlayAmbient(i,moment):
    description = [moment['ambient']]
    print("overlaying ambient ", description, " for ",i)
    
    output = model_audio.generate(
        description,
        progress=True
    )
    audio_write(f'ambient_{i}', output[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    print("generated ambient saved for ",i)
    # Overlay the ambient sound with the generated music
    
    audio1 = AudioSegment.from_file(f'music_{i}.wav')
    audio2 = AudioSegment.from_file(f'ambient_{i}.wav')
    audio2 = audio2.apply_gain(-20)

    # Overlay audio2 on top of audio1, starting at the beginning of audio1
    overlayed = audio1.overlay(audio2,loop=True)

    # Export the overlayed audio
    overlayed.export(f"music_overlay_{i}.wav", format="wav")

    return

def concatePieces(num):
    print("concating ", num, " pieces.")
    all_music_segments=[]
    for i in range(num):
        all_music_segments.append(AudioSegment.from_file(f"music_overlay_{i}.wav"))
    
    combined_audio = sum(all_music_segments, AudioSegment.empty())

    # Export the combined audio to a new file
    combined_audio.export("combined.wav", format="wav")

    return

def plot_emotion_vs_time(data):
    # Sort data by time
    sorted_data = sorted(data, key=lambda x: x['time_value'])
    
    # Calculate the x and y coordinates for each point
    x_coords = [int(d['time_value'] * 12.8) for d in sorted_data]
    y_coords = [int(d['emotion_value'] * 6.4) for d in sorted_data]
    
    # Create a list of strings representing drawLine parameters
    segments = []
    for i in range(len(sorted_data) - 1):
        x1, y1 = x_coords[i], y_coords[i]
        x2, y2 = x_coords[i + 1], y_coords[i + 1]
        segment = (x1,y1,x2,y2)
        segments.append(segment)
    
    return segments


if __name__ == "__main__":
    chathistory = chatbot()
    print("HERE CHATS",chathistory)
    #chathistory = [{'role': 'system', 'content': '\n        You are an assistant who will guide me through the process of reflecting on my day. \n        Start by asking me: "Do you want to share your day?"\n\n        You can prompt me then a total of two questions, choosing one from the following each time:\n        1. "Were there any times today when you felt calm, relaxed, or at peace?";\n        2. "Did you have any moments of fear or anxiety today? What were you afraid of?";\n        3. "Were there any moments today when you felt completely present and engaged in the moment?";\n        4. "What time today were you the most happy?";\n        5. "Were there any times today when you felt angry and acted out of character?";\n        6. "Were there any times today where you made decisions that you now regret?";\n        7. "When did the most meaningful interaction with others happen today, and what happened?";\n        \n        At the end, say Goodnight and exit.\n    '}, {'role': 'user', 'content': 'yes I want to share I want to share my day'}, {'role': 'assistant', 'content': 'That\'s great! First, let\'s start by asking: "Were there any times today when you felt calm, relaxed, or at peace?"'}, {'role': 'user', 'content': "yes I think currently I'm feeling very relaxed and I'm hearing the winds that's blowing outside"}, {'role': 'assistant', 'content': 'I\'m glad to hear that you\'re feeling relaxed now. Listening to the wind can indeed be calming. For the next question: "When did the most meaningful interaction with others happen today, and what happened?"'}, {'role': 'user', 'content': 'It happened about an hour ago when I was telling my roommate about swim competitions in general. It was exciting.'}, {'role': 'assistant', 'content': "That sounds like a wonderful conversation. It's fantastic when we can share our passions with others. Thank you for sharing your day with me. Goodnight!"}]
    moments = analyze(chathistory)
    print("Moments",moments)
    moments_list = ast.literal_eval(moments)
    moments_list.sort(key=lambda x: x['time_value'])
    print("Moments",moments_list)
    # moments_list =[{'emotion': 'calm', 'time': 'now', 'ambient': 'raining sound', 'prompt': 'Relaxing jazz track with smooth saxophone and a gentle rhythm section'}, {'emotion': 'excitement', 'time': 'an hour ago', 'ambient':'remote voices chatting and laughter', 'prompt':'Energetic pop track with upbeat drums and engaging vocals'}]
    for i, moment in enumerate(moments_list):
        generateMusic(i,moment)
        overlayAmbient(i,moment)
        
    # generateMusic(1,{'emotion': 'calm', 'time': 'currently', 'ambient': 'winds blowing outside', 'prompt': 'Soft instrumental track with calming wind sounds'})
    concatePieces(len(moments_list))
    points = plot_emotion_vs_time(moments_list)