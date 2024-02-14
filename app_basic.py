# A basic Chatbot using OpenAI's completions model with a Chainlit user 
# interface. Built with help from Bappy's demo here:
# https://www.youtube.com/watch?v=AzfV0r2O_gk.

import chainlit as cl
from src.llm import get_chesters_response, messages

# Application logic. Go to https://docs.chainlit.io/get-started/pure-python
# and copy the code chunk for the basic structure.
#
# @cl.on_message decoration calls main() when user enters a message.
# async is required for the await keyword. The function will pause and wait for
# asynchonous operations to complete without blocking the event loop.

@cl.on_message
async def main(message: cl.Message):
    # Custom logic: Append the user message to messages, and send to LLM. 
    # Append response to messages.
    messages.append({"role": "user", "content": message.content})
    response = get_chesters_response(messages)
    messages.append({"role": "assistant", "content": response})

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()
