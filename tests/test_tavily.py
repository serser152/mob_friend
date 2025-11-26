#!/usr/bin/env python
"""test tavily web search"""
import os
import langchain_tavily
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

class TestTavily:
    """test tavily"""
    def test_tavily_key(self):
        """check key in env"""
        assert os.environ.get('TAVILY_API_KEY','') != ""

    def test_tavily_search(self):
        """test search"""
        tool = langchain_tavily.TavilySearch(max_results=5)
        res = tool.invoke({"query":"Сколько лет Риму?"})
        print(res)
        assert len(res['results']) > 0
