#!/usr/bin/env python
"""
UI for app.
Runs web interface for agentic system.
"""
import sys
import os

import streamlit as st
from  .sound_interface import file_to_text, text_to_speech
from time import sleep
from agent.agent import MyAgent

subdir = os.getcwd()
sys.path.append(subdir)

# диалог настройки
@st.dialog('Settings', width='medium')
def settings_dialog():
    """Settings dialog"""

    # get values from session state
    llm_provider = st.session_state.get("llm", "gigachat")
    use_search_tool = st.session_state.get("use_search", False)
    voice_input = st.session_state.get("voice_input", False)
    voice_output = st.session_state.get("voice_output", False)
    mdl = st.session_state.get("model", "openai/gpt-oss-20b:free")

    # show form
    st.header('Settings')

    #Выбор LLM
    llm_providers = ['gigachat', 'openrouter']
    llm_provider = st.radio('Select LLM provider',
                   llm_providers,
                   llm_providers.index(llm_provider)
                            )
    if llm == 'openrouter':

        openrouter_models = ['openai/gpt-oss-20b:free',
         "meta-llama/llama-3.3-8b-instruct:free",
         "z-ai/glm-4.5-air:free"]

        mdl = st.radio('Select model name from provider',
                         openrouter_models,
                         index=openrouter_models.index(mdl)
                         )

    # Включение голосового интерфейса
    voice_input = st.checkbox('Voice input', value = voice_input)
    voice_output = st.checkbox('Voice output', value = voice_output)

    # Поисковик
    use_search_tool = st.checkbox(label="Use websearch tools", value = use_search_tool)

    # Кнопка для сохранения настроек
    if st.button('Save'):
        st.session_state["llm"] = llm_provider
        st.session_state["use_search"] = use_search_tool
        st.session_state["voice_input"] = voice_input
        st.session_state["voice_output"] = voice_output
        st.session_state["model"] = mdl

        st.write(f'Settings saved')
        st.rerun() # restart app



@st.dialog('Enter', width='medium')
def login_dialog():
    """
    Login dialog
    Reading and saving login for unique user
    """
    st.header('Enter')
    login = st.text_input('Login:')

    if len(login) <= 3:
        st.markdown('Login length must be more than 3 symbols')
    else:
        # Кнопка для сохранения настроек
        if st.button('Save'):
            st.session_state["login"] = login
            st.write(f'Hello, {login}')
            st.rerun() # Перезапустить приложение, чтобы применить новые настройки

# Проверка ключей

llm = st.session_state.get("llm", "gigachat")
use_search = st.session_state.get("use_search", False)
voice_input = st.session_state.get("voice_input", False)
voice_output = st.session_state.get("voice_output", False)
model = st.session_state.get("model", "openai/gpt-oss-20b:free")
login = st.session_state.get("login", "")
#agent = MyAgent(llm, model, use_search)
if login == "":
    login_dialog()
else:
    # initialize llm api
    with st.spinner("Loading...", show_time=True):
        agent = MyAgent(llm, model, use_search)

    # main page
    st.markdown('## Personal assistant')

    if login:
        st.markdown(f'### Hello, {login}')
        st.markdown("---")

        if voice_input:
            def change():
                #st.text =  sound.size
                sleep(1)

            sound = st.audio_input('Voice in:',
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
        with st.spinner("Preparing answer...", show_time=True):
            ans = agent.ask(prompt) if prompt else ''
        st.markdown(ans)
        if voice_output and ans != '':
            with st.spinner("Preparing voice answer...", show_time=True):
                text_to_speech(ans)
            st.audio('tmp_output.mp3', autoplay=True)
        prompt=''

        st.markdown('---')
        if st.button('Settings'):
            settings_dialog()
