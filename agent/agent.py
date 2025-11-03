#!/usr/bin/env python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from os import environ
from langchain_openai import ChatOpenAI
from langchain_gigachat.chat_models import GigaChat

llm = None

def init_openrouter(model="meta-llama/llama-3.3-8b-instruct:free"):
    """
    Initialize llm via openrouter
    """
    global llm
    llm=ChatOpenAI(model=model,
    base_url="https://openrouter.ai/api/v1",
    api_key=environ["OPENROUTER_API_KEY"],)


def init_gigachat():
    """ 
    Initialize Gigachat
    """
    global llm
    llm = GigaChat(credentials=environ["GIGACHAT_API_KEY"],
                    verify_ssl_certs=False)


def ask_llm(message: str) -> str:
    """
    return model anser
    """
    response = llm.invoke(message)
    return response.content

#init_gigachat()
#print(ask_llm('hello'))