#!/usr/bin/env python
"""
UI for app.
Runs web interface for agentic system.
"""
import sys
import os

import streamlit as st

from  sound_interface import file_to_text, text_to_speech
from time import sleep

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

subdir = os.getcwd()
sys.path.append(subdir)

from agent.agent import MyAgent
from settings import load_settings, save_settings, openrouter_models, ollama_models, llm_providers, MCPServer

#======================
#   dialogs
#======================

@st.dialog('Settings', width='medium')
def settings_dialog():
    st.header('Settings')
    settings.login = st.text_input('Login:', value=settings.login)

    # === LLM Settings Block ===
    st.subheader("LLM Configuration")
    with st.container(border=True):
        settings.llm_provider = st.radio(
            'LLM Provider',
            llm_providers,
            index=llm_providers.index(settings.llm_provider)
        )

        if settings.llm_provider == 'openrouter':
            try:
                idx = openrouter_models.index(settings.model)
            except ValueError:
                idx = 0
            settings.model = st.radio(
                'Model (OpenRouter)',
                openrouter_models,
                index=idx
            )
        elif settings.llm_provider == 'ollama':
            try:
                idx = ollama_models.index(settings.model)
            except ValueError:
                idx = 0
            settings.model = st.radio(
                'Model (Ollama)',
                ollama_models,
                index=idx
            )
        else:
            st.text(f"Using default model: {settings.model}")

    # === Voice Settings ===
    st.subheader("Voice Interface")
    settings.voice_input = st.checkbox('Voice input', value=settings.voice_input)
    settings.voice_output = st.checkbox('Voice output', value=settings.voice_output)

    # === Tools ===
    st.subheader("Tools")
    settings.use_search = st.checkbox("Use web search tools", value=settings.use_search)

    # === MCP Servers ===
    st.subheader("MCP Servers")

    # Форма для добавления нового сервера
    with st.expander("Add new MCP server"):
        new_url = st.text_input("URL (must start with http:// or https://)")
        new_desc = st.text_input("Description (optional)")

        if st.button("Add Server"):
            if not new_url.strip():
                st.warning("URL не может быть пустым.")
            elif not (new_url.startswith("http://") or new_url.startswith("https://")):
                st.warning("URL должен начинаться с http:// или https://")
            else:
                # Проверяем дубликаты по URL
                if any(s.url == new_url.strip() for s in settings.mcp_servers):
                    st.warning("Сервер с таким URL уже существует.")
                else:
                    server = MCPServer(url=new_url.strip(), description=new_desc.strip())
                    settings.mcp_servers.append(server)
                    st.success(f"Сервер добавлен: {new_url}")

    # Отображение существующих серверов
    if settings.mcp_servers:
        st.write("Current MCP servers:")
        print(settings.model_dump())
        to_remove = []
        for i, server in enumerate(settings.mcp_servers):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"🔹 {server.url}")
                if server.description:
                    st.caption(server.description)
            with col2:
                if st.checkbox("Remove", key=f"remove_mcp_{i}"):
                    to_remove.append(server)

        for server in to_remove:
            settings.mcp_servers.remove(server)
            st.info(f"Removed: {server.url}")
    else:
        st.caption("No MCP servers added.")

    # === Save Button ===
    if st.button('Save'):
        save_settings(settings)
        st.success('Settings saved!')
        st.rerun()
@st.dialog('Enter', width='medium')
def login_dialog():
    st.header('Enter')
    settings.login = st.text_input('Login:')

    if len(settings.login) <= 3:
        st.markdown('Login length must be more than 3 symbols')
    else:
        save_settings(settings)
        st.write(f'Hello, {settings.login}')
        st.rerun()

#======================
#   main page
#======================

settings = load_settings()

if settings.login == "":
    login_dialog()
else:
    # initialize llm api
    with st.spinner("Loading...", show_time=True):
        agent = MyAgent(name = settings.llm_provider,
                        model=settings.model,
                        use_search=settings.use_search,
                        mcp_servers=settings.mcp_servers)

    # main page
    st.markdown('## Personal assistant')

    if settings.login:
        st.markdown(f'### Hello, {settings.login}')
        st.markdown("---")

        if settings.voice_input:
            def change():
                #st.text =  sound.size
                sleep(1)

            sound = st.audio_input('Your voice input:',
                                   on_change = change,
                                   kwargs = {
#                                       'sound': sound
                                   },
                                   )

            #save recorded sound to file
            txt = ''
            if sound:
                sound.seek(0)
                with open('tmp_in.wav', 'wb') as f:
                    f.write(sound.read())
                sound.seek(0)

                # transcribe recorded sound
                txt = file_to_text(sound)

                # show transcribed text and player
                st.audio(sound)
            st.markdown("You: " + txt)
            prompt = txt
        else:
            prompt = st.text_input('Message:', value='')
        with st.spinner("Preparing answer...", show_time=True):
            ans = agent.ask(prompt) if prompt else ''
        st.markdown(ans)
        if settings.voice_output and ans != '':
            with st.spinner("Preparing voice answer...", show_time=True):
                text_to_speech(ans)
            st.audio('tmp_output.mp3', autoplay=True)
        prompt=''

        st.markdown('---')
        if st.button('⚙️ Settings'):
            settings_dialog()
