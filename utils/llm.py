from dotenv import load_dotenv
import os
import requests

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_your_"):
    GROQ_API_KEY = None
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = os.getenv("GROQ_URL", "https://api.groq.com/openai/v1/chat/completions")


print("Current Directory:", os.getcwd())
print("KEY FOUND:", bool(GROQ_API_KEY))


def ask_llm(question, context, temperature=0.0):

    if not GROQ_API_KEY:
        raise ValueError(
            "Missing or placeholder Groq API key. Set GROQ_API_KEY in .env to a valid Groq key from the Groq dashboard."
        )

    prompt = f"""
You are a helpful assistant.

Answer only from the given context.

If the answer is not present in the context, say:
'I could not find the answer in the document.'

Context:
{context}

Question:
{question}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature,
        "max_tokens":1024
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        answer = (
    result.get("choices", [{}])[0]
    .get("message", {})
    .get("content", "No response generated.")
)

        return answer

    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e}\n\n{response.text}"

    except Exception as e:
        return f"Error: {str(e)}"