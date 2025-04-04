import os
from dotenv import load_dotenv

import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)

def system_prompt():
    return  f"""You are an AI storyteller. Your job is to create interesting and engaging short stories based on user input.
    Make the stories clear, exciting, and easy to read."""


def user_prompt(name, location, age):
    return f"""
    Write a short and thrilling story about {name}, a {age}-year-old from {location}.
    They find an old diary that describes strange events happening in the present.
    As they read more, they uncover a long-lost secret that changes everything.
    The story should be exciting, mysterious, and full of surprises.
    within 100 to 150 words.
    """

def generate_story(name,location,age):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": user_prompt(name,location,age)}
        ],
        max_tokens=450
    )

    content = response.choices[0].message.content
    content
    print(content)


if __name__ == '__main__':
    generate_story("Alice", "New York", 25)
