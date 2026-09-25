from dotenv import load_dotenv
load_dotenv()

import os

from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs


# ============================================================
# Step 1: gTTS
# ============================================================

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )

    audioobj.save(output_filepath)

    return output_filepath


# ============================================================
# Step 2: ElevenLabs
# ============================================================

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(
        api_key=ELEVENLABS_API_KEY
    )

    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )

    elevenlabs.save(audio, output_filepath)

    return output_filepath


# ============================================================
# Step 3: gTTS for Gradio
# ============================================================

def text_to_speech_with_gtts(input_text, output_filepath):

    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )

    # Generate MP3 file
    audioobj.save(output_filepath)

    # IMPORTANT:
    # Return the filepath to Gradio.
    # Do NOT use SoundPlayer or ffplay here.
    return output_filepath


# ============================================================
# Step 4: ElevenLabs for Gradio
# ============================================================

def text_to_speech_with_elevenlabs(input_text, output_filepath):

    client = ElevenLabs(
        api_key=ELEVENLABS_API_KEY
    )

    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )

    # Generate MP3 file
    elevenlabs.save(audio, output_filepath)

    # Return filepath to Gradio
    return output_filepath


#text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")