#!/usr/bin/env python
"""
Agent module
Agent tools and llm initialization
"""

from os import environ
from datetime import datetime
from datetime import date
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_gigachat.chat_models import GigaChat
from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain.agents import create_agent
from ddgs import DDGS
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv(find_dotenv())

'''
Tools
Описание инструментов для агента
'''


# Tools
# Описание инструментов для агента

tools=[]
@tool
def search_web_ddgs(query: str) -> str:
    """ 
    Найти информацию в интернете.
    Агрументы:
    query - поисковый запрос
    """
    with DDGS() as ddgs:
        max_results=5
        hits = ddgs.text(query, region="ru-ru", time="w", max_results=max_results)
        return "\n".join(f"{hit['title']}: {hit['body']} -- {hit['href']}" \
                         for hit in hits[:max_results])

tools.append(search_web_ddgs)


@tool
def search_web_tavily(query:str) -> str:
    """ 
    Найти информацию в интернете.
    Агрументы:
    query - поисковый запрос
    """
    tav = TavilySearch(max_results=5)
    res=tav.invoke({'query':query})
    return '\n'.join([t['title']+":"+t['content'] for t in res['results']])

tools.append(search_web_tavily)


@tool
def get_current_time():
    """Получить текущее время и дату"""
    dt=datetime.now()
    return dt.strftime('%H:%M:%S %d.%m.%Y')

tools.append(get_current_time)

@tool
def get_current_date():
    """Получить текущую дату"""
    dt=datetime.now()
    return dt.strftime('%Y-%m-%d')

tools.append(get_current_date)





def init_openrouter(model="meta-llama/llama-3.3-8b-instruct:free"):
    """
    Initialize llm via openrouter
    """
    llm=ChatOpenAI(model=model,
    base_url="https://openrouter.ai/api/v1",
    api_key=environ.get("OPENROUTER_API_KEY",""))
    return llm


def init_gigachat():
    """ 
    Initialize Gigachat
    """
    llm = GigaChat(credentials=environ.get("GIGACHAT_API_KEY",""),
                    verify_ssl_certs=False)
    return llm


def init_llm(
        name='gigachat',
        model='meta-llama/llama-3.3-8b-instruct:free'
):
    """
    :param name: openrouter/gigachat
    :param model:
        "meta-llama/llama-3.3-8b-instruct:free"
        "z-ai/glm-4.5-air:free"
        "openai/gpt-oss-20b:free"
    :return: llm instance
    """
    llm = None
    if name == 'gigachat':
        llm = init_gigachat()
    elif name == 'openrouter':
        llm = init_openrouter(model=model)
    else:
        raise Exception('Unknown llm initialization')
    return llm

def init_agent(
        name='gigachat',
        model='openai/gpt-oss-20b:free',
        use_search=False
):
    """

    :param name: openrouter/gigachat
    :param model:
        "meta-llama/llama-3.3-8b-instruct:free"
        "z-ai/glm-4.5-air:free"
        "openai/gpt-oss-20b:free"
    :param use_search: use web search tools
    :return:
    """
    llm = init_llm(name, model)

    if use_search:
        tools_used = tools
    else:
        tools_used = []


    checkpointer = InMemorySaver()

    today = date.today().strftime("%d.%m.%Y")  # DD.MM.YYYY
    system_prompt = (
        f"Сегодня {today}. "
        "Ты полезный ассистент. Используй search_web_tavily и "
        "search_web_ddgs для поиска информации в интернете."
    )
    agent = create_agent(
            model = llm,
            tools = tools_used,
            system_prompt=system_prompt,
            checkpointer=checkpointer,
            )
    return llm, agent


class MyAgent:
    llm, agent = None, None

    def __init__(self, name='gigachat', model='openai/gpt-oss-20b:free', use_search=False):
        self.llm, self.agent = init_agent(name, model, use_search)
        self.config = {'configurable': {'thread_id': 1}}

    def ask(self, message: str) -> str:
        """
        return agent anser
        """

        response = self.agent.invoke(
            {'messages': [{'role': 'user', 'content': message}]},
            config = self.config,
            print_mode=('updates'))
        return response['messages'][-1].content

    def ask_llm(self, message: str) -> str:
        """
        return model anser
        """
        response = self.llm.invoke(message)
        return response.content

#a = MyAgent('gigachat',use_search=True)
#a = MyAgent('openrouter', model='openai/gpt-oss-20b:free',use_search=True)
#print(a.ask('Какой 22.11.2025 день недели? Ответь в одно слово.'))
#print(ask_agent('Какой сегодня день недели?'))
