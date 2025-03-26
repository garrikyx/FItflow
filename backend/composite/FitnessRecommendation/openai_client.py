import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  
)

def get_recommendation(user_data, activity_log, weather):
    prompt = f"""
Based on this user profile: {user_data}
And recent activity history: {activity_log}
And current weather: {weather}

Recommend a suitable outdoor or indoor exercise with sunscreen suggestion if needed. Be concise and friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=[{ "role": "user", "content": prompt }]
    )

    return response.choices[0].message.content
