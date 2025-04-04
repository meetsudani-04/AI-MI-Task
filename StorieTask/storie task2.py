import os
from dotenv import load_dotenv

import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)

def system_prompt():
    return  f"""You are an AI storyteller. Your job is to create interesting and engaging short stories based on user input.
    Make the stories clear, exciting, and easy to read."""

def user_prompt(name, location, age, hobby, favorite_color, special_item):
    return f"""
    Write a short and exciting story about {name}, a {age}-year-old from {location}.
    One day, while enjoying their favorite hobby, {hobby}, they find an old diary.
    The diary, with a {favorite_color} cover, talks about strange events happening now.
    As they read more, they discover a big secret linked to their special item: {special_item}.
    The story should be fun, mysterious, and full of surprises.
    Keep it between 100 to 150 words.
    """

def generate_story(name,location,age,hobby,favorite_color,special_item):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": user_prompt(name, location, age, hobby, favorite_color, special_item)}
        ],
        max_tokens=450
    )

    content = response.choices[0].message.content
    print(content)


if __name__ == '__main__':
    generate_story("John", "New York", 30, "Painting", "Red", "Watch")

