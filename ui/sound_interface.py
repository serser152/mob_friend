#!/usr/bin/env python
"""
Module for Speech to Text and Text to Speech processing.
"""

import speech_recognition as sr
from gtts import gTTS

def text_to_speech(text, out_filename='tmp_output.mp3'):
    """Преобразуем текст в звук и сохраняем файл."""
    tts = gTTS(text=text, lang='ru')
    tts.save(out_filename)

def file_to_text(filename='tmp_in.wav'):
    """Распознаём речь из аудиофайла."""
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
    try:
        recognized_text = r.recognize_google(audio_data, language='ru-RU')
    except Exception as e:
        print("Ошибка:", str(e))
        return ''
    return recognized_text

