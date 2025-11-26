#!/usr/bin/env python

from ui.sound_interface import text_to_speech, file_to_text
import os

class TestLLMBase:

    def test_file_to_text(self):
        txt = file_to_text('tests/test_in.wav')
        print(txt)
        assert len(txt) > 5

    def test_tts(self):
        txt='Три.\nПродолжим?'
        text_to_speech(txt, 'tests/test_output2.mp3')
        size1 = os.path.getsize("tests/test_output.mp3")
        size2 = os.path.getsize("tests/test_output2.mp3")
        assert size1 == size2