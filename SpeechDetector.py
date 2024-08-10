import requests
import pyaudio
import wave
import os

def DetectSpeech(language='en'):
    # Set your API endpoint and authorization token
    url = 'https://api.deepinfra.com/v1/inference/openai/whisper-large-v3'
    headers = {'Authorization': 'bearer Y9a3TYuaelNtXwiPMIxvDdWbGtThp9uo', "language": language}

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Set audio parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    # Record audio from the microphone
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    print("Recording... (Press Ctrl+C to stop)")

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    print("Recording finished.")

    # Save recorded audio to a file
    output_file = 'my_recorded_voice.wav'
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Send the recorded audio to the API
    files = {'audio': open(output_file, 'rb')}
    response = requests.post(url, headers=headers, data={"language": language}, files=files)

    # Clean up
    stream.stop_stream()
    stream.close()
    audio.terminate()


    # Handle the response here (e.g., print the content or save it to a file)
    return response.content


    
