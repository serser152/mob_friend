#!/usr/bin/env python
import streamlit as st
from time import sleep
import sys
import os
subdir = os.getcwd()
sys.path.append(subdir)
from agent.agent import ask_llm
st.

st.header('hello')
st.markdown(' ** applicatoion assistant ** ')

promt = st.text_input('Message:')
with st.spinner("Wait for it...", show_time=True):
    ans = "asdf" #ask_llm(promt)
st.write(ans)