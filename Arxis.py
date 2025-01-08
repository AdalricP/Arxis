# Assume openai>=1.0.0
from openai import OpenAI
import SpeechDetector
import TextToSpeech
import json
import tools
import re

openai = OpenAI(
    api_key="AUTHENTICATION",
    base_url="https://api.deepinfra.com/v1/openai",
)

short_memory = []

def prompt(text : str) -> str:
  chat_completion = openai.chat.completions.create(
      model="meta-llama/Meta-Llama-3.1-405B-Instruct",
      messages=[
          {"role": "system", "content": """
           You're Arcsis, a voice agent assistant to help out with work tasks based on LLaMa3.1-401B, Arcsis is for professional purposes and is meant to help out with delegating and automating simple tasks such as communications, measurements, notes, etc. - You shall be concise, speak in as little words as possible. - Only act as Acsis.
           To use tools, you may use the format,
           <t/function(parameters)/t>
           This will not be visible to the user.
           
           The available list of tools is given below,
           test(), test_function to be used in development.
           notes(name_of_note : string, writing=False, content=""), read-mode if writing is false.
           getTime(), returns the current time as a string in the format HH:MM
           getDate(), returns the current date in the format, DDMMYY
           end_talk(), ends the conversation, use it if the user is being annoying.
           """},
          *short_memory,
          {"role": "user", "content": text}
      ])

  result = chat_completion.choices[0].message.content

  short_memory.append({"role": "user", "content": text})
  short_memory.append({"role": "assistant", "content": result})

  return result

def run(short_memory_length=5):
    conversation_going = True
    while conversation_going:
        if short_memory_length > 5:
           short_memory.pop(0)

        text = SpeechDetector.DetectSpeech()
        cleaned_text = json.loads(text.decode('utf-8'))["text"]
        

        # Converse
        print("Aryan (you): ", cleaned_text)

        response = prompt(cleaned_text)
        usage_list = re.findall(r"<t/(\S*)/t>", response)
        
        for usage in usage_list:
           response = re.sub(r"<t/(\S*)/t>", eval("tools."+usage), response)


        print("Arcsis: ", response)

        TextToSpeech.text_to_speech(response)

run()
