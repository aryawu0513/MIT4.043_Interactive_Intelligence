import os
import io
import sys
import argparse
import pyaudio
import wave
from google.cloud import speech
from google.cloud import texttospeech


import os
from pathlib import Path
from openai import OpenAI

import openai
import time

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

# model = MusicGen.get_pretrained('facebook/musicgen-melody')
# model.set_generation_params(duration=9)  # generate 8 seconds.

def main():
    emotion_results=""

    # Define the initial prompt
    prompt = """
        You are an assistant who will guide me through the process of reflecting on my day. 
        Start by asking me: "Do you want to share your day?"
        You can prompt me then a total of three questions, choosing one from the following each time:
        1. "Were there any times today when you felt calm, relaxed, or at peace?";
        2. "Did you have any moments of fear or anxiety today? What were you afraid of?";
        3. "Were there any moments today when you felt completely present and engaged in the moment?";
        4. "What time today were you the most happy?";
        5. "Were there any times today when you felt angry and acted out of character?";
        6. "Were there any times today where you made decisions that you now regret?";
        7. "When did the most meaningful interaction with others happen today, and what happened?";

        For each question, please analyze my answer and map it to a tuple of an emotion and a time. For example, if the question is about anxiety and I said I was a little anxious in the late afternoon, map it to {emotion: anxiety, time: 17:00}. Also identify a element that makes ambient sounds, think of objects that might appear in the setting i was in from my answer, for example tree leaves or racing heartbeats. Also, store a music genre that fits my description of the event that happened at that time. Some examples of music genre prompts are '80s pop track with bassy drums and synth' or 'Bluesy guitar instrumental with soulful licks and a driving rhythm section'. For each of my answers to one of your questions, store a dictionary of time, emotion, and genre prompt. For example: {emotion: anxiety, time: 17:00, prompt: 'Relaxing jazz track with raining sounds and a gentle rhythm section'}.
        
        At the end, say Goodnight, and return me with a list of three dictionaries, one for each question and answer.
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
                emotion_results = gpt_response

                print("Exiting chat...")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
    return emotion_results

    # descriptions = [music_genre]

    # melody, sr = torchaudio.load('sample2.wav')
    # # generates using the melody from the given audio and the provided descriptions.
    # wav = model.generate_with_chroma(descriptions, melody[None], sr)

    # audio_write('output1', wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    

if __name__ == "__main__":
    result = main()
    print("result",result)