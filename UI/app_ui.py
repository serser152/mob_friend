#!/usr/bin/env python
import streamlit as st
from time import sleep
import sys
import os
subdir = os.getcwd()
print(subdir+'/..')
sys.path.append(subdir)
from agent.agent import ask_llm, init_llm


# диалог настройки
@st.dialog('Настройки приложения', width='medium')
def settings_dialog():
        global use_search
        global llm
        st.header('Параметры')
        llm = st.radio('Выберете LLM',[ 'gigachat', 'openrouter'], index=1 if llm == "openrouter" else 1)

        if llm == 'openrouter':
            mn=st.text_input('Имя модели:')

        use_search = st.checkbox(label="Использовать поисковик tavily", value=use_search)
        # Кнопка для сохранения настроек
        if st.button('Сохранить'):
            st.session_state["llm"] = llm
            st.session_state["use_search"] = use_search
            st.write(f'Настройки сохранены: модель = {llm}')
            st.rerun() # Перезапустить приложение, чтобы применить новые настройки


# диалог логина
@st.dialog('Вход', width='medium')
def login_dialog():
        st.header('Вход')
        login = st.text_input('Login:')

        if len(login) < 3:
            st.markdown('Слишком малая длинна логина')
        else:
            # Кнопка для сохранения настроек
            if st.button('Сохранить'):
                st.session_state["login"] = login
                st.write(f'Здравствуйте, {login}')
                st.rerun() # Перезапустить приложение, чтобы применить новые настройки


# Проверка ключей

if 'llm' not in st.session_state:
    st.session_state["llm"] = "openrouter"

login = st.session_state.get("login", "")
if login == "":
    login_dialog()
else:
    # initialize llm api
    with st.spinner("Загрузка...", show_time=True):
        llm = st.session_state.get("llm", "gigachat")
        use_search = st.session_state.get("use_search", False)
        init_llm(llm, use_search)

    # main page
    st.markdown('## Персональный ассистент')

    if login:
        st.markdown(f'### Здравствуйте {login}')
        st.markdown("---")

        promt = st.text_input('Message:')
        with st.spinner("Ждем ответа...", show_time=True):
            ans = ask_llm(promt) if promt else ''
        st.markdown(ans)
        promt=''

        st.markdown('---')
        if st.button('Настройки'):
            settings_dialog()

