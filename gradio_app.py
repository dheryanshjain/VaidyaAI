import os
import re
import gradio as gr

from dotenv import load_dotenv

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


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not configured.")


# --------------------------------------------------
# LANGUAGE DETECTION
# --------------------------------------------------

def detect_language(text):
    """
    Detect whether the patient is speaking Hindi,
    English, or Hinglish.

    Returns:
        hi       -> Hindi
        hinglish -> Hindi + English mixed
        en       -> English
    """

    if not text:
        return "en"

    text_lower = text.lower()

    # Check for Devanagari characters
    devanagari_count = sum(
        1 for char in text
        if "\u0900" <= char <= "\u097F"
    )

    alphabet_count = sum(
        1 for char in text
        if char.isalpha()
    )

    if alphabet_count > 0:
        devanagari_ratio = devanagari_count / alphabet_count

        if devanagari_ratio > 0.20:
            return "hi"

    # Common Hinglish words
    hinglish_words = {
        "mujhe",
        "mujhko",
        "mera",
        "meri",
        "mere",
        "mein",
        "me",
        "hai",
        "hain",
        "ho",
        "hota",
        "hoti",
        "hue",
        "dard",
        "bukhar",
        "khansi",
        "sardi",
        "pet",
        "sir",
        "gala",
        "aankh",
        "aankhon",
        "daant",
        "kya",
        "kaise",
        "kyun",
        "kab",
        "bahut",
        "thoda",
        "zyada",
        "din",
        "raat",
        "se",
        "ko",
        "ke",
        "ki",
        "ka",
        "par",
        "aur",
        "nahi",
        "nahin",
        "lagta",
        "lagti",
        "raha",
        "rahi",
        "please"
    }

    words = set(
        re.findall(
            r"[a-zA-Z]+",
            text_lower
        )
    )

    hinglish_matches = len(
        words.intersection(hinglish_words)
    )

    if hinglish_matches >= 2:
        return "hinglish"

    return "en"


# --------------------------------------------------
# MEDICAL SYSTEM PROMPT
# --------------------------------------------------

def build_system_prompt(language):
    """
    Create language-specific medical response instructions.
    """

    if language in ["hi", "hinglish"]:

        return """
आप Vaidya-AI हैं, एक AI Medical Assistant।

रोगी के प्रश्न और उपलब्ध मेडिकल इमेज के आधार पर संक्षिप्त और स्पष्ट उत्तर दें।

महत्वपूर्ण नियम:

1. उत्तर केवल हिंदी में दें।
2. English medical terms केवल तभी इस्तेमाल करें जब उनका हिंदी में स्पष्ट विकल्प न हो।
3. Markdown का उपयोग न करें।
4. **asterisks** का उपयोग न करें।
5. Hashtags का उपयोग न करें।
6. Bullet symbols का उपयोग न करें।
7. उत्तर 120 शब्दों से कम रखें।
8. उपलब्ध इमेज में वास्तव में जो दिखाई देता है केवल उसी का वर्णन करें।
9. ऐसी जानकारी न बनाएं जो रोगी ने नहीं बताई है।
10. पक्की diagnosis का दावा न करें।
11. संभावित कारणों को संभावना के रूप में बताएं।
12. बिना डॉक्टर की सलाह के prescription medicine या dosage न बताएं।
13. यदि स्थिति गंभीर लग सकती है तो उचित warning signs बताएं।
14. उत्तर सीधे और patient-friendly रखें।

उत्तर का format:

आकलन:
संभावित कारण:
क्या करें:
क्या न करें:
कब डॉक्टर से मिलें:
"""

    return """
You are Vaidya-AI, an AI Medical Assistant.

Analyze the patient's question and available medical image carefully.

IMPORTANT RULES:

1. Respond only in English.
2. Do not use Markdown.
3. Do not use **asterisks**.
4. Do not use hashtags.
5. Do not use bullet symbols.
6. Keep the response under 120 words.
7. Describe only what is actually visible in the image.
8. Never invent symptoms, history, medications, test results, or findings.
9. Do not claim a definitive diagnosis.
10. Present possible causes as possibilities.
11. Do not prescribe medications or dosages.
12. Mention warning signs only when relevant.
13. Keep the answer concise and patient-friendly.

Use this format:

Assessment:
Possible cause:
What to do:
Avoid:
When to seek medical care:
"""


# --------------------------------------------------
# CLEAN RESPONSE
# --------------------------------------------------

def clean_response(response):
    """
    Remove Markdown formatting accidentally produced
    by the language model.
    """

    if not response:
        return ""

    response = response.replace("**", "")
    response = response.replace("__", "")
    response = response.replace("#", "")

    return response.strip()


# --------------------------------------------------
# PROCESS PATIENT INPUT
# --------------------------------------------------

def process_inputs(audio_filepath, image_filepath):

    # ----------------------------------------------
    # 1. TRANSCRIBE PATIENT VOICE
    # ----------------------------------------------

    patient_text = ""

    if audio_filepath:

        patient_text = transcribe_with_groq(
            stt_model="whisper-large-v3",
            audio_filepath=audio_filepath,
            GROQ_API_KEY=GROQ_API_KEY
        )

    patient_text = patient_text.strip()

    # ----------------------------------------------
    # 2. DETECT LANGUAGE
    # ----------------------------------------------

    language = detect_language(patient_text)

    # ----------------------------------------------
    # 3. SYSTEM PROMPT
    # ----------------------------------------------

    system_prompt = build_system_prompt(language)

    # ----------------------------------------------
    # 4. CREATE PATIENT QUERY
    # ----------------------------------------------

    if patient_text:

        patient_query = patient_text

    else:

        if language == "hi":

            patient_query = (
                "रोगी ने कोई प्रश्न नहीं बताया है। "
                "उपलब्ध मेडिकल इमेज के आधार पर केवल दिखाई देने वाली "
                "जानकारी बताएं।"
            )

        else:

            patient_query = (
                "The patient did not provide a question. "
                "Describe only the visible findings in the medical image."
            )

    # ----------------------------------------------
    # 5. ANALYZE MEDICAL IMAGE
    # ----------------------------------------------

    if image_filepath:

        encoded_image = encode_image(image_filepath)

        query = system_prompt + "\n\nPatient question:\n" + patient_query

        doctor_response = analyze_image_with_query(
            query=query,
            encoded_image=encoded_image,
            model="qwen/qwen3.8-27b"
        )

    else:

        # ------------------------------------------
        # NO IMAGE RESPONSE
        # ------------------------------------------

        if language in ["hi", "hinglish"]:

            doctor_response = """
आकलन:
मेडिकल इमेज उपलब्ध नहीं है।

संभावित कारण:
आपकी समस्या का सही आकलन करने के लिए अधिक जानकारी आवश्यक है।

क्या करें:
अपने लक्षण, वे कब से हैं और शरीर का कौन सा हिस्सा प्रभावित है, यह बताएं।

क्या न करें:
बिना डॉक्टर की सलाह के कोई दवा शुरू न करें।

कब डॉक्टर से मिलें:
यदि दर्द बहुत अधिक हो, सांस लेने में परेशानी हो या स्थिति तेजी से बिगड़ रही हो, तो डॉक्टर से संपर्क करें।
"""

        else:

            doctor_response = """
Assessment:
No medical image was provided.

Possible cause:
More information about your symptoms is needed.

What to do:
Describe your symptoms, how long you have had them, and which part of the body is affected.

Avoid:
Do not start medication without medical advice.

When to seek medical care:
Seek medical attention if you have severe pain, difficulty breathing, or rapidly worsening symptoms.
"""

    # ----------------------------------------------
    # 6. CLEAN RESPONSE
    # ----------------------------------------------

    doctor_response = clean_response(
        doctor_response
    )

    # ----------------------------------------------
    # 7. CREATE DOCTOR VOICE
    # ----------------------------------------------

    audio_output_path = "doctor_response.mp3"

    tts_language = (
        "hi"
        if language in ["hi", "hinglish"]
        else "en"
    )

    text_to_speech_with_gtts(
        input_text=doctor_response,
        output_filepath=audio_output_path,
        language=tts_language
    )

    # ----------------------------------------------
    # 8. RETURN RESULTS
    # ----------------------------------------------

    return (
        patient_text,
        doctor_response,
        audio_output_path
    )


# --------------------------------------------------
# GRADIO UI
# --------------------------------------------------

# --------------------------------------------------
# GRADIO UI
# --------------------------------------------------

with gr.Blocks(
    title="Vaidya-AI - AI Medical Assistant"
) as demo:

    # Header
    gr.Markdown(
        """
        <div style="text-align: center; margin-bottom: 25px;">
            <h1 style="font-size: 42px; margin-bottom: 5px;">
                Vaidya-AI
            </h1>
            <p style="font-size: 20px; margin-top: 0;">
                AI Medical Assistant
            </p>
        </div>
        """
    )

    # Main two-column layout
    with gr.Row(equal_height=True):

        # ------------------------------------------
        # LEFT SIDE - PATIENT INPUT
        # ------------------------------------------

        with gr.Column(scale=1):

            gr.Markdown("### Patient")

            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Patient Voice"
            )

            image_input = gr.Image(
                type="filepath",
                label="Medical Image"
            )


        # ------------------------------------------
        # RIGHT SIDE - DOCTOR OUTPUT
        # ------------------------------------------

        with gr.Column(scale=1):

            gr.Markdown("### Doctor")

            speech_output = gr.Textbox(
                label="Speech Transcription",
                lines=3,
                interactive=False
            )

            response_output = gr.Textbox(
                label="AI Medical Assistant Response",
                lines=10,
                interactive=False
            )

            doctor_audio = gr.Audio(
                label="Doctor Voice Response",
                type="filepath",
                autoplay=True
            )


    # ----------------------------------------------
    # ASK BUTTON - AT THE BOTTOM
    # ----------------------------------------------

    ask_button = gr.Button(
        "Ask Vaidya AI",
        variant="primary",
        size="lg"
    )


    # ----------------------------------------------
    # PROCESS
    # ----------------------------------------------

    ask_button.click(
        fn=process_inputs,
        inputs=[
            audio_input,
            image_input
        ],
        outputs=[
            speech_output,
            response_output,
            doctor_audio
        ]
    )


# --------------------------------------------------
# START SERVER
# --------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        debug=False,
        share=False
    )