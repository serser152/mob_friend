#!/usr/bin/env python

from agent.agent import ask_llm, init_openrouter, init_gigachat, init_llm, ask_agent

class TestLLMBase:

    def test_llm_openrouter_answer(self):
        init_openrouter()
        assert 'hello' in ask_llm('hello').lower()

    def test_llm_gigachat_answer(self):
        init_gigachat()
        assert 'привет' in ask_llm('hello').lower()

    def test_llm_openrouter_answer2(self):
        init_llm("openrouter")
        assert 'hello' in ask_llm('hello').lower()

    def test_llm_gigachat_answer2(self):
        init_llm("gigachat")
        assert 'привет' in ask_llm('hello').lower()

    def test_llm_gigachat_answer_with_search(self):
        init_llm('gigachat', use_search=True)
        assert 'привет' in ask_llm('hello').lower()


    def test_agent_gigachat_answer(self):
        init_llm('gigachat', use_search=True)
        res = ask_agent('hello').lower()
        print(res)
        assert 'привет' in res
