import os
import base64
import mimetypes

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Please add GROQ_API_KEY to your environment variables."
    )


# Groq client
client = Groq(api_key=GROQ_API_KEY)


def encode_image(image_path):
    """
    Convert an image file into a Base64 encoded string.
    """

    if not image_path:
        return None

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return encoded_image


def analyze_image_with_query(
    query,
    model="qwen/qwen3.8-27b",
    encoded_image=None
):
    """
    Analyze an image using a Groq vision-capable model.
    """

    if not encoded_image:
        return "No image was provided for analysis."

    # Default MIME type
    mime_type = "image/jpeg"

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
                        "url": (
                            f"data:{mime_type};base64,"
                            f"{encoded_image}"
                        )
                    }
                }
            ]
        }
    ]

    try:

        chat_completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_completion_tokens=500,
            temperature=0.2
        )

        return chat_completion.choices[0].message.content

    except Exception as e:

        return (
            "I was unable to analyze the image at this time. "
            f"Error: {str(e)}"
        )