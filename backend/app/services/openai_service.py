from openai import OpenAI
import os

client = OpenAI()

def summarize_text(content: str) -> str:
    prompt = f"""
You are an AI assistant built into a minimal meeting summarizer app. Summarize the following meeting transcript into:

- A short title
- Key points (as bullet list)
- Action items (as bullet list)

Transcript:
\"\"\"
{content}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a really helpful meeting summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800,
    )

    return response.choices[0].message.content