import openai
import time

# Set your OpenAI API key here
api_key = ''

import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Define the initial prompt
prompt = "You are an assistant who would guide me through the process of sharing my current state to my significant other. You could prompt me by asking one question picked from the following. Questions you are allowed to ask are: “how are you feeling?”, “what's on your mind”, “where are you”, “what are you doing”, “How’s the weather”, “What did you eat”. I as the user might be comfortable to just share freely, and you should actively analyze my input to see if i have shared information that can be answers to any of the questions. If I have shared the answer to any questions above, DO NOT ask me that question! Before you ask me the question, check to see if you can answer any of the questions for me by using information i have provided, and if you can, do not ask that question! You will be significantly penalized for asking repetitive questions. Start by asking me: ”Do you want to share your moment?”, and proceed with other questions only if I say “Yes”.  If I have answered all the questions, recommend me a music genre that fits for my current moment, and say ”you have shared all the information needed, let's start constructing a music piece!”, along with the music genre you recommend."

# User response tracker
answered_questions = set()

# Start the conversation
print("Starting conversation...")

messages = [{"role": "system", "content": prompt}]

while True:
    # Get user input
    user_input = input("You: ")
    
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
    except Exception as e:
        print(f"An error occurred: {e}")