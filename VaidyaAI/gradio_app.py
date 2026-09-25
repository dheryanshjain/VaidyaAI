from dotenv import load_dotenv
load_dotenv()

# ============================================================
# Imports
# ============================================================

import os
import gradio as gr

from brain_of_the_doctor import (
    encode_image,
    analyze_image_with_query
)

from voice_of_the_patient import (
    transcribe_with_groq
)

from voice_of_the_doctor import (
    text_to_speech_with_gtts
)


# ============================================================
# System Prompt
# ============================================================

system_prompt = """
You have to act as a professional doctor, i know you are not but this is for learning purpose.
What's in this image?. Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them.
Donot add any numbers or special characters in your response.
Your response should be in one long paragraph.
Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot.
Keep your answer concise (max 2 sentences).
No preamble, start your answer right away please
"""


# ============================================================
# Main Processing Function
# ============================================================

def process_inputs(audio_filepath, image_filepath):

    # --------------------------------------------------------
    # 1. Convert patient's voice to text
    # --------------------------------------------------------

    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # --------------------------------------------------------
    # 2. Analyze the image
    # --------------------------------------------------------

    if image_filepath:

        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="qwen/qwen3.8-27b"
        )

    else:

        doctor_response = "No image provided for me to analyze"

    # --------------------------------------------------------
    # 3. Generate doctor's voice
    # --------------------------------------------------------

    output_audio_path = "final.mp3"

    text_to_speech_with_gtts(
        input_text=doctor_response,
        output_filepath=output_audio_path
    )

    # --------------------------------------------------------
    # 4. Return everything to Gradio
    # --------------------------------------------------------

    return (
        speech_to_text_output,
        doctor_response,
        output_audio_path
    )


# ============================================================
# Gradio Interface
# ============================================================

iface = gr.Interface(

    fn=process_inputs,

    inputs=[

        gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Your Voice"
        ),

        gr.Image(
            type="filepath",
            label="Medical Image"
        )
    ],

    outputs=[

        gr.Textbox(
            label="Speech to Text"
        ),

        gr.Textbox(
            label="Doctor's Response"
        ),

        gr.Audio(
            label="Doctor's Voice",
            type="filepath",
            autoplay=True
        )
    ],

    title="VaidyaAI — AI-powered digital doctor"
)


# ============================================================
# Launch
# ============================================================

iface.launch(
    server_name="0.0.0.0",
    server_port=7860,
    debug=True
)