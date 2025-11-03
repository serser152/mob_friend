#!/usr/bin/env python

from agent.agent import ask_llm

class TestLLMBase:

    def test_llm_answer(self):
        assert 'hello' in ask_llm('hello').lower()
    def test_llm_answer2(self):
        assert 'hello' in ask_llm('hello').lower()
    def test_llm_answer3(self):
        assert 'hello' in ask_llm('hello').lower()
    def test_llm_answer4(self):
        assert 'hello' in ask_llm('hello').lower()
    def test_llm_answer5(self):
        assert 'hello' in ask_llm('hello').lower()

