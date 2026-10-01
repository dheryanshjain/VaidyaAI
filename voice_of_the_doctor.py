from gtts import gTTS


def text_to_speech_with_gtts(input_text, output_filepath, language="en"):
    """
    Convert doctor's response to speech.

    language:
        en = English
        hi = Hindi
    """

    if not input_text:
        return None

    # gTTS language selection
    if language == "hi":
        tts_language = "hi"
    else:
        tts_language = "en"

    audio_object = gTTS(
        text=input_text,
        lang=tts_language,
        slow=False
    )

    audio_object.save(output_filepath)

    return output_filepath