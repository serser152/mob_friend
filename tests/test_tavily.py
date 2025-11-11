#!/usr/bin/env python
import os
import langchain_tavily
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

class TestTavily:

    def test_tavily_key(self):
        """check key in env"""
        assert os.environ.get('TAVILY_API_KEY','') != ""

    def test_tavily_search(self):
        tool = langchain_tavily.TavilySearch(max_results=5)
        res = tool.invoke({"query":"Сколько лет Риму?"})
        print(res)
        assert len(res['results']) > 0

if __name__ == "__main__":
    tool = langchain_tavily.TavilySearch(max_results=5)
    res = tool.invoke({"query":"Сколько лет Риму?"})
    print(res)
