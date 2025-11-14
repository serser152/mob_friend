#!/usr/bin/env python
from dotenv import load_dotenv, find_dotenv
from os import environ
from langchain_openai import ChatOpenAI
from langchain_gigachat.chat_models import GigaChat
from langchain_tavily import TavilySearch
import langchain
from langchain.tools import tool

from langchain_tavily import TavilySearch

from ddgs import DDGS
from langchain.agents import create_agent
from datetime import datetime

load_dotenv(find_dotenv())

'''
Tools
Описание инструментов для агента
'''


tools=[]
@tool
def search_web_ddgs(query: str) -> str:
    """
    Найти информацию в интернете через поисковую систему DuckDuckGo.
    Агрументы:
    query - поисковый запрос
    """
    with DDGS() as ddgs:
        max_results=5
        hits = ddgs.text(query, region="ru-ru", time="w", max_results=max_results)
        return "\n".join(f"{hit['title']}: {hit['body']} -- {hit['href']}" for hit in hits[:max_results])

tools.append(search_web_ddgs)


@tool
def search_web_tavily(query:str) -> str:
    """
    Найти информацию в интернете через поисковую систему Tavily.
    Агрументы:
    query - поисковый запрос
    """
    tav = TavilySearch(max_results=5)
    res=tav.invoke({'query':query})
    return '\n'.join([t['title']+":"+t['content'] for t in res['results']])

tools.append(search_web_tavily)


@tool
def get_current_time():
    """Получить реальное время и дату"""
    dt=datetime.now()
    return dt.strftime('%H:%M:%S %d.%m.%Y')

tools.append(get_current_time)

llm = None
agent = None
def init_openrouter(model="meta-llama/llama-3.3-8b-instruct:free"):
    """
    Initialize llm via openrouter
    """
    global llm
    llm=ChatOpenAI(model=model,
    base_url="https://openrouter.ai/api/v1",
    api_key=environ.get("OPENROUTER_API_KEY",""))


def init_gigachat():
    """ 
    Initialize Gigachat
    """
    global llm
    llm = GigaChat(credentials=environ.get("GIGACHAT_API_KEY",""),
                    verify_ssl_certs=False)



from datetime import date
from langgraph.checkpoint.memory import InMemorySaver


def init_llm(name='gigachat', model='meta-llama/llama-3.3-8b-instruct:free', use_search=False):
    """

    :param name: openrouter/gigachat
    :param model:
        "meta-llama/llama-3.3-8b-instruct:free"
        "z-ai/glm-4.5-air:free"
        "openai/gpt-oss-20b:free"
    :param use_search: use web search tools
    :return:
    """
    global llm
    global agent

    if name == 'gigachat':
        init_gigachat()
    elif name == 'openrouter':
        init_openrouter(model=model)
    else:
        raise Exception('Unknown llm initialization')

    if use_search:
        print('Use search tools')
        tools_used = tools
    else:
        tools_used = []


    checkpointer = InMemorySaver()


    today = date.today().strftime("%d.%m.%Y")  # DD.MM.YYYY
    system_prompt = (
        f"Сегодня {today}. "
        "Ты полезный ассистент. Используй search_web_tavily и search_web_ddgs для поиска информации в интернете."
        "get_current_time - получить текущее время и дату."
        "Отвечай кратко и по делу."
    )
    agent = create_agent(
            model = llm,
            tools = tools_used,
            system_prompt=system_prompt,
            checkpointer=checkpointer
            )

def ask_llm(message: str) -> str:
    """
    return model anser
    """
    global llm

    response = llm.invoke(message)
    return response.content

def ask_agent(message: str) -> str:
    """
    return agent anser
    """
    global agent

    config={'configurable':{'thread_id':1}}

    response = agent.invoke({'messages':[{'role':'user', 'content':message}]}, config=config)
    return response['messages'][-1].content

init_llm('gigachat', use_search=True)
print(ask_agent('Какой сегодня день недели? Ответь в одно слово.'))
print(ask_agent('Сколько сейчас времени?'))
