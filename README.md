# VaidyaAI

VaidyaAI is an AI-powered digital doctor prototype that combines voice input and medical image analysis to provide a patient-style consultation experience. The app records or accepts a patient's voice, transcribes it with Groq Whisper, analyzes an uploaded medical image using a vision-capable LLM, and converts the final response into spoken audio.

## Overview

This project is designed as a demo/learning app for a clinical assistant workflow. It simulates a doctor interacting with a patient by:

- listening to the patient's symptoms through voice input
- transcribing speech to text using Groq's speech-to-text model
- analyzing an uploaded image (for example, skin rash, tongue, acne, or dandruff)
- generating a concise doctor-like response
- converting that response to audio for playback in the browser

The interface is built using Gradio, making it easy to run locally and test quickly.

## Key Features

- Voice-based symptom input
- Speech-to-text transcription using Groq Whisper
- Medical image analysis using a Groq vision model
- Doctor-style conversational response generation
- Text-to-speech output using gTTS
- ElevenLabs integration
- Local web UI with Gradio

## Tech Stack

### Core
- Python 3
- Gradio
- Groq API
- gTTS
- SpeechRecognition
- Python Dotenv

### Supporting Libraries
- FastAPI
- Pillow
- NumPy
- Pandas
- Requests
- Uvicorn
- ElevenLabs

### AI / ML Components
- Whisper Large V3 for speech transcription
- Qwen vision model for image-based diagnosis
- LLM-powered doctor-style reasoning and output formatting

## Architecture

The project follows a simple modular pipeline:

```text
User Input
  ├─ Voice (microphone / uploaded audio)
  │    └─ voice_of_the_patient.py
  │         └─ SpeechRecognition + Groq Whisper
  │              └─ transcribed patient symptoms
  │
  └─ Medical Image
       └─ brain_of_the_doctor.py
            └─ encode image as base64
            └─ Groq vision model analyzes the image
                 └─ diagnosis / differential / remedies

Combined Prompt
  └─ gradio_app.py
       ├─ merges patient symptoms + image analysis
       ├─ formats doctor-style response
       └─ passes to TTS engine

Output
  ├─ text response displayed in UI
  └─ final.mp3 generated via gTTS
```

### Component Responsibilities

- `gradio_app.py`
  - Main application entrypoint
  - Defines the Gradio UI
  - Orchestrates the voice and image processing flow
  - Produces the final doctor response and audio

- `voice_of_the_patient.py`
  - Handles audio capture and transcription
  - Uses `speech_recognition` and Groq's transcription API

- `brain_of_the_doctor.py`
  - Encodes images to base64
  - Sends prompt + image to a Groq vision model
  - Returns the AI-generated medical assessment

- `voice_of_the_doctor.py`
  - Converts the doctor's final text into speech
  - Uses gTTS by default and includes ElevenLabs code paths




## Usage

1. Open the Gradio web interface.
2. Speak into the microphone or provide audio input.
3. Upload a relevant medical image.
4. The app transcribes the voice, analyzes the image, and returns a doctor-like textual response.
5. The generated response is also converted to audio and played back.

## Example Workflow

- Patient says: “I have a painful rash on my arm and it is itchy.”
- Image is uploaded: a skin rash photograph.
- AI analyzes the combination of symptoms and image.
- Doctor-like response is generated and spoken aloud.




## Acknowledgements

- Groq for LLM and speech APIs
- Gradio for rapid UI development
- Open-source Python ecosystem for audio and ML tooling

---

Built for AI-powered healthcare interaction experiments and educational prototyping.
