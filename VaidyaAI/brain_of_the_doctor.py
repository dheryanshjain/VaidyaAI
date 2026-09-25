from dotenv import load_dotenv
load_dotenv()

import os
import base64

from groq import Groq


# ============================================================
# GROQ API KEY
# ============================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Please check your .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# Convert Image to Base64
# ============================================================

def encode_image(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# ============================================================
# Analyze Image with Groq Vision
# ============================================================

def analyze_image_with_query(
    query,
    model="qwen/qwen3.8-27b",
    encoded_image=None
):

    if not encoded_image:
        return "No image was provided for analysis."

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ]

    # ========================================================
    # Groq API Request
    # ========================================================

    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages,

        # Keep output below your 1000 OTPM limit
        max_completion_tokens=500,

        # More deterministic response
        temperature=0.2
    )

    # ========================================================
    # Return AI Response
    # ========================================================

    return chat_completion.choices[0].message.content