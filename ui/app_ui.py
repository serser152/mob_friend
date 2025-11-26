#!/usr/bin/env python
"""
UI for app.
Runs web interface for agentic system.
"""

import streamlit as st

with st.spinner("Loading...", show_time=True):
    from time import sleep
    from dotenv import load_dotenv, find_dotenv
    from streamlit_cookies_manager import CookieManager
    from  ui.sound_interface import file_to_text, text_to_speech
    from agent.agent import MyAgent

load_dotenv(find_dotenv())


# list of configs
llm_providers = ['gigachat', 'openrouter', 'ollama']

openrouter_models = [
    "openai/gpt-oss-20b:free",
    "meta-llama/llama-3.3-8b-instruct:free",
    "z-ai/glm-4.5-air:free"
]

ollama_models = [
    "gpt-oss:20b",
    "qwen3:4b",
    "llama2-uncensored:latest"
]

# raed cookies
cookies = CookieManager(
    prefix="mob_friend/",
    #password=os.environ.get("COOKIES_PASSWORD", "My super secret password"),
)
if not cookies.ready():
    st.stop()

def get_all_cookies():
    """Get all cookies"""
    return cookies

#======================
#   dialogs
#======================

@st.dialog('Settings', width='medium')
def settings_dialog():
    """Settings dialog"""
    # get values from session state
    _login = cookies.get("login", "")
    llm_provider = cookies.get("llm", "gigachat")
    use_search_tool = cookies.get("use_search", "False")
    voice_input_enabled = cookies.get("voice_input", "False")
    voice_output_enabled = cookies.get("voice_output", "False")
    mdl = cookies.get("model", "openai/gpt-oss-20b:free")

    use_search_tool = use_search_tool == "True"
    voice_input_enabled = voice_input_enabled == "True"
    voice_output_enabled = voice_output_enabled == "True"

    # show form
    st.header('Settings')

    _login = st.text_input('Login:', value=_login)

    #Select LLM

    llm_provider = st.radio('Select LLM provider',
                   llm_providers,
                   llm_providers.index(llm_provider)
                            )
    if llm_provider == 'openrouter':
        try:
            mdl_idx = openrouter_models.index(mdl)
        except ValueError:
            mdl_idx = 0

        mdl = st.radio('Select model name from provider',
                         openrouter_models,
                         index=mdl_idx
                         )
    if llm_provider == 'ollama':
        try:
            mdl_idx = ollama_models.index(mdl)
        except ValueError:
            mdl_idx = 0
        mdl = st.radio('Select model name from provider',
                         ollama_models,
                         index=mdl_idx
                         )

    # Enabled voice input/output
    voice_input_enabled = st.checkbox('Voice input', value = voice_input_enabled)
    voice_output_enabled = st.checkbox('Voice output', value = voice_output_enabled)

    # Web search tools
    use_search_tool = st.checkbox(label="Use websearch tools", value = use_search_tool)

    # Save settings
    if st.button('Save'):
        cookies["llm"] = llm_provider
        cookies["use_search"] = str(use_search_tool)
        cookies["voice_input"] = str(voice_input_enabled)
        cookies["voice_output"] = str(voice_output_enabled)
        cookies["model"] = mdl
        cookies["login"] = _login

        cookies.save()
        st.write('Settings saved')
        st.rerun() # restart app

@st.dialog('Enter', width='medium')
def login_dialog():
    """
    Login dialog
    Reading and saving login for unique user
    """
    #cookies = get_all_cookies()
    st.header('Enter')
    _login = st.text_input('Login:')

    if len(login) <= 3:
        st.markdown('Login length must be more than 3 symbols')
    else:
        cookies["login"] = _login
        cookies.save()
        st.write(f'Hello, {login}')
        st.rerun() # restart app

#======================
#   main page
#======================

cookies = get_all_cookies()
llm = cookies.get("llm", "gigachat")
use_search = cookies.get("use_search", "False") == "True"
voice_input = cookies.get("voice_input", "False") == "True"
voice_output = cookies.get("voice_output", "False") == "True"
model = cookies.get("model", "openai/gpt-oss-20b:free")
login = cookies.get("login", "")
#save cookies
cookies["llm"] = llm
cookies["use_search"] = str(use_search)
cookies["voice_input"] = str(voice_input)
cookies["voice_output"] = str(voice_output)
cookies["model"] = model
cookies.save()

if login == "":
    login_dialog()
else:
    # initialize llm api
    with st.spinner("Loading...", show_time=True):
        agent = MyAgent(llm, model, use_search=use_search)

    # main page
    st.markdown('## Personal assistant')

    if login:
        st.markdown(f'### Hello, {login}')
        st.markdown("---")

        if voice_input:
            def change():
                """
                реакция на изменение звука
                TBD
                """
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
            ans = ans.replace('**', '')
        st.markdown(ans)
        if voice_output and ans != '':
            with st.spinner("Preparing voice answer...", show_time=True):
                text_to_speech(ans)
            st.audio('tmp_output.mp3', autoplay=True)
        prompt=''

        st.markdown('---')
        if st.button('⚙️ Settings'):
            settings_dialog()
