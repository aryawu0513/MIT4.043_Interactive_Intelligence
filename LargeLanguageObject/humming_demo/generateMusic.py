import pyaudio
import wave
import ast

import os
from pathlib import Path
from openai import OpenAI

import openai
import time
from pydub import AudioSegment

# Set your OpenAI API key here
api_key = 
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
        You are an assistant who will guide me to reflect on my day. 
        Start by asking me: "How was your day today?"
        You can then follow up with one question relevant to my answer.
        After that, say something nice to me and say "Goodbye" and exit.
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

            if "Goodbye" in gpt_response:
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
        Please analyze my answer about my day today, and parse it to a dictionary with the following fields: emotion, ambient sound, and music genre prompt.
        Identify the emotion that I expressed in my answer. Also parse the emotion field into a value between 1-10, with 10 being the most positive and 1 being the most negative. Also come up with a color that reflects the emotion, give back to me in rgb tuple format.
        Some examples of the scoring of emotions: happy = 10, fulfillment/connectedness = 9, present/engaged = 8, relief/comfort=7, calm = 6, bored = 5, anxiety = 4, tired = 3, sad = 2, anger = 1...
        Also identify a element that makes ambient sounds, think of objects that might appear in the setting i was in from my answer, for example tree leaves or sea waves. 
        Also, store a music genre that fits my description of the event that happened at that time. Some examples of music genre prompts are '80s pop track with bassy drums and synth' or 'Bluesy guitar instrumental with soulful licks and a driving rhythm section'. 
        
        The format of your response should be exactly like this, with no extra words of your own!!:
        {'emotion':'', 'emotion_value':1-10, 'emotion_rgb':(r-value,g-value,b-value), 'ambient':'', 'prompt':''}
        Any extra word other than this dictionary is not allowed and you will be penalized
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
    
    melody, sr = torchaudio.load('alto-04.wav')
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
    # chathistory = chatbot()
    # print("HERE CHATS",chathistory)
    #chathistory = [{'role': 'system', 'content': '\n        You are an assistant who will guide me to reflect on my day. \n        Start by asking me: "How was your day today?"\n        You can then follow up with one question relevant to my answer.\n        After that, say something nice to me and say "Goodbye" and exit.\n    '}, {'role': 'user', 'content': 'I want to share my day.'}, {'role': 'assistant', 'content': 'That sounds great! So, how was your day today?'}, {'role': 'user', 'content': "my day was fine it was a lot of packing I have to do I'm a little stressed about the upcoming summer"}, {'role': 'assistant', 'content': 'It sounds like you had a busy day. Why are you feeling stressed about the upcoming summer?'}, {'role': 'user', 'content': "there's just a lot of work and it's gonna be hot here and I'm not a super fan of the heat I'm a"}, {'role': 'assistant', 'content': "It can indeed get challenging when we have to work in conditions that we aren't comfortable with. Maybe you can find ways to keep cool and stay hydrated? Remember, it's always important to take care of yourself amidst all the work. Have a relaxing evening and keep in mind tomorrow is another chance to conquer the day. Goodbye!"}]
    # day = analyze(chathistory)
    # print("Moments",day)
    # day_dict = ast.literal_eval(day)
    # print("Day",day_dict)
    #day_dict= {'emotion': 'stressed', 'emotion_value': 4, 'emotion_rgb': (255, 140, 0), 'ambient': 'rustle of packing materials', 'prompt': 'Ambient downtempo track with slow beats and soothing synth pads'}
    day_dict ={'emotion': 'calm', 'emotion_value': 7, 'emotion_rgb': (173, 216, 230), 'ambient': 'raining sound', 'prompt': 'Relaxing jazz track with smooth saxophone and a gentle rhythm section'}
    i=7
    generateMusic(i,day_dict)
    overlayAmbient(i,day_dict)
        
    # concatePieces(len(moments_list))
    # points = plot_emotion_vs_time(moments_list)