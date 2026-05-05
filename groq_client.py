import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

api_key = os.getenv("API_KEY")

if not api_key:
    raise EnvironmentError("No API key found in .env — set API_KEY=gsk_your_groq_key_here")

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
You are an expert at summarising articles and content.
Provide a clear, concise summary in 4 to 5 lines.
Preserve the original meaning and key points.
"""

def summarize_text(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return "Summary unavailable due to API error."
