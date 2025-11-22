#!/usr/bin/env python
import streamlit as st

from sound_interface import file_to_text, text_to_speech
from time import sleep
import sys
import os
subdir = os.getcwd()
sys.path.append(subdir)
from agent.agent import MyAgent


# диалог настройки
@st.dialog('Настройки приложения', width='medium')
def settings_dialog():
    """Диалог настроек"""
    llm_old = st.session_state.get("llm", "gigachat")
    use_search_old = st.session_state.get("use_search", False)
    voice_old = st.session_state.get("voice", False)
    model_old = st.session_state.get("model", "openai/gpt-oss-20b:free")

    st.header('Параметры')

    #Выбор LLM
    llm = st.radio('Выберете LLM',
                   ['gigachat', 'openrouter'],
                   index=0 if llm_old == "gigachat" else 1)
    if llm == 'openrouter':
        model = st.text_input('Имя модели:')

    # Включение голосового интерфейса
    voice = st.checkbox('Использовать голосовой интерфейс', value=voice_old)

    # Поисковик
    use_search = st.checkbox(label="Использовать поисковик", value=use_search_old)

    # Кнопка для сохранения настроек
    if st.button('Сохранить'):
        st.session_state["llm"] = llm
        st.session_state["use_search"] = use_search
        st.session_state["voice"] = voice
        try:
            st.session_state["model"] = model
        except:
            pass
        st.write(f'Настройки сохранены: модель = {llm}')
        st.rerun() # Перезапустить приложение, чтобы применить новые настройки


# диалог логина
@st.dialog('Вход', width='medium')
def login_dialog():
        st.header('Вход')
        login = st.text_input('Login:')

        if len(login) <= 3:
            st.markdown('Логин должен минимум 3 символа')
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
model = st.session_state.get("model", "openai/gpt-oss-20b:free")

login = st.session_state.get("login", "")
agent = MyAgent()
if login == "":
    login_dialog()
else:
    # initialize llm api
    with st.spinner("Загрузка...", show_time=True):
        agent = MyAgent(llm, model, use_search)

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

            # transcribe recorded sound
            txt = file_to_text(sound)

            # show transcribed text and player
            st.audio(sound)
            st.markdown(txt)
            prompt = txt
        else:
            prompt = st.text_input('Message:')
        with st.spinner("Ждем ответа...", show_time=True):
            ans = agent.ask(prompt) if prompt else ''
        st.markdown(ans)
        if voice and prompt != '':
            with st.spinner("Готовим голосовой ответ...", show_time=True):
                text_to_speech(ans)
            st.audio('tmp_output.mp3', autoplay=True)
        prompt=''

        st.markdown('---')
        if st.button('Настройки'):
            settings_dialog()

