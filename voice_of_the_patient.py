from groq import Groq


def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Transcribe patient voice using Groq Whisper.
    Supports Hindi, English, and other supported languages.
    """

    if not audio_filepath:
        return ""

    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=stt_model,
            response_format="text"
        )

    return transcription