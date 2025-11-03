#!/usr/bin/env python

from agent.agent import ask_llm, init_openrouter, init_gigachat

class TestLLMBase:

    def test_llm_openrouter_answer(self):
        init_openrouter()
        assert 'hello' in ask_llm('hello').lower()

    def test_llm_gigachat_answer(self):
        init_gigachat()
        assert 'привет' in ask_llm('hello').lower()

