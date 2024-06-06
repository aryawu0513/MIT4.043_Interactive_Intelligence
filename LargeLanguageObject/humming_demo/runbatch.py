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

import torchaudio
from audiocraft.models import MusicGen

from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=20) 

# from audiocraft.models import AudioGen

# model_audio = AudioGen.get_pretrained('facebook/audiogen-medium')
# model_audio.set_generation_params(duration=10)

def generateMusic(i,moment):
    description = [moment['prompt']]
    print("generating music ", description, " for ",i)
    
    melody, sr = torchaudio.load('2minor_01.wav')
    # generates using the melody from the given audio and the provided descriptions.
    wav = model.generate_with_chroma(description, melody[None], sr)

    audio_write(f'music_{i}_final_long_happy', wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    return

# def overlayAmbient(i,moment):
#     description = [moment['ambient']]
#     print("overlaying ambient ", description, " for ",i)
    
#     output = model_audio.generate(
#         description,
#         progress=True
#     )
#     audio_write(f'ambient_{i}', output[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
#     print("generated ambient saved for ",i)
#     # Overlay the ambient sound with the generated music
    
#     audio1 = AudioSegment.from_file(f'music_{i}.wav')
#     audio2 = AudioSegment.from_file(f'ambient_{i}.wav')
#     audio2 = audio2.apply_gain(-20)

#     # Overlay audio2 on top of audio1, starting at the beginning of audio1
#     overlayed = audio1.overlay(audio2,loop=True)

#     # Export the overlayed audio
#     overlayed.export(f"music_overlay_{i}.wav", format="wav")

#     return

if __name__ == "__main__":
    day_dict ={'emotion': 'calm', 'emotion_value': 5, 'emotion_rgb': (0, 255, 0), 'ambient': 'raining sound', 'prompt': 'Happy jazz track with smooth saxophone and a cheerful gentle rhythm section'}
    # day_dict ={'emotion': 'happy', 'emotion_value': 10, 'emotion_rgb': (255, 0, 0), 'ambient': 'bird chirping', 'prompt': "A cheerful country song with acoustic guitars"}
    # "a sad melody with a sense of longing and reflection, using orchestral strings and gentle piano."
    #"cheerful pop melody blending acoustic guitar and soft percussion.
    #"energetic and uplifting tune with high-pitched notes, electronic beats and lively synths."
    #A cheerful country song with acoustic guitars
    i=2
    generateMusic(i,day_dict)
    # overlayAmbient(i,day_dict)
        
    # concatePieces(len(moments_list))
    # points = plot_emotion_vs_time(moments_list)