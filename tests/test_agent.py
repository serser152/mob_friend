#!/usr/bin/env python

from agent.agent import MyAgent

class TestLLMBase:

    def test_llm_openrouter_answer(self):
        a = MyAgent('openrouter')
        ans = a.ask_llm('hello').lower()
        assert ('hello' in ans) or ('hi' in ans)

    def test_llm_gigachat_answer(self):
        a = MyAgent('gigachat')
        assert 'привет' in a.ask_llm('hello').lower()

    def test_llm_openrouter_answer2(self):
        a = MyAgent('openrouter')
        assert 'hello' in a.ask_llm('hello').lower()

    def test_llm_gigachat_answer2(self):
        a = MyAgent('gigachat')
        assert 'привет' in a.ask_llm('hello').lower()

    def test_llm_ollama_answer2(self):
        a = MyAgent('ollama', model='gpt-oss:20b')
        ans = a.ask_llm('hello').lower()
        assert ('привет' in ans) or ('hello' in ans)

    def test_llm_gigachat_answer_with_search(self):
        a = MyAgent('gigachat', use_search=True)
        res =  a.ask('Какой сегодня день недели? Ответь в одно слово.').lower()
        assert res in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    def test_agent_openrouter_answer_with_websearch(self):
        a = MyAgent('openrouter', use_search=True)
        res =  a.ask('Какой сегодня день недели? Ответь в одно слово.').lower()
        assert res in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    def test_agent_ollama_answer_with_websearch(self):
        a = MyAgent('ollama', model='gpt-oss:20b', use_search=True)
        res =  a.ask('Какой сегодня день недели? Ответь в одно слово на русском языке.').lower()
        assert res in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

