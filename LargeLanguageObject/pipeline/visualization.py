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


data = [{'emotion':'calm', 'time':'now'},{'emotion': 'engaged', 'time': 'morning'},{'emotion': 'happy', 'time': 'an hour ago'},{'emotion':'sad','time':'late afternoon'},{'emotion':'stressed','time':'noon'}]

def parseTime(data):
    prompt=f"""
        You are an assistant who takes this list of dictionaries: {data} as input, and for each dictionary parse the emotion field into a value between 1-10, and parse the time field into a numeric value also from 1-10.
        For emotion value, 10 is the most positive, and 1 is the most negative.
        Some examples of the scoring of emotions: happy = 10, fulfillment/connectedness = 9, present/engaged = 8, relief/comfort=7, calm = 6, bored = 5, anxiety = 4, fear = 3, sad,Regretful = 2, anger = 1, 
        Also come up with a color that reflects the emotion, give back to me in rgb tuple format.

        For time value, now is always the latest time at night and has the value = 10, morning = 1, noon = 4, afternoon = 6, evening = 8, if one event says an hour ago, then it is 9

        Return me the same list of dictionaries but with the values for emotion and time turned into numeric values, plus the rgb color value for that emotion
        The format of your response should be exactly like this, with no extra words of your own!!:
        [{{'emotion': 0-10, 'time': 0-10, 'rgb':(r-value,g-value,b-value)}},{{'emotion': 0-10, 'time': 0-10,'rgb':(r-value,g-value,b-value)}},{{'emotion': 0-10, 'time': 0-10,'rgb':(r-value,g-value,b-value)}}...]
        Any extra word other than this list of dictionaries is not allowed and you will be penalized
    """
    print("Starting analysis...")

    messages = [{"role": "system", "content": prompt}]
    # messages.append({"role": "user", "content": data})

    response = client.chat.completions.create(
                messages=messages,
                model="gpt-4",
            )

            # Extract the GPT response and print it
    gpt_response = response.choices[0].message.content
    
    return gpt_response

# result =ast.literal_eval(parseTime(data))
# print(result)

import matplotlib.pyplot as plt


def plot_emotion_vs_time(data):
    # Sort data by time
    times = [d['time_value']* 12.8 for d in data]
    emotions = [d['emotion_value']* 6.4 for d in data]
    rgb_colors = [(d['emotion_rgb'][0] / 255, d['emotion_rgb'][1] / 255, d['emotion_rgb'][2] / 255) for d in data]

    plt.figure(figsize=(8, 6))
    for i in range(len(times) - 1):
        plt.plot([times[i], times[i + 1]], [emotions[i], emotions[i + 1]], color='black',linewidth=2)
        plt.scatter(times[i], emotions[i], color=rgb_colors[i], edgecolors='black', zorder=5)

    # Plot the last point separately to avoid connecting it with a line
    plt.scatter(times[-1], emotions[-1], color=rgb_colors[-1], edgecolors='black', zorder=5)

    plt.xlabel('Time')
    plt.ylabel('Emotion')
    plt.title('Emotion vs. Time')
    plt.xticks(range(0, 128,10))  # Set x-axis ticks to match the time values
    plt.yticks(range(0, 64,10))  # Set y-axis ticks to match the emotion values
    plt.grid(True)
    plt.show()
    result = [(times[i], emotions[i]) for i in range(len(data))]
    
    return result

def plot_emotion_vs_time2(data):
    # Sort data by time
    sorted_data = sorted(data, key=lambda x: x['time_value'])
    
    # Calculate the x and y coordinates for each point
    x_coords = [int(d['time_value'] * 12.8) for d in sorted_data]
    y_coords = [int(d['emotion_value'] * 3.2) for d in sorted_data]
    
    # Create a list of strings representing drawLine parameters
    segments = []
    for i in range(len(sorted_data) - 1):
        x1, y1 = x_coords[i], y_coords[i]
        x2, y2 = x_coords[i + 1], y_coords[i + 1]
        segment = (x1,y1,x2,y2)
        segments.append(segment)
    
    return segments

data = [{'emotion_value': 8, 'time_value': 1, 'rgb': (174, 238, 0)},
        {'emotion_value': 1, 'time_value': 4, 'rgb': (164, 36, 59)},
        {'emotion_value': 2, 'time_value': 6, 'rgb': (141, 85, 191)},
        {'emotion_value': 10, 'time_value': 9, 'rgb': (97, 237, 99)},
        {'emotion_value': 6, 'time_value': 10, 'rgb': (62, 141, 188)},
        ]

# alldata = [{'emotion': 'excitement', 'emotion_value': 7, 'emotion_rgb': (245, 176, 65), 'time': 'an hour ago', 'time_value': 9, 'ambient': 'chattering', 'prompt': 'Upbeat pop track with rhythmic beats'}, {'emotion': 'relaxed', 'emotion_value': 6, 'emotion_rgb': (137, 207, 240), 'time': 'now', 'time_value': 10, 'ambient': 'winds blowing', 'prompt': 'Smooth jazz with wind sounds embedded'}]
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
    while True:
        # 发送数据到Arduino
        # ser.write(b'Hello Arduino!\n')
        # print("Message sent to Arduino")
        serialized_data = ';'.join([f"{x1},{y1},{x2},{y2}" for x1, y1, x2, y2 in points])
        ser.write(serialized_data.encode())
        # 读取来自Arduino的响应
        if ser.in_waiting > 0:
        # if ser.fileno() > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line.startswith("A:"):  # Check if the line starts with "A:"
                angle = float(line[2:])  # Extract the angle value
                value = angle / 315 * 128 /12.8
                print("Mapped value:", value)
                momentindex = min(range(len(data)), key=lambda i: abs(data[i]['time_value'] - value))
                print(momentindex)  # Output: 2
                if momentindex != prev_momentindex:
                    play_audio(f"music_overlay_{momentindex}.wav")
                    prev_momentindex = momentindex
                # play music_overlay_3.wav
            else:
                print("Received from Arduino:", line)
        time.sleep(1)  # 等待一秒再发送下一条消息

finally:
    ser.close()  # 确保无论如何都关闭串口
