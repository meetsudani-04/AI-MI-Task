import os
from dotenv import load_dotenv
import openai
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def system_prompt():
    return f"""
    You are an AI storyteller. Your job is to create fun, interesting, and engaging short stories based on user input.
    Use simple language, clear descriptions, and exciting twists to make each story enjoyable.
    Adjust the story`s style based on the details given by the user.
    Keep the story short but meaningful.
    Make sure to include the title and author name at the beginning of the story.
    """

def user_prompt(name, profession, city, dream, mysterious_object, fear):
    return f"""
    Write a short and thrilling story about {name}, a {profession} living in {city}.
    One night, they have a strange dream about {dream}.
    The next day, they find a mysterious object: {mysterious_object}, which seems connected to their dream.
    As they investigate, they must face their biggest fear: {fear}.
    The story should be suspenseful, full of twists, and between 100 to 150 words.
    """

def generate_story(name, profession, city, dream, mysterious_object, fear):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": user_prompt(name, profession, city, dream, mysterious_object, fear)}
        ],
        max_tokens=450
    )

    content = response.choices[0].message.content
    print(content)


if __name__ == '__main__':
    generate_story(
        name="Alice",
        profession="a detective",
        city="New York",
        dream="solving a mystery",
        mysterious_object="an old map",
        fear="heights"
    )
