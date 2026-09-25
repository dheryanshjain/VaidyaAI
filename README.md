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
- Optional ElevenLabs integration
- Local web UI with Gradio

## Tech Stack

### Core
- Python 3
- Gradio
- Groq API
- gTTS
- SpeechRecognition
- pydub
- Python Dotenv

### Supporting Libraries
- FastAPI
- Pillow
- NumPy
- Pandas
- Requests
- Uvicorn
- ElevenLabs (optional)

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

## Project Structure

```text
VaidyaAI/
├── Pipfile
├── Pipfile.lock
├── requirements.txt
├── README.md
├── gradio_app.py
├── brain_of_the_doctor.py
├── voice_of_the_patient.py
├── voice_of_the_doctor.py
├── final.mp3
├── acne.jpg
├── dandruff-optimized.webp
├── skin_rash.jpg
├── tounge.jpg
├── __pycache__/
└── .gitignore
```

## Prerequisites

- Python 3.10+
- Access to the Groq API
- Optional: ElevenLabs API key for alternative voice synthesis
- Microphone access for local voice capture

## Setup

1. Clone the repository

```bash
git clone https://github.com/dheryanshjain/VaidyaAI.git
cd VaidyaAI
```

2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# or .venv\Scripts\activate  # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

5. Run the app

```bash
cd VaidyaAI
python gradio_app.py
```

Then open the local Gradio URL shown in the terminal, usually:

```text
http://localhost:7860
```

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

## Notes

This repository is a prototype and should be treated as an educational/demo project rather than a clinical diagnostic system. It is useful for experimentation with multimodal AI workflows, but it is not intended to replace professional medical judgment.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions, feature ideas, and improvements are welcome. For major changes, please open an issue first to discuss the proposed update.

## Acknowledgements

- Groq for LLM and speech APIs
- Gradio for rapid UI development
- Open-source Python ecosystem for audio and ML tooling

---

Built for AI-powered healthcare interaction experiments and educational prototyping.
