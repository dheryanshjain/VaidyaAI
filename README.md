# VaidyaAI

VaidyaAI is an AI-powered medical assistant that lets patients ask questions using their voice and optionally provide a medical image. It transcribes the patient's speech, detects the response language, analyzes the image when available, and returns a concise text and voice response.

> VaidyaAI is an informational assistant, not a replacement for a qualified medical professional. It does not provide definitive diagnoses or prescribe medication dosages.

## Why this project?

Many patients find it easier to describe symptoms by speaking than by typing. VaidyaAI combines voice interaction with optional visual context so users can explain a concern naturally and receive an accessible response in English, Hindi, or Hinglish.

The project also demonstrates how speech recognition, multimodal AI, language detection, text-to-speech, and a lightweight web interface can work together in one practical healthcare workflow.

## Features

- Voice-based patient input through a microphone.
- Speech transcription using Groq Whisper (`whisper-large-v3`).
- Optional medical image upload for visual analysis.
- Vision-language analysis using Groq's `qwen/qwen3.8-27b` model.
- Automatic detection of English, Hindi, and Hinglish input.
- Language-specific, patient-friendly response prompts.
- Text response organized as assessment, possible cause, next steps, precautions, and when to seek care.
- Hindi or English voice output using Google Text-to-Speech.
- Gradio interface with separate patient input and doctor response areas.
- Safe response guidance: no definitive diagnosis, invented findings, or medication dosage recommendations.

## Tech Stack

- **Python**: Application and workflow logic.
- **Gradio**: Browser-based user interface.
- **Groq API**: Speech transcription and multimodal model inference.
- **Whisper Large V3**: Patient voice transcription.
- **Qwen 3.8 27B**: Medical image and question analysis through Groq.
- **gTTS**: Text-to-speech conversion.
- **python-dotenv**: Loading environment variables from a `.env` file.



## Project Structure

```text
VaidyaAI/
├── brain_of_the_doctor.py   # Image encoding and Groq vision analysis
├── gradio_app.py             # Main workflow, language detection, and UI
├── voice_of_the_doctor.py   # Converts responses to Hindi or English speech
├── voice_of_the_patient.py  # Transcribes patient audio with Groq Whisper
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT license
└── README.md                 # Project documentation
```

## How the Workflow Works

1. The patient records a voice question in Gradio and may upload a medical image.
2. The app transcribes the audio, detects the language, and prepares a safe response prompt.
3. The Groq vision model analyzes the image when provided; otherwise, the app uses a safety-focused fallback.
4. The UI displays the written response and plays the Hindi or English voice response.

## System Architecture

```mermaid
flowchart LR
    Patient[Patient] --> UI[Gradio Web UI]
    UI --> Input[Voice question<br/>Optional medical image]
    Input --> Processing[Application workflow<br/>Transcription and language detection]
    Processing -->|Image provided| Vision[Groq vision model]
    Processing -->|No image| Fallback[Safety fallback response]
    Vision --> Response[Patient-friendly text response]
    Fallback --> Response
    Response --> Voice[gTTS voice response]
    Response --> UI
    Voice --> UI
    UI --> Patient
```



## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
