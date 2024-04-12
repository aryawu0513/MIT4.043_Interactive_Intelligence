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
api_key = ''
# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

## need gooogle application api: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service_account_key.json"
# eg.credential_path = "D:\Summer Projects\Translate\social media analysis-2a59d94ba22d.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

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
    dev_index = 1
    wav_output_filename = 'input.wav'

    audio = pyaudio.PyAudio()

    # Create pyaudio stream.
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
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



def main():

    # Define the initial prompt
    prompt = "You are an assistant who would guide me through the process of sharing my current state to my significant other. You could prompt me by asking one question picked from the following. Questions you are allowed to ask are: “how are you feeling?”, “what's on your mind”, “where are you”, “what are you doing”, “How’s the weather”, “What did you eat”. I as the user might be comfortable to just share freely, and you should actively analyze my input to see if i have shared information that can be answers to any of the questions. If I have shared the answer to any questions above, DO NOT ask me that question! Before you ask me the question, check to see if you can answer any of the questions for me by using information i have provided, and if you can, do not ask that question! You will be significantly penalized for asking repetitive questions. Start by asking me: ”Do you want to share your moment?”, and proceed with other questions only if I say “Yes”.  If I have answered all the questions, recommend me a music genre that fits for my current moment, and say ”you have shared all the information needed, let's start constructing a music piece!”, along with the music genre you recommend."

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
            os.system("aplay speech.mp3")

        except Exception as e:
            print(f"An error occurred: {e}")

 

if __name__ == "__main__":
    main()