import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  
)

def get_recommendation(user_data, activity_log, weather,summary_stats):
    prompt = f"""
    The user is trying to stay fit. Based on their profile, recent activity, and current weather, provide a personalized recommendation (maximum 5 sentences).

    👤 User Info:
    - ID: {user_data['id']}
    - Name: {user_data.get('name')}
    - Recent activity history: {activity_log}
    - Preferences: {', '.join(user_data.get('preferences', []))}

    🏃 Weekly Activity Summary:
    - Total sessions: {summary_stats['total_sessions']}
    - Total minutes: {summary_stats['total_minutes']}
    - Average intensity: {summary_stats['avg_intensity']}

    🌤️ Current Weather in their location:
    {weather}

    Please provide(max 5 sentences):
    - A motivational yet practical recommendation.
    - Whether they should rest, continue, or push harder.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=[{ "role": "user", "content": prompt }]
    )

    return response.choices[0].message.content
