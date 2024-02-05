# Project to create a basic Chatbot using OpenAI's completions model with a
# Chainlit user interface. I built this bot following along with Bappy's demo
# here: https://www.youtube.com/watch?v=AzfV0r2O_gk.

import chainlit as cl
from src.llm import get_chesters_response, messages

@cl.on_message
async def main(message: cl.Message):
    # Custom logic goes here...
    messages.append({"role": "user", "content": message.content})
    response = get_chesters_response(messages)
    messages.append({"role": "assistant", "content": response})

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()
