#!/usr/bin/env python
import streamlit as st
from click import prompt

from sound_interface import file_to_text, text_to_speech
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
        global voice

        st.header('Параметры')

        # Выбор LLM
        llm = st.radio('Выберете LLM',
                       ['gigachat', 'openrouter'],
                       index=0 if llm == "gigachat" else 1)
        if llm == 'openrouter':
            mn=st.text_input('Имя модели:')

        # Включние голосового интерфейса
        voice = st.checkbox('Использовать голосовой интерфейс', value=voice)

        # Поисковик
        use_search = st.checkbox(label="Использовать поисковик", value=use_search)

        # Кнопка для сохранения настроек
        if st.button('Сохранить'):
            st.session_state["llm"] = llm
            st.session_state["use_search"] = use_search
            st.session_state["voice"] = voice
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

llm = st.session_state.get("llm", "gigachat")
use_search = st.session_state.get("use_search", False)
voice = st.session_state.get("voice", False)

login = st.session_state.get("login", "")
if login == "":
    login_dialog()
else:
    # initialize llm api
    with st.spinner("Загрузка...", show_time=True):
        init_llm(llm, use_search)

    # main page
    st.markdown('## Персональный ассистент')

    if login:
        st.markdown(f'### Здравствуйте {login}')
        st.markdown("---")

        if voice:
            def change():
                #st.text =  sound.size
                sleep(1)

            sound = st.audio_input('Голосовой ввод:',
                                   on_change = change,
                                   kwargs = {
#                                       'sound': sound
                                   },
                                   )

            #save recorded sound to file
            if sound:
                sound.seek(0)
                with open('tmp_in.wav', 'wb') as f:
                    f.write(sound.read())

            sound.seek(0)
            txt = file_to_text(sound)

            st.audio(sound)
            st.markdown(txt)
            prompt = txt
        else:
            prompt = st.text_input('Message:')
        with st.spinner("Ждем ответа...", show_time=True):
            ans = ask_llm(prompt) if prompt else ''
        st.markdown(ans)
        if voice and prompt != '':
            with st.spinner("Готовим голосовой ответ...", show_time=True):
                text_to_speech(ans)
            st.audio('tmp_output.mp3', autoplay=True)
        prompt=''

        st.markdown('---')
        if st.button('Настройки'):
            settings_dialog()

