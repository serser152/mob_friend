"""Settings module.
All settings are stored in cookies.
"""
import json
from typing import List, Optional
from streamlit_cookies_manager import CookieManager
from pydantic import BaseModel, field_validator
import streamlit as st


# === Конфигурация ===
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


class SettingsException(Exception):
    """Исключение для ошибок настроек."""
    pass


class MCPServer(BaseModel):
    """Модель MCP-сервера с описанием и URL."""
    url: str
    description: str = ""

    @field_validator("url")
    def validate_url(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("URL не может быть пустым")
        # Простая проверка формата
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL должен начинаться с http:// или https://")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        return v.strip()


class AppSettings(BaseModel):
    """Основная модель настроек приложения."""
    login: str = ""
    llm_provider: str = "gigachat"
    model: str = "openai/gpt-oss-20b:free"
    use_search: bool = False
    voice_input: bool = False
    voice_output: bool = False
    mcp_servers: List[MCPServer] = []

    @field_validator("llm_provider")
    def validate_llm(cls, v):
        valid_providers = llm_providers
        if v not in valid_providers:
            raise ValueError(f"LLM должен быть одним из: {valid_providers}")
        return v

    @field_validator("login")
    def validate_login(cls, v):
        if v and len(v) <= 3:
            raise ValueError("Логин должен быть больше 3 символов")
        return v


# Инициализация менеджера кук
cookies = CookieManager(prefix="mob_friend/")
if not cookies.ready():
    st.stop()


def load_settings() -> AppSettings:
    """Загружает настройки из кук и возвращает объект AppSettings."""
    try:
        data = {
            "login": cookies.get("login", ""),
            "llm_provider": cookies.get("llm", "gigachat"),
            "model": cookies.get("model", "openai/gpt-oss-20b:free"),
            "use_search": cookies.get("use_search", "False") == "True",
            "voice_input": cookies.get("voice_input", "False") == "True",
            "voice_output": cookies.get("voice_output", "False") == "True",
            "mcp_servers": [],
        }

        # Загрузка MCP-серверов
        mcp_json = cookies.get("mcp_servers", "[]")
        if len(mcp_json) == 0:
            mcp_json = "[]"
        try:
            if type(mcp_json) == str:
                mcp_list = json.loads(mcp_json)
            else:
                mcp_list = mcp_json
            # Преобразуем словари в объекты MCPServer
            data["mcp_servers"] = [MCPServer(**item) for item in mcp_list]
        except Exception as e:
            st.warning(f"Ошибка загрузки MCP-серверов: {e}")
            data["mcp_servers"] = []

        return AppSettings(**data)
    except Exception as e:
        st.error(f"Ошибка загрузки настроек: {e}")
        return AppSettings()


def save_settings(settings: AppSettings):
    """Сохраняет настройки в куки."""
    cookies["login"] = settings.login
    cookies["llm"] = settings.llm_provider
    cookies["model"] = settings.model
    cookies["use_search"] = str(settings.use_search)
    cookies["voice_input"] = str(settings.voice_input)
    cookies["voice_output"] = str(settings.voice_output)
    # Сохраняем MCP-серверы как список словарей
    cookies["mcp_servers"] = settings.model_dump()["mcp_servers"]
    cookies.save()