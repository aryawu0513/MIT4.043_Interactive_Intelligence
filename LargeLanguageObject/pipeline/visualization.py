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

import pygame

# Set your OpenAI API key here
api_key = ''
# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

import matplotlib.pyplot as plt

def plot_emotion_vs_time2(data):
    # Sort data by time
    sorted_data = sorted(data, key=lambda x: x['time_value'])
    
    # Calculate the x and y coordinates for each point
    x_coords = [int(d['time_value'] * 21.3) for d in sorted_data]
    y_coords = [int(d['emotion_value'] * 3.2) for d in sorted_data]
    
    # Create a list of strings representing drawLine parameters
    segments = []
    for i in range(len(sorted_data) - 1):
        x1, y1 = x_coords[i], y_coords[i]
        x2, y2 = x_coords[i + 1], y_coords[i + 1]
        segment = (x1,y1,x2,y2)
        segments.append(segment)
    
    return segments

data = [{'emotion_value': 2, 'time_value': 0, 'rgb': (237, 56, 43)},
        {'emotion_value': 10, 'time_value': 1, 'rgb': (39, 1, 128)},
        {'emotion_value': 5, 'time_value': 2, 'rgb': (39, 1, 128)},
        {'emotion_value': 8, 'time_value': 3, 'rgb': (2, 240, 80)},
        {'emotion_value': 7, 'time_value': 4, 'rgb': (2, 240, 80)},
        {'emotion_value': 3, 'time_value': 5, 'rgb': (140, 230, 30)},
        # {'emotion_value': 0, 'time_value': 6, 'rgb': (140, 230, 30)},
        ]

data.append({'emotion_value': 0, 'time_value': 6, 'rgb': (140, 230, 30)})


points = plot_emotion_vs_time2(data)
print(points)

import serial

# Establish serial connection with Arduino
# ser = serial.Serial('/dev/cu.HUAWEISoundJoy-21808', 9600,timeout=0.1)  # Use the correct port and baud rate
# ser = serial.Serial('/dev/cu.usbmodem2101', 9600,timeout=0.1)

try:
    ser = serial.Serial('/dev/cu.usbmodem2101', 9600,timeout=0.1)
    time.sleep(2)  # 给Arduino重启和准备数据传输的时间
    prev_momentindex = None
    momentindex=0
    rgbcolor=(0,0,0)
    while True:
        # 发送数据到Arduino
        # ser.write(b'Hello Arduino!\n')
        # print("Message sent to Arduino")
        serialized_data = ';'.join([f"{x1},{y1},{x2},{y2}" for x1, y1, x2, y2 in points])
        # print("serialized_data",serialized_data)
        serialized_data += f":{','.join(map(str, rgbcolor))};"
        # print("color",serialized_data)
        ser.write(serialized_data.encode())
        # 读取来自Arduino的响应
        if ser.in_waiting > 0:
        # if ser.fileno() > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line.startswith("A:"):  # Check if the line starts with "A:"
                print("Received Angle:", line)
                angle = float(line[2:])  # Extract the angle value
                value = angle / 315 * 128 /21.3
                print("Mapped value:", value)
                momentindex = min(range(len(data)), key=lambda i: abs(data[i]['time_value'] - value))
                
                if momentindex != prev_momentindex:
                    print("change!")  # Output: 2
                    print(momentindex)  # Output: 2
                    play_audio(f"music_overlay_{momentindex}.wav")
                    prev_momentindex = momentindex
                # play music_overlay_3.wav
            else:
                print("Received from Arduino:", line)
        rgbcolor = data[momentindex]['rgb']
        print("rgbcolor",rgbcolor)
        time.sleep(1)  # 等待一秒再发送下一条消息

finally:
    ser.close()  # 确保无论如何都关闭串口
