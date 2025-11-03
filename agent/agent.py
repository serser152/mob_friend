#!/usr/bin/env python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from os import environ
from langchain_openai import ChatOpenAI
llm=ChatOpenAI(model="meta-llama/llama-3.3-8b-instruct:free",
  base_url="https://openrouter.ai/api/v1",
  api_key=environ["OPENROUTER_API_KEY"],)
 

def ask_llm(message: str) -> str:
    """
    return model anser
    """
    response = llm.invoke(message)
    return response.content

print(ask_llm('hello'))