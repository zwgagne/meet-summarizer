import openai
import os

openai.api_key = os.getenv("open-ai-key")  # move to .env file

def summarize_text(content):
    prompt = f"""
You are an AI assistant builted in a minimal meet summarizer app. Summarize the following meeting transcript into:

- A short title
- Key points (as bullet list)
- Action items (as bullet list)

Transcript:
\"\"\"
{content}
\"\"\"
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a really helpful meeting summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )

    return response.choices[0].message.content