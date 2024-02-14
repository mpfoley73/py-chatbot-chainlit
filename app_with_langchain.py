# This implementation extends the basic bot defined in app_basic.py to 
# integrate with LangChain. See demos
# https://www.youtube.com/watch?v=xZDB1naRUlk (45:00 mark),
# https://docs.chainlit.io/integrations/langchain

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl

from src.prompt import system_instructions

# @cl.on_chat_start decoration calls on_chat_start() when a chat session is
# started. on_chat_start creates a simple pipeline: user prompt | OpenAI 
# model | response parser. It puts this pipeline into the user session.

@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(streaming = True)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_instructions),
            ("human", "{question}")
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)

# @cl.on_message decoration calls on_message() when the user enters a message. 
# It retrieves the pipeline and creates an empty message object. It
# asycnchronously loops over the output chunks of astream(), appending it to 
# msg. Finally, the msg is sent. This creates a streamed output rather than a
# single output.

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
