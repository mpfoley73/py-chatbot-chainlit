# This is the OpenAI API logic. Refer to the Open AI documentation here:
# https://platform.openai.com/docs/guides/text-generation/chat-completions-api.

from openai import OpenAI
from src.prompt import system_instructions

client = OpenAI()

# Initialize the conversation by setting the system prompt. system_instructions
# is defined in prompt.py. messages is an array of dictionaries.

messages = [
    {"role": "system", "content": system_instructions}
]

# Standard call to OpenAI API. The model and temperature are parameters, but 
# I don't know how to create drop-down menus in Chainlit, so values are not
# passed in and the defaults are always used.

def get_chesters_response(messages, model="gpt-3.5-turbo", temperature=0.2):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    return response.choices[0].message.content
