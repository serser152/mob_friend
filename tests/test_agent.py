#!/usr/bin/env python
"""Тесты для агента."""
from agent.agent import MyAgent

class TestLLMBase:
    """Тесты для LLM."""
    def test_llm_openrouter_answer(self):
        """Тест LLM OpenRouter."""
        a = MyAgent('openrouter')
        ans = a.ask_llm('hello').lower()
        assert ('hello' in ans) or ('hi' in ans)

    def test_llm_gigachat_answer(self):
        """Тест LLM GigaChat."""
        a = MyAgent('gigachat')
        assert 'привет' in a.ask_llm('hello').lower()

    def test_llm_openrouter_answer2(self):
        """Тест LLM OpenRouter."""
        a = MyAgent('openrouter')
        assert 'hello' in a.ask_llm('hello').lower()

    def test_llm_gigachat_answer2(self):
        """Тест LLM GigaChat."""
        a = MyAgent('gigachat')
        assert 'привет' in a.ask_llm('hello').lower()

    def test_llm_ollama_answer2(self):
        """Тест LLM Ollama."""
        a = MyAgent('ollama', model='gpt-oss:20b')
        ans = a.ask_llm('hello').lower()
        assert ('привет' in ans) or ('hello' in ans)

    def test_llm_gigachat_answer_with_search(self):
        """Тест агента с поиском на LLM GigaChat."""
        a = MyAgent('gigachat', use_search=True)
        res =  a.ask('Какой сегодня день недели? Ответь в одно слово.').lower()
        assert res in ['понедельник', 'вторник', 'среда', 'четверг',
                       'пятница', 'суббота', 'воскресенье']

    def test_agent_openrouter_answer_with_websearch(self):
        """Тест агента с поиском на LLM OpenRouter."""
        a = MyAgent('openrouter', use_search=True)
        res =  a.ask('Какой сегодня день недели? Ответь в одно слово.').lower()
        assert res in ['понедельник', 'вторник', 'среда', 'четверг',
                       'пятница', 'суббота', 'воскресенье']

    def test_agent_ollama_answer_with_websearch(self):
        """Тест агента с поиском на LLM Ollama."""
        a = MyAgent('ollama', model='gpt-oss:20b', use_search=True)
        res =  a.ask('Какой сегодня день недели? Ответь в одно слово на русском языке.').lower()
        assert res in ['понедельник', 'вторник', 'среда', 'четверг',
                       'пятница', 'суббота', 'воскресенье']
